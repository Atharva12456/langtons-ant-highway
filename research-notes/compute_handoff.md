# Langton-ant proof and compute handoff

Last updated: 2026-07-21 19:25 CDT (post-research manuscript and referee phase)

## Live session checkpoint

The research interval ended at 19:00 CDT on 21 July 2026.  The width-four result that
survived audit has now been integrated into both manuscripts.  An independent
adversarial referee re-derived the proof, found an omitted label hypothesis, and
passed the repaired theorem; a second consistency audit supplied additional scope
corrections.  Final PDF/release QA and the requested unsent Gmail drafts remain in
progress.  No universal proof or counterexample exists at this checkpoint.

Codebase audit note: the Java class whose filename contains `Indep` is best
described as the **residue-theorem-free variant**, not as an independent
implementation. All three Java variants share enumeration and representation;
the separate Python literal-criterion verifier supplies the implementation-level
cross-check. Preserve the larger residue-free counts in the paper. Before release,
repair the principal paper's lifetime-state wording and explicitly qualify the
labelled touch-graph theorem under physical row/column pushforward.

## Truth status

The finite-seed Langton-ant highway conjecture is still open. Nothing in this project is a universal proof or a counterexample. Do not mark the research goal complete.

The exact target used here is:

> Every initial coloring with finite black support, with the ant at a specified lattice pose, eventually enters an exact translating periodic regime equivalent under a lattice symmetry and phase shift to the standard period-104 highway.

Finite computation can exclude bounded periods and test candidate mechanisms, but it cannot by itself prove this universal entrance statement.

## Current rigorous frontier

The principal new theorem is P22, the signed mod-four wake-residue theorem. For a finite-support repeating trace with nonzero drift d=(a,b), canonical wake bases c_i, and growth g:

- if a is nonzero, then for every residue r modulo |a|,
  sum over c_ix congruent to r of (-1)^(c_ix+c_iy) is 2 modulo 4;
- if b is nonzero, the analogous row sum is 2 modulo 4;
- exact columns or rows in a zero drift coordinate have signed sum 0 modulo 4.

Consequently every nonzero drift residue contains a positive even number of strands and

    g >= 2|a|  and  g >= 2|b|.

In particular g=0 is impossible for every exact finite-support repeating trace. This is an independent proof of the no-clean-translator conclusion previously obtained from the cylinder argument. It is not an entrance theorem and does not classify all positive-growth traces.

The exterior-dynamics continuation proves:

- P23, a finite-history renewal theorem for quiet flights;
- P24, if active Tait cycles are eventually bounded, every black Tait component has uniformly bounded size and diameter;
- P25, arbitrarily long bad seam episodes contain detached stationary seam islands with unbounded stationary duration and excursion radius; and
- P26, a warmed nonzero-drift renewal flight that moves its complete footprint beyond the finite black support present when that flight began can never be interrupted and escapes forever as a positive-growth periodic trace;
- P27, the row-column incidence boundary of every finite color defect is exactly the two endpoint ant tokens, so arbitrary collision checkpoints telescope and all but at most one defect component are Eulerian;
- P28, every L collision is exactly a bridge split or a nonbridge merge, with the old live successor selecting the active daughter; and
- P29, every completed R-to-L black lifetime has an Eulerian odd-visit component through its paired cell and therefore involves at least four distinct cells. In the four-cell case, signed mod-four charges determine the rectangle's add/remove pattern from arrival type and side parities.

Thus a returning bad core needs an unbounded chronological chain of flight changes/ancestral-debris collisions, or quiet intervals repeatedly too short to complete a warmed record cycle. Abstract planar binary-counter and one-marker returners prove that locality, finite state, bounded components, finite support, a fixed anchor, and even injectivity on the reachable orbit do not alone exclude this behavior. P27 rules out their displayed one-row tape mechanisms as literal Langton dynamics, but neutral row-column cycles can have arbitrary span. The exact remaining bounded-loop obstruction is the Langton-specific production and ordering of those neutral cycle packets among uniformly small Tait islands. The unbounded-active-loop branch remains open.

## Exact periodic search status

**Update (paper/repo continuation, 14 Jul 2026):** two-engine, rank-audited exclusion now extends to **period 46 and 48**. Period 46: both engines 3,463,441,745 nodes / 98,568,824 leaves / 0 hits. Period 48: both engines 8,677,026,370 nodes / 451,962,870 leaves / 0 hits; residue engine pruned 439,705,662 leaves via P22. All per-rank counters agree. Therefore **no finite-support periodic highway of nonzero drift has period at most 48.** Shards: work/p46_*_shards/, work/p48_*_shards/. Aggregated summary: langtons-ant-highway/results/period_exclusion_summary.json. The Lean project now includes Langton/P3Endpoint.lean in the build graph (previously silently broken); clean 16-job build, no sorry.


Odd heading-reset periods are analytically impossible. Zero-growth repeating traces are analytically impossible at every period by P22.

Two independent complete period-42 searches cover prefix ranks 0 through 8191 exactly once:

    nodes             528,451,911
    leaves             14,561,206
    hits                        0

The original implementation applied exact P3 to all 14,561,206 leaves. The residue-aware implementation rejected 13,487,309 leaves using P22 and applied P3 to the remaining 1,073,897. All shared per-rank counters agree. Together with earlier searches, no finite-support periodic highway has period at most 42.

Two independent complete period-44 runs have finished over prefix ranks 0 through 16383:

    nodes           1,319,080,456
    leaves             67,839,409
    residue prunes      65,050,414
    P3 checks            2,788,995
    hits                        0

Both ten-shard families are contiguous and exhaustive; every shard has search_complete=true, node_cap=null, the exact expected number of per-rank records, and zero hits. The original engine checked P3 on all 67,839,409 leaves. The residue-aware engine rejected 65,050,414 with P22 and checked P3 on the remaining 2,788,995. Nodes, growth prunes, endpoint prunes, leaves, and hits agree at every one of the 16,384 ranks. Therefore no finite-support periodic Langton highway has period at most 44, conditional on the written mathematical and implementation audit dependencies.

