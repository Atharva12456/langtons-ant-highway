#!/usr/bin/env python3
"""Independent structural and counter audit for the two period-44 searches."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RESIDUE_DIR = ROOT / "work" / "p44_residue_shards_v2"
ORIGINAL_DIR = ROOT / "work" / "p44_original_shards_independent_20260714"
SUMMARY_PATH = ROOT / "work" / "p44_independent_audit_summary_2026-07-14.json"
NOTE_PATH = ROOT / "work" / "p44_independent_audit_note_2026-07-14.md"

PERIOD = 44
PREFIX_LENGTH = 15
TOTAL_RANKS = 1 << (PREFIX_LENGTH - 1)
BOUNDARIES = [
    (0, 1638),
    (1638, 3276),
    (3276, 4915),
    (4915, 6553),
    (6553, 8192),
    (8192, 9830),
    (9830, 11468),
    (11468, 13107),
    (13107, 14745),
    (14745, 16384),
]

BASE_COUNTERS = [
    "nodes",
    "growth_prunes",
    "endpoint_prunes",
    "deficit_checks",
    "deficit_prunes",
    "deficit_endpoints_tested",
    "leaves",
    "p3_checks",
]
SHARED_COUNTERS = [
    "nodes",
    "growth_prunes",
    "endpoint_prunes",
    "deficit_checks",
    "deficit_prunes",
    "deficit_endpoints_tested",
    "leaves",
]
RESIDUE_COUNTERS = ["residue_checks", "residue_prunes"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def prefix_for_rank(rank: int) -> str:
    return "R" + "".join(
        "R" if ((rank >> bit) & 1) == 0 else "L"
        for bit in range(PREFIX_LENGTH - 2, -1, -1)
    )


def independently_valid_prefix(prefix: str) -> bool:
    # Directly implement only the two prefix-admission conditions: nonnegative
    # R-L balance, and alternation on every revisited physical cell.
    dx = (0, 1, 0, -1)
    dy = (1, 0, -1, 0)
    x = y = 0
    direction = 0
    balance = 0
    last_turn: dict[tuple[int, int], int] = {}
    for symbol in prefix:
        turn = 0 if symbol == "R" else 1
        previous = last_turn.get((x, y))
        if previous is not None and turn != 1 - previous:
            return False
        balance += 1 if turn == 0 else -1
        if balance < 0:
            return False
        last_turn[(x, y)] = turn
        direction = (direction + (1 if turn == 0 else -1)) & 3
        x += dx[direction]
        y += dy[direction]
    return True


def java_version() -> str:
    completed = subprocess.run(
        ["java", "-version"], check=True, text=True, capture_output=True
    )
    return (completed.stderr or completed.stdout).strip()


def load_family(directory: Path, schema: str, residue: bool) -> tuple[list[dict], dict[int, dict], list[dict]]:
    files = sorted(directory.glob("shard_*.json"))
    assert [path.name for path in files] == [f"shard_{i:02d}.json" for i in range(10)]
    all_records: dict[int, dict] = {}
    shard_summaries: list[dict] = []
    docs: list[dict] = []

    for index, (path, (start, stop)) in enumerate(zip(files, BOUNDARIES)):
        console = directory / f"shard_{index:02d}.console.txt"
        stderr = directory / f"shard_{index:02d}.stderr.txt"
        assert console.is_file() and stderr.is_file()
        assert stderr.stat().st_size == 0
        assert path.read_bytes() == console.read_bytes()

        doc = json.loads(path.read_text(encoding="utf-8"))
        docs.append(doc)
        assert doc["schema"] == schema
        assert doc["period"] == PERIOD
        assert doc["prefix_length"] == PREFIX_LENGTH
        assert (doc["rank_start"], doc["rank_stop"]) == (start, stop)
        assert doc["total_rank_count"] == TOTAL_RANKS
        assert doc["deficit_depths"] == []
        assert doc["search_complete"] is True
        assert doc["node_cap"] is None
        assert doc["hits"] == []
        records = doc["results"]
        assert len(records) == stop - start
        assert [record["rank"] for record in records] == list(range(start, stop))

        counters = BASE_COUNTERS + (RESIDUE_COUNTERS if residue else [])
        for counter in counters:
            assert doc[counter] == sum(record[counter] for record in records), (path, counter)
        assert doc["hits"] == [hit for record in records for hit in record["hits"]]

        for record in records:
            rank = record["rank"]
            assert rank not in all_records
            assert record["prefix"] == prefix_for_rank(rank)
            assert record["prefix_valid"] is independently_valid_prefix(record["prefix"])
            assert record["hits"] == []
            assert record["deficit_checks"] == 0
            assert record["deficit_prunes"] == 0
            assert record["deficit_endpoints_tested"] == 0
            if residue:
                assert record["residue_checks"] == record["leaves"]
                assert record["residue_prunes"] + record["p3_checks"] == record["residue_checks"]
            else:
                assert record["p3_checks"] == record["leaves"]
            all_records[rank] = record

        shard_summaries.append(
            {
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(path),
                "console_sha256": sha256(console),
                "stderr_sha256": sha256(stderr),
                "rank_start": start,
                "rank_stop": stop,
                "rank_count": stop - start,
                "valid_prefixes": sum(bool(record["prefix_valid"]) for record in records),
                "search_complete": doc["search_complete"],
                "node_cap": doc["node_cap"],
                "nodes": doc["nodes"],
                "growth_prunes": doc["growth_prunes"],
                "endpoint_prunes": doc["endpoint_prunes"],
                "leaves": doc["leaves"],
                "p3_checks": doc["p3_checks"],
                "residue_checks": doc.get("residue_checks"),
                "residue_prunes": doc.get("residue_prunes"),
                "hits": len(doc["hits"]),
                "seconds": doc["seconds"],
            }
        )

    assert sorted(all_records) == list(range(TOTAL_RANKS))
    return docs, all_records, shard_summaries


def aggregate(docs: list[dict], residue: bool) -> dict:
    counters = BASE_COUNTERS + (RESIDUE_COUNTERS if residue else [])
    result = {counter: sum(doc[counter] for doc in docs) for counter in counters}
    result.update(
        {
            "rank_count": sum(doc["rank_stop"] - doc["rank_start"] for doc in docs),
            "valid_prefixes": sum(
                bool(record["prefix_valid"])
                for doc in docs
                for record in doc["results"]
            ),
            "hits": sum(len(doc["hits"]) for doc in docs),
            "sum_shard_seconds": sum(doc["seconds"] for doc in docs),
        }
    )
    return result


def main() -> None:
    residue_docs, residue_by_rank, residue_shards = load_family(
        RESIDUE_DIR, "positive-growth-periodic-residue-search-v2", True
    )
    original_docs, original_by_rank, original_shards = load_family(
        ORIGINAL_DIR, "positive-growth-periodic-search-v1", False
    )

    mismatch_count = 0
    for rank in range(TOTAL_RANKS):
        residue_record = residue_by_rank[rank]
        original_record = original_by_rank[rank]
        for field in ["rank", "prefix", "prefix_valid", *SHARED_COUNTERS, "hits"]:
            if residue_record[field] != original_record[field]:
                mismatch_count += 1

    assert mismatch_count == 0
    residue_total = aggregate(residue_docs, True)
    original_total = aggregate(original_docs, False)
    for field in ["rank_count", "valid_prefixes", "hits", *SHARED_COUNTERS]:
        assert residue_total[field] == original_total[field], field
    assert original_total["p3_checks"] == original_total["leaves"]
    assert residue_total["residue_checks"] == residue_total["leaves"]
    assert residue_total["residue_prunes"] + residue_total["p3_checks"] == residue_total["leaves"]
    assert original_total["hits"] == residue_total["hits"] == 0

    source_paths = [
        ROOT / "outputs" / "PositiveGrowthSearch.java",
        ROOT / "work" / "PositiveGrowthResidueSearch.java",
        Path(__file__).resolve(),
    ]
    source_hashes = {
        str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
        for path in source_paths
    }

    validations = {
        "ten_expected_shards_each_family": True,
        "exact_contiguous_rank_coverage_0_through_16383": True,
        "no_duplicate_or_missing_ranks": True,
        "json_equals_console_bytes_for_every_shard": True,
        "all_stderr_empty": True,
        "all_search_complete_true": True,
        "all_node_cap_null": True,
        "all_shard_totals_equal_sums_of_per_rank_records": True,
        "all_prefix_strings_independently_recomputed": True,
        "all_prefix_valid_flags_independently_recomputed": True,
        "rank_by_rank_shared_counter_mismatches": mismatch_count,
        "aggregate_shared_counters_equal": True,
        "all_original_p3_checks_equal_original_leaves": True,
        "all_residue_checks_equal_residue_leaves": True,
        "residue_prunes_plus_residue_p3_checks_equal_residue_leaves": True,
        "original_hits": original_total["hits"],
        "residue_hits": residue_total["hits"],
    }

    command_template = (
        "java -cp outputs PositiveGrowthSearch --period 44 --prefix-length 15 "
        "--rank-start START --rank-stop STOP --deficit-depths 0 "
        "--output work/p44_original_shards_independent_20260714/shard_NN.json"
    )
    summary = {
        "schema": "langton-period-44-independent-cross-audit-v1",
        "audit_date": "2026-07-14",
        "host": {"python": platform.python_version(), "java": java_version()},
        "scope": {
            "period": PERIOD,
            "prefix_length": PREFIX_LENGTH,
            "rank_start": 0,
            "rank_stop": TOTAL_RANKS,
            "deficit_depths": [],
            "rank_boundaries": BOUNDARIES,
        },
        "commands": {
            "compile_original": "javac -d outputs outputs\\PositiveGrowthSearch.java",
            "original_shard_template": command_template,
            "audit": "python work\\p44_independent_audit.py",
        },
        "source_sha256": source_hashes,
        "residue": {"aggregate": residue_total, "shards": residue_shards},
        "original": {"aggregate": original_total, "shards": original_shards},
        "validations": validations,
        "conclusion": (
            "PASS: both exact searches cover all 16,384 ranks, have identical "
            "shared counters at every rank, and report zero hits."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    summary_hash = sha256(SUMMARY_PATH)

    note = f"""# Independent period-44 search audit

