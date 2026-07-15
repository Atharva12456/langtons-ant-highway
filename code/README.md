# Code

Exact, integer-only implementations. No floating point, no hashing, and no
probabilistic equality tests decide any result.

## `java/` — the two search engines

Both engines enumerate the tree of legal periodic turn-words for a fixed period and
apply the exact periodic-realisability criterion (paper, Theorem 3.1) at every leaf.

| File | Role |
|------|------|
| `PositiveGrowthSearch.java` | **Reference engine.** Applies the exact criterion to every positive-growth leaf. |
| `PositiveGrowthResidueSearch.java` | **Residue-pruned engine.** First rejects leaves violating the signed mod-four wake-residue identity (paper, Theorem 7.1), then applies the exact criterion to survivors. |
| `HammingStandard.java` | Enumerates Hamming-neighbourhoods of the standard 104-word (isolation result). |

### Build
```bash
javac -d build/original java/PositiveGrowthSearch.java
javac -d build/residue  java/PositiveGrowthResidueSearch.java
```

### Run one shard
```
java -cp build/original PositiveGrowthSearch \
     --period N --prefix-length K \
     --rank-start START --rank-stop STOP \
     --deficit-depths 0 --output out.json
```
- The half-open interval of length-`K` prefix ranks is `[0, 2^(K-1))`; partition it
  into disjoint `[START, STOP)` worker intervals to distribute the search.
- The residue engine takes identical arguments with class `PositiveGrowthResidueSearch`.

### Check a single word
```
java -cp build/original PositiveGrowthSearch --check-trace RRRR...RL
```
Prints `prefix_rules_valid`, `growth`, `drift`, `p16_valid`, `p3_valid`. The standard
word (in `../results/standard_highway.json`) returns growth 12, drift (2,-2), all valid.

### What a complete exclusion requires
1. every rank covered exactly once across all shards;
2. every shard reports `search_complete=true` and `node_cap=null`;
3. all hit lists empty;
4. aggregate node/leaf/prune counters equal the sums of the per-rank counters; and
5. the two engines agree rank-by-rank on nodes and leaves (the cross-audit).

## `python/` — reference implementation and audits

| File | Role |
|------|------|
| `langton_research.py` | Reference implementation of the criterion (`finite_seed_for_periodic_trace`), the ant simulator, the Tait-graph maps, and diagnostics. The trusted checker any Java hit must be re-validated against. |
| `translator_residue_charge_audit.py` | Independent check of the mod-four residue-charge equations. |
| `residue_theorem_adversarial_audit.py` | Enumerates all words through length 18 and checks the residue identity directly. |
| `g4_case_audit.py` | The growth-four case analysis and its heading-reset countermodels. |
| `p44_independent_audit.py` | Cross-audit of the period-44 two-engine records. |

Run any audit with `python <script>.py`. Requires Python 3.10+ (standard library only).