Period-44 residue shards:

    work\p44_residue_shards_v2\shard_00.json
    ...
    work\p44_residue_shards_v2\shard_09.json

Period-44 original-engine shards:

    work\p44_original_shards_independent_20260714\shard_00.json
    ...
    work\p44_original_shards_independent_20260714\shard_09.json

Deterministic cross-audit:

    python work\p44_independent_audit.py

    script SHA-256 35d134a3f4bd98c51ce8a9bf3814e156e303adada3cda93881621a94fea0e0ba
    summary SHA-256 682b9bf0118684f3c2595e7deae39c785dd5d31bf38812df0ac47ca8c4869ada
    note SHA-256 49aea8b22b068e04bb9d6d330acb229a13f2ef18e5b5a2c725fa1780673ab5c7

Validated search sources:

    outputs\PositiveGrowthSearch.java
    SHA-256 f2fadea8b323bf7bc817505e36b83146e4489ee5954d98dc1a87b52adb8dbf8d

    work\PositiveGrowthResidueSearch.java
    SHA-256 859a5c683898375cd8e94637cdbb50824b59eb88f83e6876e225c82c8c421b17

Period-42 records:

    work\positive_growth_original_p42_complete.json
    SHA-256 daef0982d24dd84e0a889f6f4f84795d670f32c29886d990f7b709b683ef4136

    work\positive_growth_residue_p42_complete.json
    SHA-256 bd8634a72855805d3913560b177b9d71eb5dfebc51b3ca07a241f8737246a2c7

To rerun a complete period N search with prefix length k, divide the half-open prefix-rank interval [0,2^(k-1)) into disjoint worker intervals. A representative original-engine period-44 command is:

    java -cp outputs PositiveGrowthSearch --period 44 --prefix-length 15 --rank-start START --rank-stop STOP --deficit-depths 0 --output OUTPUT.json

For the residue-aware engine use class path work and class PositiveGrowthResidueSearch with the same arguments. A complete exclusion requires exact rank coverage once each, search_complete=true, node_cap=null, empty hit lists, identical source/settings, and aggregate counters equal to the sums of all per-rank counters.

Any nonstandard hit must immediately be rechecked using finite_seed_for_periodic_trace in outputs\langton_research.py. A verified hit would disprove uniqueness of the standard highway, not automatically disprove eventual periodicity for every finite seed.

## Lean checkpoint

The portable Lean project is at:

    work\lean_langton

Build from the project root with:

    powershell -ExecutionPolicy Bypass -File work\lean_langton\build.ps1

The current independent clean build completes 16 jobs and a source scan reports no `sorry` or `admit` declarations. It machine-checks the finite-support transition kernel, heading residue, the finite parity telescope core, four-corner checker-signed weights, the mod-four fiber arithmetic, fiber positivity/evenness, the finite counting implication g>=2n, collision-chain endpoint parity, and exact directed-pose row/column discrepancy charges.

The module work\lean_langton\Langton\ChargeTelescoping.lean proves finite potential telescoping, checker-cycle monodromy 2*sum(alpha), translated-widget cancellation, and derivation of the residue identity from a structured LocalResidueCertificate. It has SHA-256 990adca871641dfbc3a4563d72e8a83f2e40ff21ed4c931cfc88b19b026b1da9.

`Langton\TraceGeometry.lean` now derives exact phase/address lists, finite per-level toggle totals, 0/1 orbit totals, the canonical strand-plus-widget decomposition, terminal widget zero, grouped phase-to-strand charge, the residue alpha cycle, widget cancellation, and the old local certificate fields. Its SHA-256 is 4e58c91dcf272fe3cf06c2517fe303cc038921c0f5b062182309ae52f397d596.

Important limitation: P22 is still not formalized end to end. The remaining explicit inputs are the endpoint binary normal form derived on paper from P3, a physical closed residue traversal, its local potential law, and exact grouped trace-charge conservation. The exact boundary is in work\lean_langton\FORMALIZATION_BOUNDARY.md, SHA-256 71bb7718328fac3b6f426c4e59ace55d634d5e4193df433e1de2cc1b982f503d.

`Langton\CollisionParity.lean` proves the one-step/run endpoint boundary and arbitrary checkpoint telescoping (SHA-256 80a83a42be952d75870ccd55cbedbb2d8b44eb63767add5908430fe75f745be2). `Langton\DirectedPoseDiscrepancy.lean` constructs explicit exact-column and exact-row mod-four potentials, verifies all eight R/L cases, proves unconditional same-pose endpoint congruences, and checks the minimum-rectangle sign formula (SHA-256 ee53b7aa884effb94b42213affe37bab4762075cc672ba77a4fa3d2a763a7c17).

## Independent P22 audit

Run:

    python work\translator_residue_charge_audit.py
    python work\residue_theorem_adversarial_audit.py

The first audit checked 944,640 local turn equations, 3,360,000 nonzero-drift monodromy equations including both drift signs, and 2,016,000 zero-coordinate equations. The adversarial audit enumerated all 524,286 words through length 18; all 172,092 heading-reset, nonzero-drift candidates satisfied the direct residue identity. It also independently checked known standard phase/power words and their dihedral transforms. No failure was found.

## Structured positive-growth searches

The following finite families produced no nonstandard P3 certificate:

- 196,762 delete-one-return-loop / insert-one-closed-standard-subword splices;
- all 10,816 concatenations of two cyclic standard phases;
- 70,616 same-rotated-drift phase triples; and
- 9,568 targeted low-score mixed-drift triples.

These data show isolation of the period-104 word in selected families. They do not prove unbounded uniqueness. The missing periodic theorem is a single-tour chronology/interlacement result strong enough to eliminate abstract signed-residue configurations not realizable by one ant tour.

