"""Run the pocket repair engineering checks; never train on biological labels."""
import hashlib,json,os,subprocess,sys,re
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"research/pocket_repair_20261110"
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env["PYTHONPATH"]=str(ROOT);env["PYTHONDONTWRITEBYTECODE"]="1"
    report={"status":"RUNNING","evidence":"ENGINEERING_ONLY_SYNTHETIC",
            "timestamp_utc":datetime.now(timezone.utc).isoformat(),"checks":[]}
    for name in ("pocket_interaction_repair_test.py","pocket_repair_training_test.py"):
        path=ROOT/"tests_v4"/name
        p=subprocess.run([sys.executable,str(path)],cwd=ROOT,env=env,capture_output=True,text=True,timeout=180)
        log=p.stdout+"\n"+p.stderr
        (OUT/(name+".log")).write_text(log,encoding="utf-8")
        count=re.search(r"Ran (\d+) tests?",log)
        report["checks"].append({"file":name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
           "exit_code":p.returncode,"test_count":int(count.group(1)) if count else None})
        print(name,p.returncode,flush=True)
    report["source_sha256"]={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [ROOT/"dynacpi/pocket_interaction_dev.py",ROOT/"scripts/train_pocket_repair_dev.py"]}
    report["status"]="PASS" if all(c["exit_code"]==0 for c in report["checks"]) else "FAIL"
    (OUT/"validation.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report),flush=True)
    return 0 if report["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
