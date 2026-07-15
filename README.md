# Langton's Ant: Structural Constraints on Finite-Support Periodic Highways

**Author:** Atharva Jillhewar

This repository accompanies two papers on the **finite-support highway conjecture**
for Langton's ant, together with the exact search code, the result records, and a
machine-checked Lean 4 formalization of the algebraic core.

> **Status.** The highway conjecture is a well-known **open** problem. Nothing here
> proves or disproves it. What this project contributes is the first body of
> *structural and arithmetic constraints* on what a finite-support periodic highway
> can look like, plus an exhaustive exclusion of short-period highways. The papers
> are explicit about exactly what remains open.

---

## The problem

Langton's ant lives on `Z^2`. On a white cell it turns right, blackens the cell,
and steps forward; on a black cell it turns left, whitens the cell, and steps
forward. Started on the all-white plane, after 9977 steps it builds the **highway**:
a period-104 pattern that drifts diagonally forever.

**Highway conjecture.** *For every finite initial set of black cells, the ant
eventually builds a (translated/rotated/reflected/phase-shifted) copy of this
period-104 highway.*

## Main results (all proved / computed here)

| # | Result | Where |
|---|--------|-------|
| 1 | **Even-winding theorem** — no finite-support pattern can drift to an exact copy of itself with *zero* net black growth. Hence every periodic highway grows a wake of size `g ∈ 4ℤ₍>0₎`. | `paper/` §6 |
| 2 | **Signed mod-four wake-residue identity** — checker-signed strand bases sum to `2 (mod 4)` in each drift residue class, giving the sharp bound `g ≥ 2·max(|a|,|b|)`. | `paper/` §7 |
| 3 | **Tait-graph conjugacy** + cycle-rank surgery identity `E + ΔC = 2β`. | `paper/` §4 |
| 4 | **Two-endpoint collision-chain parity** + touch-graph interlacement rank formula. | `paper/` §8 |
| 5 | **Exhaustive exclusion of every finite-support periodic highway of period ≤ 48** (two independent engines, rank-by-rank cross-audited, `hits = 0`). | `paper/` §9, `results/` |
| 6 | **Decidable periodic-realisability criterion** with an explicit finite seed. | `paper/` §3 |

The algebraic cores of results (1) and (2) are **machine-checked in Lean 4**
(`lean/`), with no `sorry`s and only the standard axioms.

## What is *not* claimed

None of the above resolves the conjecture. Every result is a *necessary condition*
on a periodic highway or an exact finite computation. The single missing geometric
ingredient — a bounded-retreat / bounded-active-core lemma, plus a single-tour
chronology theorem — is stated precisely in `paper/` §10.

---

## Repository layout

```
paper/            The publishable paper (self-contained main.tex, arXiv-ready)
companion/        Extended technical report: the full ledger of results, with proofs
docs/             HTML renderings (for GitHub Pages / quick reading)
lean/             Lean 4 formalization of the transition kernel + algebraic core
code/java/        The two exact search engines (reference + residue-pruned)
code/python/      Reference implementation of the criterion, and audit scripts
results/          Aggregated search results + the standard highway word/seed
research-notes/   The full research journal and compute handoff (honest audit trail)
```

---

## Building the paper

The papers are **single self-contained `.tex` files** — the bibliography is embedded,
so there is no separate `.bib` file and no BibTeX step.

### Overleaf (recommended)
1. Create a new **Blank Project** on [overleaf.com](https://www.overleaf.com).
2. Delete the default `main.tex`, then **upload** `paper/main.tex` (drag-and-drop).
3. Make sure the compiler is **pdfLaTeX** (Menu → Compiler → pdfLaTeX).
4. Press **Recompile.** References and appendices render automatically (Overleaf runs
   the two pdfLaTeX passes needed to resolve `\cite` and `\ref`).

> If you previously saw an *empty References section*, it was because the old file
> used `\bibliography{references}`, which needs a separate `.bib` upload and a BibTeX
> run. This version embeds the bibliography, so that cannot happen.

### Local
```bash
cd paper
pdflatex main.tex
pdflatex main.tex      # second pass resolves cross-references
```
Requires a standard TeX distribution (TeX Live / MiKTeX) with `amsart`, `amsmath`,
`amssymb`, `mathtools`, `enumitem`, `booktabs`, `listings`, `hyperref` (all default).

---

## Reproducing the search results

The exclusion of periodic highways of period ≤ 48 is produced by two independent
engines. The **full per-rank shard records are large (~150 MB) and are not committed**;
`results/period_exclusion_summary.json` holds the aggregated totals, and the commands
below regenerate everything exactly.

```bash
# Compile both engines
javac -d build/original code/java/PositiveGrowthSearch.java
javac -d build/residue  code/java/PositiveGrowthResidueSearch.java

# One shard of a period-48 search (rank interval [START, STOP) of 2^16 length-17 prefixes)
java -cp build/original PositiveGrowthSearch \
     --period 48 --prefix-length 17 --rank-start 0 --rank-stop 4096 \
     --deficit-depths 0 --output shard_00.json

# The residue-pruned engine (Theorem 7.1) — same arguments, must agree rank-by-rank
java -cp build/residue PositiveGrowthResidueSearch \
     --period 48 --prefix-length 17 --rank-start 0 --rank-stop 4096 \
     --deficit-depths 0 --output shard_00_res.json
```
A complete exclusion requires: every rank covered exactly once, every shard
`search_complete=true` with `node_cap=null`, empty hit lists, and the two engines'
per-rank node/leaf/prune counters in agreement. See `code/README.md`.

**Positive control.** Both engines *accept* the standard highway word:
```bash
java -cp build/original PositiveGrowthSearch --check-trace <standard-word>
# => {"prefix_rules_valid":true,"growth":12,"drift":[2,-2],"p16_valid":true,"p3_valid":true}
```
The standard word and its 13-cell seed are in `results/standard_highway.json`.

---

## Building and checking the Lean formalization

The Lean project is pinned to **Lean 4.32.0** and uses only the standard library.

```powershell
# From the lean/ directory, with elan/Lean installed (https://leanprover.github.io):
cd lean
lake build
lake env lean Audit.lean   # prints the axioms of every audited theorem
```
Every audited theorem depends only on `propext`, `Classical.choice`, `Quot.sound`;
there are no `sorry`s, no custom axioms, and no `native_decide`. See
`lean/README.md` and `lean/FORMALIZATION_BOUNDARY.md` for exactly what is and is not
certified.

---

## Citing

See [`CITATION.cff`](CITATION.cff). Suggested:

> A. Jillhewar, *New Structural and Arithmetic Constraints on Finite-Support Periodic
> Highways of Langton's Ant*, preprint, 2026.

## License

- **Code, Lean, data** (`code/`, `lean/`, `results/`): MIT — see [`LICENSE`](LICENSE).
- **Papers and prose** (`paper/`, `companion/`, `docs/`, `research-notes/`):
  Creative Commons Attribution 4.0 (CC BY 4.0).

## Acknowledgements

Large exact searches were run on a high-performance computing cluster.