The growth-four case is now completely classified at the wake-residue level. Possible drifts are only (±1,±1), (±2,0), (0,±2), and (±2,±2). Axis skeletons are two residue-paired rows or columns separated by an arbitrary even distance; diagonal skeletons have the parity patterns forced by P22. The additional kinematic congruence is

    N/2 + a + b + A = 0 modulo 4,

where A is the number of even-checker odd classes for a P3-valid word. Every even-drift growth-four case has N divisible by 8; primitive diagonal cases have the corresponding 2 or 6 residue modulo 8 and analytic lower bounds 10 or 14.

Most importantly, exact heading-reset chronological countermodels exist for every growth-four drift type. They satisfy within-period physical-cell alternation, local class excess, and all residue equations, but fail cross-period P3; one period-24 drift-(2,-2) model has only one bad stabilized adjacency. Reproduce all six with:

    python work\g4_case_audit.py

Source SHA-256: 0c7e001c68d7333e544f94f41ffe88d14f35d0b83b3bf34de3838e375ef06360. This establishes that additional incidence or residue counts cannot close even growth four; the missing information is exactly stabilized level/phase chronology.

## Exterior computation and warnings

The centered 3-by-3 mask 0x16d sheds a length-eight inner loop at step 14,989 and reabsorbs that unchanged loop at step 38,262, after an age of 23,273. This is a finite obstruction witness, not a counterexample; the orbit later highways.

An isolated obstacle added to a certified immediate highway can force a deep exact reversal: obstacle (-23,26) is first hit at step 1,173, the ant returns to the launch cell at step 6,636 heading north, and an exact standard-highway certificate appears at step 10,668. A scan of 682 leading-cell/level obstacle placements found eventual standard gateways in every case before 200,000 steps. This refutes naive local monotonicity but supplies no universal scattering bound.

The collision-time audit is sharper. At time 1,173 the ancestral obstacle edge is a degree-(3,1) leaf bridge in a 34-edge, cycle-rank-two component. Its length-120 active boundary splits into a pristine live four-cycle and a non-pristine shed length-116 boundary, yet the eventual drift reverses from (-2,2) to (2,-2). Therefore ancestry, bridge status, boundary rotation, and a pristine live exit do not impose a nonnegative drift projection. Reproduce the single witness with:

    python work\one_obstacle_collision_audit.py

The script SHA-256 is 21d77bbb8404ae75888341df7e55eb855680339d113091a2b16d46ba45960ecb. Between times 0 and 6,636 its 524-cell defect is one Eulerian row-column incidence component of cycle rank 444, showing exactly how a reversal hides in endpoint-neutral cycle storage.

The blank orbit also contains 35 pairwise-crossing R-to-next-L black-lifetime intervals. Do not assume black-memory intervals are laminar or LIFO.

For the periodic chronology branch, read `work\chronology_pairing_hostile_audit.md` and `work\interlace_touchgraph_notes.md`. Every completed R-to-L interval has at least three other odd-visited cells. The Dyck-versus-physical exchange formulas are correct but also hold for nonchronological within-class bijections; all six fixed g=4 near-models pass them, so do not use them as a P3-order obstruction.

The stronger voltage/touch-graph reduction is rigorous. Paired lifetimes become 4-valent phase-cylinder vertices; wake R events are degree-2 H/V switches. After suppressing those switches, Traldi's modified interlacement rows span the full cycle space of the contracted touch graph, with rank

    m - c - kappa + 1,

where c counts closed H/V smoothing circuits and kappa counts cycles in the 2-regular wake-edge subgraph. The uncontracted graph has kappa additional wake-cycle directions. On the standard trace, m=46, c=5, kappa=1, and both predicted and measured projected rank are 41, while the full boundary rank is 42. For g=4, kappa can be 1 or 2 and arbitrarily many closed H/V backtracking circuits remain possible. The exact unresolved lemma is to control that wake-cycle lift and those closed circuits using voltage/lattice/signed-charge data.

Reproduce the narrow audit (standard trace plus the six already fixed near-models only) with:

    python work\chronology_pairing_audit.py

Script SHA-256: e0b063427e30428c8d43b09bd8621bcf0456ee87c3292a721ff7025653f780e1. The independent rerun exited successfully; for the standard word it reproduced the integer chord identity 192=192 and ranks 41/41 versus boundary rank 42.

## Highest-value next work

1. Finish the exact P3-to-`NormalizedTrace` bridge in Lean: derive the endpoint binary normal form, physical residue traversal, local potential law, and grouped charge conservation rather than supplying them as structure fields.
2. Attack the bounded-loop island-collision ordering problem: prove that uniformly bounded detached islands cannot generate infinitely many returns to an old stationary seam island, or construct an exact Langton counterexample gadget.
3. Find a coercive invariant or normalization for the unbounded-active-loop branch.
4. For the periodic branch, control the `Z(W)` wake-cycle lift and the unbounded closed H/V smoothing circuits in the now-rigorous voltage boundary touch graph. General circuit nullity already closes the contracted graph and cannot supply this missing restriction.
5. Do not spend compute merely extending a numerical horizon. Run a search only when it certifies a stated bounded theorem, independently checks a proof dependency, or targets a precise counterexample mechanism.

## Files to read first after interruption

1. outputs\langton_proof_journal.md — authoritative detailed proof journal.
2. outputs\langton_highway_research_note.md — shorter research exposition.
3. work\translator_classification_notes.md — P22 derivation and periodic classification notes.
4. work\residue_theorem_independent_audit.md — hostile independent rederivation.
5. work\exterior_gap_notes.md — P23–P25 and exact obstruction witnesses.
6. work\lean_langton\Langton\ResidueCharge.lean — checked arithmetic kernel.

