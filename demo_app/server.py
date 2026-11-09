"""DynaCPI demo workbench: live RDKit chemistry + frozen engineering model.
Only the fixed legacy DAVIS development cohort is used. Not a clinical or
independent affinity benchmark. The app does not train or alter checkpoints.
"""
import os
import sys
import json
import hashlib
import threading
import time
import msvcrt
from contextlib import contextmanager
from pathlib import Path

from flask import Flask, request, jsonify, send_file
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8192
MODEL_LOCK = threading.RLock()
MODEL = None
MODEL_ERROR = None
TARGETS = {}
SEED = 1107
CHEM_MAX_CHARS = 450
ALLOWED_K = {0, 1, 2, 5, 10, 20}


@contextmanager
def short_gpu_lease():
    """Respect the original project's shared GPU lock; give up if busy."""
    lock_path = ROOT / ".gpu.lock"
    with lock_path.open("a+b") as stream:
        if not lock_path.stat().st_size:
            stream.write(b"1")
            stream.flush()
        started = time.monotonic()
        while True:
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if time.monotonic() - started > 15:
                    raise RuntimeError("GPU is reserved by another project job; please retry later.")
                time.sleep(0.5)
        try:
            yield
        finally:
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)


def canonicalize(value):
    if not isinstance(value, str) or not value.strip() or len(value) > CHEM_MAX_CHARS:
        raise ValueError("Provide a nonempty SMILES string with at most 450 characters.")
    mol = Chem.MolFromSmiles(value.strip())
    if mol is None or mol.GetNumAtoms() > 250:
        raise ValueError("SMILES is invalid, or molecule exceeds the 250-atom demo limit.")
    canonical = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
    return mol, canonical


def chemistry(smiles):
    mol, canonical = canonicalize(smiles)
    draw = rdMolDraw2D.MolDraw2DSVG(430, 244)
    draw.drawOptions().addAtomIndices = False
    rdMolDraw2D.PrepareAndDrawMolecule(draw, mol)
    draw.FinishDrawing()
    svg = draw.GetDrawingText().replace("<?xml version='1.0' encoding='iso-8859-1'?>", "")
    return {
        "canonical": canonical,
        "svg": svg,
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "molecular_weight": round(Descriptors.MolWt(mol), 2),
        "logp": round(Crippen.MolLogP(mol), 2),
        "tpsa": round(rdMolDescriptors.CalcTPSA(mol), 1),
        "hbd": rdMolDescriptors.CalcNumHBD(mol),
        "hba": rdMolDescriptors.CalcNumHBA(mol),
        "atoms": mol.GetNumAtoms(),
    }


def _load_targets():
    global TARGETS
    if TARGETS:
        return TARGETS
    manifest = json.loads((ROOT / "data/engineering_pilot/limited_alpha_3d_graph_manifest.json").read_text(encoding="utf-8"))
    selected = {
        r["source_name"]: r for r in manifest["records"]
        if r.get("status") == "GRAPH_MAPPED_ENGINEERING_ONLY"
        and r.get("pilot_split") == "val"
    }
    if set(selected) != {"FRK", "MEK5", "ADCK4", "OSR1"}:
        raise RuntimeError("Unexpected pilot target manifest; do not silently change the benchmark.")
    rows = json.loads((ROOT / "data/engineering_pilot/rows.json").read_text(encoding="utf-8"))
    compounds = json.loads((ROOT / "data/staging/compounds.json").read_text(encoding="utf-8"))
    for name, rec in selected.items():
        tid = rec["sequence_sha256"]
        pool = []
        for row in rows:
            if row["sequence"] != tid or row["split"] != "val":
                continue
            mol, smi = canonicalize(compounds[row["compound"]])
            cid = hashlib.sha256(smi.encode()).hexdigest()
            pool.append({"id": cid, "smiles": smi, "y": float(row["y"])})
        pool.sort(key=lambda x: hashlib.sha256(("demo_support|" + tid + "|" + x["id"]).encode()).hexdigest())
        if len(pool) != 54:
            raise RuntimeError("Expected exactly 54 fixed DAVIS development observations per target.")
        selected[name] = {"id": tid, "record": rec, "pool": pool, "esm": None, "graph": None, "cache": {}}
    TARGETS = selected
    return TARGETS


def _load_model():
    global MODEL, MODEL_ERROR
    if MODEL is not None:
        return MODEL
    try:
        import torch
        from dynacpi.sequence_model import SequenceFoundation
        from dynacpi.geometry_branch import GeometryBranch
        from dynacpi.frozen_pair_predictor import FrozenPairPredictor

        # The project's molecular graph module explicitly places tensors on CUDA.
        # Respect GPU job locks before allocating memory or running inference.
        device = "cuda"
        if not torch.cuda.is_available():
            raise RuntimeError("This frozen model requires an NVIDIA CUDA GPU.")
        seq_path = ROOT / "research/pilot_sequence/checkpoint.pt"
        geo_path = ROOT / "research/pilot_geometry_seed_sweep_dev/seed_1107/best_checkpoint.pt"
        seqck = torch.load(seq_path, map_location="cpu", weights_only=False)
        geock = torch.load(geo_path, map_location="cpu", weights_only=False)
        if seqck.get("kind") != "sequence":
            raise RuntimeError("Sequence checkpoint metadata mismatch.")
        if geock.get("sequence_checkpoint_sha256") != hashlib.sha256(seq_path.read_bytes()).hexdigest():
            raise RuntimeError("Frozen sequence and geometry checkpoints do not match.")
        sequence = SequenceFoundation()
        sequence.load_state_dict(seqck["state"], strict=True)
        geometry = GeometryBranch()
        geometry.load_state_dict(geock["state"], strict=True)
        predictor = FrozenPairPredictor(
            sequence, geometry, device=device,
            label_mean=float(seqck["label_mean"]), label_std=float(seqck["label_std"])
        )
        MODEL = {"torch": torch, "predictor": predictor, "device": device}
        MODEL_ERROR = None
        return MODEL
    except Exception as exc:
        MODEL_ERROR = str(exc)
        raise


