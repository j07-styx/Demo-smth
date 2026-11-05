"""Unit tests for artifact-level research gate. Fake entries are synthetic."""
import json
import sys
import tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from dynacpi.scientific_cohort_gate import require_approved_cohort, sha256, ROLES, current_status

real=current_status(root)
assert real["status"]=="BLOCKED_UNAPPROVED_NOT_TRAINING_READY"

with tempfile.TemporaryDirectory(prefix="synthetic_cohort_gate_") as temp:
    temp=Path(temp)
    cohort_path=temp/"fictional_approved.json"
    split_path=temp/"fictional_frozen.json"
    synthetic_tasks=[
        {"task_id":"fake_task_"+str(n),
         "protein_component_id":"fake_component_"+str(n),
         "source_review_record_id":"fake_human_review_test_"+str(n),
         "n_unique_compounds":15}
         for n in range(30)]
    co={"status":"APPROVED_EXPERIMENTAL_COHORT_SOURCE_REVIEWED",
        "review_policy_id":"FAKE_TEST_ONLY",
        "reviewer_identity":"AUTOMATED_UNIT_TEST_NOT_HUMAN",
        "review_evidence_manifest_sha256":"FAKE_TEST_ONLY",
        "tasks":synthetic_tasks}
    cohort_path.write_text(json.dumps(co),encoding="utf-8")
    assignment={x["task_id"]:ROLES[i//6] for i,x in enumerate(synthetic_tasks)}
    split={"status":"FROZEN_PROTEIN_GROUP_SPLIT","cohort_sha256":sha256(cohort_path),
           "split_policy_id":"SYNTHETIC_TEST_ONLY","freeze_timestamp_utc":"2026-11-05T00:00:00+00:00",
           "frozen_by":"AUTOMATED_UNIT_TEST","task_roles":assignment}
    split_path.write_text(json.dumps(split),encoding="utf-8")
    passed=require_approved_cohort(cohort_path,split_path)
    assert passed["status"]=="ARTIFACT_GATE_PASSED_NOT_BIOLOGICAL_VALIDATION"
    # Contradict protein component independence without altering task identities.
    contaminated=dict(split)
    ta=dict(assignment)
    co["tasks"][7]["protein_component_id"]=co["tasks"][1]["protein_component_id"]
    cohort_path.write_text(json.dumps(co),encoding="utf-8")
    contaminated["cohort_sha256"]=sha256(cohort_path)
    contaminated["task_roles"]=ta
    split_path.write_text(json.dumps(contaminated),encoding="utf-8")
    try:
        require_approved_cohort(cohort_path,split_path)
    except PermissionError as exc:
        assert "component assigned multiple roles" in str(exc)
    else:
        raise AssertionError("Protein component leaked across training and validation")
    # Original cohort with a split tied to a different manifest must be rejected.
    co["tasks"][7]["protein_component_id"]="fake_component_7"
    cohort_path.write_text(json.dumps(co),encoding="utf-8")
    try:
        require_approved_cohort(cohort_path,split_path)
    except PermissionError as exc:
        assert "cohort changed" in str(exc)
    else:
        raise AssertionError("Unexpected altered cohort accepted")

report={"status":"PASS","real_scientific_cohort":"BLOCKED_NOT_APPROVED",
        "test_synthetic_only":True,
        "unit_checks":["reject missing science-approved manifests",
          "accept internally consistent fictional metadata for structural testing only",
          "reject protein component reuse between roles",
          "reject changed cohort checksum"],
        "warning":"Mock artifact consistency is not source-level experimental verification."}
dest=root/"data/audit/scientific_cohort_gate_validation.json"
dest.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2),flush=True)