7. work\chronology_pairing_notes.md — Dyck/physical matching, all-lifetimes discrepancy theorem, and current interlacement frontier.
8. work\directed_pose_discrepancy_audit.md — independent paper and Lean audit of the signed lifetime theorem.
9. work\lean_langton\FORMALIZATION_BOUNDARY.md — exact current Lean assumptions and derived layers.

All project material is organized under the project root directory. Paths beginning
with `work/` and `outputs/` in this note are relative to that root. In this public
repository the corresponding sources live under `code/`, `lean/`, and `results/`;
the bulk search-shard data referenced here is regenerable via the commands in the
top-level `README.md`.

## 20 July 2026 publication-continuation handoff (supersedes stale counts above)

The conjecture remains open. The current submission is
`paper/main.tex`, retitled *Finite-Support Periodic Highways of Langton's Ant:
Necessary Conditions and Short-Period Exclusion*. It states two separate open
obligations: eventual entrance for every finite seed and unbounded-period
classification/uniqueness of positive-growth periodic traces.

### Formal boundary

`lean/Langton/P3Endpoint.lean` now contains
`StabilizedP3Word.toOrbitEndpointData`. Given an explicit stabilized nonincreasing P3
level word, it derives the first positive endpoint, zero-sum balanced remainder, and
binary widget prefix. It does not extract that word from every actual periodic ant
trace, and the lifted residue path/local potential geometry remains explicit. A clean
official-Lean-4.32.0 Docker build completed all 18 jobs; the axiom audit lists only
`propext`, `Quot.sound`, and where used `Classical.choice`. Use `lean/Dockerfile` or
the repaired `lean/build.ps1`.

### Exact computation boundary

Do not call `PositiveGrowthSearchIndep.java` an independent implementation. It is the
**residue-free variant** of the shared Java enumeration framework. It certifies the
period-34--48 rows by applying P3 to every positive-growth nonzero-drift leaf; the
P16/P22 variants are conditional consistency checks.

The period-at-most-32 tree was freshly regenerated under current Python source:
59 unprefixed nodes through depth 5 plus 46,185,421 nodes in the 32 length-six prefix
shards, 46,185,480 total, zero hits, all complete. The current source SHA-256 is
`b395ed3aac53bb9f43aea375ffd7257cd81ec3df5404df098783ed0656c4bcfc`.

`records/aggregate_indep.py` now checks all eight counters and fails on a missing
period. The archive described at this historical checkpoint was later rebuilt. Do
not use its obsolete checksum; the canonical archive and checksum are specified in
the superseding final-release section below.
Period 48 is 51,856.023 aggregate shard-seconds (14.404 shard-hours), with recorded
wall time 1:28:48 using 11 workers.

### Narrow growth-four result

The compatible abstract wake matchings have (kappa=1) for axis drift,
(kappa=2) for even diagonal drift, and (kappa\in\{1,2\}) for primitive diagonal
drift. This is a topology classification only. `cycle_functionals` uses alternating
oriented coefficients and is not P22; do not infer that P22 annihilates or controls
the wake kernel.

### Paper corrections already applied

The cyclic-minimum normalization now has a proof. Bare reflection was removed as a
symmetry. The affine-invariant theorem was narrowed to what it proves. The unsupported
clean-translator refinement and Hamming-isolation proposition were removed. The
completed-lifetime token argument was repaired. The touch-graph statement now keeps
labels/multigraph conventions and explicitly limits physical pushforward to
(pi_*Z(T/W)). Bibliographic metadata and runtime/cap claims were corrected.

### Immediate continuation checklist

1. Resolve the two final internal adversarial referee reports; do not describe them as
   peer review.
2. Recompile twice and require zero undefined references and zero overfull boxes.
3. Render all PDF pages and inspect every page visually.
4. Regenerate `results/artifact_hashes.json` after final source/PDF changes.
5. Finish `professor_outreach_email.md` with placeholders; state clearly that the
   preprint does not solve the conjecture and request targeted technical feedback.
6. Mirror this handoff and the proof journal to `outputs/` after every final correction.

## 20 July 2026 final release handoff (supersedes every earlier checkpoint above)

### Mathematical status

The finite-support highway conjecture is **not proved or disproved**. No
counterexample certificate was found. The release proves necessary conditions on
finite-support periodic highways and one exact bounded computation. A complete proof
still needs both:

1. a bounded-active-core/entrance theorem placing the ant and every cell or
   Tait-boundary component capable of influencing the future in one finite translated
   window, with all outside debris permanently inert; and
2. an unbounded-period chronology theorem showing that every positive-growth
   periodic highway agrees in path and turn trace with the standard period-104
   highway up to translation, quarter-turn rotation, and cyclic phase.

Do not revive the earlier exterior-dynamics, centered-3-by-3, Hamming-isolation,
minimum-rectangle, or physical touch-graph-rank claims. They were removed from the
release because their proof or publication certificate was incomplete. The narrow
growth-four wake-port matching audit is only an abstract topology classification;
its alternating oriented functionals are not the signed all-`+1` P22 charges.

### Canonical documents

- Principal source: `paper/main.tex`
- Principal PDF: `paper/main.pdf` (18 pages), SHA-256
  `d3b30f6ca9c9656690c12a9ed637649ad721f72f8d1826d7687e9d0ca0183ea3`
- Technical companion: `companion/main.tex`
- Companion PDF: `companion/main.pdf` (15 pages), SHA-256
  `8c711ae8cdb5b94f006db9a73b8ffdc8753effc16582044ee585349a108afa74`
- Accessible copies: `docs/paper.pdf` and `docs/companion.pdf`; each is byte-identical
  to its source PDF.
- Outreach template: `docs/professor_outreach_email.md`
- Detailed audit trail: `research-notes/proof_journal.md`

Both LaTeX files were compiled twice after the final source edit. Their logs contain
no LaTeX warning, undefined citation/reference, overfull box, underfull box, or fatal
error. The PDFs have explicit title/author metadata. All companion pages and all
changed main-paper pages were rendered and visually inspected; the main paper had
already received a complete all-page visual pass earlier in the same session.

