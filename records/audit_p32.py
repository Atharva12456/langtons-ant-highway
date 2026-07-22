"""Audit the first-R cyclic-phase search certificate through period 32."""
from __future__ import annotations

import itertools
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent.parent / "work"
CURRENT = WORK / "p32_current_shards"
ARCHIVE_DIR = ROOT / "p32_legal_trace_shards"
EXPECTED_NODES = 46_185_421
EXPECTED_BASELINE_NODES = 59


def main() -> None:
    source = ARCHIVE_DIR if ARCHIVE_DIR.is_dir() else CURRENT
    files = sorted(source.glob("highway_words_p32_*.json"))
    expected = {"R" + "".join(bits) for bits in itertools.product("RL", repeat=5)}
    seen: set[str] = set()
    problems: list[str] = []
    nodes = 0
    seconds = 0.0

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        prefix = data.get("prefix")
        seen.add(prefix)
        if path.stem != f"highway_words_p32_{prefix}":
            problems.append(f"{path.name}: filename/prefix mismatch")
        if data.get("max_period") != 32:
            problems.append(f"{path.name}: max_period is not 32")
        if data.get("search_complete") is not True:
            problems.append(f"{path.name}: search_complete is not true")
        if data.get("exact_period") is not False:
            problems.append(f"{path.name}: exact_period is not false")
        if data.get("target_growth") is not None:
            problems.append(f"{path.name}: target_growth is not null")
        if data.get("proved_clean_pruning") is not False:
            problems.append(f"{path.name}: proved_clean_pruning is not false")
        cap = data.get("node_cap")
        if not isinstance(cap, int) or data.get("nodes", cap) >= cap:
            problems.append(f"{path.name}: configured cap was absent or reached")
        if data.get("highways_found") != 0 or data.get("highways") != []:
            problems.append(f"{path.name}: nonempty hit record")
        nodes += int(data.get("nodes", 0))
        seconds += float(data.get("seconds", 0.0))

    if seen != expected:
        problems.append(
            f"prefix partition mismatch: missing={sorted(expected-seen)}, "
            f"extra={sorted(seen-expected)}"
        )
    if nodes != EXPECTED_NODES:
        problems.append(f"node total {nodes} != {EXPECTED_NODES}")

    baseline_path = source / "highway_words_p5_all.json"
    if not baseline_path.is_file():
        problems.append("missing unprefixed period-<=5 baseline")
        baseline = {}
    else:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        baseline_cap = baseline.get("node_cap")
        if (
            baseline.get("max_period") != 5
            or baseline.get("prefix") != ""
            or baseline.get("search_complete") is not True
            or baseline.get("exact_period") is not False
            or baseline.get("target_growth") is not None
            or baseline.get("proved_clean_pruning") is not False
            or not isinstance(baseline_cap, int)
            or baseline.get("nodes", baseline_cap) >= baseline_cap
            or baseline.get("nodes") != EXPECTED_BASELINE_NODES
            or baseline.get("highways_found") != 0
            or baseline.get("highways") != []
        ):
            problems.append("invalid unprefixed period-<=5 baseline")

    summary = {
        "schema": "langton-p32-exclusion-v2",
        "max_period": 32,
        "prefix_partition": "R followed by every 5-symbol R/L word",
        "records": len(files),
        "prefixes_covered_exactly_once": len(files) == 32 and seen == expected,
        "configured_node_cap_per_shard": 100_000_000,
        "pruning_metadata_checked": {
            "exact_period": False,
            "target_growth": None,
            "proved_clean_pruning": False,
        },
        "largest_shard_nodes": max(
            (json.loads(p.read_text(encoding="utf-8"))["nodes"] for p in files),
            default=0,
        ),
        "nodes": nodes,
        "period_le_5_baseline_nodes": baseline.get("nodes"),
        "cyclic_phase_normalized_nodes_through_period_32": (
            nodes + int(baseline.get("nodes", 0))
        ),
        "coverage": (
            "all first-R cyclic-phase representatives through period 32, plus "
            "the unprefixed period-<=5 baseline; every positive-growth "
            "heading-resetting word is represented"
        ),
        "aggregate_shard_seconds": round(seconds, 6),
        "highways_found": 0,
        "problems": problems,
        "all_checks_passed": not problems,
        "generator_sha256": hashlib.sha256(
            ((ROOT / "python/langton_research.py") if ARCHIVE_DIR.is_dir() else
             (ROOT.parent / "code/python/langton_research.py")).read_bytes()
        ).hexdigest(),
    }
    output = ROOT / "p32_exclusion_summary.json"
    output.write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(summary, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
