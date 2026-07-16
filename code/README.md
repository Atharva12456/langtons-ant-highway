# Code

Exact, integer-only implementations. No floating point, no hashing, and no
probabilistic equality tests decide any result.

## `java/` — the search engines

All three engines enumerate the tree of legal periodic turn-words for a fixed period
and apply the exact periodic-realisability criterion (paper, Theorem 3.1) at the
leaves they reach. **They differ in which theorem they assume**, which decides what
each one is able to certify:

| File | Role |
|------|------|
| `PositiveGrowthSearchIndep.java` | **Independent engine — this is what certifies the exclusion.** Assumes *no* consequence of the residue theorem (paper, Theorem 7.1). Applies the exact criterion to **every** positive-growth nonzero-drift leaf. |
| `PositiveGrowthSearch.java` | **Strand-pruned engine.** Additionally prunes with the strand-density bound `g >= 2*max(|dx|,|dy|)` (paper, Corollary 7.3), which is a *consequence of Theorem 7.1*. Faster, but its result is conditional on that theorem. |
| `PositiveGrowthResidueSearch.java` | **Residue-pruned engine.** Adds the full signed mod-four wake-residue identity (paper, Theorem 7.1). Fastest; also conditional. |
| `HammingStandard.java` | Enumerates Hamming-neighbourhoods of the standard 104-word (isolation result). |

> **Note on a corrected claim.** Earlier releases described
> `PositiveGrowthSearch.java` as the reference engine, making "no use of Theorem 7.1"
> and applying the criterion "to every leaf". Both statements were wrong: it prunes
> with Corollary 7.3, and because that pruning acts at the *node* level, the leaves it
> never reaches were never counted. At period 44 it evaluates the criterion on
> 67,839,409 leaves, whereas the honest count is 1,018,293,035 — a factor of 15.
> `PositiveGrowthSearchIndep.java` was written to remove the assumption, and the
> published exclusion counts are its output.

### Build
```bash
javac -d build/indep    java/PositiveGrowthSearchIndep.java
javac -d build/original java/PositiveGrowthSearch.java
javac -d build/residue  java/PositiveGrowthResidueSearch.java
```

### Run one shard
```
java -cp build/indep PositiveGrowthSearchIndep \
     --period N --prefix-length K \
     --rank-start START --rank-stop STOP \
     --deficit-depths 0 --output out.json
```
- The half-open interval of length-`K` prefix ranks is `[0, 2^(K-1))`; partition it
  into disjoint `[START, STOP)` worker intervals to distribute the search.
- The other two engines take identical arguments with class `PositiveGrowthSearch` /
  `PositiveGrowthResidueSearch`.
- Every shard record of the independent engine carries
  `"residue_theorem_used": false`.

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
5. the run is done with the **independent** engine, so the outcome does not assume
   Theorem 7.1. The pruned engines are cross-checks; because they explore a strictly
   smaller tree, their counters are *not* expected to equal the independent engine's,
   and their leaf sets are subsets of it.

`../work/aggregate_indep.py` checks 1–4 mechanically and refuses to pass a period
whose ranks are not covered exactly once.

## `python/` — reference implementation and audits

| File | Role |
|------|------|
| `langton_research.py` | Reference implementation of the criterion (`finite_seed_for_periodic_trace`), the ant simulator, the Tait-graph maps, and diagnostics. The trusted checker any Java hit must be re-validated against. |
| `translator_residue_charge_audit.py` | Independent check of the mod-four residue-charge equations. |
| `residue_theorem_adversarial_audit.py` | Enumerates all words through length 18 and checks the residue identity directly. |
| `g4_case_audit.py` | The growth-four case analysis and its heading-reset countermodels. |
| `p44_independent_audit.py` | Cross-audit of the period-44 two-engine records. |
| `verify_criterion_indep.py` | **Independent verifier of Theorem 3.1**, written from the theorem statement rather than from the Java source. Builds translation classes by explicit pairwise membership tests + union-find (not the Java's arithmetic reduction + global sort), and evaluates the *literal* criterion — every `S_{I,n}` — rather than the single stabilised word that Remark 3.2 licenses. It therefore also tests Remark 3.2, which the Java engines assume. |
| `cross_check_criterion.py` | Runs that verifier against the Java engines: agreement on all 172,092 heading-reset nonzero-drift words of length ≤ 18 (zero disagreements), on the standard 104-word, and on words sampled directly from the Java binary. |
| `verify_nomonotone.py` | Certificate for the no-monotone-invariant proposition: enumerates the eight `(ΔE,ΔV,Δk)` increments on the blank orbit and shows the set is centrally symmetric and spans, so no nonconstant affine combination of `(E,V,k,β)` is monotone. |

Run any audit with `python <script>.py`. Requires Python 3.10+ (standard library only).
