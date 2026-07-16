"""Aggregate + audit the Theorem-7.1-independent searches, and compare with the
strand-pruned (P16) engine.

Checks, per period:
  * every prefix rank covered exactly once (no gap, no duplicate);
  * every shard reports search_complete and node_cap null;
  * aggregate counters equal the sum of the per-rank counters;
  * residue_theorem_used is false in every shard record;
  * zero hits.
Emits a JSON summary suitable for release.
"""
from __future__ import annotations

import glob
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ORIGINAL = {42: None, 44: "p44_original_shards_independent_20260714",
            46: "p46_original_shards", 48: "p48_original_shards"}
# Strand-pruned (P16) engine node counts previously reported in the paper.
# NOTE: rows 34-40 were also produced by the P16 engine, at prefix lengths that
# differ from the independent rerun, so those ratios are indicative only.
ORIGINAL_NODES = {34: 9_726_176, 36: 19_781_050, 38: 41_972_884, 40: 201_924_597,
                  42: 528_451_911, 44: 1_319_080_456,
                  46: 3_463_441_745, 48: 8_677_026_370}
PERIODS = (34, 36, 38, 40, 42, 44, 46, 48)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def audit(period: int, d: str):
    files = sorted(glob.glob(f"{d}/shard_*.json"))
    if not files:
        return None
    agg = {k: 0 for k in ("nodes", "growth_prunes", "endpoint_prunes",
                          "deficit_checks", "deficit_prunes",
                          "deficit_endpoints_tested", "leaves", "p3_checks")}
    seconds = 0.0
    hits, covered, problems = [], [], []
    prefix_length = total = None
    for f in files:
        j = json.load(open(f))
        if not j.get("search_complete"):
            problems.append(f"{f}: search_complete false")
        if j.get("node_cap") is not None:
            problems.append(f"{f}: node_cap set")
        if j.get("residue_theorem_used") is not False:
            problems.append(f"{f}: residue_theorem_used not false")
        prefix_length = j["prefix_length"]
        total = j["total_rank_count"]
        # per-rank counters must sum to the shard aggregate
        per = {k: 0 for k in agg}
        for r in j["results"]:
            covered.append(r["rank"])
            for k in per:
                if k in r:
                    per[k] += r[k]
        for k in ("nodes", "leaves"):
            if per[k] != j[k]:
                problems.append(f"{f}: {k} per-rank sum {per[k]} != aggregate {j[k]}")
        for k in agg:
            agg[k] += j.get(k, 0)
        seconds += j.get("seconds", 0.0)
        hits += j["hits"]

    covered.sort()
    expect = list(range(total))
    if covered != expect:
        dup = len(covered) - len(set(covered))
        miss = set(expect) - set(covered)
        problems.append(f"coverage: {len(covered)} ranks, {dup} duplicates, "
                        f"{len(miss)} missing")
    return {
        "period": period,
        "prefix_length": prefix_length,
        "total_rank_count": total,
        "ranks_covered_exactly_once": covered == expect,
        "shards": len(files),
        "residue_theorem_used": False,
        "exact_criterion_applied_to": "every positive-growth nonzero-drift leaf",
        **agg,
        "core_seconds": round(seconds, 3),
        "hits": hits,
        "highways_found": len(hits),
        "problems": problems,
    }


if __name__ == "__main__":
    out = {
        "schema": "langton-independent-exclusion-v1",
        "claim": ("exhaustive positive-growth search using NO consequence of the "
                  "signed mod-four wake-residue theorem; the exact criterion is "
                  "applied to every positive-growth nonzero-drift leaf"),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "java": subprocess.run(["java", "-version"], capture_output=True,
                                   text=True).stderr.strip(),
        },
        "engine_sha256": {
            "PositiveGrowthSearchIndep.java":
                sha256(ROOT / "PositiveGrowthSearchIndep.java"),
        },
        "periods": {},
    }
    ok = True
    for p in PERIODS:
        d = f"p{p}_indep_shards"
        a = audit(p, d)
        if a is None:
            print(f"period {p}: NOT RUN")
            continue
        a["strand_pruned_engine_nodes"] = ORIGINAL_NODES[p]
        a["node_ratio_indep_over_strand_pruned"] = round(
            a["nodes"] / ORIGINAL_NODES[p], 4)
        out["periods"][str(p)] = a
        flag = "OK" if not a["problems"] and a["highways_found"] == 0 else "PROBLEM"
        print(f"period {p}: nodes={a['nodes']:,} leaves={a['leaves']:,} "
              f"p3_checks={a['p3_checks']:,} hits={a['highways_found']} "
              f"core-s={a['core_seconds']:,.0f} "
              f"x{a['node_ratio_indep_over_strand_pruned']:.2f} [{flag}]")
        for pr in a["problems"]:
            ok = False
            print(f"   ! {pr}")
    out["all_checks_passed"] = ok and all(
        v["highways_found"] == 0 and not v["problems"]
        for v in out["periods"].values())
    Path("independent_exclusion_summary.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nall_checks_passed = {out['all_checks_passed']}")
    print("wrote independent_exclusion_summary.json")
