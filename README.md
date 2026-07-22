# Finite-Support Periodic Highways of Langton's Ant

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21381637.svg)](https://doi.org/10.5281/zenodo.21381637)
[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Paper: CC BY 4.0](https://img.shields.io/badge/paper-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Author:** Atharva Jillhewar

📄 **[Read the paper (PDF)](https://atharva12456.github.io/langtons-ant-highway/paper.pdf)** ·
🌐 **[Project page](https://atharva12456.github.io/langtons-ant-highway/)** ·
📌 **Cite:** [`10.5281/zenodo.21381637`](https://doi.org/10.5281/zenodo.21381637)

This repository accompanies a main paper and a companion technical report on the
**finite-support highway conjecture** for Langton's ant, together with the exact search code, the result records, and a
machine-checked Lean 4 formalization of selected algebraic kernels.

> **Status.** The highway conjecture is a well-known **open** problem. Nothing here
> proves or disproves it. What this project contributes is a collection of
> *structural and arithmetic constraints* on what a finite-support periodic highway
> can look like, all-period exclusions of diagonal transverse widths two and four,
> plus an exhaustive exclusion of short-period highways. The width-four theorem is
> explicitly computer-assisted: two independent local enumerators certify its finite
> edge table, while Lean checks the graph-rank consequence. The papers
> are explicit about exactly what remains open.

---

## The problem

Langton's ant lives on `Z^2`. On a white cell it turns right, blackens the cell,
and steps forward; on a black cell it turns left, whitens the cell, and steps
forward. Started on the all-white plane, after 9977 steps it builds the **highway**:
a period-104 pattern that drifts diagonally forever.

**Highway conjecture.** *For every finite initial set of black cells, the ant's future
path and turn trace eventually agree with a translated, quarter-turn-rotated, and
phase-shifted copy of this period-104 highway.* Finite stationary debris away from
the future path is allowed; equality of the entire colouring is not asserted.

## Main results (all proved / computed here)

| # | Result | Where |
|---|--------|-------|
| 1 | **Even-winding theorem** — no finite-support pattern can drift to an exact copy of itself with *zero* net black growth. Hence every periodic highway grows a wake of size `g ∈ 4ℤ₍>0₎`. | `paper/` §6 |
| 2 | **Signed mod-four wake-residue identity** — checker-signed strand bases sum to `2 (mod 4)` in each drift residue class, giving the strand-density lower bound `g ≥ 2·max(|a|,|b|)`. (A lower bound, not claimed attained: the standard highway has `g = 12` against a bound of `4`.) | `paper/` §7 |
| 3 | **Tait-graph conjugacy** + cycle-rank surgery identity `E + ΔC = 2β`. | `paper/` §4 |
| 4 | **Two-endpoint collision-chain parity** for row-column colour defects. | `paper/` §8 |
| 5 | **Transverse rigidity** — for diagonal drift, the two extremal level lines of a periodic highway share one arrival axis (horizontal after normalizing the drift so `ab < 0`), every turn on them is `R`, and each of their cells the ant reaches is entered exactly once and never revisited: the highway runs between two guard rails of permanent wake. The transverse width is therefore even. | `paper/` §9 |
| 6 | **No periodic highway of transverse width 2** — the first exclusion here that is **not** bounded by a period cutoff: it holds at every period. Follows from (5) by collapsing the strip to a one-dimensional walk. | `paper/` §9 |
| 7 | **No diagonal periodic highway of transverse width 4, at any period** — exact crossing sequences through untouched five-cell columns form a 12-edge acyclic graph. Two independent enumerators certify the complete local table; Lean certifies the displayed rank decrease. Hence diagonal highway width is even and at least 6. | `paper/` §9, `results/width4_crossing_graph_certificate.json` |
| 8 | **Exhaustive exclusion of every finite-support periodic highway of period ≤ 48** — prefix-shard audited through period 32 and rank-by-rank audited for periods 34–48, with `hits = 0`; the exact criterion is applied to every positive-growth nonzero-drift leaf without assuming result 2. | `paper/` §10, `results/` |
| 9 | **Decidable periodic-realisability criterion** with an explicit finite seed. | `paper/` §3 |

Results (5)–(7) are of a different kind from (1)–(4): those are *incidence*
statements (counts of strands, edges and charges), and the paper records explicit
countermodels satisfying all of them. (5) and (6) instead use the **order** in which a
cell is visited — that the turn sequence at a cell alternates and starts with `R` — and
so apply at every period rather than up to a search bound. Result (7) combines that
rigidity with exact local dynamics; its computer-assisted boundary is stated above.

Selected algebraic kernels used by results (1) and (2) are **machine-checked in Lean
4** (`lean/`), with no `sorry`s and only the standard axioms. Lean also checks the
width-four graph-rank certificate. This is not an
end-to-end formalization of the dynamics or of either full paper theorem; the exact
boundary is listed in `lean/FORMALIZATION_BOUNDARY.md`.

## What is *not* claimed

None of the above resolves the conjecture. Every result is a *necessary condition*
on a periodic highway or an exact finite computation. Two separate gaps remain: an
entrance theorem for arbitrary finite seeds and a classification theorem for all
positive-growth periodic traces. Widths six and eight, non-diagonal translators, and
universal entrance remain open. They are stated precisely in `paper/` §11.

---

## Repository layout

```
paper/            Main preprint (self-contained main.tex, submission-ready source)
companion/        Companion technical report; the main paper controls submission claims
docs/             Current accessible summaries and compiled PDFs for GitHub Pages
lean/             Lean 4 transition kernel + selected algebraic kernels
code/java/        One residue-free certifying variant + two conditional pruned variants
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

The exclusion of periodic highways of period ≤ 48 is certified by the **residue-free
variant**, which assumes no consequence of the signed mod-four wake-residue theorem
(paper, Theorem 7.1) and applies the exact criterion to *every* positive-growth
nonzero-drift leaf. Two faster variants that do assume that theorem are kept as
cross-checks; because they prune at the node level they explore a strictly smaller
tree, so their counters are **not** expected to match the residue-free variant's.

The **complete search records are archived**: per-rank records for periods 34–48,
plus the depth-5 baseline and all 32 complete six-symbol prefix-shard logs through
period 32 (compressed, a few MB). `results/period_exclusion_summary.json` holds the
aggregated totals. The commands below are illustrative; the exact complete commands
and rank partitions are recorded in `records/RECORDS_MANIFEST.json` and the audit
scripts in `records/`. The period-48 certificate records
51,856.023 aggregate shard-seconds (14.40 shard-hours) and 1:28:48 wall time with
11 workers on the machine described below.

```bash
# Compile the engines
javac -d build/indep    code/java/PositiveGrowthSearchIndep.java   # certifies the result
javac -d build/original code/java/PositiveGrowthSearch.java        # strand-pruned cross-check
javac -d build/residue  code/java/PositiveGrowthResidueSearch.java # residue-pruned cross-check

# One shard of a period-48 search (rank interval [START, STOP) of 2^16 length-17 prefixes)
java -cp build/indep PositiveGrowthSearchIndep \
     --period 48 --prefix-length 17 --rank-start 0 --rank-stop 4096 \
     --output shard_00.json
# Every record of this engine carries "residue_theorem_used": false.

# The pruned variants (conditional on Theorem 7.1) — same arguments
java -cp build/residue PositiveGrowthResidueSearch \
     --period 48 --prefix-length 17 --rank-start 0 --rank-stop 4096 \
     --output shard_00_res.json
```
A complete period-34--48 exclusion requires every rank covered exactly once, every
shard `search_complete=true` with `node_cap=null`, empty hit lists, and every
per-rank counter summing to its shard aggregate. The conditional variants explore
smaller trees and are consistency checks, not independent implementations. See
`code/README.md`.

**Positive control.** All three Java variants *accept* the standard highway word:
```bash
java -cp build/original PositiveGrowthSearch --check-trace <standard-word>
# => {"prefix_rules_valid":true,"growth":12,"drift":[2,-2],"p16_valid":true,"p3_valid":true}
```
The standard word, its **11-cell** seed (for the normalized printed phase, first turn
`R`, drift `(2,-2)`), and the **13-cell** seed of the shifted phase (first turn `L`,
drift `(-2,2)`) are in `results/standard_highway.json`. The two phases are different
and their seeds must not be interchanged.

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

> A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant: Necessary
> Conditions, Transverse Exclusions, and Exact Search*, preprint, 2026. Supplementary code, data and Lean
> formalization: Zenodo, doi:[10.5281/zenodo.21381637](https://doi.org/10.5281/zenodo.21381637).

The DOI above is the **concept DOI**: it always resolves to the latest archived
release. To pin an exact version, use the version DOI shown on that Zenodo release;
do not substitute the concept DOI when exact file identity matters.

## License

- **Code, Lean, data** (`code/`, `lean/`, `results/`): MIT — see [`LICENSE`](LICENSE).
- **Papers and prose** (`paper/`, `companion/`, `docs/`, `research-notes/`):
  Creative Commons Attribution 4.0 (CC BY 4.0) — see `LICENSE-PAPER.md`.

## Acknowledgements

The exact searches were run on a single workstation (Intel Core i5-1334U, 10 physical
cores, 16 GB RAM, Windows 11 build 26200; Eclipse Temurin OpenJDK 25.0.1+8; CPython
3.13.14) — one JVM per shard, at most 12 concurrent shards. No cluster or special
allocation was used. The period-48 run totals 14.40 aggregate shard-hours and
records 1:28:48 wall time with 11 workers.