The external-facing claims passed two final internal adversarial agent audits: one
mathematical/companion audit and one cold repository/release audit. These are not peer
review and must never be represented as such.

### Exact computation certificate

The period-at-most-32 records are a complete **first-R cyclic-phase-normalised**
enumeration, not a literally unnormalised binary tree: 59 unprefixed nodes through
depth 5 plus 46,185,421 nodes in all 32 `R` plus five-symbol prefix shards through
depth 32, for 46,185,480 nodes total. Every positive-growth heading-resetting word
contains `R`, and cyclic phase shift preserves the represented periodic orbit and
finite-support realisability. All shards completed below their 100,000,000-node cap
and found zero highways.

Periods 34--48 are certified by the residue-theorem-free shared-framework Java
variant, applying the exact criterion at every positive-growth nonzero-drift leaf.
The strand- and residue-pruned variants are conditional consistency checks, not
independent implementations. The certifying Java source SHA-256 is
`dacd32f6ab2f0c033c4e8226987333f21582e5aecad25322863439065645d68f`.

The frozen archive `records/langton_search_records.tar.gz` contains exactly 460
members and has SHA-256
`7052f3070829bf804ae317a40379f6bb045b00775aff826b4e347880747bcc1a`.
Its constructor verified the exact member set and every inner hash. A fresh extraction
passed both:

    python audit_p32.py
    python aggregate_indep.py

The latter reported `all_checks_passed = True` for every even period 34--48, with
exact rank coverage and zero hits.

The post-normalisation cold extraction was run at 20:32 CDT on 20 July 2026 into a
new directory, without reusing repository-side generated files. `audit_p32.py`
reported schema `langton-p32-exclusion-v2`, all 32 prefixes exactly once,
46,185,480 cyclic-phase-normalised nodes, and zero problems. `aggregate_indep.py`
reported `[OK]` for each even period 34--48 and `all_checks_passed = True`. The
embedded `RECORDS_MANIFEST.json` contains zero CRLF byte pairs.

### Lean boundary

Lean 4.32.0 cleanly built all 18 jobs in the provided Docker environment. The axiom
audit lists only `propext`, `Quot.sound`, and where used `Classical.choice`; the source
contains no `sorry`, `admit`, custom axiom, `native_decide`, or unsafe escape.
`StabilizedP3Word.toOrbitEndpointData` derives the first positive endpoint, balanced
remainder, and binary widget-prefix facts from an explicitly supplied stabilized P3
word. Lean still does not extract that word or the physical lifted potential geometry
from every periodic ant orbit, so P22 and the conjecture are not end-to-end Lean
theorems.

### Release metadata and remaining human actions

`CITATION.cff` validates against CFF schema 1.2.0. `.zenodo.json` records the mixed
license: code/Lean/data are MIT; papers/prose are CC BY 4.0. The deterministic script
`results/update_artifact_hashes.py` regenerates `results/artifact_hashes.json` from all
tracked and non-ignored untracked release files, excluding the self-referential
manifest itself. The manifest was regenerated only after the final PDFs, journal,
handoff, archive, and mirrored outputs were fixed.

Before emailing or depositing:

1. fill the commented author address and professional-email fields in
   `paper/main.tex`;
2. personalize one targeted theorem/interface request per professor;
3. mint or identify an exact Zenodo version DOI (the concept DOI does not pin these
   bytes); and
4. after any such edit, rebuild the PDFs, resync `docs/`, and rerun
   `python results/update_artifact_hashes.py`.

## 21 July 2026 continuation: transverse rigidity (supersedes the section above on open obligations)

### What changed

Two new theorems were proved, audited, corrected, and added to both papers. They
address obligation 2 (periodic classification), and they are the first results in this
project that hold at **every period** rather than up to a search bound.

- **Extremal-line rigidity.** For diagonal drift $|a|=|b|=m$, normalise by quarter-turn
  rotation so that $ab<0$ and take $t=x+y$. Then both extremal level lines $t=T$ and
  $t=T'$ are horizontal, the arrival is east on $t=T$ and west on $t=T'$, every turn on
  them is `R`, every cell of them the trace reaches is entered exactly once (so every
  class meeting an extremal line is a singleton and its cells end black), and $W=T-T'$
  is even.
- **Width-two exclusion.** No finite-support periodic highway with diagonal drift has
  transverse width $2$; hence $W$ is even and $W\ge4$. The standard highway has $W=10$.

Both use only the HV partition and the *ordering* content of the periodic criterion —
that the stabilised word at a cell alternates and begins with `R`. Neither uses the
residue theorem or any of its corollaries. Full statements, proofs and the audit
record are in journal Section 37.

### Two defects found by adversarial audit, both repaired

Recorded in full in journal 37.6. Summarised because both are traps that will recur:

1. Defining the transverse functional by a case split ($x+y$ when $ab<0$, $x-y$ when
   $ab>0$) and then arguing in one frame gives a **false** conclusion in the other: the
   two frames differ by a quarter turn, which exchanges the axes, so "both extremal
   lines are horizontal" fails for half of all drifts. The counterexample is the
   standard highway itself read from an east-facing start. Repaired by normalising to
   $ab<0$ and writing the proof with explicit compass directions.
2. The width-two proof asserted that a site's first visit turns `R`. That is false:
   criterion (ii) constrains only *stabilised* words, and the seed construction
   blackens cells below their class's maximal level precisely so that some first turns
   are `L`. Repaired by counting **edge crossings** instead of site visits: each gap is
   crossed at most once in each direction (each crossing consumes an extremal cell), and
   drift forces net $+1$ per gap, so every site above the start is entered exactly once,
   arrives heading south, departs east, and therefore turns `L` — contradicting (ii).

`verify_width.py` had hard-coded the same false assumption as defect 2, so it could not
have caught it. It has been rewritten to check the geometric inputs and to run an
adversarial search in which an opponent chooses the colour of every not-yet-visited
site; no opponent survives more than $k+4$ steps on $k$ black seeds.

