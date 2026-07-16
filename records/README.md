# Search records

The **complete per-rank certificate** for every exhaustive search reported in the
paper. Aggregate summaries alone are weaker than the records themselves, and a
period-48 search is expensive enough that most readers will not rerun it — so the
records are archived here rather than left to be regenerated.

## `langton_search_records.tar.gz` (3.4 MB, 417 members)

| Contents | |
|---|---|
| `p{34,36,38,40,42,44,46,48}_indep_shards/` | every shard of the **independent** engine — the runs that certify the exclusion |
| `p{44,46,48}_original_shards*/`, `p{44,46,48}_residue_shards*/` | the strand-pruned and residue-pruned cross-check runs |
| `RECORDS_MANIFEST.json` | SHA-256 of every member, environment strings, exact commands |
| engine source + audit scripts | `PositiveGrowthSearchIndep.java`, `aggregate_indep.py`, `run_indep.sh`, `verify_*.py`, `cross_check_criterion.py` |

Each shard record holds, **per rank**: node / leaf / prune / criterion-evaluation
counters, wall time, the hit list, and `"residue_theorem_used": false` for the
independent engine.

```bash
tar xzf langton_search_records.tar.gz
python aggregate_indep.py        # re-runs the coverage + counter audit
```

## `independent_exclusion_summary.json`

The audited aggregate. Per period it records the counters, `hits`, and
`ranks_covered_exactly_once`. `all_checks_passed: true` requires, for every period:

1. every prefix rank covered **exactly once** (no gap, no duplicate);
2. every shard `search_complete` with `node_cap: null`;
3. per-rank counters summing to the shard aggregate;
4. `residue_theorem_used: false` in every record;
5. zero hits.

The audit is not decorative — it fails loudly on an incomplete run (e.g. mid-run it
reported `coverage: 6830 ranks, 0 duplicates, 58706 missing` and refused to pass).

## Headline

| Period | Nodes | Leaves | Criterion evaluations | Highways |
|-------:|------------------:|-----------------:|-----------------:|:-:|
| 42 | 2,133,302,151 | 376,781,423 | 376,781,423 | 0 |
| 44 | 5,748,138,964 | 1,018,293,035 | 1,018,293,035 | 0 |
| 46 | 15,483,269,352 | 2,757,152,898 | 2,757,152,898 | 0 |
| **48** | **41,710,394,384** | **7,446,719,550** | **7,446,719,550** | **0** |

Criterion evaluations **equal** leaves at every period: no leaf discarded unexamined.
This is what makes the exclusion independent of Theorem 7.1.

## Environment

Single workstation — **no cluster**. Intel Core i5-1334U (10 physical / 12 logical
cores, 1.3 GHz base), 16 GB RAM, Windows 11 build 26200; Eclipse Temurin OpenJDK
25.0.1+8 (64-bit Server VM), one JVM per shard, ≤ 12 concurrent shards; CPython
3.13.14. Period 48 is ~52,000 core-seconds — a few core-hours here.
