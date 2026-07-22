# A rigorous attempt on the finite-support Langton-ant highway conjecture

**Status, 20 July 2026:** I did not obtain a complete proof or a counterexample. This
is a historical working note, not the source of submission claims. Some later sections
preserve exploratory reductions and finite computations that were subsequently
withdrawn, narrowed, or not packaged with publication-grade certificates; they must
not be cited as theorems merely because they remain in this notebook. The canonical
claims and proofs are `../paper/main.tex`; the continuously updated audit trail is
`proof_journal.md`. In particular, the released paper does not claim the old exterior-
dynamics, Hamming-isolation, centered-$3\times3$, or touch-graph-rank statements.

## 1. Formal statement

Let (c_0:\mathbb Z^2\to\{0,1\}) be an initial coloring, where (0) is white and (1) is black. Assume finite support:

\[
\left|\{z\in\mathbb Z^2:c_0(z)=1\}\right|<\infty.
\]

At a white cell the ant turns right; at a black cell it turns left. It flips the current cell and then moves one unit.

The classical highway conjecture says that after some time the ant's future path and
turn trace agree with the standard period-$104$ highway, up to lattice translation,
quarter-turn rotation, and cyclic phase. Finite stationary debris outside the future
path is allowed; equality of the entire colouring is not asserted. The conjecture
remains open.

There are two possible disproofs:

1. a finite configuration whose trajectory is never eventually periodic; or
2. under the “same period-104 highway” formulation, a finite configuration producing a different highway.

## 2. What is already rigorously known

### Unboundedness