### Current document state

- `paper/main.tex` → `paper/main.pdf`, **22 pages**, compiles with zero errors, zero
  Type-3 fonts. New Section 9 "Transverse rigidity and a period-unbounded exclusion";
  small-period exclusion is now Section 10 and the gap section Section 11.
- `companion/main.tex` → `companion/main.pdf`, **16 pages**, zero errors.
- `docs/paper.pdf` and `docs/companion.pdf` are byte-identical to their sources.
- New verification scripts, all in `code/python/`: `verify_extremal.py`,
  `verify_width.py`, `explore_chronology.py`, `explore_skeleton.py`.
- `results/artifact_hashes.json` regenerated over 70 files.

### Immediate next steps

1. **Fill the author address and professional email** in `paper/main.tex`, rebuild,
   resync `docs/`, rerun `results/update_artifact_hashes.py`.
2. **Commit and tag** (the working tree is not committed). Mint a version DOI.
3. **Send outreach** from `docs/professor_outreach_email.md` — nine verified
   recipients with individually personalised letters, ordered; send one at a time.
   arXiv now requires a personal endorsement for independent researchers; Propp
   (math.CO) and Troubetzkoy (math.DS) are the best-positioned endorsers.

### The obvious research continuation

Width $4$. Lines $0,2,4$ are horizontal and $1,3$ vertical; the extremal lines $0$ and
$4$ remain single-visit, but the interior horizontal line $2$ may be revisited, so the
one-dimensional collapse used for width two does not apply. For each fixed $W$ the
question is finite-state — a highway of width $W$ is an orbit of a machine whose tape
cells are the strip's columns, with alphabet $2^{\lceil (W+1)/2\rceil}$ — so widths
$4,6,8$ are a well-posed decidable target. Settling them would prove the standard
highway is the narrowest possible, which is the transverse counterpart of the
arithmetic constraints already proved.

## 21 July 2026 width-four checkpoint

This section supersedes the immediately preceding claim that fixed width is
automatically finite-state. A finite alphabet on an unbounded longitudinal tape can
retain unbounded memory. What is now proved finite at width four is the search at each
*fixed diagonal drift*, via the period bound below. Decidability for an arbitrary
fixed width still requires a bounded-memory theorem.

Detailed derivations and failed attempts are in
`research-notes/width4_research_2026-07-21.md`. The new paper-grade statements are:

1. **Diagonal width--growth sandwich.** For normalised drift `(m,-m)`, growth `g`,
   and even transverse width `W`, `2m <= g <= mW`.
2. **Six-mask theorem at width four.** In each `x` residue, and independently in
   each `y` residue, the set of odd transverse levels is exactly one of
   `{0,2}`, `{1,3}`, `{0,4}`, `{2,4}`, `{0,1,2,4}`, `{0,2,3,4}`. If `h` residues
   have four-element masks, then `g=2m+2h` and `h=m (mod 2)`.
3. **Width-four period--drift bound.** For macro period `P` and ant period `N=2P`,
   `P+8x<=7m`, hence `P<=7m`, `N<=14m`, and `P=m (mod 2)`, where `x` counts the
   `LN->LN` bottom-boundary macro transition. This uses P3 and extremal singleton
   rigidity, but not the residue theorem. With strand density it gives `N<=7g`.
4. **Primitive width-four exclusion.** No width-four highway has
   `(|a|,|b|)=(1,1)` at any period. The proof forces `P=7` and lists six possible
   words, each with an explicit stabilised-class ordering failure. It is independent
   of the residue theorem.

The fixed-drift Java search combines item 3 with early extremal-residue uniqueness.
It has now excluded every width-four highway for `1<=m<=9`.  The final theorem-bound
row `(m,P)=(9,63)` visited `17,532,472,230` nodes, reached no structural leaf, and
therefore had no P3 hit. The unrestricted width-four
search has zero hits through ant period 76. Result summary:
`results/width4_drift_exclusion_summary.json`.

Lean 4.32.0 now builds 22 jobs and audits the arithmetic kernels in
`lean/Langton/WidthFour.lean`: the six-mask enumeration, even-fiber upper-bound step,
`P+8x<=7m`, period parity, `N<=7g`, and primitive `P=7`. There are no `sorry` or
`admit` declarations. The macro geometry remains a paper input, not an end-to-end
formalisation.

Two negative lessons must remain in the journal:

- `starts R` alone fails: period-50 structural countermodels satisfy it but violate
  alternation;
- an attempted boundary-transition reduction was false because the two-symbol macro
  label was read in the wrong order; it was deleted before use.

`code/python/width4_smt.py` supplies an independent symbolic P3 ordering model. It
returns exact UNSAT on several small instances but times out on harder ones; timeouts
are not exclusions. An incremental class-arithmetic Java prune reduced nodes by only
0.054% and slowed the `m=9,P=57` benchmark from 329.221 to 410.472 seconds, so it was
removed.

Later in the same research window, P3 was rewritten in **spatial block form**. For a
fixed line and residue, the stabilised word is the concatenation of each physical
cell's ordinary visit word from largest longitudinal coordinate to smallest. Hence
the nonzero physical-cell charges `#R-#L` alternate `+1,-1,+1,...` from front to
back, and every forward prefix charge is `0` or `1`. This is exact all-period
ordering information, not another aggregate incidence identity.

A connected integer-flow relaxation satisfying all those prefix inequalities is
still SAT for `m=2,3`; its Euler order fails ordinary same-cell chronology. Therefore
the outstanding obstruction is specifically an order-compatible Euler-trail
problem. A separate exact density lemma gives a more promising finite-reduction
route: among the `m` longitudinal cuts, at least `m/4` are crossed at most seven
times, because their positive odd crossing counts sum to at most `P<=7m`. Repeated
finite crossing signatures may support a pumping theorem, but the splice must still
be proved to preserve tape colours and the P3 seed/wake relation.

