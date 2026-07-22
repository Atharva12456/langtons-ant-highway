"""Build the complete, hash-audited search-record archive.

The large shard trees live in the sibling ``work`` directory rather than in the
Git checkout.  This script deliberately fails if any reported record family is
missing; silently producing a partial archive would invalidate the paper's
reproducibility claim.
"""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
WORK = REPO.parent / "work"
OUT = ROOT / "langton_search_records.tar.gz"
TEMP_OUT = ROOT / "langton_search_records.tar.gz.tmp"

SHARD_DIRS = (
    "p34_indep_shards", "p36_indep_shards", "p38_indep_shards",
    "p40_indep_shards", "p42_indep_shards", "p44_indep_shards",
    "p46_indep_shards", "p48_indep_shards",
    "p44_original_shards_independent_20260714", "p44_residue_shards_v2",
    "p46_original_shards", "p46_residue_shards",
    "p48_original_shards", "p48_residue_shards",
)

WORK_FILES = (
    "run_indep.sh",
    "run_indep_q.sh",
    "run_all.sh",
    "run_all.log",
    "chain_indep.sh",
    "chain_indep.log",
    "verify_nomonotone.py",
    "verify_criterion_indep.py",
    "cross_check_criterion.py",
    "crosscheck18.log",
)

REPO_FILES = (
    (REPO / "code/java/PositiveGrowthSearchIndep.java",
     "PositiveGrowthSearchIndep.java"),
    (REPO / "code/java/PositiveGrowthSearch.java", "java/PositiveGrowthSearch.java"),
    (REPO / "code/java/PositiveGrowthResidueSearch.java",
     "java/PositiveGrowthResidueSearch.java"),
    (REPO / "code/python/langton_research.py", "python/langton_research.py"),
    (ROOT / "aggregate_indep.py", "aggregate_indep.py"),
    (ROOT / "audit_p32.py", "audit_p32.py"),
    (ROOT / "rerun_p32.py", "rerun_p32.py"),
    (ROOT / "make_archive.py", "make_archive.py"),
    (ROOT / "p32_exclusion_summary.json", "p32_exclusion_summary.json"),
    (ROOT / "independent_exclusion_summary.json",
     "independent_exclusion_summary.json"),
)

COMMANDS = r"""# From the repository root: regenerate and audit the period <= 32
# first-R cyclic-phase certificate (all 32 choices of BITS in {R,L}^5):
python records/rerun_p32.py
python records/audit_p32.py

# From an extracted archive root, audit the packaged p<=32 and p34--48 records:
python audit_p32.py
python aggregate_indep.py

# From an extracted archive or equivalent work directory: regenerate the
# residue-theorem-free period-34--48 variant, one JVM per shard:
javac -d indep_classes PositiveGrowthSearchIndep.java
bash run_indep_q.sh 34 10 48 12 p34_indep_shards
bash run_indep_q.sh 36 11 48 12 p36_indep_shards
bash run_indep_q.sh 38 12 48 12 p38_indep_shards
bash run_indep_q.sh 40 13 48 12 p40_indep_shards
bash run_indep.sh 42 14 12 p42_indep_shards
bash run_indep.sh 44 15 12 p44_indep_shards
bash run_indep.sh 46 16 12 p46_indep_shards
bash run_indep_q.sh 48 17 96 11 p48_indep_shards
python aggregate_indep.py

# Criterion verifier written from the theorem statement, not the Java source:
python cross_check_criterion.py 18

# No-monotone-affine-invariant certificate:
python verify_nomonotone.py
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_member(members: dict[str, Path], source: Path, arcname: str) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"required archive member is missing: {source}")
    if arcname in members:
        raise ValueError(f"duplicate archive name: {arcname}")
    members[arcname] = source


def main() -> None:
    members: dict[str, Path] = {}
    shard_counts: dict[str, int] = {}

    for directory in SHARD_DIRS:
        source_dir = WORK / directory
        files = sorted(source_dir.glob("shard_*.json"))
        if not files:
            raise FileNotFoundError(f"missing shard family: {source_dir}")
        shard_counts[directory] = len(files)
        for path in files:
            add_member(members, path, f"{directory}/{path.name}")

    p32_root = WORK / "p32_current_shards"
    p32_files = sorted(p32_root.glob("highway_words_p32_*.json"))
    if len(p32_files) != 32:
        raise RuntimeError(f"expected 32 period-<=32 records, found {len(p32_files)}")
    shard_counts["p32_legal_trace_shards"] = len(p32_files)
    for path in p32_files:
        add_member(members, path, f"p32_legal_trace_shards/{path.name}")
    add_member(
        members,
        p32_root / "highway_words_p5_all.json",
        "p32_legal_trace_shards/highway_words_p5_all.json",
    )

    for name in WORK_FILES:
        add_member(members, WORK / name, name)
    for source, arcname in REPO_FILES:
        add_member(members, source, arcname)

    manifest = {
        "schema": "langton-search-records-v2",
        "description": (
            "Complete per-rank records for the period-34--48 searches, plus the "
            "unprefixed period-<=5 baseline and all 32 complete first-R "
            "six-symbol prefix-shard logs for the period-<=32 cyclic-phase "
            "enumeration. Every positive-growth heading-resetting word is "
            "represented up to cyclic phase."
        ),
        "packaging_environment": {
            "os": platform.platform(),
            "cpu": platform.processor(),
            "python": platform.python_version(),
            "java": subprocess.run(
                ["java", "-version"], capture_output=True, text=True, check=False
            ).stderr.strip(),
        },
        "commands": COMMANDS,
        "sha256": {name: sha256(path) for name, path in sorted(members.items())},
        "shard_counts": shard_counts,
    }

    manifest_path = ROOT / "RECORDS_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    with tarfile.open(TEMP_OUT, "w:gz", compresslevel=9) as archive:
        archive.add(manifest_path, arcname="RECORDS_MANIFEST.json")
        for arcname, source in sorted(members.items()):
            archive.add(source, arcname=arcname)

    with tarfile.open(TEMP_OUT, "r:gz") as archive:
        names = archive.getnames()
        expected_names = {"RECORDS_MANIFEST.json", *members.keys()}
        if len(names) != len(set(names)) or set(names) != expected_names:
            raise RuntimeError("temporary archive member-set audit failed")
        packed_manifest = json.load(archive.extractfile("RECORDS_MANIFEST.json"))
        for arcname, expected_hash in packed_manifest["sha256"].items():
            handle = archive.extractfile(arcname)
            if handle is None:
                raise RuntimeError(f"cannot read archived member: {arcname}")
            actual_hash = hashlib.sha256(handle.read()).hexdigest()
            if actual_hash != expected_hash:
                raise RuntimeError(f"temporary archive hash mismatch: {arcname}")

    TEMP_OUT.replace(OUT)
    print(f"wrote {OUT.name}: {OUT.stat().st_size / 1048576:.2f} MB")
    print(f"members: {len(members) + 1}")
    print(f"sha256: {sha256(OUT)}")
    for directory, count in shard_counts.items():
        print(f"{directory}: {count}")


if __name__ == "__main__":
    main()