Every trajectory visits infinitely many cells. Briefly, if the visited set were finite, reversibility and finiteness would make the trajectory periodic. Every cell is always entered horizontally or always vertically. Choose a visited cell maximizing (x+y). Its north and east neighbors are unvisited. If it is entered horizontally, it must enter from the west and leave south; after its color flips, the next visit from the west makes it leave north, a contradiction. The vertical case is the rotated argument. This is associated with the flipping Lorentz-lattice work of [Bunimovich and Troubetzkoy](https://doi.org/10.1007/BF01049035).

Unboundedness is much weaker than eventual periodic drift.

### Finite-domain escape bounds

A June 2026 preprint proves that while the ant is confined to a fixed (d)-cell connected domain, the same coloring of that domain cannot occur twice. Consequently it escapes in at most (2^d) steps; stronger shape-dependent bounds are also proved. This controls every fixed box but does not control the geometry as the box grows. [Etse (2026)](https://arxiv.org/abs/2606.26677)

### Computational complexity

Finite patterns can make the ant evaluate arbitrary Boolean circuits. Periodic backgrounds with finite perturbations can simulate cellular automata and Turing machines. Thus long transients can contain genuine computation, and a proof cannot reasonably rely on a small empirical time cutoff. [Gajardo–Moreira–Goles, *Complexity of Langton's Ant*](https://arxiv.org/abs/nlin/0306022)

## 3. An exact periodic-trace criterion

The following criterion turns the search for a nonstandard highway into a finite, exact problem.

Let

\[
w=w_0w_1\cdots w_{N-1}\in\{R,L\}^N
\]

be a proposed repeating turn word. Fix an initial direction (q_0), and let (p_i) be the cell occupied immediately before turn (w_i). Calculate the path solely from (w). Suppose after (N) steps the direction is again (q_0) and the displacement is a nonzero vector

\[
d=p_N-p_0\ne0.
\]

Define an equivalence relation on phases by

\[
i\sim j \quad\Longleftrightarrow\quad p_i-p_j\in\mathbb Z d.
\]

For each equivalence class (I), choose a representative point (b_I) and integers (a_i) satisfying

\[
p_i=b_I+a_i d\qquad(i\in I).
\]

For an integer (n\ge \min_{i\in I}a_i), form the word (S_{I,n}) from all (w_i) with (a_i\le n), ordered by the pair

\[
(n-a_i,i).
\]

This is the chronological sequence of turns made at the physical cell (b_I+nd) during the infinite proposed trajectory (w^\omega).

### Theorem — finite-support periodic-trace criterion

The infinite word (w^\omega) is exactly the trace of Langton's ant from some finite-support initial coloring if and only if, for every class (I):

1. every (S_{I,n}), for
   \(min a_i\le n\le\max a_i\), alternates strictly between (R) and (L); and
2. the stabilized word (S_{I,\max a_i}) begins with (R).

When these conditions hold, an explicit finite initial black set is

\[
B=\{b_I+nd:\ n<\max a_i\text{ and }S_{I,n}\text{ begins with }L\}.
\]

### Proof

At a fixed cell, each visit flips its color. Therefore its encountered turn sequence must alternate (R,L,R,L,\ldots) or (L,R,L,R,\ldots). This proves the necessity of condition 1.

The occurrence of phase (i) in period (k\ge0) is at (p_i+kd=b_I+(a_i+k)d). It visits the physical cell (b_I+nd) exactly when (k=n-a_i\ge0), and chronological order is precisely lexicographic order of ((n-a_i,i)). Hence (S_{I,n}) is the complete visit sequence at that cell.

Once (n\ge\max a_i), every phase in (I) is present and the ordering no longer changes with (n); the sequence has stabilized. Infinitely many cells therefore have this same first turn. Since only finitely many cells may initially be black, that stable first turn must be (R), proving the necessity of condition 2.

Conversely, color exactly the finite set (B) black and every other cell white. At each boundary cell the chosen initial color gives the first symbol of (S_{I,n}); strict alternation then gives every later symbol because the cell flips at each visit. At every stabilized cell, condition 2 makes the first encounter (R), matching its white initial state, and condition 1 again supplies all subsequent visits. Induction in chronological time proves that the ant follows (w^\omega) forever. Its position is translated by (d\ne0) every (N) steps, so this is a highway. ∎

There is a useful equivalent one-sequence test. In a fixed class, sort all entries by decreasing (a_i), breaking ties by increasing phase (i). This is the stabilized word. Every boundary word (S_{I,n}) is a suffix of it, obtained by deleting whole high-level blocks. Consequently it is enough to check that this single stabilized word alternates and begins with (R). This reduces the checker to one sort per translation class. A class and its integer level can also be found in constant time by reducing one coordinate modulo the corresponding nonzero coordinate of (d).

This theorem is implemented independently of finite-time pattern matching in [`langton_research.py`](./langton_research.py), function `finite_seed_for_periodic_trace`.

## 4. Exact computational results obtained in this attempt

All calculations use integer coordinates and exact finite sets—no hashes or probabilistic equality tests determine the result.

### The standard highway has a 13-cell gateway

The blank orbit first enters its repeating trace at step 9,977 under zero-based step indexing. Its 104-symbol word has least period 104 and drift ((-2,2)) when normalized to an initially north-facing ant. Applying the theorem constructs the following 13-cell black seed:

```text
(-6,0), (-5,0), (-5,1), (-4,0), (-4,2),
(-3,-1), (-3,2), (-2,-1), (-2,1), (-1,1),
(0,0), (0,1), (0,2)
```

Starting north at the origin with only those cells black produces the 104-step highway immediately. The code also verifies the equivalent finite gateway induction: after 104 steps the required local pattern and direction recur translated by the drift, and the entire semi-infinite leading corridor is white.

### All centered (3\times3) patterns are certified

For a north-facing ant at the center, all (2^9=512) possible black/white patterns supported in the centered (3\times3) block were exhaustively simulated. Every one reached an exact gateway certificate by step 43,577. The last-certified pattern was

```text
#.#
#.#
#.#
```

This is a rigorous computer-assisted result for those 512 cases, not evidence for all finite configurations.

### No finite-support highway of period at most 40

A depth-first enumeration completed the entire legal trace tree through period 32. It is enough to search words beginning with (R): the criterion implies that every finite-support periodic trace contains an (R), and restarting that orbit at such a phase preserves finite support. The 32 length-six prefix shards beginning with (R) contained 25 dynamically legal prefixes, visited 46,185,421 feasible nodes, and all reported zero highways. Periods shorter than six are covered by the earlier searches, and an odd period cannot restore the heading because an odd sum of quarter-turns cannot be divisible by four.

Thus the original periodic-trace search excluded every highway from finite support of nonzero drift and period (1\le N\le32). Independent implementations were cross-checked on all 131,070 binary words through length 16.

After the analytic elimination of zero growth, a new exact positive-growth search completed periods 34, 36, 38, and 40. Its primary runs visited 9,726,176; 19,781,050; 41,972,884; and 201,924,597 nodes and checked 295,495; 1,194,951; 1,469,976; and 10,313,586 exact periodic-criterion leaves, with zero hits. Every rank interval completed without a cap. Independent no-deficit reruns reproduced the zero-hit result at periods 34, 36, and 38; Python/Java per-shard candidate counts agree at periods 16 and 20; and the Java checker positively accepts the known standard word.

Odd lengths cannot restore heading. Combining these computations with the even-winding theorem therefore excludes **every finite-support periodic highway of period at most 40**. This remains a bounded-period computer-assisted theorem and does not exclude aperiodic behavior or periods above 40. The full pruning and coverage audit is in `langton_positive_growth_search_audit.md`.

### The standard word is isolated through Hamming radius four

All 5,356 distance-two and all 4,598,126 distance-four mutations of the standard 104-symbol word were checked exactly; none passed the criterion. A mutation at odd Hamming distance cannot restore the heading, because every flipped turn changes the net rotation by two quarter-turns modulo four. Hence there is no distinct finite-support periodic highway word within Hamming distance four of the standard word. The compiled distance-four checker was first cross-validated against the Python reference on the complete distance-two score histogram.

A targeted constructive search then checked 265,125 distance-six words obtained by extending every distance-four word with violation score at most five. No highway was found; the best three words had two remaining violations. This is not a complete distance-six exclusion—the full sphere has 1,517,381,580 words.

### Adversarial transient search

A small evolutionary run over 221 seven-by-seven patterns found no non-highway behavior; its longest heuristic onset was 44,845 steps. This is only exploratory evidence and has no theorem status.

### Historical computer exclusion at zero-growth period 40

For a repeating trace with zero net black growth, the endpoint decomposition eventually leaves a clean finite translator after its stationary debris separates from the translated path. The proved clean-translator restrictions and the bound $N\ge8|d|$ imply that a nonzero-drift period-40 candidate can have only drift $(\pm4,0)$ or $(0,\pm4)$, and that every drift-translation class of phase positions must have even cardinality.

An exact depth-first search then covered all $2^{11}=2,048$ length-12 prefixes beginning with R. Of those shards, 650 were locally valid; together they visited 16,837,779 legal-prefix nodes. Every shard finished without reaching its node cap, and none produced a finite-support trace certificate. The saved full-shard computation record is `langton_zero_growth_p40_complete_2026-07-14.json`.

A later exhaustive rerun phase-shifted each closed black-count walk to a minimum, so every retained prefix balance was nonnegative. It covered the same 2,048 prefix ranks, retained 342 normalized valid prefixes, visited 5,610,368 nodes, and again found zero hits. The compact source-hash audit is `langton_zero_growth_p40_dyck_audit_2026-07-14.json`.

Thus, conditional on the proved pruning lemmas and the exact implementation, this calculation excluded nonzero-drift zero growth at period 40. The later theorem immediately below now subsumes it at every period. The computation is retained as an independent audit of the exact trace checker.

### Analytic exclusion of every zero-growth periodic highway

There is no clean finite translator: no finite black pattern and ant state can recur as exactly one nonzero translate of itself with restored heading.

To see this, rotate its already-proved axis-aligned drift to $d=(L,0)$ and quotient the bi-infinite clean orbit by $d$. Every quotient vertex has $2k_v$ visits, with exactly $k_v$ R and $k_v$ L turns, because the corresponding physical cell is white before its first and after its last visit. Let $H$ and $V$ be the horizontal and vertical edge multiplicities of the projected closed trace. At each vertex,

\[
H_-+H_+=V_-+V_+=2k_v.
\]

Horizontal edge parity is therefore constant along each row; call it $h_y$. Vertical edge parity is constant down each column and vanishes outside the finite footprint, so every vertical multiplicity is even: $V_e=2G_e$. The exact local turn-parity formula gives $k_v\equiv h_y\pmod2$ at both HV cell types. Dividing the vertical incidence equation by two gives

\[
k_{x,y}=G_{x,y-1/2}+G_{x,y+1/2}.
\]

Summing over all rows in a fixed column cancels every $G$ twice, so $\sum_yh_y$ is even. But modulo two this sum is exactly the winding number of the closed trace across a cylinder seam. A translator lifted from $p$ to $p+d$ winds once, a contradiction.

Every zero-growth repeating trace with nonzero drift eventually separates into stationary debris plus a clean moving packet, so the theorem excludes it. Zero drift would confine the ant to the finitely many positions of one period. Negative growth cannot continue forever, and heading reset makes growth a multiple of four. Consequently every finite-support periodic highway has strictly positive black growth divisible by four. This still permits the ordinary highway, whose growth is 12.

## 5. Exact Tait-graph / boundary-loop reformulation

The checkerboard HV partition gives a planar reformulation that exposes more topology than the raw cell colors. Normalize the ant so even cells receive vertical arrivals and odd cells receive horizontal arrivals. In the frozen all-white routing, admissible directed arcs form clockwise four-cycles around one checkerboard class of plaquettes.

There is also a basic modular conservation law. Number headings by (0,1,2,3) so a right turn adds one, and let (|B_t|) be the number of black cells. Every right turn increases both the heading and (|B_t|) by one, while every left turn decreases both by one. Hence

\[
q_t-|B_t|\equiv q_0-|B_0|\pmod 4.
\]

In particular, a heading-resetting period changes the black-cell count by a multiple of four.

Take those plaquettes as vertices of a rotated square lattice. Each ant cell is the crossing of exactly two such white cycles and therefore corresponds to one lattice edge. Explicitly, for an ant cell (z=(x,y)), label a plaquette by its lower-left corner and define

\[
e_z=\begin{cases}
\{(x,y-1),(x-1,y)\},&x+y\text{ even},\\
\{(x-1,y-1),(x,y)\},&x+y\text{ odd}.
\end{cases}
\]

Let (H_B) be the finite edge-subgraph consisting of (e_z) for black cells (z\in B). White and black are the two smoothings of the corresponding directed crossing. Consequently:

1. the frozen routing loops are the boundary components of a regular neighborhood of (H_B), together with untouched four-cycles;
2. the ant moves along its current boundary loop and then toggles the edge (e_z); and
3. every step either merges two frozen loops or splits one frozen loop into two.

This is an exact conjugacy, not a heuristic picture. It is implemented by `tait_edge` and `tait_graph_stats` in the supplied code.

If (E=|B|), (V) is the number of incident Tait vertices, (k) is the number of nonempty components, and

\[
\beta=E-V+k
\]

is the cycle rank, then the regular neighborhood has (k+\beta=E-V+2k) boundary components. Relative to the (V) separate white plaquette cycles, the loop-count change is

\[
\Delta C=E-2V+2k,
\qquad E+\Delta C=2\beta.
\]

Thus adding a white edge between different components merges two loops and leaves (\beta) unchanged; adding an edge within a component splits a loop and increases (\beta) by one. Removing a bridge splits a loop and leaves (\beta) unchanged; removing a nonbridge merges two loops and decreases (\beta) by one.

Once a new bounding-box record lies outside the finite initial black support, its first visit is white; a new east, north, west, or south record then turns respectively south, east, north, or west. In the Tait graph its new edge has an endpoint in a previously untouched plaquette, so it is a bridge: every sufficiently advanced record expansion merges the active loop with a fresh four-cycle and leaves (\beta) unchanged. Therefore any unbounded production of cycle rank must occur strictly inside territory that has already been explored.

This rules out several tempting proof ideas. The active loop length, its signed area/orientation, the black-edge count, the component count, and the cycle rank all fail to be monotone, with explicit failures already on the blank trajectory. The active loop can shrink by hundreds of arcs in one step.

The standard highway has a particularly rigid graph form. Starting from the 13-black-cell immediate seed, after a short finite settling phase its active component is a translated unicyclic graph with 16 vertices and 16 edges. Each 104-step period leaves the active core unchanged up to displacement and sheds a separate 13-vertex, 12-edge tree. The total cycle rank remains two. The existing gateway induction makes this observation exact for all subsequent periods.

## 6. The attempted universal proof and its exact failure point

The most plausible proof route is to study record frontiers. For a diagonal functional, for example

\[
h(t)=\max_{0\le s\le t}(x_s+y_s),
\]

once (h(t)) exceeds the finite initial support, the half-plane beyond the record frontier is untouched and white.

If the following lemma could be proved, the rest could be made finite and rigorous.

### Missing bounded-retreat lemma

For every finite-support initial configuration, there exist a diagonal direction, a time (T), and a width (W<\infty) such that after (T):

1. the ant never retreats more than (W) layers behind its current record frontier; and
2. all transverse excursions remain in a width-(W) corridor.

Under this lemma, the colors in a bounded frontier window, the ant's position in that window, and its direction form a finite state modulo translation. Determinism then makes the frontier dynamics eventually periodic. The periodic-trace criterion above can classify the resulting cycles and decide whether each is the standard highway.

No proof of the bounded-retreat lemma is known. Unboundedness and finite-domain escape do not imply it: an orbit may keep expanding a two-dimensional region while escaping every fixed box. Moreover, the symbolic trace system on the square grid has infinite-memory effects, so a finite-state argument cannot hold for arbitrary backgrounds; it would have to exploit finite support in an essential way. See [Gajardo, *A symbolic projection of Langton's Ant*](https://doi.org/10.46298/dmtcs.2312).

This is the central gap. Claiming that “the ant eventually forgets its interior” without proving this lemma would simply assume the difficult part of the conjecture.

In the Tait formulation, the missing lemma can be sharpened: one needs to show that the boundary component carrying the ant eventually has a bounded translating core and that components shed behind it can no longer be reabsorbed. A bound on any single scalar invariant is insufficient.

The most tempting pumping argument fails for a precise reason. Even if the same bounded neighborhood of the ant recurs modulo translation, the two boundary strands visible in that neighborhood may or may not be connected through an arbitrarily distant part of the previously explored Tait graph. That nonlocal connectivity determines whether a later edge toggle merges two loops or splits one. Thus equality of a local core does not by itself determine the future. A valid finite-state proof must first establish permanent separation from the discarded graph (or encode an equivalent finite connectivity summary); assuming that separation is exactly assuming the unresolved part.

### Exact loop-memory trichotomy

The nonlocal obstruction can now be stated more sharply. Freeze the coloring before a step and let (\Gamma_t) be the frozen routing cycle containing the ant. Toggling the current cell swaps the successors of the two opposite incoming strands. If those strands lie on different frozen cycles, the swap merges them; if they lie on the same cycle, it splits the cycle. Timestamp the inactive daughter created by a split. It remains literally unchanged until a later merge reabsorbs it.

If active-cycle lengths are eventually bounded by (L), and every reabsorbed non-pristine daughter has age at most (A), then the active cycle together with the at most (A+1) recent daughters is a finite packet modulo translation. Every stored loop has length at most (L) and lies within distance (A+L) of the ant. The packet update is deterministic: an opposite strand not belonging to the active or stored loops must belong to the canonical pristine white four-cycle. A packet repeats, yielding a periodic turn word and a fixed nonzero drift; zero drift would contradict unboundedness.

Consequently every finite-support orbit satisfies at least one of:

1. active frozen-cycle lengths are unbounded;
2. reabsorption ages of non-pristine shed cycles are unbounded; or
3. the orbit eventually follows a translating periodic word.

If a length-(L) daughter is reabsorbed after (D) steps, the excursion endpoints are within (L), while the fixed-domain escape bound forces the excursion to visit at least (\lceil\log_2D\rceil) distinct cells. Thus the second obstruction is specifically a sequence of larger and larger near-return excursions, not an unspecified "memory of the interior." Whether bounded active length alone rules out such unbounded ages remains open.

Jordan separation narrows it further. If the active ant is left on the bounded side of a shed length-(L) loop, it is confined to (O(L^2)) cells until reabsorption, giving an explicit finite delay bound. Any unbounded-age sequence must therefore consist of exterior-side excursions around small stationary marker loops. Exact charge-neutral four-cell patterns can store arbitrarily many such markers, so the row/column and mod-four charges do not eliminate this case. A complete proof must use the forced visit/root order to forbid self-generated arbitrarily long exterior returns.

Three later lemmas sharpen this gap. If active frozen-loop length is eventually at most $L$, the opposite partner loop is also at most $L$, and every temporal segment through pairwise distinct cells has length at most $L$. For finite memory it is enough to bound only black-cell lifetimes: if every R visit is followed by that cell's next, necessarily L, visit within a uniform time, the last bounded number of relative positions and turns determines the future and the ant must enter a translating periodic word. Thus a non-highway orbit must leave cells black for arbitrarily long times before revisiting them.

Also, bounded black count bounds all active frozen loops by the total affected boundary length. Combining that fact with the bounded-loop/age theorem and the even-winding obstruction shows that any bounded-black-count orbit must reabsorb non-pristine loops after unboundedly large delays.

The exact Tait split taxonomy leaves two exterior memory carriers: inner hole markers created by cycle-edge additions, and outer island markers created by bridge removals. A bridge can lie in a bounded face, in which case an inner parent splits into an inner and an outer daughter; omitting this case gives a false classification.

There is also an exact root-order anchor. An R visit leaves a fixed successor arc at that black cell until its next L visit. Under active-loop bound $L$, the frozen cycle carrying this seam always has length at most $L$. If every uninterrupted inactive episode of the seam lasts at most $D$, arbitrarily many dock/undock cycles still keep the whole black lifetime inside radius $L+D$; finite-state counting bounds its duration. Consequently a bounded-loop non-highway requires individual non-pristine seam loops to stay inactive for unbounded times. The surviving loophole is now one genuinely long exterior episode, not merely an unbounded count of short dock/undock cycles.

Finally, a quantitative non-isolation theorem shows that, for every $A$, an explicitly sufficiently long black-cell lifetime contains the ending time of another lifetime longer than $A$. The intervals need not be nested—they can cross—so this gives temporal clustering rather than an infinite descent. Controlling those crossing lifetime chains is a new concrete route toward the remaining memory theorem.

The exact diagnostic code reproduces this mechanism. Through 20,000 blank-orbit steps, the maximum active length is 1,388 and the maximum non-pristine reabsorption age is 4,414; neither maximum increases after the step-9,977 highway onset. On the certified immediate gateway, the corresponding maxima are 152 and 90 through 200 periods. These finite measurements are not universal bounds.

A targeted exact search found a substantially stronger exterior witness in the centered $3\times3$ seed `#.#/#.#/#.#`. A length-eight inner marker is shed at step 14,989, remains literally unchanged, and is reabsorbed at step 38,262, for age 23,273. During the exterior-side excursion the ant reaches Manhattan distance 68 from the shed point and returns within distance three. Redundant daughter tracing and the independent reference diagnostic agree on all event counts. This is a finite witness, not an unbounded-delay proof; the same seed is already known to reach the standard highway later.

### New exact charges and translator restrictions

Let (b_t=|B_t|). Since a white/R step increments both heading and black count and a black/L step decrements both,

\[
q_t-b_t\equiv q_0-b_0\pmod4,
\qquad
p_{t+1}-p_t=u_{q_0-b_0+b_{t+1}}.
\]

Thus the complete spatial path is determined by the one-dimensional black-count walk, subject to the independent cell-alternation constraint.

There are also exact Laurent-polynomial charges over (\mathbf F_2):

\[
\sum_{(x,y)\in B_t}X^x+[q_t\text{ vertical}]X^{x_t},
\qquad
\sum_{(x,y)\in B_t}Y^y+[q_t\text{ horizontal}]Y^{y_t}.
\]

Together with mod-four first-moment charges, they prove that any *clean* finite translator—one whose entire black set and ant recur translated, with no wake—must be axis-aligned, have period divisible by eight and at least 16, and have drift $(4a,0)$ or $(0,4a)$. A complete degree-two additive-charge audit finds one extra quadratic mod-four class, $Q(x,y)=x^2+2xy$, but proves that it gives no stronger endpoint restriction once the drift is an axis multiple of four. This clean-translator theorem does not apply to the ordinary diagonal highway, because that highway continually emits debris.

For an exact repeating word, let (g=\#R-\#L). The stabilized translation classes show that (g) equals the number of odd alternating classes, so (g\ge0) and heading reset makes (g) a multiple of four. Each odd class becomes one solid translation-orbit strand in the wake. If (g>0), the centered first-moment identity proves that some black cells remain at distance at least ((\|d\|/2)n-O(1)) behind the ant after (n) periods. A growing highway therefore cannot have its entire black support in a bounded moving window.

The winding argument also forces every residue modulo each nonzero drift coordinate to carry a positive even number of odd classes. If $d=(a,b)$, then

\[
g\ge2\max(|a|,|b|).
\]

The earlier Laurent charges forced those residue counts to be even but allowed zero; intersection with the translation-cylinder seam forces them to be nonzero. This bound is sharp for static aggregate-flow profiles, although the equality profiles found in the audit are not single chronological ant traces.

More precisely, every repeated trace has a canonical endpoint decomposition into a finite moving widget, a finite stationary correction, and exactly (g) solid (d)-spaced strands. The Laurent charges force an even number of strand bases in every drift-coordinate residue class and determine the moving-widget parity; the mod-four charge then gives a congruence involving only the drift and strand bases. For the normalized standard word this decomposition is exactly two stationary black cells, an 11-cell moving widget, and 12 strands; hence (|B_n|=13+12n) at period boundaries.

If $g=0$, the stationary part eventually separates from the path, and deleting it leaves a genuine clean translator. The even-winding theorem above excludes that translator at every height and period. The earlier corner-free footprint bound $N\ge8|d|$, small-height cylinder algebra, and period-40 search are retained in the proof journal as the route to this stronger result, but they are no longer needed to eliminate zero growth.

The clean first-moment equation also reduces to four residue totals and can be exhaustively enumerated over its unbounded starting black count. Exactly 362 edge-multiplicity profiles survive at period 40 and 4,707 at period 48. Thus every period-48 candidate has a phase with at most 11 moving black cells and never more than 25. An explicit surviving profile exists for every $N=8h\ge24$, so this arithmetic obstruction is useful pruning but cannot prove the conjecture by itself.

### Collision-chain and lifetime interlacement theorems

There is now an exact endpoint theorem for every finite run. Regard a changed cell $(x,y)$ as the edge between a column vertex $C_x$ and a row vertex $R_y$. Associate to an ant state the column token $C_x$ when its heading is vertical and the row token $R_y$ when its heading is horizontal. Over $\mathbf F_2$, the boundary of the row-column incidence graph of $B_s\mathbin\triangle B_t$ is exactly the sum of the two endpoint tokens. Intermediate tokens telescope across arbitrary collision checkpoints. Hence at most one defect component is non-Eulerian, and a same-pose return has only Eulerian defect components.

This yields a sharp local chronology theorem. If an R visit to a cell is followed by its next, necessarily L, visit, the odd-visit support between them contains the paired cell and has even degree in every exact row and column. It therefore contains at least four distinct cells. Parallel arrivals align the two pre-turn directed poses; opposite arrivals align the two post-move poses. Explicit checker-signed mod-four row and column charges then determine the add/remove signs of a minimum four-corner rectangle from the arrival type and the two side parities. The exact potentials and sign algebra are machine checked in Lean. The theorem forces interlacement but is sharp: the standard highway itself has unit-square four-cell examples.

At an L collision, the occupied Tait edge is a bridge exactly when the live and opposite roots lie on the same frozen boundary; deletion then splits that boundary. A nonbridge puts the roots on distinct boundaries and deletion merges them. This exhaustive local classification still does not control the eventual drift. In the exact obstacle reversal, an ancestral degree-one leaf bridge in a 34-edge component splits a length-120 boundary and ejects the ant onto a pristine live four-cycle, yet the eventual standard drift reverses from $(-2,2)$ to $(2,-2)$. The return stores its 524 changed cells in one endpoint-neutral Eulerian incidence component of cycle rank 444.

An attempted touch-graph/interlacement compression was later found to lose information
under the pushforward from distinct lifetime labels to physical row/column labels.
The labelled cycle-space theorem therefore does not imply a full physical touch-graph
rank theorem, and no such theorem is claimed in the paper. A narrow growth-four port-
matching audit does show that the abstract wake kernel has $\kappa=1$ for axis drift,
$\kappa=2$ for even diagonal drift, and $\kappa\in\{1,2\}$ for primitive diagonal
drift. Natural oriented coordinate functionals are noninjective on this kernel; this
is a negative result, not the signed all-$+1$ wake-residue theorem. Controlling the
physical chronology remains open.

## 7. Best disproof program

There are two certificate-producing searches worth scaling:

1. **Alternative highways.** Search periodic words with the exact criterion. A hit gives a finite seed and an inductive proof immediately. A non-104 hit—or a nonstandard period-104 hit—disproves the unique-highway formulation.
2. **Self-enlarging widgets.** Search for a finite pattern that returns after (K) steps with one or more repeated boundary widgets added. An algebraic induction on the number of widgets would prove an increasing, nonperiodic trajectory and disprove even the broad “some highway” statement. Generalized ants are now known to have precisely such finite-seed increasing behaviors, but none is known for the classical two-state ant. [Lutfalla (2025)](https://arxiv.org/abs/2505.05426)

Merely running one configuration for (10^{20}) steps without seeing a highway would not be a disproof. A counterexample needs a finite invariant or a parameterized recurrence proving its behavior for all time.

## 8. Using a large compute cluster

The supplied program supports independent shards.

To divide the periodic-word search, assign every (R/L) prefix of a fixed length to a separate job:

```powershell
python outputs\langton_research.py search-highway-words `
  --max-period 103 `
  --prefix RLLRLRRLLRRL `
  --node-cap 1000000000 `
  --output result_RLLRLRRLLRRL.json
```

The union of all prefixes of the selected length covers the complete tree. Every shard must report `"search_complete": true`; a capped shard proves nothing about its unexplored remainder.

The Hamming-sphere search is also shardable. For example, the distance-six sphere around the standard word contains 1,517,381,580 candidates, so a cluster can divide it by combination rank:

```powershell
python outputs\langton_research.py search-standard-hamming `
  --distance 6 --shards 4096 --shard 0 `
  --output hamming6_shard_0000.json
```

Run shard indices 0 through 4095 and require every output to finish. The implementation un-ranks the first combination in each contiguous interval directly, so a worker does not scan combinations assigned to other shards. Each shard contains about 370,455 candidates; shard zero completed 370,454 candidates in about 90 seconds on the reference machine and found no highway. A zero score is not merely suggestive: the program immediately applies the exact periodic-trace checker and emits the finite black seed.

To divide an exact (4\times4) configuration search, partition the integer interval ([0,65536)):

```powershell
python outputs\langton_research.py exhaustive `
  --side 4 --exact --max-steps 10000000 `
  --start 0 --stop 4096 `
  --output exact_4x4_00000_04096.json
```

Again, an `unresolved_count` greater than zero means only that the time cap was reached. It is not a counterexample.

For serious scaling I would next replace the Python depth-first engine with a compiled, work-stealing implementation and add checkpointed prefix queues. The exact periodic criterion and gateway verifier can remain the trusted reference checker.

## 9. Current conclusion (superseding the historical list)

There is still no universal proof or counterexample. The release establishes only the
claims proved in `../paper/main.tex`:

- an exact constructive criterion deciding whether a proposed heading-resetting,
  nonzero-drift periodic word is realizable from finite support;
- an exact Tait-graph conjugacy and planar cycle-rank surgery identity;
- an even-winding proof that no clean finite translator exists, implying that every
  finite-support periodic highway has positive growth divisible by four;
- a signed mod-four wake-residue identity and the bound
  $g\ge2\max(|a|,|b|)$;
- a two-endpoint row/column collision-chain parity theorem and the resulting
  four-cell lower bound for a completed black lifetime; and
- a residue-theorem-free, rank-audited computation excluding every finite-support
  periodic highway of nonzero drift and period at most $48$.

Selected algebraic kernels are checked in Lean 4, but the extraction of the required
geometric trace certificate is not formalized end to end. The two unresolved duties
are a universal bounded-active-core/entrance theorem and an unbounded-period
classification of all positive-growth periodic highways. Computation may find a
finite counterexample certificate or extend a bounded exclusion, but cannot by itself
close either infinite gap.