The `m=10` continuation has completed every even row through `P=66` with zero P3
hits. At `P=56=5m+6` there are exactly ten ordinary-alternating/extremal leaves, none
passing the odd-class identity; `P=58` and `P=60` have no structural leaf. The
`P=60` row visited `19,138,313,024` nodes; `P=62` visited `30,238,836,043`; and
`P=64` visited `47,442,673,612`; and `P=66` visited `74,038,045,927`. All four had
no structural leaf. The `P=68` and `P=70` workers were stopped unfinished at
18:56:13 CDT and produced no completed rows. The proved fixed-drift range therefore
remains `m<=9`. The completed partial rows are preserved
in `results/width4_m10_partial_2026-07-21.json`.

### Candidate width-four pumping reduction (research only)

The corrected cut signature for residue `r` contains every macro transition that
crosses a lifted cut `r+qm+1/2`, sorted by the stabilised crossing time `i-Pq`.
The signatures partition the `P` macro steps. Their lengths are positive odd
integers summing to `P<=7m`, so at least `m/4` residues have length at most seven.

The current candidate splice lemma says that equal signatures at two residues let
one delete the intervening slab in every future translate and produce a smaller-
drift width-four highway. Its most precise formulation encodes the strip ant as a
deterministic one-tape machine: a tape symbol is a five-bit longitudinal column and
finite control stores transverse line and heading. The splice-sufficient control
signature keeps direction and destination even line, so the classical
crossing-sequence induction preserves all reads and writes on retained columns.
Start the infinitely many disjoint deletions beyond the finite seed and define them
by a finite-time direct limit; every finite prefix uses only finitely many ordinary
splices and the compressed initial tape still has finite support.

For a rightward crossing the destination is `2` or `4`; for a leftward crossing it
is `0` or `2`. Thus after direction is fixed there are only two choices per event,
and at most `2+2^3+2^5+2^7=170` short control signatures. This supersedes both the
three-line overcount `2460` and the earlier decorated count `287934`.

The full average-length budget improves the cutoff further. The short signatures
can supply at most `6*2+4*8+2*32=108` units below average length seven; every
remaining signature has length at least nine and costs at least two units. Hence
there are at most 54 long signatures and at most `2+8+32+128+54=224` residues total.

Extremal singleton rigidity is stronger still. In a length-`2n+1` control
signature, `(+ ,4)` and `(- ,0)` can each occur at most once, so the capacity is at
most `(n+2)(n+1)`. The length-`1,3,5,7` capacities are `2,6,12,20`; their deficit is
60, allowing at most 30 longer signatures. The resulting strongest conditional
cutoff is `m<=70`.

If an independent audit accepts the remaining equivariance step, a minimal drift
has pairwise-distinct control signatures and therefore satisfies the explicit cutoff
`m<=70`; together with `P<=7m`, width-four existence would be decidable by a
finite search. This does **not** exclude width four and is not yet a manuscript
theorem. The remaining hostile point is to prove that old tail translation by
`(2P,m)` advances the oriented spliced event path by a fixed positive finite number
of events after compression, rather than merely preserving its unoriented image.
The full audit checklist is
`research-notes/width4_crossing_splice_proof_draft.md`.

The current proposed discharge uses the crossing-sequence graph. The all-white
far-tail columns form a closed compatible walk of length `m`; equal control
signatures are equal vertices, so deleting the intervening subwalk gives length
`m'`. Translation by one new cycle maps ordered local transcripts and `j`-th
boundary occurrences to their translates, hence is a successor-preserving map of
the one-way tail event path and must be `n -> n+k`. Since it shifts space by
`m'>0`, `k>0`. The remaining independent-audit question is whether the finite-splice
direct limit rules out truncation of a crossing sequence only at infinity.

The current proof rules it out by chronology monotonicity: paired right crossings
occur left-cut then right-cut, while paired left crossings occur right-cut then
left-cut, so every splice jumps forward and only deletes events. Successive finite
splices form subsequences; each retained occurrence has a nonincreasing natural
event index and stabilises. The one-cut lemma supplies it at every finite stage, and
no extra finite-index event can first appear in the limit. Independent review must
still attack this argument before paper promotion.

### Stronger candidate: direct width-four exclusion

`code/python/width4_crossing_graph.py` simulates one initially white five-cell
column from its exact left/right control crossing sequences. Extremal rigidity lets
each boundary use the exceptional rightward top landing and exceptional leftward
bottom landing at most once. An unbounded recursion over column masks, entry state,
and four flags finds exactly 12 compatible edges on 10 vertices, zero reachable
entry cycles, and a directed graph of longest path three. An independent pairwise
check of all 910 constrained signatures through length 25 gives the same 12 edges.

The edge certificate is:

```
202 -> 4
4220222 -> 2, 202, 20222, 2022224
2042222 -> 2, 202, 20222, 2022224
202242222 -> 422, 42202, 4220222
```

Infinitely many initially white columns ahead of any finite seed would require an
infinite path in this acyclic graph. Hence no diagonal width-four highway exists at
any period.  An independent adversarial model has now verified the simulator and
global bridge; Journal \S38.16 records the omitted label hypothesis it caught and the
repair.  The result is promoted with the explicit status ``computer-assisted; local
classifier completeness not formalised in Lean.'' Source SHA-256:
`2AF99EDCBC355945B547AB1F80CAEE6927FA75D6C1C064C5ADC41D13B5FE3E33`.
The unbounded generator reaches 22 entry states, has maximum entry depth eight, and
finds no reachable entry cycle.

`lean/Langton/WidthFourCrossing.lean` checks that the listed graph has the claimed
rank decrease and no four-edge chain. SHA-256:
`548DF94E2B8B60CE23269153EE446CFF824AC1DB6AA1A41773F4E605205324FF`.
It does not yet formalise the Python enumeration's completeness.