Date: 2026-07-14  
Scope: exact positive-growth finite-support periodic trace search, period 44,
prefix length 15, ranks 0 through 16,383, and no deficit depths.

## Verdict

**PASS.** The residue-aware and original engines both searched the full stated
rank interval with `search_complete=true`, `node_cap=null`, and zero hits. All
shared search counters agree rank-by-rank across all 16,384 records. This is an
independent computational exclusion of positive-growth periodic traces of
period 44 under the engines' rigorously documented normalization and pruning
rules; it is not a proof of the universal finite-seed highway conjecture.

## Exact run command

The original source was recompiled with:

```powershell
javac -d outputs outputs\\PositiveGrowthSearch.java
```

Ten processes used the following template, with the exact boundaries stored in
the summary JSON:

```powershell
{command_template}
```

The automated audit was run with:

```powershell
python work\\p44_independent_audit.py
```

## Aggregate counters

| Counter | Original | Residue-aware |
|---|---:|---:|
| Ranks | {original_total['rank_count']:,} | {residue_total['rank_count']:,} |
| Valid prefixes | {original_total['valid_prefixes']:,} | {residue_total['valid_prefixes']:,} |
| Nodes | {original_total['nodes']:,} | {residue_total['nodes']:,} |
| Growth prunes | {original_total['growth_prunes']:,} | {residue_total['growth_prunes']:,} |
| Endpoint prunes | {original_total['endpoint_prunes']:,} | {residue_total['endpoint_prunes']:,} |
| Leaves | {original_total['leaves']:,} | {residue_total['leaves']:,} |
| Residue prunes | n/a | {residue_total['residue_prunes']:,} |
| P3 checks | {original_total['p3_checks']:,} | {residue_total['p3_checks']:,} |
| Hits | {original_total['hits']:,} | {residue_total['hits']:,} |

