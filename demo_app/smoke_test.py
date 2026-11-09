"""Non-destructive local smoke tests for the DynaCPI demo server."""
import json, math, time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = "http://127.0.0.1:8765"
def fetch(path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = Request(BASE+path, data=data, headers={"Content-Type":"application/json"} if data else {})
    with urlopen(req, timeout=180) as r:
        return r.status, json.load(r) if path!="/" else r.read()
t0=time.perf_counter()
status,health=fetch("/api/health")
assert status==200 and health["ok"] and len(health["targets"])==4, health
print("HEALTH: PASS", health, flush=True)
status,b=fetch("/api/benchmarks")
assert status==200 and len(b["rows"])==18 and b["protein_count"]==4, b
print("BENCHMARKS: PASS, 18 rows",flush=True)
status,c=fetch("/api/chemistry",{"smiles":"Cn1c(=O)c2c(ncn2C)n(C)c1=O"})
assert status==200 and c["formula"]=="C8H10N4O2" and "<svg" in c["svg"], c
print("LIVE RDKIT: PASS", c["formula"],flush=True)
try:
    fetch("/api/chemistry",{"smiles":"not_a_smiles"})
    raise AssertionError("Invalid SMILES was accepted")
except HTTPError as e:
    assert e.code==400, e.code
print("INVALID SMILES REJECTION: PASS",flush=True)
status,p=fetch("/api/predict",{"smiles":c["canonical"],"target":"ADCK4","k":0})
assert status==200 and p["target"]=="ADCK4" and p["support_k"]==0 and math.isfinite(p["full_pkd"]), p
print("FROZEN MODEL ZERO-SHOT: PASS", {k:round(p[k],4) for k in ("sequence_pkd","geometry_pkd","full_pkd")},flush=True)
status,q=fetch("/api/predict",{"smiles":c["canonical"],"target":"ADCK4","k":5})
assert status==200 and q["support_k"]==5 and math.isfinite(q["full_pkd"]), q
print("FEW-SHOT ADAPTATION K=5: PASS", {k:round(q[k],4) for k in ("full_pkd","calibration_offset")},flush=True)
print("TOTAL PASS: 6 tests; seconds=",round(time.perf_counter()-t0,2),flush=True)
