"""Aggregate the residue-theorem-free searches and compare with the P16 variant.

Checks, per period:
  * every prefix rank covered exactly once (no gap, no duplicate);
  * every shard reports search_complete and node_cap null;
  * aggregate counters equal the sum of the per-rank counters;
  * shard period/prefix/rank-interval metadata are mutually consistent;
  * each result rank and encoded prefix matches the declared shard interval;
  * per-rank hit lists aggregate exactly to the shard hit list;
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
    files = sorted(str(path) for path in (ROOT / d).glob("shard_*.json"))
    if not files:
        return None
    agg = {k: 0 for k in ("nodes", "growth_prunes", "endpoint_prunes",
                          "deficit_checks", "deficit_prunes",
                          "deficit_endpoints_tested", "leaves", "p3_checks")}
    seconds = 0.0
    hits, covered, problems = [], [], []
    prefix_length = total = None
    for f in files:
        with open(f, encoding="utf-8") as stream:
            j = json.load(stream)
        if j.get("period") != period:
            problems.append(f"{f}: period {j.get('period')} != expected {period}")
        if not j.get("search_complete"):
            problems.append(f"{f}: search_complete false")
        if j.get("node_cap") is not None:
            problems.append(f"{f}: node_cap set")
        if j.get("residue_theorem_used") is not False:
            problems.append(f"{f}: residue_theorem_used not false")
        shard_prefix_length = j.get("prefix_length")
        shard_total = j.get("total_rank_count")
        if (not isinstance(shard_prefix_length, int) or shard_prefix_length < 1
                or not isinstance(shard_total, int)):
            problems.append(
                f"{f}: invalid prefix metadata "
                f"{(shard_prefix_length, shard_total)!r}")
            continue
        if shard_total != 1 << (shard_prefix_length - 1):
            problems.append(
                f"{f}: total_rank_count {shard_total} inconsistent with "
                f"prefix_length {shard_prefix_length}")
        if prefix_length is None:
            prefix_length, total = shard_prefix_length, shard_total
        elif (shard_prefix_length, shard_total) != (prefix_length, total):
            problems.append(
                f"{f}: prefix metadata {(shard_prefix_length, shard_total)} != "
                f"{(prefix_length, total)}")
        start, stop = j.get("rank_start"), j.get("rank_stop")
        if (not isinstance(start, int) or not isinstance(stop, int)
                or not (0 <= start <= stop <= shard_total)):
            problems.append(f"{f}: invalid rank interval [{start},{stop})")
            expected_ranks = []
        else:
            expected_ranks = list(range(start, stop))
        actual_ranks = [r.get("rank") for r in j.get("results", [])]
        if actual_ranks != expected_ranks:
            problems.append(
                f"{f}: result ranks do not equal declared interval [{start},{stop})")
        if j.get("deficit_depths") != []:
            problems.append(
                f"{f}: deficit_depths {j.get('deficit_depths')!r} != []")
        for key in ("deficit_checks", "deficit_prunes",
                    "deficit_endpoints_tested"):
            if j.get(key) != 0:
                problems.append(f"{f}: inactive deficit counter {key} is {j.get(key)!r}")
        # per-rank counters must sum to the shard aggregate
        per = {k: 0 for k in agg}
        per_hits = []
        for r in j.get("results", []):
            rank = r.get("rank")
            if isinstance(rank, int):
                covered.append(rank)
                expected_prefix = "R" + "".join(
                    "L" if rank & (1 << bit) else "R"
                    for bit in range(shard_prefix_length - 2, -1, -1))
                if r.get("prefix") != expected_prefix:
                    problems.append(
                        f"{f}: rank {rank} prefix {r.get('prefix')!r} != "
                        f"{expected_prefix!r}")
            else:
                problems.append(f"{f}: invalid result rank {rank!r}")
            for k in per:
                if k not in r:
                    problems.append(f"{f}: rank {rank} missing counter {k}")
                else:
                    per[k] += r[k]
            rank_hits = r.get("hits")
            if not isinstance(rank_hits, list):
                problems.append(f"{f}: rank {rank} hits is not a list")
            else:
                per_hits.extend(rank_hits)
        shard_hits = j.get("hits")
        if not isinstance(shard_hits, list):
            problems.append(f"{f}: shard hits is not a list")
            shard_hits = []
        if per_hits != shard_hits:
            problems.append(f"{f}: per-rank hit lists do not equal shard hits")
        for k in agg:
            if k not in j:
                problems.append(f"{f}: missing aggregate counter {k}")
            elif per[k] != j[k]:
                problems.append(f"{f}: {k} per-rank sum {per[k]} != aggregate {j[k]}")
        if j.get("p3_checks") != j.get("leaves"):
            problems.append(
                f"{f}: p3_checks {j.get('p3_checks')} != leaves {j.get('leaves')}")
        for k in agg:
            agg[k] += j.get(k, 0)
        seconds += j.get("seconds", 0.0)
        hits += shard_hits

    covered.sort()
    expect = list(range(total)) if isinstance(total, int) else []
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
        "deficit_rule_active": False,
        "exact_criterion_applied_to": "every positive-growth nonzero-drift leaf",
        **agg,
        "core_seconds": round(seconds, 3),
        "hits": hits,
        "highways_found": len(hits),
        "problems": problems,
    }


if __name__ == "__main__":
    out = {
        "schema": "langton-residue-free-exclusion-v2",
        "claim": ("exhaustive positive-growth search using NO consequence of the "
                  "signed mod-four wake-residue theorem; the exact criterion is "
                  "applied to every positive-growth nonzero-drift leaf"),
        "audit_environment": {
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
    missing_periods = []
    for p in PERIODS:
        d = f"p{p}_indep_shards"
        a = audit(p, d)
        if a is None:
            print(f"period {p}: NOT RUN")
            missing_periods.append(p)
            ok = False
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
    out["missing_periods"] = missing_periods
    out["all_checks_passed"] = ok and len(out["periods"]) == len(PERIODS) and all(
        v["highways_found"] == 0 and not v["problems"]
        for v in out["periods"].values())
    (ROOT / "independent_exclusion_summary.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\nall_checks_passed = {out['all_checks_passed']}")
    print("wrote independent_exclusion_summary.json")