Thus the residue theorem removes
{residue_total['residue_prunes']:,} / {residue_total['leaves']:,} surviving
leaves before P3, while preserving all shared counters and the zero-hit result.

## Validation performed

- Exactly ten expected JSON shards exist in each family.
- The shard intervals abut exactly and cover every rank in `[0, 16384)` once.
- Every JSON file is byte-identical to its captured stdout; every stderr file is empty.
- Every shard has the expected schema/configuration, `search_complete=true`, and `node_cap=null`.
- Every top-level counter was recomputed as the sum of its per-rank records.
- Every prefix string and every `prefix_valid` flag was independently recomputed.
- `nodes`, both ordinary prune counters, all deficit counters, `leaves`, and `hits`
  agree rank-by-rank between engines; mismatch count: {mismatch_count}.
- Original `p3_checks = leaves`; residue-aware
  `residue_prunes + p3_checks = residue_checks = leaves`.
- Both engines report zero per-rank and aggregate hits.

## Hashes

- `outputs/PositiveGrowthSearch.java`: `{source_hashes['outputs/PositiveGrowthSearch.java']}`
- `work/PositiveGrowthResidueSearch.java`: `{source_hashes['work/PositiveGrowthResidueSearch.java']}`
- `work/p44_independent_audit.py`: `{source_hashes['work/p44_independent_audit.py']}`
- `work/p44_independent_audit_summary_2026-07-14.json`: `{summary_hash}`

Every shard JSON, console, and stderr SHA-256 is recorded individually in the
summary JSON. Timing fields were deliberately excluded from cross-engine
equality because they are not mathematical counters.
"""
    NOTE_PATH.write_text(note, encoding="utf-8")
    print(json.dumps({
        "verdict": "PASS",
        "summary": str(SUMMARY_PATH),
        "summary_sha256": summary_hash,
        "note": str(NOTE_PATH),
        "note_sha256": sha256(NOTE_PATH),
        "original_aggregate": original_total,
        "residue_aggregate": residue_total,
        "rank_mismatches": mismatch_count,
    }, indent=2))


if __name__ == "__main__":
    main()
