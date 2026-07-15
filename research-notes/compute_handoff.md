# Langton-ant proof and compute handoff

Last updated: 2026-07-14 (live continuation checkpoint)

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
