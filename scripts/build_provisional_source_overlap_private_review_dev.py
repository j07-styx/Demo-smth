"""Private metadata-only review worklist for provisional source-linked split crossings.

Reads only the published source-family preflight, split role manifest and our
aggregate overlap audit. Does not read any labels, protein sequences, SMILES,
predictions, or reserved-test outcomes. Output is LOCAL ONLY under data/audit.
"""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/bindingdb_publication_connected_protein_review_preflight_20261108.json"
SPLIT = ROOT / "research/bindingdb_frozen_component_split_manifest_dev.json"
AUDIT = ROOT / "research/bindingdb_provisional_role_source_overlap_audit_20261108.json"
OUT = ROOT / "data/audit/PROVISIONAL_SOURCE_SPLIT_REVIEW_PRIVATE_20261108.csv"
FIELDS = ("source_family_sha256", "protein_component_sha256", "provisional_role",
          "source_family_roles", "components_in_selected_family",
          "review_status")


def review_rows(mapping, roles):
    by_family = defaultdict(list)
    seen = set()
    for role in ("train", "inner_dev", "test"):
        for component in roles[role]:
            if component in seen:
                raise ValueError("Component appears in multiple roles")
            if component not in mapping:
                raise ValueError("Unknown component")
            seen.add(component)
            by_family[mapping[component]].append((role, component))
    rows = []
    for family in sorted(by_family):
        members = by_family[family]
        family_roles = {r for r, _ in members}
        if len(family_roles) < 2:
            continue
        role_summary = "+".join(r for r in ("train", "inner_dev", "test") if r in family_roles)
        for role, component in sorted(members):
            rows.append({
                "source_family_sha256": family,
                "protein_component_sha256": component,
                "provisional_role": role,
                "source_family_roles": role_summary,
                "components_in_selected_family": len(members),
                "review_status": "UNREVIEWED_METADATA_CONFLICT",
            })
    return rows


def main():
    if OUT.exists():
        raise FileExistsError("Existing confidential reviewer worklist; do not overwrite")
    src = json.loads(SOURCE.read_text(encoding="utf-8-sig"))
    split = json.loads(SPLIT.read_text(encoding="utf-8-sig"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8-sig"))
    if src["scientific_gate"] != "BLOCKED_UNAPPROVED_NOT_TRAINING_READY":
        raise PermissionError("Source scientific gate unexpectedly changed")
    for path, key in ((SOURCE, "original_source_linkage_sha256"),
                      (SPLIT, "original_provisional_split_sha256")):
        if hashlib.sha256(path.read_bytes()).hexdigest() != audit[key]:
            raise ValueError("Input manifest no longer matches verified audit")
    roles = {"train": split["train_components"],
             "inner_dev": split["inner_dev_components"],
             "test": split["test_components"]}
    rows = review_rows(src["linkage"]["source_family_by_protein_component"], roles)
    if len(rows) != audit["components_in_cross_role_families"]:
        raise ValueError("Cross-role component count differs from immutable audit")
    if len({r["source_family_sha256"] for r in rows}) != audit["families_crossing_two_or_more_roles"]:
        raise ValueError("Source family count differs from immutable audit")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("x", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({
        "status": "PRIVATE_METADATA_ONLY_HUMAN_REVIEW_WORKLIST_CREATED",
        "cross_role_families": len({r["source_family_sha256"] for r in rows}),
        "affected_components": len(rows),
        "role_counts": dict(Counter(r["provisional_role"] for r in rows)),
        "no_affinity_labels_or_test_predictions_accessed": True,
        "zero_source_approvals": True,
        "location": str(OUT.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
