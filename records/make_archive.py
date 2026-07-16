"""Package the COMPLETE per-rank shard records for release.

Review round 7, point 3: aggregate summaries alone are weaker than the certificate.
Uncompressed the records are ~150 MB; compressed they are a few MB, so there is no
reason not to ship them.  This builds a single .tar.gz containing:

  * every shard record (per-rank node/leaf/prune/p3 counters, wall time, hit list)
    for the independent, strand-pruned, and residue-pruned engines;
  * the aggregation + coverage audit output;
  * the engine sources actually used, with SHA-256;
  * environment strings (OS, CPU, JVM, Python);
  * the exact commands.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "langton_search_records.tar.gz"

DIRS = [
    "p42_indep_shards", "p44_indep_shards", "p46_indep_shards", "p48_indep_shards",
    "p34_indep_shards", "p36_indep_shards", "p38_indep_shards", "p40_indep_shards",
    "p44_original_shards_independent_20260714", "p44_residue_shards_v2",
    "p46_original_shards", "p46_residue_shards",
    "p48_original_shards", "p48_residue_shards",
]
FILES = [
    "PositiveGrowthSearchIndep.java",
    "independent_exclusion_summary.json",
    "aggregate_indep.py",
    "run_indep.sh",
    "verify_nomonotone.py",
    "verify_criterion_indep.py",
    "cross_check_criterion.py",
    "crosscheck18.log",
]
REPO_FILES = [
    "../langtons-ant-highway/code/java/PositiveGrowthSearch.java",
    "../langtons-ant-highway/code/java/PositiveGrowthResidueSearch.java",
]

COMMANDS = """\
# Independent (residue-theorem-free) engine, one JVM per shard:
javac -d indep_classes PositiveGrowthSearchIndep.java
bash run_indep.sh 42 14 12 p42_indep_shards
bash run_indep.sh 44 15 12 p44_indep_shards
bash run_indep.sh 46 16 12 p46_indep_shards
bash run_indep.sh 48 17 12 p48_indep_shards
python aggregate_indep.py          # coverage + counter audit -> summary JSON

# Criterion verifier written from the theorem statement, not the Java source:
python cross_check_criterion.py 18 # literal Thm 3.1 vs Remark 3.2 shortcut vs Java

# No-monotone-invariant certificate (Prop. 4.4):
python verify_nomonotone.py
"""


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    manifest = {
        "schema": "langton-search-records-v1",
        "description": ("Complete per-rank shard records for every exhaustive "
                        "search reported in the paper, plus audit output, engine "
                        "sources, environment, and exact commands."),
        "environment": {
            "os": platform.platform(),
            "cpu": platform.processor(),
            "python": platform.python_version(),
            "java": subprocess.run(["java", "-version"], capture_output=True,
                                   text=True).stderr.strip(),
        },
        "commands": COMMANDS,
        "sha256": {},
        "shard_counts": {},
    }
    members = []
    for d in DIRS:
        p = ROOT / d
        if not p.is_dir():
            continue
        js = sorted(p.glob("shard_*.json"))
        manifest["shard_counts"][d] = len(js)
        members += js
    for f in FILES:
        p = ROOT / f
        if p.exists():
            members.append(p)
    for f in REPO_FILES:
        p = (ROOT / f).resolve()
        if p.exists():
            members.append(p)

    for p in members:
        manifest["sha256"][p.name if p.parent == ROOT else
                           f"{p.parent.name}/{p.name}"] = sha256(p)

    man_path = ROOT / "RECORDS_MANIFEST.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with tarfile.open(OUT, "w:gz", compresslevel=9) as tf:
        tf.add(man_path, arcname="RECORDS_MANIFEST.json")
        for p in members:
            arc = (p.name if p.parent == ROOT
                   else f"{p.parent.name}/{p.name}")
            tf.add(p, arcname=arc)

    size = OUT.stat().st_size
    print(f"wrote {OUT.name}: {size/1048576:.2f} MB, {len(members)+1} members")
    print(f"  sha256 = {sha256(OUT)}")
    for d, n in manifest["shard_counts"].items():
        print(f"  {d}: {n} shards")


if __name__ == "__main__":
    main()
