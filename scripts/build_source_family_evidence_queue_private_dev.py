"""Construct a PRIVATE source-evidence queue for known provisional split crossings.

Input strictly precomputed metadata: publication family preflight, 40 source-review
leads, and local role-conflict worksheet. No assay records/affinities read.
Do not publish family-to-role mappings, even hashes.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "research/bindingdb_publication_connected_protein_review_preflight_20261108.json"
PRIVATE = ROOT / "data/audit/PROVISIONAL_SOURCE_SPLIT_REVIEW_PRIVATE_20261108.csv"
OUT = ROOT / "data/audit/PROVISIONAL_SOURCE_FAMILY_EVIDENCE_QUEUE_PRIVATE_20261108.json"


def project_review_evidence(preflight: dict, rows: list[dict]) -> list[dict]:
    family_members = preflight["linkage"]["family_members"]
    families = sorted(set(r["source_family_sha256"] for r in rows))
    if not families:
        raise ValueError("Empty conflict queue")
    leads = defaultdict(list)
    for lead in preflight["source_independent_review_leads"]:
        if lead["source_family_id"] in families:
            leads[lead["source_family_id"]].append({
                "task_id": lead["task_id"],
                "source_doi_candidates": lead["doi_candidates"],
                "source_pmid_candidates": lead["pmid_candidates"],
                "source_patent_candidates": lead["patent_candidates"],
                "target_name_candidates": lead["target_names"],
                "uniprot_accessions_from_metadata": lead["uniprot_accessions"],
                "assay_text_method_keywords_unverified": lead["explicit_physical_binding_method_keywords"],
                "method_risk_keyword_flags_unverified": lead["potential_indirect_or_competition_keywords"],
                "review_status": "UNREVIEWED_PRIMARY_SOURCE_REQUIRED",
            })
    prefixes = defaultdict(set)
    for family, members in family_members.items():
        for comp in members:
            prefixes[comp[:12]].add(family)
    examples = defaultdict(set)
    for source, info in preflight["linkage"]["shared_identifier_examples"].items():
        for prefix in info["component_prefixes"]:
            for family in prefixes[prefix]:
                if family in families:
                    examples[family].add(source)
    group_rows = defaultdict(list)
    for row in rows:
        group_rows[row["source_family_sha256"]].append(row)
    result = []
    for family in families:
        if family not in family_members:
            raise ValueError("Source family absent from preflight")
        assigned = group_rows[family]
        role_counts = Counter(row["provisional_role"] for row in assigned)
        if len(role_counts) < 2:
            raise ValueError("Reviewer queue included non-conflicting family")
        existing_components = set(family_members[family])
        if not {r["protein_component_sha256"] for r in assigned} <= existing_components:
            raise ValueError("Reviewer queue conflicts with source family membership")
        result.append({
            "source_family_sha256": family,
            "affected_provisional_role_component_counts": dict(sorted(role_counts.items())),
            "pre_split_family_protein_components": len(family_members[family]),
            "source_identifier_examples_only_not_exhaustive": sorted(examples[family]),
            "preexisting_ranked_source_leads": leads[family],
            "human_review_required": [
                "Find all underlying source DOI/PMID/patent links, including unrepresented tasks",
                "Locate original binding measurement table and supplementary methods",
                "Confirm KD vs IC50/Ki/activity or indirect displacement and qualifier handling",
                "Verify exact protein construct, domains, tags, mutations and chain composition",
                "Check pH, temperature, assay technology, replicate and library batch",
                "Document direct original-record alignment and reviewer evidence",
                "Adjudicate source-family disjointness prior to any new split freeze",
            ],
            "review_status": "UNREVIEWED_METADATA_CONFLICT_NOT_APPROVED",
        })
    return result


def main():
    if OUT.exists():
        raise FileExistsError("Refusing to overwrite local confidential source queue")
    source = json.loads(PREFLIGHT.read_text(encoding="utf-8-sig"))
    if source.get("scientific_gate") != "BLOCKED_UNAPPROVED_NOT_TRAINING_READY":
        raise PermissionError("Unexpected scientific review gate")
    with PRIVATE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    result = project_review_evidence(source, rows)
    if len(result) != 7 or sum(len(x["preexisting_ranked_source_leads"]) for x in result) != 5:
        raise ValueError("Unexpected review lead/source-family counts")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("x", encoding="utf-8") as f:
        json.dump({
            "status": "PRIVATE_HUMAN_REVIEW_QUEUE_UNAPPROVED",
            "input_scope": "Precomputed source metadata only, no raw assay records or labels",
            "families": result,
        }, f, indent=2)
        f.write("\n")
    print(json.dumps({
        "conflicting_families": len(result),
        "lead_coverage": sum(bool(x["preexisting_ranked_source_leads"]) for x in result),
        "families_without_preexisting_priority_lead": sum(not x["preexisting_ranked_source_leads"] for x in result),
        "with_sample_source_identifier_examples": sum(bool(x["source_identifier_examples_only_not_exhaustive"]) for x in result),
        "human_approved": 0,
        "confidential_local_output": str(OUT.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