def _predict(target, smiles, k):
    if target not in _load_targets():
        raise ValueError("Choose a listed development protein.")
    if not isinstance(k, int) or k not in ALLOWED_K:
        raise ValueError("K must be 0, 1, 2, 5, 10 or 20.")
    from dynacpi.frozen_adapter import adapt_episode
    from dynacpi.episode_data import PredictionEpisode, QueryCompound, SupportObservation

    _, query = canonicalize(smiles)
    qid = hashlib.sha256(query.encode()).hexdigest()
    item = TARGETS[target]
    supports = [r for r in item["pool"] if r["id"] != qid][:k]
    if len(supports) != k:
        raise RuntimeError("Not enough nonoverlapping pilot support compounds.")
    m = _load_model()
    torch = m["torch"]
    predictor = m["predictor"]
    if item["esm"] is None:
        esm = torch.load(ROOT / "data/esm2_t33_650M_layer33_w1000_o128_fp16" / (item["id"] + ".pt"),
                         map_location="cpu", weights_only=True)
        graph = torch.load(ROOT / "data/engineering_pilot/structure_graphs" / item["id"] / "graph.pt",
                           map_location="cpu", weights_only=True)
        item["esm"] = esm["embeddings"]
        item["graph"] = graph
    all_smis = [query] + [r["smiles"] for r in supports if r["id"] not in item["cache"]]
    # Cache the immutable support baseline forward passes for subsequent queries.
    new_predictions = predictor.predict(all_smis, item["esm"], item["graph"])
    for sid, means in new_predictions.items():
        if sid != qid:
            item["cache"][sid] = means
    means = {qid: new_predictions[qid]}
    means.update({r["id"]: item["cache"][r["id"]] for r in supports})
    episode = PredictionEpisode(
        task_id="DAVIS_DEV_DEMO_" + item["id"],
        sequence_sha256=item["id"],
        protein_component_id=item["id"],
        assay_key=item["id"],
        support=tuple(SupportObservation(r["id"], r["smiles"], r["y"], item["id"]) for r in supports),
        queries=(QueryCompound(qid, query),),
    )
    result = adapt_episode(episode, means)[0]
    return {
        "target": target, "seed": SEED, "support_k": k,
        "sequence_pkd": result.sequence_pKd,
        "geometry_pkd": result.geometry_pKd,
        "uncalibrated_pkd": result.A,
        "calibrated_pkd": result.B,
        "full_pkd": result.D,
        "calibration_offset": result.offset,
        "geometry_delta": result.differential,
        "support_kernel_strength": result.W,
        "note": "Frozen model; DAVIS development targets/support only. Not validated for new molecules or clinical use."
    }


@app.get("/")
def home():
    return send_file(HERE / "index.html")


@app.get("/api/health")
def health():
    try:
        targets = list(_load_targets())
        return jsonify({"ok": True, "targets": targets, "model_loaded": MODEL is not None,
                        "device": MODEL["device"] if MODEL else "CUDA (lazy load)",
                        "scope": "LEGACY_DAVIS_DEVELOPMENT_ONLY"})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.get("/api/examples")
def examples():
    """Fixed, label-free example molecules from the real development pool."""
    targets = _load_targets()
    return jsonify({"examples": {name: item["pool"][26]["smiles"] for name, item in targets.items()},
                    "note": "DAVIS development examples; source affinities are not displayed."})


@app.get("/api/benchmarks")
def benchmarks():
    source = ROOT / "research/geometry_factorial_dev/factorial.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    return jsonify({
        "rows": data["macro_by_seed_K"],
        "seeds": data["seeds"], "support_sizes": data["support_sizes"],
        "protein_count": data["independent_dev_protein_count"],
        "draw_count": data["repeated_support_draws_per_protein"],
        "query_count": data["fixed_query_compounds_per_protein"],
        "status": data["status"],
        "source": "research/geometry_factorial_dev/factorial.json",
    })


@app.post("/api/chemistry")
def chemical_analysis():
    try:
        payload = request.get_json(force=True, silent=False)
        return jsonify(chemistry(payload.get("smiles")))
    except (ValueError, TypeError, AttributeError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/predict")
def live_inference():
    try:
        payload = request.get_json(force=True, silent=False)
        k = payload.get("k", 0)
        if type(k) is not int:
            raise ValueError("K must be a whole number.")
        with MODEL_LOCK:
            with short_gpu_lease():
                return jsonify(_predict(payload.get("target"), payload.get("smiles"), k))
    except (ValueError, TypeError, AttributeError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        app.logger.exception("Demo inference failed")
        return jsonify({"error": "Inference unavailable: " + str(exc)}), 503


if __name__ == "__main__":
    print("DynaCPI Research Demo: http://127.0.0.1:8765", flush=True)
    app.run(host="127.0.0.1", port=8765, debug=False, use_reloader=False, threaded=True)