Independent implementation check:
`code/python/verify_width4_crossing_graph_indep.py` imports no project search code,
uses compass-letter headings and set-valued black rows, and reproduces the same 12
edges. SHA-256:
`694C1178B00FA8AB929A5375255E53762C403DE02FC1D2958A4409EF9B84AFE0`.
It also extracts crossings at cuts 100 and 101 of the documented standard-highway
finite seed and exactly replays the initially white column between them (boundary
lengths 31 and 21), validating the convention on a genuine highway.

Why this does not immediately exclude widths six/eight:
`code/python/explore_even_width_crossing_cycles.py` finds a reachable two-state
interior cycle `({1,2},2,E) <-> ({1,3},2,W)` at both widths, while finding none at
width four. It does not reuse an extreme event. This is a local-memory obstruction,
not a highway. SHA-256:
`760CD63D8CCC0292AD5FF2A3134CAE7A4E2CDD1AA16758527BFF5F706806F327`.

Machine-readable table, statistics, hashes, and formalisation boundary:
`results/width4_crossing_graph_certificate.json`.

Final pre-manuscript self-audit of the bridge: with `t=x+y` and longitudinal
coordinate `x`, vertical moves remain in a five-cell tape column and horizontal
moves cross its boundaries.  The even destination line plus alternating event
parity is therefore complete boundary control.  Positive periodic drift makes each
far-boundary sequence finite, nonempty, odd, and right/left alternating.  The four
exception flags are exactly the two extremal-cell singleton constraints on each of
the two sides.  Because the preperiod and initial black support touch only finitely
many cells, all sufficiently far columns are untouched white symbols; their exact
boundary sequences would form an infinite directed path through the 12-edge graph.
This pins the only computer-assisted premise to completeness of the independently
reproduced local edge table.  The global reduction and acyclicity contradiction are
not heuristic.

The width-six/two-state failure was hand-decoded as a centre-line rotor oscillator:
mask `{1,2}` with an eastward entry on line 2 changes to `{1,3}` and exits east;
the westward return on line 2 restores `{1,2}` and exits west.  The two reused cells
turn `L,R,L,R,...` in alternating phases and no extreme repeats.  Thus ordinary
same-cell alternation does not kill the recurrence.  A width-six attack must couple
neighbouring columns or use stabilised class-start order; this local cycle is not a
global highway.

Research froze at 19:00:02 CDT on 21 July 2026.  Immediately before the cutoff the
two width-four classifiers and their standard-highway convention test passed again,
and the Docker-pinned Lean 4.32.0 project built 22/22 targets.  All subsequent edits
belong to the manuscript/review/release phase rather than new mathematical research.

## 21 July 2026 release-packaging note (authoritative on final document state)

Supersedes the page counts in every earlier checkpoint, which were accurate when
written but predate the width-four additions. As frozen for release:

- `paper/main.tex` -> `paper/main.pdf`: **24 pages**, compiles with zero errors and
  zero Type-3 fonts; text layer intact (ligatures extract correctly). Section 9 is
  "Transverse rigidity and period-unbounded exclusions" (plural: it now carries the
  width-two theorem, the blank-column classification lemma, and the width-four
  theorem, W>=6). Small-period exclusion is Section 10, the gap Section 11.
- `companion/main.tex` -> `companion/main.pdf`: **18 pages**, zero errors.
- `docs/paper.pdf` and `docs/companion.pdf` are byte-identical to their sources.
- Corresponding author email on the paper: Atharvajil124@gmail.com; affiliation line
  reads "Independent researcher" (the ASSIP/GMU summer account is deliberately not
  claimed as an institutional affiliation).
- `lean/` is clean of sorry/admit/native_decide/custom axioms across all modules,
  including the two new width-four files.

Not yet done, and explicitly the user's to authorise: (1) commit and push the
width-four working tree -- the live GitHub Pages PDF and the concept DOI still resolve
to the pre-width-four release, so any outreach link is stale until this is pushed;
(2) mint a Zenodo version DOI for the new bytes; (3) send the prepared outreach drafts.

## 22 July 2026 consolidation note (single paper; companion folded in and removed)

The project previously shipped two overlapping documents: `paper/main.tex` and a
`companion/main.tex` technical report. They had drifted to cover essentially the same
results and did not cross-reference each other, so publishing both would read as
redundant self-overlap. Consolidated to a single paper of record:

- The companion's one genuinely unique result -- the width-four six-mask structure and
  the period bound P <= 7m (companion `prop:width4arithmetic`) -- was folded into the
  main paper as a new appendix, "Width-four structure and an independent partial
  exclusion" (`app:width4arith`), with `prop:width4arithmetic` and a corollary framing
  it as a logically independent route: P <= 7m bounds each fixed drift to a finite
  search, excluding width four for m <= 9 WITHOUT the blank-column table
  (Lemma 9.4), corroborating Theorem 9.5 on that range. This is non-vacuous because it
  does not assume the crossing-graph completeness premise.
- Everything else in the companion (criterion, invariant, Tait conjugacy, even-winding,
  residue, collision parity, extremal rigidity, width-two, width-four crossing graph,
  period-<=48 exclusion, gateway seed, Lean) was already present in the main paper, so
  nothing else was lost.
- Removed: `companion/main.tex`, `docs/companion.pdf`, `docs/companion.html`. Updated
  `README.md`, `docs/index.html`, `.zenodo.json`, `LICENSE`, `LICENSE-PAPER.md` to stop
  referencing a companion. `CITATION.cff` already cited only the one paper.

Final state: single paper `paper/main.tex` -> `paper/main.pdf`, **25 pages**, zero
errors, zero Type-3 fonts, ligatures intact; `docs/paper.pdf` byte-identical to source.
Manifest regenerated after removal. The mathematics is unchanged; this is a packaging
consolidation, not a new result. Supersedes the "18-page companion" line in the
21 July release-packaging note above.
