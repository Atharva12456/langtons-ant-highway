# Langton's ant finite-support highway conjecture — proof journal

**Working date:** 14 July 2026  
**Last detailed update:** 14 July 2026, collision-chain/chronology/Lean continuation  
**Status:** No complete proof or counterexample. Everything below is labeled as a proof, an exact finite computation, a conjecture, or a failed argument.

## 1. Problem and conventions

The initial black set $B_0\subset\mathbb Z^2$ is finite. White cells cause a right turn, black cells cause a left turn, and the current cell is then flipped. Directions are numbered $0,1,2,3$ as north, east, south, west. Translation and rotation let us normalize the initial ant position and heading to $p_0=(0,0)$ and $q_0=N$; without that convention, $B_0$ alone is not a complete state. A *standard highway* means the usual least-period-104 turn trace with diagonal displacement $(\pm2,\pm2)$ per period, up to translation, quarter-turn rotation, and phase. A bare spatial reflection swaps left and right and is not assumed as a symmetry of the rule.

The central conjecture is that every finite $B_0$ eventually enters this standard highway. It is stronger than unboundedness.

## 2. Ledger of rigorously proved statements

### P1. HV/checkerboard partition

At a fixed cell, every arrival is horizontal or every arrival is vertical. Indeed, heading parity changes at every step, as does the checkerboard parity of the ant's position. Their difference is invariant. Consequently the admissible square-grid edges have a fixed orientation: every cell has two incoming and two outgoing directed edges.

### P2. Alternating visit rule

At each cell, encountered turns alternate strictly because every visit flips the cell. All but finitely many cells have R as their first encountered turn, since only finitely many cells are initially black.

### P3. Exact finite-support periodic-trace criterion

For a proposed repeating word $w$ with nonzero drift $d$ and restored heading, group phase positions modulo translations by $d$. In each translation class, order occurrences by decreasing translation level and then increasing phase. The infinite trace $w^\omega$ is realizable from finite black support if and only if each resulting stabilized word alternates and begins with R. Boundary suffixes determine an explicit finite black seed. The proof and implementation are in the main research note and `finite_seed_for_periodic_trace`.

### P4. Heading/black-count invariant

For every time $t$,

\[
q_t-|B_t|\equiv q_0-|B_0|\pmod 4.
\]

A right turn increments both quantities; a left turn decrements both. Therefore a heading-resetting period changes the black-cell count by a multiple of four.

### P5. Tait-graph / boundary-loop conjugacy

Normalize the HV partition so even ant cells receive vertical arrivals. The frozen all-white routing is a collection of clockwise directed four-cycles around one checkerboard class of plaquettes. Use those plaquettes as vertices of a rotated square lattice. An ant cell $z=(x,y)$ corresponds to the Tait edge

\[
e_z=\begin{cases}
\{(x,y-1),(x-1,y)\},&x+y\text{ even},\\
\{(x-1,y-1),(x,y)\},&x+y\text{ odd}.
\end{cases}
\]

Black cells are occupied Tait edges. The frozen routing loops are boundary components of a regular neighborhood of this finite edge-subgraph, together with untouched four-cycles. The moving ant follows a boundary loop and then toggles the corresponding edge. A toggle either merges two loops or splits one loop.

### P6. Exact cycle-rank identity

Let $E$ be the black-edge count, $V$ the number of incident Tait vertices, $k$ the number of nonempty connected components, and $\beta=E-V+k$ the graph cycle rank. A regular neighborhood has $k+\beta$ boundary components. Relative to the $V$ separate all-white plaquette loops,

\[
\Delta C=E-2V+2k,
\qquad E+\Delta C=2\beta.
\]

Adding a bridge merges loops and preserves $\beta$; adding a cycle edge splits a loop and raises $\beta$ by one. Removing a bridge splits a loop and preserves $\beta$; removing a nonbridge merges loops and lowers $\beta$ by one.

### P7. Eventual record-edge lemma

Once a new bounding-box record lies outside the finite initial support, its first visit is white. A new east, north, west, or south record turns respectively south, east, north, or west. Its Tait edge has a previously untouched endpoint, so it is a bridge. Therefore sufficiently advanced record creation cannot increase cycle rank; any unbounded production of $\beta$ must occur inside already explored territory.

### P8. Conditional frontier theorem

If after some time the ant remains in a uniformly bounded window behind one advancing record frontier, has uniformly bounded transverse width, and never re-enters discarded territory, then the state in that window has finitely many possibilities modulo translation. Determinism forces eventual translational periodicity. The exact trace criterion can then decide the resulting period. The unproved part is establishing these geometric hypotheses for every finite initial configuration.

### P15. Even-winding obstruction for a clean translator

There is no nonzero clean finite translator: no finite black pattern and ant state can evolve in finitely many steps to exactly one nonzero translate of itself with restored heading. The proof quotients a putative translator by its drift. Equal R/L counts at every quotient vertex force all vertical edge multiplicities to be even; the halved vertical flows then force the projected closed trace to have even cylinder winding. A translator's trace winds exactly once. The full proof and its zero-growth corollary are in Section 21.

### P16. Positive-growth strand-density bound

If an exact finite-support repeating trace has drift $d=(a,b)\ne0$ and net black growth $g$, then

\[
g\ge2\max(|a|,|b|).
\]

More precisely, every residue class modulo a nonzero drift coordinate contains a positive even number of odd stabilized visit classes. The older Laurent charges gave evenness; cylinder winding forces nonemptiness. The proof is in Section 22.

### P17. Bounded black count forces unbounded loop memory

If an infinite finite-support orbit has a uniformly bounded number of black cells, then the reabsorption ages of non-pristine shed frozen loops are unbounded. A black-count bound automatically bounds every frozen active loop; bounded reabsorption age would then force an eventual translating word by P14, but bounded black count would make its growth zero, contradicting P15. The proof is in Section 23.

### P18. Bounded black-cell lifetimes force a positive-growth highway

It is enough to bound only R-to-L lifetimes: if every later R visit that is eventually followed by another visit receives that next, necessarily L, visit within a fixed number of steps, then a finite normalized visit-history state determines the future. The orbit is eventually translationally periodic with nonzero drift and, by P15, positive growth. Thus every non-highway orbit has cells that are left black for arbitrarily long times before their next visit. The proof is in Section 24.

### P19. Short self-avoiding factors under bounded active loops

If the active frozen-loop length is eventually at most $L$, then the partner loop at every later toggle is also at most $L$, and no later temporal path segment through pairwise distinct cells contains more than $L$ positions. This forces frequent local returns but does not bound excursion radius. The proof is in Section 24.

### P20. Persistent successor-seam reduction

An R visit leaves a fixed directed successor arc at that black cell until its next L visit. Under an active-loop bound $L$, the frozen cycle carrying this seam always has length at most $L$. If each uninterrupted inactive episode of that seam lasts at most $D$, then the whole R-to-L lifetime is explicitly bounded by a finite-state function of $L+D$. Thus unbounded black lifetimes under bounded active loops force individual non-pristine seam loops to remain inactive for unbounded times; unboundedly many short dock/undock episodes alone cannot hide the delay. The proof is in Section 24.

### P21. Long black lifetimes occur in temporal clusters

For every threshold $A$, an explicitly sufficiently long R-to-L lifetime contains the ending time of another cell's R-to-L lifetime longer than $A$. Thus arbitrarily long black memory cannot occur as an isolated event. The inner lifetime may have begun before the outer one, so the theorem gives crossing-or-nested clusters, not laminar nesting. The proof and explicit bound are in Section 24.

### P22. Signed mod-four wake charge in every drift residue

For a finite-support repeating trace with drift $d=(a,b)\ne0$ and canonical wake bases $c_1,\ldots,c_g$, every residue $r\pmod {|a|}$, when $a\ne0$, satisfies

\[
\sum_{i:c_{i,x}\equiv r\ (|a|)}(-1)^{c_{i,x}+c_{i,y}}\equiv2\pmod4,
\]

and the rotated statement holds for every nonzero $y$-drift residue. If a drift coordinate is zero, the corresponding signed sum is $0\pmod4$ in every exact coordinate. This independently implies positivity, evenness, and at least two strands per nonzero drift residue, hence $g\ge2\max(|a|,|b|)$ and $g>0$. It gives a shorter independent proof of the conclusions of P15/P16. The proof, hostile audit, and Lean-checked finite consequence are in Section 27.

### P23. Finite-history flight renewal

Between visits ending black lifetimes longer than a fixed memory horizon $A$, normalized $A$-histories evolve by a finite deterministic white-default map. A repeated history gives a translating finite flight. A zero-drift repetition must hit omitted black memory within one further period. If the drift is nonzero and the flight survives its first $P+1$ repetitions, any later collision ending that flight is with a cell already black when the repeated flight began. The proof is in Section 28.

### P24. Bounded active loops force bounded black components

If the active frozen-cycle length is eventually at most $L$, then every connected component of the black Tait graph thereafter has uniformly bounded edge count and diameter, with a bound depending only on $L$ and the finite black graph at the start of the bounded regime. The repaired proof treats internal new edges correctly by bounding the component's outer boundary, not by claiming that every new edge touches it. See Section 28.

### P25. Long seam episodes have stationary-island cores

Under a fixed active-cycle bound, every sequence of realized successor-seam episodes with unbounded durations has a subsequence containing intervals of unbounded duration and radius during which the entire bounded seam-bearing black component is detached from the active component and unchanged. Thus rapid dock/undock behavior near the anchor cannot account for the long core. The remaining obstruction is guidance by other bounded islands. See Section 28.

### P26. A repeated renewal flight that clears its ancestral frontier escapes forever

Suppose a nonzero-drift $A$-quiet record cycle has survived the precise $P+1$-level warm-up of P23. If at a later quiet level its entire period footprint lies strictly beyond the time-$r$ black support in some integer linear functional increasing along the drift, then the cycle can never be interrupted and repeats forever. P23 rules out a late self-wake collision; the frontier inequality rules out every cell black when the flight began. The resulting trace has positive growth by P15. Hence every sufficiently warmed fixed renewal flight either collides with ancestral black debris before clearing it or escapes as a highway. See Section 32.

### P27. Two-endpoint row/column boundary for every finite run

Represent each changed cell $(x,y)$ as an edge from a column vertex $C_x$ to a row vertex $R_y$ over $\mathbf F_2$. Associate to an ant state the token $C_x$ for a vertical heading and $R_y$ for a horizontal heading. For every interval $[s,t]$, the boundary of the symmetric difference $B_s\mathbin\triangle B_t$ is exactly the sum of the two endpoint tokens. Thus its incidence graph has zero or two odd vertices; if there are two they lie in one component, and every other component is Eulerian. For the same directed pose the symmetric difference is nonempty by P13, every component is Eulerian, and at least four cells differ. Arbitrary collision checkpoints telescope to the same two endpoint tokens. The proof and Lean formalization are in Section 33.

### P28. Exact bridge/nonbridge classification of every black-cell collision

At an L visit, the occupied Tait edge is a bridge exactly when the live and opposite roots lie on the same frozen boundary cycle; deleting it swaps their successors and splits that cycle, with the actual old successor selecting the live daughter. If the edge is not a bridge, the two roots lie on distinct boundary cycles and deletion merges them while lowering cycle rank by one. This is an exhaustive local collision theorem. It does not determine the later drift: the exact one-obstacle witness has an ancestral leaf-bridge split onto a pristine live four-cycle and nevertheless changes eventual drift from $(-2,2)$ to $(2,-2)$. See Section 33.

### P29. Every completed black-cell lifetime carries an Eulerian discrepancy cycle

Let $r<l$ be consecutive visits to one cell, with R at $r$ and L at $l$. The odd-visit support over $[r,l)$ equals that over $(r,l]$, contains the paired cell exactly once, and has even degree at every row and column vertex. Hence it contains that cell on an incidence cycle and has at least four distinct cells. If the two arrivals are parallel, the pre-turn poses at $r,l$ agree; if they are opposite, the post-move poses at $r+1,l+1$ agree. The signed mod-four row/column charges then determine all add/remove signs in a minimum four-corner rectangle from the arrival type and the two side parities. See Section 33.

### P30. Voltage-aware lifetime interlacement and rotation identity

For every P3-valid repeating trace, retain the integral period offset of each physical R-to-L pair. The odd-visit vector of a pair is exactly its base cell plus all translated paired lifetimes with one endpoint inside it and all translated unmatched wake events inside it. Its row-column boundary is zero. The oriented interlacement coefficients are skew-reciprocal under exchanging pair types and reversing voltage. Closing each lifetime walk gives an exact integer rotation identity; summing over all pair types cancels the oriented pair terms and yields $m-2E+H_{\rm tot}=4\sum_e\omega_e$. See Section 34.

### P31. Contracted boundary touch-graph theorem

On the phase cylinder, paired lifetimes are 4-valent temporal vertices and unmatched wake events are degree-2 H/V switches. H/H and V/V smoothing gives a boundary touch graph whose wake-edge subgraph is a disjoint union of $\kappa$ even cycles. Suppressing the wake switches produces a genuine connected 4-regular Euler system whose touch graph is the boundary graph with those wake cycles contracted. The projected lifetime rows span its full binary cycle space, of dimension $m-c-\kappa+1$, where $c$ counts closed H/V smoothing circuits. The uncontracted graph has $\kappa$ additional wake-cycle directions. See Section 34.

## 3. Exact finite computational theorems

1. The blank orbit enters its standard trace at zero-based step 9,977.
2. The standard trace has least period 104 and normalized drift $(-2,2)$.
3. The periodic criterion constructs an immediate 13-black-cell seed and verifies its infinite gateway induction.
4. All 512 centered $3\times3$ initial patterns reach an exact standard gateway by step 43,577.
5. Every finite-support periodic highway of nonzero drift and period at most 32 is excluded. The period-32 search covered 46,185,421 legal nodes in 32 complete prefix shards.
6. Every distinct period-104 word within Hamming distance four of the standard word is excluded: 5,356 distance-two and 4,598,126 distance-four words.
7. A targeted set of 265,125 distance-six words produced no highway; its best score was two. This is not the complete distance-six sphere.
8. The first of 4,096 complete distance-six rank shards checked 370,454 words and found no highway.
9. The computer-assisted search independently excluded every finite-support, **nonzero-drift zero-growth** periodic highway of period 40. It covered all 2,048 length-12 prefix shards beginning with R, visited 16,837,779 legal-prefix nodes, reached no node cap, and found zero certificates. P15 now subsumes this result and excludes the entire zero-growth periodic subclass at every period. The period-40 computation is retained as an independent implementation audit, not as a needed premise of the stronger theorem.
10. Exact positive-growth searches exclude periods 34, 36, 38, and 40. The complete primary runs visited respectively 9,726,176; 19,781,050; 41,972,884; and 201,924,597 nodes, checked 295,495; 1,194,951; 1,469,976; and 10,313,586 exact P3 leaves, and found no hits. All rank intervals completed without caps. Together with item 5, the impossibility of odd heading-resetting periods, and P15's period-independent zero-growth exclusion, **every finite-support periodic highway of period at most 40 is excluded**. The code-audit dependencies and independent checks are in Section 25.
11. Two complete uncapped period-42 searches independently visited the same 528,451,911 nodes and 14,561,206 positive-growth leaves and found zero P3 certificates. The original audited search checked P3 on all leaves. A second implementation first applied P22, rejecting 13,487,309 leaves and checking P3 on the remaining 1,073,897; every per-rank node and leaf count agreed with the original. Therefore every finite-support periodic highway of period at most 42 is excluded. Details and hashes are in Section 30.
12. Two complete uncapped period-44 searches independently visited the same 1,319,080,456 nodes and 67,839,409 positive-growth leaves and found zero P3 certificates. The original engine checked every leaf; the P22-aware engine rejected 65,050,414 leaves and checked the remaining 2,788,995. All 16,384 prefix ranks were covered once, and all shared counters agreed rank by rank. Therefore every finite-support periodic highway of period at most 44 is excluded. Details and hashes are in Section 30.

## 4. Standard highway in Tait-graph form

The immediate 13-edge seed is a forest with 16 incident vertices and three components. After a finite settling phase, the mature period boundary has total cycle rank two. The component carrying the ant is a translated unicyclic component with 16 vertices and 16 edges. Each 104-step period sheds a separate 13-vertex, 12-edge tree while reproducing the active core translated by $(-2,2)$. This follows indefinitely from the already verified gateway induction.

## 5. Failed proof attempts and exact counterexamples

### F1. “The active frozen-loop length is monotone.” False.

On the blank trajectory, at step 4 the frozen active loop drops from length 20 to length 4 in one update. Within the first 2,000 blank steps, decreases of hundreds of arcs occur. Merge/split surgery allows both signs.

### F2. “The ant always remains on an outer clockwise boundary.” False.

On the blank trajectory, at time 14 the active frozen loop is a counterclockwise four-cycle (signed doubled area $+2$). The ant repeatedly enters finite inner-boundary loops.

### F3. “Cycle rank is monotone.” False.

During one mature standard-highway period, total cycle rank takes every value from 1 through 5 and changes on 26 of 104 steps, although it returns from 2 to 2 at the period boundary.

### F4. “Repeating a bounded local core forces the same future.” Invalid.

Two boundary strands visible in the same local window can be connected through different, arbitrarily distant parts of the explored Tait graph. That hidden connectivity changes a later toggle from a merge to a split. A local pumping argument is valid only after permanent separation from the discarded graph, or after a finite summary of all relevant connectivity has been proved sufficient.

### F5. “Unboundedness implies bounded retreat.” Invalid.

Escaping every finite domain permits an orbit that repeatedly enlarges a two-dimensional region. Known fixed-domain escape bounds do not bound the transverse width or the number of returns to old frontier layers.

## 6. Current proof target

The strongest remaining route is to prove one of the following, in decreasing order of strength:

1. **Permanent-separation lemma:** eventually the boundary component carrying the ant cannot reconnect to any component already shed behind an advancing frontier.
2. **Finite-connectivity-summary lemma:** even without separation, all connectivity relevant to future motion can eventually be represented by a bounded number of noncrossing boundary ports.
3. **Bounded active-core lemma:** the portion of the Tait graph belonging to the ant's active boundary component and lying at or ahead of the current record has uniformly bounded size.

Any one must be proved from finite initial support; assuming a bounded corridor would merely restate the missing part.

**Later refinement.** P18 shows it would suffice to bound only the time from an R visit, which leaves a cell black, to that cell's next L visit; long returns to cells left white are irrelevant. Section 24 identifies the persistent successor seam of such a black cell as the exact memory carrier.

## 7. Counterexample program

A genuine disproof must output an infinite certificate, not just a long simulation. Two acceptable forms are:

1. a nonstandard periodic word satisfying the exact finite-support criterion, which disproves uniqueness of the 104-step highway; or
2. a finite self-enlarging Tait gadget whose state recurs with a parameter increased, giving an induction proof of nonperiodic growth.

The complete Hamming-distance-six search is divided into 4,096 contiguous lexicographic rank intervals. Each worker evaluates only its own approximately 370,455 candidates.

## 8. Next experiments and proof checks

- Determine whether bounded active-loop length alone implies a finite connectivity state or construct a formal counterexample model.
- Enumerate noncrossing port-connectivity states for frontier widths 1 through $W$ and derive exact update rules.
- Measure and certify when shed Tait components are last reabsorbed in all centered $3\times3$ cases.
- Search for repeating active cores that emit cyclic rather than tree debris.
- Complete all distance-six rank shards on a cluster.

This journal will be extended rather than overwritten so that failed ideas remain auditable.

## 9. Continuation-session process log

This section records what was attempted in this continuation, including negative results.

1. I split the work into four independent fronts: frozen-loop finite-state reduction, invariant search, primary-literature audit, and an independent audit of the new black-count/moment derivation.
2. I required the two algebraic arguments below to be rederived independently before recording them as proofs.
3. I added exact implementations of the new charges, black-count path reconstruction, centered-moment test, frozen routing, and loop-surgery diagnostics to `langton_research.py`.
4. I ran a deterministic invariant regression on 1,000 random finite states for 200 steps each, for 200,000 checked transitions in total. It checked the heading/black-count invariant, exact path reconstruction, both Laurent-polynomial parity charges, the two affine mod-four charges, and the independent quadratic mod-four charge. All checks passed. This is a regression test, not the proof; the proofs are below.
5. I exactly retraced frozen cycles for 20,000 blank-orbit steps and 20,800 immediate-gateway steps. The commands and JSON outputs are recorded in Section 17.
6. I tested several proposed monotones. Exact compact states realize both signs of every independent local change vector in $(E,V,k,\beta)$, so no nonconstant affine combination of those four quantities can be universally monotone.
7. I checked whether the new first-moment obstruction might force period 104. It does not. At its own level it is sharp already at period 16; the period-16 abstract word fails the separate cell-alternation rule. This failure is kept explicitly in Section 12.
8. I derived the signed translation-orbit decomposition $D=S+(T_d-1)A$, then separated the $g=0$ case into stationary debris $C$ and a moving packet. An independent notation audit caught that an earlier draft reused $S$ for both strand bases and stationary debris; the present version uses $C:=\mathbf1_{B_0}-A$ consistently.
9. I first obtained the footprint estimate $N\ge7|d|$. A later column-by-column audit showed that, in the height-three case, **every** middle-row cell has at least four visits, not merely half of them. Rechecking both HV cases strengthened the proved bound to $N\ge8|d|$. The period-40 candidate drift set is unchanged by this strengthening.
10. I ran the complete nonzero-drift zero-growth period-40 search over 2,048 prefix shards with 10 workers. The saved run visited 16,837,779 nodes in 50.45 seconds and found zero hits. During this final audit I reran all 2,048 shards from scratch: the node total and zero-hit result reproduced exactly; the second wall time was 82.72 seconds. Wall time is machine-load dependent and is not part of the theorem.
11. Three independent audit passes checked the written proof, the pruning logic, and the code/artifacts. They found no invalid period-40 prune. They did identify and trigger the $S/C$ notation repair, the stronger $8|d|$ bound, explicit exclusion scope for $d=0$, and stricter wording that the JSON is a computation record rather than a self-authenticating proof certificate.
12. I hardened `run_zero_growth_cluster.py`: a partial rank interval now labels itself partial; checkpoint reuse requires a complete matching prefix, search settings, schema version, and exact engine and runner SHA-256 hashes; the top-level complete label requires every rank exactly once and every shard complete; and invalid worker/period/prefix arguments are rejected.
13. I compressed the clean zero-moment equation into the four residue totals $(P,Q,R,S)$ in Step 3b, then exhaustively enumerated every ordered edge-multiplicity composition for $N=40$ and $N=48$. Two independent exact implementations agreed. The surviving profiles and the explicit infinite family in Step 3b show precisely why this obstruction prunes but does not settle the conjecture.
14. I solved the additive-charge cocycle for arbitrary weights, classified all polynomial weights of degree at most two modulo four and eight, and found one genuinely new quadratic mod-four class. Its exact potentials were added to the code and rechecked over the same 200,000 transitions. The endpoint analysis then proved that it supplies no restriction beyond axis drift divisible by four.
15. I then passed from footprint cell counts to directed edge-flow multiplicities on the translation cylinder. The local R/L balance gives a parity rule at every HV cell. Chasing that rule around strips proves that height three is impossible for every clean horizontal translator and height four is impossible for drift magnitude four. At this checkpoint, exploratory hints of a general even-winding obstruction were **not** promoted to a claim; the later independent derivation and audits in Section 21 finally establish it as P15.
16. Finally, I normalized every zero-growth word at a minimum of its closed black-count walk. This forces all relative prefix balances to be nonnegative and is exhaustive up to cyclic phase. Adding that proved prune reduced the complete period-40 rerun from 16,837,779 to 5,610,368 sharded nodes. The current source-hashed run again completed all 2,048 ranks with zero hits.

No item in this process log is being promoted to a universal result merely because it survived computation.

## 10. P9 - exact black-count path reduction

Let

- $B_t$ be the finite black set immediately before step $t$;
- $b_t=|B_t|$;
- $p_t\in\mathbb Z^2$ be the ant position;
- $q_t\in\mathbb Z/4\mathbb Z$ be its heading, numbered $0=N,1=E,2=S,3=W$; and
- $u_q$ be the unit vector in heading $q$.

Put $r_t=b_{t+1}-b_t$. A white/R step adds the current cell to $B_t$ and turns clockwise, so $r_t=+1$ and $q_{t+1}-q_t=+1$. A black/L step removes it and turns counterclockwise, so both differences are $-1$. Therefore

\[
q_t-b_t\equiv q_0-b_0\pmod4.
\]

The movement occurs after the turn. Hence

\[
\boxed{p_{t+1}-p_t=u_{q_0-b_0+b_{t+1}}.}
\]

This is stronger than the earlier modular observation: after the single residue $q_0-b_0$ is fixed, the complete two-dimensional path is determined by the one-dimensional nonnegative nearest-neighbor walk $b_t$. It does **not** say that every nonnegative nearest-neighbor walk is color-realizable; repeated visits must still request alternating turns.

Implementation: `predicted_path_from_black_count`. The 200,000-transition regression reconstructed every final position, direction, and black count exactly.

## 11. P10 - centered first-moment identity

Define the ordinary and ant-centered black first moments

\[
M_t=\sum_{z\in B_t}z,
\qquad
J_t=M_t-b_tp_t=\sum_{z\in B_t}(z-p_t).
\]

Toggling $p_t$ changes $M_t$ by $r_tp_t$. Expanding the centered moment gives

\[
\begin{aligned}
J_{t+1}-J_t
&=r_tp_t-\bigl(b_{t+1}p_{t+1}-b_tp_t\bigr)\\
&=-b_{t+1}(p_{t+1}-p_t).
\end{aligned}
\]

Using P9,

\[
\boxed{J_{t+1}-J_t=-b_{t+1}u_{q_0-b_0+b_{t+1}}.}
\]

The sign was checked independently by using

\[
b_{t+1}p_{t+1}-b_tp_t
=(b_{t+1}-b_t)p_t+b_{t+1}(p_{t+1}-p_t).
\]

This identity is exact for every finite-support orbit and every step. It is useful because a translation of the entire black set together with the ant leaves $J_t$ unchanged.

## 12. P11 - restrictions on a clean finite translator

### Definition and theorem

A **clean finite translator with nonzero drift** is a finite state for which, for some $N>0$ and $d\in\mathbb Z^2\setminus\{0\}$,

\[
B_N=B_0+d,\qquad p_N=p_0+d,\qquad q_N=q_0.
\]

The word *clean* means that the complete black set translates; there is no stationary debris and no newly emitted wake. This is not the usual 104-step highway, which grows a wake.

**Theorem.** Every clean finite translator with nonzero drift satisfies

\[
N\equiv0\pmod8,\qquad N\ge16,
\]

and its nonzero drift is axis-aligned with coordinate divisible by four:

\[
d=(4a,0)\quad\text{or}\quad d=(0,4a),\qquad a\ne0.
\]

### Step 1: necessary zero-moment equation

Clean translation gives $J_N=J_0$. Summing P10 and rotating away the fixed heading offset yields

\[
\boxed{\sum_{t=0}^{N-1}b_{t+1}u_{b_{t+1}}=0.}
\]

The count path is closed because $b_N=b_0$. For every height edge $k\leftrightarrow k+1$, let $m_k$ be its number of upcrossings. A closed walk has exactly $m_k$ downcrossings. Its traversed height edges form one contiguous interval, and

\[
N=2H,\qquad H=\sum_{k\ge0}m_k.
\]

Pairing an upcrossing, whose arrival height is $k+1$, with a downcrossing, whose arrival height is $k$, converts the moment equation to

\[
\boxed{\sum_{k\ge0}m_k\bigl(ku_k+(k+1)u_{k+1}\bigr)=0.}
\]

### Step 2: period is divisible by eight

Rotate coordinates so $u_0=(1,0)$ and headings still advance clockwise. Put

\[
v_k=ku_k+(k+1)u_{k+1}.
\]

Then

\[
\begin{array}{c|c}
k\bmod4&v_k\\ \hline
0&(k,-k-1)\\
1&(-k-1,-k)\\
2&(-k,k+1)\\
3&(k+1,k)
\end{array}
\]

The second coordinate in every row is $-1$ modulo four. Therefore the zero-vector equation implies

\[
0\equiv-\sum_km_k=-H\pmod4.
\]

Thus $H\equiv0\pmod4$ and $N=2H\equiv0\pmod8$.

### Step 3: exclude period eight

The only positive $H<8$ consistent with the preceding congruence is $H=4$. If the lowest traversed height edge is $a$, contiguity says the positive multiplicities are one of the eight ordered compositions of four. After rotating the axes by $-a$ quarter-turns, the exact moment sums are

\[
\begin{array}{c|c}
(m_a,m_{a+1},\ldots)&\sum m_kv_k\\ \hline
(4)&(4a,-4a-4)\\
(1,3)&(-2a-6,-4a-4)\\
(2,2)&(-4,-4a-4)\\
(3,1)&(2a-2,-4a-4)\\
(1,1,2)&(-2a-6,4)\\
(1,2,1)&(-2a-6,-2a)\\
(2,1,1)&(-4,-2a)\\
(1,1,1,1)&(0,4)
\end{array}
\]

No row vanishes for integer $a\ge0$. Hence $H\ne4$ and $N\ge16$.

### Step 3b: exact residue form of the count-spectrum obstruction

The edge-multiplicity equation admits a useful four-residue compression. Put

\[
M_r=\sum_{k\equiv r\ (4)}m_k,qquad
K_r=\sum_{k\equiv r\ (4)}k,m_k,
\]

and define

\[
P=M_0-M_2,quad Q=M_1-M_3,quad
R=K_0-K_2,quad S=K_1-K_3.
\]

Direct substitution of the four vectors $u_k$ gives

\[
\boxed{
d=(P-Q,-P-Q),qquad
Z=(R-S-Q,-R-S-P),
}
\]

where $Z$ is the left side of the zero-moment equation. Thus $Z=0$ and an axis drift of magnitude four have exactly the following scalar targets:

\[
\begin{array}{c|rrrr}
d&P&Q&R&S\\ \hline
(4,0)&2&-2&-2&0\\
(-4,0)&-2&2&2&0\\
(0,-4)&2&2&0&-2\\
(0,4)&-2&-2&0&2
\end{array}
\]

This makes the unbounded lowest black count exactly enumerable. Write the positive contiguous multiplicities as $(m_a,\ldots,m_{a+\ell-1})$, with sum $H=N/2$, and express $a=r+4s$ for $0\le r<4$. For a fixed ordered composition and residue $r$, changing $s$ leaves $P,Q$ fixed and sends

\[
(R,S)\longmapsto(R+4sP,S+4sQ).
\]

For nonzero drift, at most one integer $s\ge0$ can therefore solve the target equations. Enumerating the $2^{H-1}$ ordered compositions and four residues is finite and exhaustive despite the absence of an a priori bound on $a$.

There is an exact infinite family showing the limitation of this obstruction. For every $h\ge3$, take $H=4h$, $a=h-2$, and, in four consecutive residue positions,

\[
(m_a,m_{a+1},m_{a+2},m_{a+3})=(h,h+2,h-2,h).
\]

In axes rotated by the residue of $a$, its drift is $(0,-4)$ and its moment is exactly zero; in the original axes the drift is the corresponding quarter-turn rotation. The bidirected height-path multigraph is balanced and connected, so it has an Euler circuit and hence a closed black-count walk. This does **not** make it a Langton trace: the separate spatial cell-alternation condition can still fail. It proves that first-moment/count-spectrum arithmetic alone cannot exclude all periods $N=8h\ge24$.

### Step 4: parity charges force axis alignment

Work in the Laurent polynomial rings over $\mathbf F_2$. Define

\[
C_t(X)=\sum_{(x,y)\in B_t}X^x,
\qquad
R_t(Y)=\sum_{(x,y)\in B_t}Y^y.
\]

Let $V_t$ be one when $q_t$ is vertical and zero otherwise, and let $H_t=1-V_t$. Then

\[
\boxed{A_t=C_t(X)+V_tX^{x_t},
\qquad D_t=R_t(Y)+H_tY^{y_t}}
\]

are conserved exactly. For columns: if the incoming heading is vertical, the cell toggle at column $x_t$ cancels the disappearing vertical correction; if it is horizontal, the post-turn motion is vertical, so $x_{t+1}=x_t$ and the cell toggle cancels the newly appearing correction. The row proof is the rotated argument.

If a complete state translates by $d=(a,b)$, then conservation and translation give

\[
A=X^aA,\qquad D=Y^bD.
\]

The Laurent rings are integral domains. Thus $a\ne0$ forces $A=0$, and $b\ne0$ forces $D=0$. But

\[
A(1)=|B|+V,\qquad D(1)=|B|+H
\]

in $\mathbf F_2$, and these two values cannot both vanish because $V+H=1$. Therefore $a$ and $b$ cannot both be nonzero: every clean translator is axis-aligned.

These charges also exhaust all invariants that are additive over black cells with an $\mathbf F_2$ ant-state correction. For completeness, if the correction is $f_q(z)$ and the black-cell weight is $w(z)$, the R and L step equations are

\[
w(z)=f_q(z)+f_{q+1}(z+u_{q+1})
=f_q(z)+f_{q-1}(z+u_{q-1}).
\]

Eliminating the four $f_q$ gives the zero mixed-difference equation

\[
w(x+1,y+1)+w(x+1,y)+w(x,y+1)+w(x,y)=0.
\]

Its complete solutions are $w(x,y)=\alpha(x)+\beta(y)$. Substitution in the step equations gives exactly the column and row charges above, apart from a constant depending only on the fixed HV kinematic sector.

### Step 5: a mod-four charge strengthens the drift to a multiple of four

The following quantity is conserved modulo four:

\[
I_4(B,p,q)=\sum_{(x,y)\in B}(x+y)+F_q(x_p,y_p),
\]

where

\[
\begin{array}{c|c}
q&F_q(x,y)\\ \hline
N&2x+3y+3\\
E&x+2y+2\\
S&y+3\\
W&3x+2.
\end{array}
\]

For a turn sign $s=+1$ on R and $s=-1$ on L, toggling contributes $s(x+y)$ and a direct eight-case substitution gives $\Delta F=-s(x+y)$ modulo four.

For a clean translation by $(a,b)$ with $b_0=|B|$, the constants cancel and conservation requires

\[
b_0(a+b)+L_q(a,b)\equiv0\pmod4,
\]

where $L_N=2a+3b$, $L_E=a+2b$, $L_S=b$, and $L_W=3a$. If the translation is horizontal, the vanishing column charge gives $b_0\equiv V\pmod2$; the coefficient of $a$ is respectively $b_0+2,b_0+1,b_0,b_0+3$ for $N,E,S,W$, always odd. Hence $a\equiv0\pmod4$. The vertical argument uses $b_0\equiv H\pmod2$ and coefficients $b_0+3,b_0+2,b_0+1,b_0$, again always odd. Hence $b\equiv0\pmod4$.

There is a rotated companion with black weight $x-y$ and potentials

\[
(F_N,F_E,F_S,F_W)=(2x+3y+3,\ x+2,\ y+3,\ 3x+2y+2).
\]

It is a genuine conserved charge and is included in the regression. For an affine weight $w=\alpha x+\beta y+\gamma$, the complete cocycle calculation solves the eight coefficient equations

\[
F_{q+1}(z+u_{q+1})-F_q(z)=-w(z),\qquad
F_{q-1}(z+u_{q-1})-F_q(z)=w(z)
\pmod4
\]

for affine $F_q$. They are consistent exactly when $\alpha\equiv\beta\pmod2$. If both are even, the invariant is a doubled row/column $\mathbf F_2$ charge; if both are odd, it differs from the displayed $x+y$ charge by doubled row/column charges. Thus no unexamined independent affine-linear mod-four moment remains.

### Complete degree-two additive-charge audit

The same local equations permit a full functional classification, not just an affine ansatz. For an additive charge

\[
I(B,p,q)=\sum_{z\in B}w(z)+F_q(p)\pmod m,
\]

an unrestricted ant-state correction $F_q$ exists if and only if

\[
\boxed{4w(z)=0,\qquad
w(x,y)+w(x+1,y)+w(x,y+1)+w(x+1,y+1)=0\pmod m.}
\]

Necessity follows by comparing the opposite R/L equations, which gives both $F_S=F_N-2w$ and $F_S=F_N+2w$, and then summing around an elementary unit diamond. Conversely, the two diagonal increments obtained from the N/E equations have zero diamond curl under the displayed conditions; define $F_N$ on each checkerboard sublattice by path integration, put $F_E(z)=F_N(z-e_x)-w(z-e_x)$, $F_S=F_N+2w$, and $F_W=F_E+2w$, and direct substitution verifies all eight equations.

For

\[
w=ax^2+bxy+cy^2+dx+ey+f\pmod4,
\]

the conditions reduce exactly to

\[
b\equiv0\pmod2,\qquad
2a+b+2c+2d+2e\equiv0\pmod4.
\]

Modulo the constant/heading charge, the affine charges above, and doubled $\mathbf F_2$ row/column charges, there is exactly one new quadratic class. A convenient representative is

\[
Q(x,y)=x^2+2xy\pmod4,
\]

with potentials

\[
\begin{aligned}
F_N&=2xy+3x,&F_E&=3x^2+x,\\
F_S&=2x^2+2xy+3x,&F_W&=x^2+x
\end{aligned}
\pmod4.
\]

The other apparent generator $y^2+2xy$ differs by old charges, and $2Q=2x$ modulo four, so the new quotient class has order two. Modulo eight, $4w=0$ first forces the coefficient parities $a\equiv d$, $c\equiv e$, with $b,f$ even. The $x$- and $y$-coefficients of the square sum force $b/2\equiv d\equiv e\pmod2$; its constant coefficient rules out the odd case. Hence $b$ is divisible by four and every other coefficient is even. Dividing by two leaves exactly the mod-four classification above. Thus every degree-at-most-two mod-eight solution is twice an admissible mod-four solution; there is no primitive quadratic lift. This audit does **not** strengthen the clean-translator endpoint theorem: translation by four in either axis fixes all these polynomial weights and potentials modulo four (and their doubles modulo eight). The new $Q$ charge is implemented as `mod4_quadratic_charge` and included in the deterministic regression.

### Sharp limitation of the theorem

The abstract count word

```text
RRRRRLLLRLLRLLRL
```

has period 16, count sequence

```text
0,1,2,3,4,5,4,3,2,3,2,1,2,1,0,1,0
```

and satisfies the zero-moment equation with drift $(2,0)$. It is nevertheless impossible for Langton's ant: the predicted path visits $(0,0)$ at phases 0 and 4 and requests R both times, contradicting visit alternation. Thus moment theory alone is sharp at $N=16$ and cannot replace cell-consistency. The mod-four charge rules out its drift for a genuine clean state.

Most importantly, this clean-translator theorem must **not** be applied to the ordinary highway: the standard orbit emits black wake cells and does not translate its entire finite black set.

## 13. P12 - exact structure of any repeating trace and its debris

Suppose an R/L word of length $N$ repeats exactly from a finite-support gateway, with nonzero spatial drift $d$. Let

\[
g=\#R-\#L
\]

be the black-count increase per period. Heading reset gives $g\equiv0\pmod4$. Indefinite repetition from finite support gives $g\ge0$, since $g<0$ would eventually make the black count negative.

There is a sharper proof from the periodic-trace classes. Each stabilized translation class begins with R and alternates. Its contribution to $\#R-\#L$ is zero when its length is even and one when its length is odd. Therefore

\[
\boxed{g=\text{number of odd stabilized translation classes}.}
\]

In particular, the growing classes occur in a number divisible by four. For the standard word, $g=12$.

Define the signed one-period toggle pattern relative to the period start by

\[
D(s)=\sum_{j:p_j-p_0=s}(b_{j+1}-b_j).
\]

At period boundaries,

\[
\boxed{\mathbf1_{B_{n+1}}-\mathbf1_{B_n}=T_d^nD.}
\]

On an orbit $O$ of translation by $d$, put $g_O=\sum_{x\in O}D(x)$. Accumulating translated copies of $D$ produces, far from the two finite caps, a cell value $g_O$. Since cell colors are binary and the initial black support is finite,

\[
\boxed{g_O\in\{0,1\}.}
\]

Thus $g=\sum_Og_O$ is exactly the number of growing $d$-spaced black strands. A repeating highway consists at period boundaries of finitely many solid translation-orbit strands with finite stationary and moving caps. This is an algebraic restatement of the alternating translation-class criterion, not an assumption about the picture.

The caps and strands have a canonical exact normal form. On one orbit $c+\mathbb Zd$, index the signed pattern by $D_k$ and put $F(k)=\sum_{r\le k}D_r$. Evaluating the binary color at a point moving with the period number shows

\[
s-F(k)\in\{0,1\},\qquad s=\sum_kD_k\in\{0,1\}.
\]

If $s=1$, then $F\in\{0,1\}$ and the nonzero signs of $D_k$ alternate $+,-,\ldots,+$. If $s=0$, then $F\in\{-1,0\}$ and they alternate $-,+,\ldots,-,+$. Choose a base $c_i$ at the first positive entry on each $s=1$ orbit. The prefix sums construct a finite $0/1$ moving widget $A$ and base pattern $S=\sum_i\delta_{c_i}$ satisfying

\[
\boxed{D=S+(T_d-1)A,\qquad |S|=g.}
\]

Consequently, as an exact integer-indicator identity,

\[
\boxed{
\mathbf1_{B_n}=(\mathbf1_{B_0}-A)+T_d^nA+
\sum_i\sum_{j=0}^{n-1}\delta_{c_i+jd}.
}
\]

After a finite phase shift this becomes literally finite stationary debris, a finite translated packet, and $g$ solid segments with finite endpoint decorations. In the displayed algebraic form, the stationary correction can be signed before overlapping terms are combined; the complete sum is always the binary color configuration.

### Strand-only consequences of the conserved charges

Write $d=(a,b)$, let $p$ be the period-start position, and put $V=[q\text{ vertical}]$, $H=1-V$. Define

\[
S_x=\sum_iX^{c_{i,x}},\qquad S_y=\sum_iY^{c_{i,y}},
\]

with $A_x,A_y$ the parity profiles of $A$. Substitution into the Laurent charges gives

\[
\boxed{
S_x=(1+X^a)(A_x+VX^{p_x}),\qquad
S_y=(1+Y^b)(A_y+HY^{p_y}).
}
\]

Therefore every residue class modulo $|a|$ contains an even number of strand bases when $a\ne0$; if $a=0$, every exact column does. The analogous statement holds for rows. Equivalently, the bases form an Eulerian bipartite multigraph between the column and row residue classes, so they decompose into even cycles.

When $a\ne0$, let $Q_x=S_x/(1+X^a)$. Then

\[
|A|\equiv V+Q_x(1)\pmod2.
\]

There is an analogous row formula. If both drift components are nonzero, compatibility requires

\[
Q_x(1)+Q_y(1)\equiv1\pmod2.
\]

Let $\kappa=|A|\bmod2$, as determined above. Since heading reset makes the period even, $a+b$ is even. The mod-four charge eliminates the rest of the moving widget and gives the strand-only test

\[
\boxed{
\sum_i(c_{i,x}+c_{i,y})+(a+b)\kappa+L_q(a,b)\equiv0\pmod4,
}
\]

where $L_N=2a+3b$, $L_E=a+2b$, $L_S=b$, and $L_W=3a$. The rotated $x-y$ charge is a cross-check but is algebraically redundant after the complete Laurent equations are imposed.

For example, if $d=(\pm2,0)$, each used row contains the two possible $x$-parity strands. The number of used rows is even; for four strands the two rows must have the same parity. These are rigorous pruning rules for a widget search, not a classification of all highways.

If $g=0$, then $D=T_dA-A$ for a finite integer pattern $A$, so

\[
\mathbf1_{B_n}=C+T_d^nA,
\qquad C:=\mathbf1_{B_0}-A.
\]

For sufficiently large $n$, the two finite supports separate. Binary validity forces $C$ and $A$ to be $0/1$ patterns. Hence every zero-growth repeated trace decomposes into stationary finite debris $C$ plus a finite translating packet $A+nd$. The clean case is $C=\varnothing$.

The moving packet is genuinely clean even when the stationary part is nonempty. Let $K$ be the union of all phase positions in one word, relative to its period-start position. For fixed $c\in C$ and $k\in K$, the equation $c=k+nd$ has at most one solution because $d\ne0$. Since $C$ and $K$ are finite, after a sufficiently late period none of the phase footprints in any later period meets $C$. Deleting $C$ then changes no subsequent local color, so the remaining packet evolves by

\[
(A,p,q)\longmapsto(A+d,p+d,q)
\]

in one period, after translating the late state back to the origin.

There is a bookkeeping warning. If $c=|C|$, $a_j$ is the moving-packet black count during phase $j$, and $v_j$ is the step vector, then the full count is $c+a_j$ but the full centered moment changes by $-cd$ per period. P10 gives

\[
\sum_j(c+a_{j+1})v_j=cd.
\]

Since $\sum_jv_j=d$, the stationary part cancels and the correct clean-packet equation is

\[
\sum_ja_{j+1}v_j=0.
\]

Applying the zero-moment condition directly to the total black count would therefore be wrong unless $C=\varnothing$.

### Corner-free footprint and a new period lower bound for zero growth

The clean translator extends bi-infinitely because a Langton step is reversible: its period-boundary states are $A+nd$ for every $n\in\mathbb Z$. At each of the finitely many phases, the black set is a finite pattern translated by $nd$. For a fixed lattice cell and a fixed phase, the equation placing that translated pattern or phase position on the cell has at most one solution in $n$, because $d\ne0$. Thus every footprint cell has finitely many visits and is white before its first visit and after its last visit. It is consequently visited a positive even number of times, starting with R, alternating, and ending with L.

The footprint itself has no corners. If a visited cell had two adjacent footprint neighbors missing, one missing incident arc would be incoming and one outgoing. All arrivals would use the other incoming arc; at least two alternating visits from that fixed heading force both outgoing arcs, a contradiction.

Assume $d=(L,0)$ with $L>0$; rotate for the vertical case. The footprint has finite height and is invariant under translation by $(L,0)$. Its nonempty top row is full by the corner argument, and the row immediately below is full because at each top cell either every arrival must come from below or every departure must go below. The bottom two rows are full symmetrically. Each footprint cell has at least two visits. Horizontal departures from the extreme top row balance east/west, since its relevant cells receive a fixed vertical arrival and alternate R/L evenly; the bottom row also has zero net horizontal contribution. A height-two footprint would therefore have zero total horizontal displacement, contradicting $d=(L,0)$. Hence the height is at least three.

Quotient the bi-infinite trace by translation through $(L,0)$. A full row has exactly $L$ cell classes in this quotient, and the sum of their visit multiplicities over all footprint classes is exactly the period $N$.

If its height is exactly three, top and bottom contribute at least $4L$ visits. In each column the top and bottom cells have the same HV type, because their heights differ by two; the middle cell has the opposite type. If the extreme cells have vertical arrivals, each of their at least two visits arrives across its middle--extreme edge, forcing the middle cell to make at least two departures to each extreme. If the extreme cells have horizontal arrivals, each makes at least two departures across that edge, forcing at least two middle-cell arrivals from each extreme. Thus every middle cell has at least four visits, contributing another $4L$. If the height is at least four, the four distinct full boundary rows already contribute at least $8L$. Therefore

\[
\boxed{N\ge8|d|.}
\]

### Stronger cylinder-flow exclusions at small height

The same quotient supports sharper local statements. Work on the cylinder

\[
C_L=(\mathbb Z/L\mathbb Z)\times\mathbb Z
\]

for a horizontal translator $d=(L,0)$, $L>0$. P11 already gives $L\in4\mathbb Z$. Its projected trace is closed, while its lift has signed horizontal displacement $L$. If a quotient cell $v$ has $n_v$ visits, choose a physical lift of it. As above, that lift starts and ends white, so

\[
n_v=2k_v
\]

with exactly $k_v$ R turns and $k_v$ L turns. For an admissible directed edge $u\to v$, let $f(u,v)$ be its traversal multiplicity in one quotient period.

There is a local parity lemma. At a vertical-arrival cell $v$, let $I_N=f(v+(0,1),v)$ and $E=f(v,v+(1,0))$. If $r_N,r_S$ count R turns arriving from north and south, then

\[
E=(I_N-r_N)+r_S=I_N+k_v-2r_N,
\qquad \boxed{E\equiv I_N+k_v\pmod2.}
\]

At a horizontal-arrival cell, if $I_W=f(v-(1,0),v)$ and $O_N=f(v,v+(0,1))$, the rotated calculation gives

\[
\boxed{O_N\equiv I_W+k_v\pmod2.}
\]

The top boundary multiplicities are uniform. A top-row vertical-arrival cell receives all $2k_v$ arrivals from below and sends $k_v$ departures each east and west. A top-row horizontal-arrival cell cannot depart north, so it receives $k_v$ arrivals from each horizontal side. Hence the horizontal edge multiplicity agrees with $k_v$ at both endpoints; going around the cylinder shows that every top $k_v$ equals one integer $T>0$, and every top vertical edge has multiplicity $2T$. Similarly the bottom row has a uniform $B>0$, its vertical edges have multiplicity $2B$, and both extreme rows have zero signed horizontal displacement.

**Height three is impossible for every $L$.** Number the rows $0,1,2$. The extreme rows have the same HV type. Each middle cell has $2(B+T)$ visits; put $U=B+T$. Label the middle vertical-arrival cells cyclically by $v_j$, let $h_j$ be the horizontal-arrival cell immediately east of $v_j$, and put $A_j=f(v_j,h_j)$. The westward flow out of $v_j$ is $2U-A_j$. Flow balance at $h_j$ gives

\[
A_j+(2U-A_{j+1})=2U,
\]

so every $A_j$ equals one value $A$. The middle row's signed displacement is

\[
D_1=\frac L2[A-(2U-A)]=L(A-U).
\]

At a middle vertical-arrival cell, the north-arrival multiplicity is $2T$ or $2B$, hence even. The local parity lemma gives $A\equiv U\pmod2$. Thus $D_1$ is divisible by $2L$. The extreme rows contribute zero, contradicting total lifted displacement $L$ (or $-L$ after reflection).

**Height four is impossible when $L=4$.** Number rows $0,1,2,3$ and take vertical-arrival cells to have $x+y$ even. Let the middle-cut flow in column $x\pmod4$ be $2c_x$. Evenness follows because a row-1 cell has total visits $2B+f_x$, and similarly in row 2. Middle-cut flow balance and the local parity lemma on the two interior rows give

\[
c_0+c_2=c_1+c_3,
\qquad
c_0\equiv c_1\equiv c_2\equiv c_3\pmod2.
\]

For full auditability, let $a$ be the east flow from $(1,1)$ to $(2,1)$. The four row-1 horizontal flows, obtained successively from vertex balance, are

\[
a,quad 2(B+c_1)-a,quad 2(B+c_2)-a,quad
a+2(c_3-c_2).
\]

Therefore

\[
D_1=4a-4B+2c_3-2c_1-4c_2.
\]

The local parity lemma at the vertical-arrival cell $(1,1)$ says $a\equiv B+c_1\pmod2$; substituting this and the balance equation yields

\[
D_1\equiv2(c_0-c_2)\pmod8.
\]

Likewise, if $b$ is the east flow from $(0,2)$ to $(1,2)$, the row-2 calculation gives

\[
D_2=4b-4T-2c_0+2c_2-4c_1,
\qquad
D_2\equiv2(c_3-c_1)\pmod8.
\]

The boundary rows contribute zero, so

\[
D\equiv2[(c_0-c_2)+(c_3-c_1)]
\equiv4(c_0-c_1)\equiv0\pmod8.
\]

This contradicts $D=\pm4$. Consequently every clean translator with drift magnitude four has footprint height at least five. Since every intermediate row is nonempty and hence contributes at least one quotient cell with two visits,

\[
N\ge 8L+2(h-4)
\]

for footprint height $h\ge5$ when $L=4$. In particular a period-40 candidate has $5\le h\le8$, and a period-48 candidate has $5\le h\le12$. These height bands are necessary conditions, not existence claims.

Combining P11, the already certified period-at-most-32 exclusion, and the period-40 computation recorded in Section 17 gives a substantially sharper nonzero-drift zero-growth statement:

\[
\boxed{
d\text{ is axis-aligned},\quad |d|\in4\mathbb Z_{>0},\quad
N\in8\mathbb Z,\quad N\ge8|d|,\quad N\ge48.
}
\]

The last inequality combines P11, the independent all-word exclusion through period 32, and the complete theorem-pruned zero-growth period-40 search recorded in Section 17. It is not obtained from the footprint bound alone.

**Later status.** P15 in Section 21 strictly supersedes this candidate bound: no nonzero-drift zero-growth clean translator exists at any height or period. The small-height algebra is retained because it shows the route by which the height-independent parity theorem was found.

There is also an exact debris-distance theorem. At period boundaries write

\[
b_n=b_*+ng,\qquad p_n=p_*+nd.
\]

Let $h_j$ be cumulative black-count change within one period, let $v_j$ be its $j$th step vector, and put $Q=\sum_jh_{j+1}v_j$. Summing P10 one period at a time gives

\[
J_{n+1}-J_n=-b_nd-Q,
\]

and therefore

\[
\boxed{J_n=J_0-n(b_*d+Q)-\frac{gd}{2}n(n-1).}
\]

If $g>0$ and $d\ne0$, and $R_n=\max_{z\in B_n}\|z-p_n\|$, then $\|J_n\|\le b_nR_n$ implies

\[
R_n\ge \frac{\|d\|}{2}n-O(1).
\]

So every growing periodic highway necessarily leaves black cells linearly far behind the ant. Its black centroid is

\[
\frac1{b_n}\sum_{z\in B_n}z=p_n-\frac n2d+O(1).
\]

This formally explains why a proof based on the entire black support fitting inside a bounded moving window cannot work for the standard highway.

### Exact standard-strand decomposition

For the normalized standard word, $p=0$, $q=N$, and $d=(-2,2)$. The 12 canonical strand bases are

\[
\begin{aligned}
S=\{&(-8,1),(-7,0),(-7,1),(-6,1),(-4,3),(-3,0),\\
&(-2,0),(-2,2),(-1,2),(-1,3),(-1,4),(0,3)\}.
\end{aligned}
\]

The moving widget is

\[
\begin{aligned}
A=\{&(-6,0),(-5,0),(-5,1),(-4,0),(-4,2),(-3,-1),\\
&(-3,2),(-2,-1),(-1,1),(0,1),(0,2)\},
\end{aligned}
\]

and the stationary cap is $C=\{(-2,1),(0,0)\}$. Exactly, for every $n\ge0$,

\[
B_n=C\;\dot\cup\;(A+nd)\;\dot\cup
\bigcup_{c\in S,\,0\le j<n}\{c+jd\},
\qquad |B_n|=13+12n.
\]

There are 21 signed-toggle translation orbits: 12 growing and 9 zero-sum. The strand profiles factor as

\[
S_x=(1+X^{-2})(X^{-6}+X^{-2}+X^{-1}+1),
\qquad
S_y=(1+Y^2)(1+Y+Y^2).
\]

Thus both $x$-parities and both $y$-parities receive six strands; $Q_x(1)=0$, $Q_y(1)=1$, and $|A|$ is odd. Finally $\sum_{c\in S}(c_x+c_y)=-22$, $a+b=0$, and $L_N(-2,2)=2$, so the strand-only congruence is $-22+2\equiv0\pmod4$.

## 14. P13 - no-corners theorem and strip corollary

Let $S$ be the set of cells visited infinitely often. In the HV-directed grid, incident arcs around a cell alternate incoming and outgoing.

**No-corners theorem.** No $v\in S$ has two adjacent neighbors outside $S$.

**Proof.** If two adjacent neighbors of $v$ are outside $S$, then after some time the corresponding incident edges are never used. Because incoming/outgoing arcs alternate, one of those dead arcs is incoming and one is outgoing. Every sufficiently late arrival at $v$ must then use the sole remaining incoming arc. The color at $v$ flips on every visit, so exits from that fixed incoming arc alternate between the two outgoing arcs. One is the supposedly dead outgoing arc, a contradiction. $\square$

This gives unboundedness: if a trajectory were confined to finitely many cells, its nonempty finite infinite-visit set would have a geometric corner.

It also gives a useful strip reduction. If nonempty $S$ lies in an axis-aligned strip of finite height, choose a topmost $v\in S$. Its north neighbor is outside $S$, so no-corners forces both east and west neighbors into $S$. Repeating the argument fills the entire bi-infinite horizontal row. Thus a bounded-width recurrence proof can be reduced further to excluding a recurrent full row. That exclusion remains open.

## 15. P14 - frozen-loop memory theorem and trichotomy

### Frozen routing and exact surgery

Let

\[
\mathcal A=\{((x,y),q):q\equiv x+y\pmod2\}
\]

be the normalized admissible directed states. For fixed finite $B$, define

\[
\rho_B(z,q)=\bigl(z+u_{q+\epsilon_B(z)},q+\epsilon_B(z)\bigr),
\]

where $\epsilon_B(z)=+1$ on white and $-1$ on black. This frozen routing is a permutation. The all-white permutation consists of four-cycles, and a finite $B$ performs finitely many successor swaps, so every affected cycle remains finite.

Let $a_t=(p_t,q_t)$, let $\bar a_t=(p_t,q_t+2)$ be the opposite incoming strand, and let $\Gamma_t$ and $\Lambda_t$ be their frozen cycles. If

\[
u=\rho_{B_t}(a_t),\qquad v=\rho_{B_t}(\bar a_t),
\]

then toggling $p_t$ changes only

\[
\rho_{B_{t+1}}(a_t)=v,
\qquad
\rho_{B_{t+1}}(\bar a_t)=u.
\]

This is a two-break on a permutation. If $\Gamma_t\ne\Lambda_t$, the cycles merge and the new active length is their sum. If they are equal, one cycle splits into two; their lengths sum to $|\Gamma_t|$, the active daughter contains the actual next state $u$, and the other daughter is *shed*. A shed inactive loop remains literally unchanged until a future merge reabsorbs it.

### Bounded-loop plus bounded-age theorem

Assume that eventually

1. $|\Gamma_t|\le L$; and
2. every non-pristine loop that is reabsorbed was most recently shed at most $A$ steps earlier.

Only finitely many non-pristine cycles can be ancestral, because $B_0$ is finite. Each is either never absorbed or loses its ancestral identity at its first absorption; any later shed daughter receives a timestamp. Choose $T$ after all ancestral absorptions that ever occur.

For $t\ge T$, form a packet containing the complete embedded rooted active cycle and every inactive loop shed within the last $A$ steps, with their ages, all translated so the ant is at the origin. At most one loop is shed per step, so there are at most $A+1$ stored loops. Every shed loop has length at most $L$ and was created within $A$ ant steps, so it lies within $\ell_1$ radius $A+L$ of the current ant. Hence only finitely many normalized packets exist.

The packet determines its successor. The opposite strand is on the active loop, on a stored loop, or on neither. In the last case it cannot be an ancestral loop after $T$, and it cannot be an old non-pristine shed loop without violating the age bound; therefore it is the canonical pristine white four-cycle. The successor-swap rule then updates the packet exactly.

A normalized packet repeats. Translation-equivariant determinism makes all later packets and turns periodic with a fixed displacement. Zero displacement would confine the ant to the finitely many positions of one period, contradicting P13. Therefore the displacement is nonzero.

**Trichotomy.** For every finite-support orbit, at least one holds:

1. active frozen-loop lengths are unbounded;
2. reabsorption delays of non-pristine shed loops are unbounded; or
3. the ant eventually follows a translating periodic word with nonzero drift.

The third outcome means *some* highway; it does not establish that its word is the standard 104-step word.

### What unbounded reabsorption delay means geometrically

If a loop is shed at time $s$ and reabsorbed at time $t$, it contains crossings at both $p_s$ and $p_t$ and is unchanged between them. Under the active-length bound,

\[
\|p_t-p_s\|_1\le L.
\]

Thus unbounded age requires arbitrarily long excursions whose endpoints return within $L$. If the excursion visits $d$ distinct cells, the published fixed-domain estimate gives $t-s\le2^d$, hence $d\ge\lceil\log_2(t-s)\rceil$. Even without that sharp estimate, the elementary state count $4d2^d$ gives the same logarithmic conclusion. Consequently the only bounded-loop obstruction is an explicit one: larger and larger area/radius excursions that return to increasingly old nearby loops.

This can be sharpened by Jordan separation. An inactive frozen loop is an embedded Jordan curve. Until it is reabsorbed, the active ant cannot cross between its two complementary faces: the first toggle at one of its crossings is exactly the merge that reabsorbs it. If the ant is left on the **bounded** side of a shed loop of length at most $L$, it is confined to at most $(L+3)^2$ cells up to a conservative embedding margin. The finite-state bound then gives an explicit finite delay bound. Therefore every unbounded-delay sequence under bounded active length must consist of **exterior-side** excursions around small stationary loops.

The exact active-length accounting over any interval is

\[
|\Gamma_t|-|\Gamma_s|
=\sum_{\text{merges }i}|\Lambda_i|
-\sum_{\text{splits }i}|\text{shed}_i|.
\]

Every sufficiently advanced coordinate-record event merges a pristine four-cycle, contributing $+4$. Bounded active length merely forces comparable loop length to be shed later; it does not make record edges permanently consume active perimeter.

The known charges cannot bound exterior marker memory. Two exact neutral families are:

1. the $2\times2$ black block, with zero row/column charges, black count four, mod-four coordinate sum zero, Tait statistics $(E,V,k,\beta)=(4,4,1,1)$, and affected loop lengths 4 and 12; and
2. $Q_{r,s}=\{(0,0),(r,0),(0,s),(r,s)\}$ for $r,s\ge4$ and $r+s$ even. It has the same zero charges and consists of four isolated Tait edges, with $(4,8,4,0)$ and four marker loops of length 8.

Arbitrarily many well-separated translates remain invisible to every additive charge listed above.

The marker mechanism itself occurs in a genuine two-step Langton segment. Start with $B=\{(1,0)\}$, $p=(0,0)$, $q=N$. The first R step adds $(0,0)$ and makes active length 12; the next L step removes $(1,0)$. At time 2, $B=\{(0,0)\}$, $p=(1,1)$, $q=N$: the ant is on a pristine four-cycle and the one-edge black component is an inactive non-pristine loop of length 8. What remains unproved is delaying its later reabsorption without ever allowing active length to grow.

At the level of planar Tait surgery alone, arbitrary delay is possible with active length at most 16: split a three-edge path at its middle bridge, move the active one-edge token along an arbitrarily long route by alternating adjacent bridge additions/removals, return, and reconnect the old one-edge marker. The first split is itself a legal Langton step. The missing fact is whether the forced subsequent root order and visit alternation can realize the entire prescribed toggle schedule. Thus Tait topology, Jordan separation, record bridges, and the charges are insufficient by themselves; a successful proof must exploit exact root evolution.

Failed subarguments now ruled out precisely:

- a shed loop need not enclose the ant;
- record edges can later be refunded into bounded debris by splits;
- noncrossing loops do not give finite memory because the unbounded face can have arbitrarily many holes;
- conserved charges do not bound charge-neutral remote markers; and
- a near-returning temporal path is not a fixed Jordan curve because every visit changes the smoothing.

### Exact witnesses against a naive local pumping proof

On the blank orbit, times 10 and 20 have the same complete rooted active four-cycle modulo translation, including heading and root parity. Their partner lengths are respectively 28 and 4, so the next active lengths are 32 and 8. Even active loop plus current partner is not enough: at times 2 and 66 those two normalized loops agree, but after their common merge the following partner lengths are 4 and 12. Hidden external connectivity is therefore genuine state memory.

This disproves only the naive Markov argument. It does **not** prove or disprove the bare implication "bounded active length implies highway"; whether bounded length forces bounded reabsorption age remains open.

## 16. Further exact Tait results and monotonicity no-go theorems

### Oriented boundary count

For a finite Tait graph with $V$ incident vertices, $E$ edges, $k$ components, and cycle rank $\beta$, the affected frozen loops have total length $4V$. Exactly $k$ are outer boundary loops with rotation $+1$, and exactly $\beta$ are inner boundary loops with rotation $-1$. Therefore

\[
\#\text{affected loops}=k+\beta,
\qquad
\text{signed rotation sum}=k-\beta=V-E.
\]

This is the oriented regular-neighborhood form of P6.

### No coloring-only universal monotone

Let $\Phi(B)$ depend only on the finite coloring and be translation-invariant. If the ant starts at the origin on a white cell, one step realizes $B\to B\cup\{0\}$; starting from the same $B\cup\{0\}$ realizes the reverse toggle. Universal nondecrease would require both inequalities, hence equality under toggling the origin. Translation invariance gives equality under toggling any cell, so $\Phi$ is constant on all finite colorings. A successful monotone must include ant state, frontier, or history.

### No affine monotone from $(E,V,k,\beta)$

Ordinary ant steps realize both signs of the four independent change vectors

\[
(1,2,1,0),\quad(1,1,0,0),\quad(1,0,0,1),\quad(1,0,-1,0).
\]

For complete auditability, positive witnesses $(B,p,q)$ are respectively

\[
\begin{array}{c|c|c}
B&p&q\\ \hline
\varnothing&(-1,-1)&N\\
\{(-1,-1)\}&(-1,0)&E\\
\{(-1,0),(0,-1),(-1,-1)\}&(0,0)&N\\
\{(-1,1),(-1,-1)\}&(-1,0)&E
\end{array}
\]

and negative witnesses are obtained from the exact states listed in `langton_invariant_audit_2026-07-14.json`. Solving for an affine functional that annihilates all four vectors gives only a multiple of

\[
E-V+k-\beta=0,
\]

which is an identity. Hence there is no nonconstant affine Tait-statistic monotone.

### Active-loop length has unbounded one-step jumps of both signs

Take the boundary cycle of an $m\times n$ rectangle in the Tait lattice, with $N=2(m+n)$ boundary vertices, and delete one edge. The resulting path has one affected frozen loop of length $4N$. Adding the missing edge produces an outer loop of length $2N+4$ and an inner loop of length $2N-4$. Put the ant on the approach that follows the new inner loop: one valid R step changes active length from $4N$ to $2N-4$, a drop of $2N+4$. The reverse valid L step removes the edge and produces a rise of $2N+4$. Therefore active-loop length is not merely nonmonotone; its one-step increases and decreases are unbounded over finite initial states.

## 17. Exact computations in this continuation

### Clean moment-spectrum enumeration

Using Step 3b, I enumerated all $2^{19}=524,288$ ordered compositions for $N=40$ and all $2^{23}=8,388,608$ for $N=48$, for each of the four possible starting residues. The shift equation solves the otherwise unbounded lowest count $a$ exactly; there is no cutoff in $a$. The exact survivors with zero moment and axis drift of magnitude four are

\[
\begin{array}{c|r|r|r|r|r|r}
N&d=(4,0)&d=(-4,0)&d=(0,-4)&d=(0,4)&\text{total}&
\max a\;/\;\max(a+\ell)\\ \hline
40&48&104&138&72&362&6/18\\
48&859&1375&1526&947&4707&11/25
\end{array}
\]

Here $a$ is the minimum black count reached and $a+\ell$ the maximum. Directionwise maxima $(\max a,\max(a+\ell))$ are, for $N=40$, $(3,15),(5,14),(4,16),(6,18)$ in the table's drift order, and for $N=48$, $(11,23),(9,25),(8,20),(7,19)$. Thus every period-48 clean candidate has a phase with at most 11 black cells and never has more than 25. These are necessary count-spectrum bounds, not realizability claims.

The composition totals were asserted internally for every residue. The $N=48$ direction counts were reproduced by an independent aggregated integer dynamic program. The user-facing enumerator and compact JSON record are listed in the final artifact audit.

### Invariant regression

Command:

```powershell
python outputs\langton_research.py audit-invariants `
  --samples 1000 --sample-steps 200 --seed 20260714 `
  --output outputs\langton_invariant_audit_2026-07-14.json
```

Result: all 200,000 transitions passed all six listed invariant/path checks. The output also records the period-16 moment-sharpness counterexample and all eight exact Tait change witnesses.

### Blank frozen-loop diagnostic

Command:

```powershell
python outputs\langton_research.py loop-diagnostics `
  --steps 20000 --initial blank `
  --checkpoints 1000 5000 9977 20000 `
  --output outputs\langton_loop_diagnostics_blank_2026-07-14.json
```

Exact cumulative maxima:

\[
\begin{array}{r|r|r|r}
\text{steps}&\max|\Gamma|&\max\text{ non-pristine delay}&\max\text{ any tracked delay}\\ \hline
1000&268&380&380\\
5000&776&2839&2839\\
9977&1388&4414&4477\\
20000&1388&4414&4477
\end{array}
\]

There were 9,126 splits and 10,874 merges. These maxima remaining unchanged after highway onset is evidence about this one orbit, not a proof of a universal bound.

### Immediate certified-gateway diagnostic

Command:

```powershell
python outputs\langton_research.py loop-diagnostics `
  --steps 20800 --initial immediate-highway `
  --checkpoints 208 312 1040 20800 `
  --output outputs\langton_loop_diagnostics_gateway_2026-07-14.json
```

The maximum active length was 152 and maximum reabsorption delay was 90. Two ancestral non-pristine intakes occurred at events 1 and 6. The maxima were unchanged through 200 periods. The previously proved gateway induction, not this finite run, is what certifies the trajectory indefinitely.

### Standard strand extraction

Command:

```powershell
python outputs\langton_research.py analyze-periodic-trace `
  --standard `
  --output outputs\langton_standard_strands_2026-07-14.json
```

The normalized word has drift $(-2,2)$, growth 12, 22 phase translation classes, and 32 cells with nonzero signed one-period change. Those 32 changed cells lie on 21 drift orbits: 12 growing and 9 zero-sum. The output records every phase class and signed change. The explicit $C,A,S$ normal form in Section 13 was then checked at boundaries $n=1,\ldots,19$; the one-period identity plus the gateway induction proves it for all $n$, so the 19 checks were diagnostic only.

### Specialized zero-growth search mode

The exact word search now accepts `--exact-period --growth 0` and prunes prefixes whose remaining R/L balance cannot reach zero. A complete normalized period-24 baseline checked 506,082 legal-prefix nodes and found no word in 2.12 seconds:

```powershell
python outputs\langton_research.py search-highway-words `
  --max-period 24 --exact-period --growth 0 --prefix R `
  --node-cap 1000000000 --output work\zero_growth_p24.json
```

This result is already subsumed by the stronger all-word exclusion through period 32; its purpose was to verify the new search mode. An unsharded period-32 timing run was terminated by a 124-second command limit before producing a complete result. It is not counted as an exclusion.

### Complete nonzero-drift zero-growth period-40 exclusion

After proving the clean-packet footprint bound, I added the opt-in `--proved-clean-pruning` mode. At period 40 the only possible drifts are $(\pm4,0)$ and $(0,\pm4)$. During depth-first search it also tracks the parity of every candidate drift-translation class; every such class must end even. A representative 12-symbol prefix fell from 4,020,876 nodes and 66.98 seconds without these theorem prunes to 75,200 nodes and 0.42 seconds with them, with zero hits in both runs.

As an implementation cross-check, the theorem-pruned period-32 search completed 512 prefix shards and 650,659 nodes with zero hits, agreeing with the earlier independent unpruned search that excluded **all** periodic words through period 32.

The complete normalized search used all $2^{11}=2,048$ length-12 prefixes beginning with R. Beginning with R is exhaustive because a zero-growth periodic word contains R: shift forward to a later R phase of the actual orbit, whose state still has finite support, and rotate its heading back to north. No backward finite-support assumption is used. Exact aggregate result:

\[
\begin{array}{l|r}
\text{prefix shards}&2048\\
\text{locally valid prefix shards}&650\\
\text{legal-prefix nodes}&16,837,779\\
\text{complete shards}&2048\\
\text{certified highways found}&0\\
\text{10-worker wall time}&50.45\text{ s}
\end{array}
\]

Every shard reported `search_complete: true`; no node cap was reached. The aggregate computation record is `langton_zero_growth_p40_complete_2026-07-14.json`. It stores exhaustive shard summaries rather than a replayable proof tree. Conditional on the correctness of P3, the clean-packet/pruning proofs, the implementation, and the recorded completed execution, this is a complete computer-assisted exclusion of **nonzero-drift**, zero-growth, finite-support repeating traces of length exactly 40 (and therefore of least period 40), not a finite-time orbit simulation and not an exclusion of positive-growth period-40 highways. Drift-zero repeating traces are outside the program's search domain but are independently impossible by P13.

There is a further exact cyclic normalization. Start the closed relative black-count walk at one of its minima. Its first turn is R and every prefix balance is nonnegative. Every zero-growth periodic trace has such a phase, the state there still has finite support, and rotating the heading back to north preserves the problem. Adding this Dyck-path prune produced a third complete period-40 run with the current source-hashed runner:

\[
\begin{array}{l|r}
\text{prefix ranks}&2048\text{ (all sequential and unique)}\\
\text{normalized valid prefixes}&342\\
\text{legal-prefix nodes}&5,610,368\\
\text{maximum nodes in one shard}&47,934\\
\text{complete shards}&2048\\
\text{certified highways found}&0\\
\text{10-worker wall time}&15.29\text{ s}
\end{array}
\]

The compact source/hash audit is `langton_zero_growth_p40_dyck_audit_2026-07-14.json`. The earlier 16,837,779-node full-shard record remains useful as an independent superset search that did not rely on the minimum-phase prune.

### Period-48 timing attempt and cluster handoff

A representative length-14 period-48 shard completed 396,910 nodes in 2.35 seconds, but several highly unbalanced shards ran for about six CPU-minutes without completing. I terminated the local aggregate run and make **no period-48 exclusion claim**. The user-facing `run_zero_growth_cluster.py` now writes each completed prefix to an independent checkpoint before aggregation, so a larger cluster can resume safely and a partial run cannot be mistaken for a theorem.

After hardening the runner and strengthening the footprint bound, I reran the four length-16 children of that representative prefix (ranks 25,008 through 25,011). Three prefixes were locally valid; together they visited 396,907 nodes in 1.89 wall seconds on four workers and found zero hits. The three-node difference from the length-14 run is exactly the duplicated prefix-tree interior removed by deeper sharding. This is a runner/reproducibility check over 4 of 32,768 period-48 ranks, not an exclusion.

With the later minimum-black-count normalization active, ranks 12,496 through 12,511 give a current-code benchmark: 11 of 16 prefixes were normalized-valid, all 16 shards completed, 1,108,925 nodes were visited in 2.53 wall seconds on 10 workers, and no hit was found. This deliberately sampled descendants of a heavy period-40 prefix, but it is still only 16 of 32,768 ranks; no extrapolation is a proof and no period-48 exclusion is claimed.

## 18. Primary-literature audit and precise applicability

1. [Rechtman and Rechtman, *Equivalence of Deterministic Walks on Regular Lattices on the Plane*](https://arxiv.org/abs/1603.08269) prove an exact rotator/mirror conjugacy. A finite perturbation of uniform Langton rotators becomes a finite perturbation of a **checkerboard** mirror field, not a uniform mirror field. Their eventual-highway language near a simulation figure is not a universal proof.
2. [Gale, Propp, Sutherland, and Troubetzkoy, *Further Travels with My Ant*](https://arxiv.org/abs/math/9501233) give the Truchet-contour antecedent of the loop formulation and a Jordan-separation return theorem for certain generalized even-run ants. Ordinary LR Langton flips on every visit and can leave its principal contour on the second visit, so that theorem does not apply here.
3. [Gajardo, Moreira, and Goles, *Complexity of Langton's Ant*](https://arxiv.org/abs/nlin/0306022) records the no-corners theorem; [Etse, *How Long Can the Escaping Ant Be Confined?*](https://arxiv.org/abs/2606.26677) gives a recent detailed proof and the sharp $2^d$ finite-domain estimate.
4. Rotor-router finite-perturbation theorems do not transfer. In a rotor walk the next absolute exit at a vertex follows a fixed cyclic schedule independent of arrival direction. At a Langton H- or V-cell, the absolute exit depends on both its bit and the incoming direction. The mirror conjugacy does not remove this dependence.
5. [Webb and Cohen](https://arxiv.org/abs/1404.3629) prove genuine local-to-global admissibility and blocking theorems for a honeycomb flipping-scatterer model. They are a useful proof template but do not transfer to the square lattice.
6. I found no primary paper proving eventual highway behavior for every finite perturbation. I also found no prior Langton-ant paper using the Tait-graph terminology; the published antecedent is the Truchet-loop picture. The loop-count formula itself is standard plane ribbon-graph Euler topology.

## 19. Updated exact gap and next proof attempts

The work now separates the universal conjecture into three genuinely different obligations:

1. **Entrance/global geometry:** eliminate unbounded active-loop growth and unbounded old-loop reabsorption, or prove that either behavior still forces a highway. P14 identifies the exact memory mechanism rather than calling it vaguely "the interior."
2. **Finite classification reduction:** derive an a priori bound or finite/effective enumeration of the possible periods and strand skeletons. P3 decides each proposed word, but the candidate set is still infinite.
3. **Standardization:** eliminate every remaining nonstandard positive-growth candidate and identify the 104-step word. Current exact exclusions cover all finite-support periodic highways of period at most 40 and Hamming radius four around the standard word. P15 eliminates zero-growth traces at every period, but it does not classify positive-growth words above 40.

The highest-value next mathematical target is:

> Prove that a bounded active loop cannot make arbitrarily large **exterior-side** excursions and then reabsorb an old bounded marker loop. Bounded-side reabsorptions are now already controlled.

Sections 21--24 sharpen this target further: zero-growth recurrence is impossible, bounded cell-return gaps already force a positive-growth highway, and the unresolved exterior mechanism can be represented by long-lived detached islands or by persistent holes undergoing unboundedly many bridge dock/undock changes.

The highest-value computational targets are:

- use maximum active-loop length and maximum reabsorption delay as adversarial-search fitness functions;
- add the row/column and mod-four charges as exact pruning conditions in searches for translating widgets;
- enumerate signed translation-orbit strand patterns before enumerating raw turn words;
- retire the checkpointed zero-growth period-48 search as a proof target, because P15 excludes that entire class analytically, and redirect computation toward positive-growth strand skeletons;
- complete the remaining 4,095 distance-six Hamming shards; and
- run a complete exact centered $4\times4$ seed search with certificate checking and no unresolved time-capped cases.

None of these finite computations alone proves the universal conjecture. A successful final proof still needs a theorem that reduces arbitrary finite support and unbounded time to a finite set of certified behaviors.

## 20. Reproducibility and consistency audit at the preceding checkpoint

This was the exact audit at the end of the preceding checkpoint. Section 21 records later mathematics; the source hashes below still refer specifically to the search programs and runs named there.

1. `python -m py_compile` succeeded for `langton_research.py`, `run_zero_growth_cluster.py`, and `moment_spectrum_enumerator.py`.
2. Every user-facing JSON artifact parsed successfully. No Python worker process remained alive after the completed or deliberately terminated searches.
3. The invariant regression was regenerated with seed 20,260,714 on 1,000 random finite states for 200 steps each. All 200,000 transitions passed the six listed checks, including the new quadratic charge. The regenerated parsed content agrees with `langton_invariant_audit_2026-07-14.json`.
4. The standard trace analysis was regenerated: period 104, drift $(-2,2)$, 12 growing strands, valid 13-cell finite seed, and valid canonical decomposition. The blank certificate regenerated onset 9,977, period 104, and all four rotations.
5. The user-facing moment-spectrum program re-enumerated all $2^{19}$ and $2^{23}$ ordered compositions separately in each of four starting residues. It reproduced the saved JSON content: 362 period-40 and 4,707 period-48 profiles, with every internal composition-total and marginal assertion passing.
6. The original period-40 full-shard record contains exactly the 2,048 unique sequential ranks 0 through 2,047; every stored prefix matches its rank; every shard is complete; the recomputed node sum is 16,837,779; and the recomputed hit sum is zero.
7. The current minimum-phase period-40 rerun also contains all 2,048 sequential ranks and is complete. Its recomputed node sum is 5,610,368, maximum shard size is 47,934 (below the $10^9$ cap), and its hit sum is zero. Its embedded hashes exactly match the final search engine and runner:

   ```text
   engine b395ed3aac53bb9f43aea375ffd7257cd81ec3df5404df098783ed0656c4bcfc
   runner 68d94db220090b62cdb70228c15b11925ea69115d04c4fbebf2523855dc68034
   ```

8. The current theorem-pruned/minimum-phase period-32 cross-check completed all 512 ranks, visited 245,883 sharded nodes, and found zero hits. This agrees with both the earlier 650,659-node theorem-pruned run and the independent unpruned all-word exclusion through period 32; the node differences come from stronger normalization and duplicated prefix-tree interiors, not omitted rank intervals.
9. A partial-run/resume smoke test correctly labeled the output `Partial`, reported `full_search_complete: false`, and on rerun loaded only checkpoints whose prefix, completion flag, settings, schema, engine hash, and runner hash all matched.
10. The period-48 *computer search* is partial: 16 of 32,768 ranks in the current benchmark. It was not counted as a computational exclusion. The later analytic P15 excludes zero growth at period 48 for a completely different, period-independent reason.

The SHA-256 manifest is supplied separately as `artifact_hashes_2026-07-14.json`. Hashes authenticate file identity, not mathematical truth; the proof dependencies and computer-assisted qualifications above remain essential.

## 21. Continued universal-proof attack: the even-winding theorem

### 21.1 Why the low-height flow argument was revisited

The height-three and height-four calculations in Section 13 suggested, but did not prove, that a clean translating packet might be obstructed at every height. I therefore replaced the row-by-row formulas with exact edge multiplicities on the whole translation cylinder. The first exploratory integer-flow model enforced every aggregate arrival/turn count but not chronological realizability. It found a two-winding height-three circulation and found no one-winding circulation at the small tested heights. This computation was used only to locate the invariant; none of the theorem below depends on mixed-integer solver output.

The exact proof was then audited independently twice. Both audits separately checked the phase-to-lift correspondence, footprint gaps, the two HV cell types, finite vertical support, and the seam-intersection calculation.

### 21.2 Clean translator setup and the quotient visit lemma

Assume for contradiction that a finite state is a clean translator:

\[
(A,p,q)\longmapsto(A+d,p+d,q)
\]

in one word of length $N$, where $A$ is finite and $d\ne0$. P11 makes $d$ axis-aligned with coordinate divisible by four. After rotation and reflection write $d=(L,0)$ with $L\in4\mathbb Z_{>0}$. If $A_j,p_j,q_j$ denote the phase-$j$ state during one period, reversibility and translation covariance give

\[
A_{nN+j}=A_j+nd,
\qquad p_{nN+j}=p_j+nd
\]

for every $n\in\mathbb Z$. Quotient the full trace by translation through $d$ to obtain a closed walk on

\[
C_L=(\mathbb Z/L\mathbb Z)\times\mathbb Z.
\]

The checkerboard HV type is well defined because $L$ is even.

Fix a quotient vertex $v$ and a physical representative $z$. Each phase $j$ whose position lies in $v$ has a unique translation level $m_j$ with $p_j=z+m_jd$, and the occurrence of phase $j$ in period $-m_j$ visits $z$. Conversely every all-time visit to $z$ arises uniquely this way. Thus the number of visits to $v$ in one quotient period equals the total number of visits to $z$ over the bi-infinite translated orbit.

At each fixed phase the black pattern is a finite translate. Consequently $z$ is white sufficiently far in both temporal directions. Its encountered colors alternate, so its turn sequence begins with R, ends with L, and contains equally many of each. Therefore every quotient vertex $v$ has

\[
n_v=2k_v
\]

visits, exactly $k_v$ R turns and $k_v$ L turns. This remains true when $k_v=0$; no rectangular-footprint or no-gap assumption is being made.

### 21.3 Edge multiplicities and parity propagation

For every undirected horizontal or vertical cylinder edge, let its multiplicity be the number of traversals by the projected one-period trace. P1 orients each admissible edge uniquely: at a vertical-arrival cell the vertical edges are incoming and horizontal edges outgoing, while at a horizontal-arrival cell the roles are reversed.

At a vertex $v=(x,y)$, one pair of incident edges accounts for all arrivals and the other for all departures. Hence

\[
H_{v,-}+H_{v,+}=V_{v,-}+V_{v,+}=2k_v, \tag{21.1}
\]

where $H_{v,-},H_{v,+}$ are the west/east horizontal edge multiplicities and $V_{v,-},V_{v,+}$ the south/north vertical multiplicities.

Reducing the horizontal equality modulo two shows that the parities of consecutive horizontal edges agree. Therefore every row $y$ has one well-defined horizontal-edge parity

\[
h_y\in\mathbb F_2.
\]

The same argument propagates vertical-edge parity up each column. The projected trace has finite vertical support, so an edge sufficiently far below or above it has multiplicity zero. It follows that **every vertical edge multiplicity is even**. Write

\[
V_e=2G_e,
\qquad G_e\in\mathbb Z_{\ge0}. \tag{21.2}
\]

Now use the local parity lemma from Section 13. At a vertical-arrival cell,

\[
E\equiv I_N+k_v\pmod2.
\]

Here $E$ has parity $h_y$ and the vertical input $I_N$ is even, so $k_v\equiv h_y$. At a horizontal-arrival cell,

\[
O_N\equiv I_W+k_v\pmod2.
\]

Here $O_N$ is even and $I_W$ has parity $h_y$, giving the same conclusion. Thus, at both cell types,

\[
k_v\equiv h_y\pmod2. \tag{21.3}
\]

Dividing the vertical equality in (21.1) by two and using (21.2) gives the exact identity

\[
k_{x,y}=G_{x,y-1/2}+G_{x,y+1/2}. \tag{21.4}
\]

Combining (21.3) and (21.4), then fixing any column $x$ and summing over all rows, yields

\[
\begin{aligned}
\sum_y h_y
&\equiv\sum_y\left(G_{x,y-1/2}+G_{x,y+1/2}\right)\\
&\equiv0\pmod2. \tag{21.5}
\end{aligned}
\]

Only finitely many terms are nonzero, every interior half-edge appears twice, and the two exterior terms vanish.

### 21.4 Homological contradiction

Cut the cylinder along a vertical seam between two adjacent columns. The algebraic winding number $w$ of the projected closed trace is the signed number of crossings of that seam. There is one horizontal seam edge in each row, and its multiplicity has parity $h_y$. Signs disappear modulo two, so (21.5) gives

\[
w\equiv\sum_yh_y\equiv0\pmod2. \tag{21.6}
\]

But the lift of this closed trace starts at $p$ and ends at $p+(L,0)$. It therefore winds exactly once around $C_L$, so $w=1$, contradicting (21.6). Reflection gives the same contradiction for $(-L,0)$, and rotation handles vertical drift.

This proves:

\[
\boxed{\text{No nonzero clean finite Langton-ant translator exists.}} \tag{P15}
\]

The theorem is stronger than the earlier height bounds and is independent of the period. The two-winding aggregate circulation found during exploration is consistent with the theorem: it demonstrates why the conclusion is specifically an even-winding obstruction. It is not itself asserted to be a chronological Langton orbit.

### 21.5 Elimination of every zero-growth periodic highway

P12 proves that any nonzero-drift repeating trace with zero net black growth eventually separates into finite stationary debris and a finite moving packet. After the debris no longer meets any phase footprint, deleting it gives a clean translator. P15 makes that impossible.

A repeating trace with zero drift keeps the ant on the finitely many positions of one period and is impossible by P13. Negative net black growth cannot repeat forever because the black count is nonnegative. P4 says the growth of a heading-resetting period is a multiple of four. Therefore every finite-support eventually translating periodic trajectory must satisfy

\[
\boxed{g\in4\mathbb Z_{>0}.} \tag{21.7}
\]

In particular, every genuine highway must continually create a black wake. The complete period-40 zero-growth search and the partial period-48 work are now mathematically unnecessary for exclusion; they remain useful independent checks of the trace criterion and implementation.

This is a substantial reduction, but it is not the universal highway theorem. The ordinary 104-step highway has growth $12$ and is fully compatible with (21.7). The two principal gaps remain:

1. prove that every finite initial state enters some translating periodic regime, despite possible unbounded active loops or arbitrarily old exterior-side loop reabsorptions; and
2. prove that every positive-growth periodic trace admitted by finite support is the standard period-104 trace up to symmetry and phase.

### 21.6 Precise continuation log

1. I formulated an integer aggregate-flow model with four arrival/turn counters per cylinder vertex. It enforces edge compatibility, boundary zero-flow, equal local R/L totals, and prescribed winding, but deliberately does not claim chronological realizability or connected Euler support.
2. The model found an exact height-three, circumference-four circulation with 32 total visits and horizontal lift displacement eight. Its winding is two. This falsifies any proposed claim that the aggregate equations force zero winding, while remaining consistent with even winding.
3. The same model found no one-winding solution at heights three through six before the algebraic proof was found. Those solver outcomes are diagnostic only and are not cited as proof.
4. The decisive observation was to propagate edge multiplicities modulo two first, then divide the already-proved-even vertical multiplicities by two. Summing those half-flows vertically produces (21.5) with no height assumption.
5. Two independent audits reconstructed the quotient-visit lemma and the seam argument rather than merely checking the displayed algebra. Neither found a gap. The proof above exposes every assumption used: finite packet, exact translated recurrence, restored heading, axis-aligned even drift from P11, reversibility, and finite vertical support.
6. I searched the primary literature specifically for an original-rule zero-growth or nonstandard periodic translator that would contradict the theorem and found none. Generalized-ant papers exhibit many other highways, but their multi-state turn rules do not satisfy the binary alternating-visit premise used here.

No claim beyond P15 and its stated corollaries is inferred from the exploratory solver runs.

## 22. Continued periodic-trace attack: every drift residue carries wake strands

P15 says a periodic highway must grow, but by itself gives only $g\in4\mathbb Z_{>0}$. The even-winding calculation can be localized to one residue column and gives a quantitative relation between drift and growth.

### 22.1 Odd stabilized classes

Let an exact repeating trace have restored heading, drift

\[
d=(a,b)\ne0,
\]

and one-period word $w$. At a quotient vertex $v\in\mathbb Z^2/\langle d\rangle$, P3 gives a stabilized visit word that alternates and begins with R. Put

\[
\epsilon_v=#R_v-\#L_v\in\{0,1\},
\qquad k_v=\#L_v.
\]

Then the quotient visit count is

\[
n_v=2k_v+\epsilon_v,
\]

and the net black growth is exactly

\[
g=\#R-\#L=\sum_v\epsilon_v. \tag{22.1}
\]

Heading reset gives $g\equiv0\pmod4$. Also $N=\#R+\#L\equiv g\pmod2$, so $N$ is even. Since a length-$N$ square-lattice path changes checkerboard parity by $N$, $a+b$ is even. Translation through $d$ therefore preserves the HV type, so the directed checkerboard structure descends to the quotient even when the drift is diagonal.

### 22.2 Every nonzero horizontal residue is occupied

Assume first that $a\ne0$. Use quotient representatives with

\[
x\in\mathbb Z/|a|\mathbb Z.
\]

When a horizontal edge wraps between the last and first representative columns, its height is sheared by $b$; vertical edges remain within one residue column. This shear changes no parity sum below.

At every quotient vertex, the vertical incident multiplicities sum to $n_v$. Hence, modulo two,

\[
V_{v,-}+V_{v,+}\equiv\epsilon_v. \tag{22.2}
\]

Fixing an $x$ residue and summing (22.2) over all heights cancels every internal vertical edge twice. The projected trace is finite, so the exterior terms vanish. Therefore

\[
\sum_y\epsilon_{x,y}\equiv0\pmod2. \tag{22.3}
\]

The older Laurent charge already implied this evenness. The new point is that the sum cannot be zero as an integer.

Suppose, to the contrary, that one residue column $x$ contains no odd class, so $\epsilon_{x,y}=0$ for every $y$. Vertical-edge parity then propagates unchanged up the column by (22.2), and finite support forces it to be zero. Write every vertical multiplicity in that column as $2G$.

At every cell in this column, $n_v=2k_v$ and the local clean-flow formulas apply. At a vertical-arrival cell,

\[
E\equiv I_N+k_v\pmod2;
\]

at a horizontal-arrival cell,

\[
O_N\equiv I_W+k_v\pmod2.
\]

All vertical multiplicities are even. Together with the horizontal incidence sum $2k_v$, these identities show that **both** horizontal edges incident to $v$ have parity $k_v$. Exact vertical incidence gives

\[
k_{x,y}=G_{x,y-1/2}+G_{x,y+1/2}. \tag{22.4}
\]

Consequently the parity of the total horizontal multiplicity across either boundary seam of this residue column is

\[
\sum_y k_{x,y}
\equiv\sum_y\left(G_{x,y-1/2}+G_{x,y+1/2}\right)
\equiv0\pmod2. \tag{22.5}
\]

But the lifted one-period path goes from $p$ to $p+d$. Its algebraic crossing number through every fixed $x$-residue seam is $\operatorname{sgn}(a)$: as the lifted $x$ coordinate changes by $a$, it crosses each residue boundary net exactly once. Thus its unsigned seam-crossing count is odd, contradicting (22.5).

Every one of the $|a|$ residue columns therefore contains at least one odd class. Equation (22.3) makes its number of odd classes even, so it contains at least two. Summing over residues and using (22.1) gives

\[
g\ge2|a|. \tag{22.6}
\]

Rotating the argument by a quarter-turn, if $b\ne0$ then

\[
g\ge2|b|. \tag{22.7}
\]

Combining the two inequalities proves

\[
\boxed{g\ge2\max(|a|,|b|).} \tag{P16}
\]

Equivalently, in the bipartite multigraph whose vertices are drift-coordinate residues and whose edges are the $g$ solid wake strands, every residue vertex belonging to a nonzero coordinate has positive even degree. The Laurent charges supplied ``even''; winding supplies ``positive.''

### 22.3 Scope

For the standard highway, $d=(-2,2)$ and $g=12$, so P16 is satisfied with room to spare. For a hypothetical axis highway of drift magnitude four it improves $g\ge4$ to $g\ge8$. It does not identify the period-104 word, and abstract residue patterns can satisfy the bound without satisfying chronological cell alternation. This is a necessary condition, not a construction or classification.

The proof was independently audited in the axis case and then in the sheared fundamental-domain formulation. The audit checked heading/checkerboard parity, the wrap-edge shear, vertical boundary cancellation, both HV local formulas, and the fact that every residue seam has algebraic intersection $\pm1$ with a one-period lift.

The coefficient two is sharp at the aggregate-flow level. An exact circumference-two, height-three integer profile has winding one, $g=4=2|a|$, period count eight, two odd classes in each residue column, and valid local R/L allocations. Its positive flow decomposes into two transition circuits rather than one ant trace, so it is **not** a Langton highway or counterexample. A separate circumference-four model attains $g=8=2|a|$ with two odd classes per column. These profiles show that improving P16 from the same static incidence equations alone is impossible; a stronger bound would have to use chronological root connectivity or cell alternation across the single projected tour.

## 23. Completion deficits and a bounded-black-count reduction

### 23.1 Exact alternating-superword deficit

This lemma improves exact trace search and states precisely what information a partial translation class has already made unavoidable.

Let $s=s_1\cdots s_m$ be the symbols already present in one translation class, in their final relative order. Future phases may insert symbols anywhere but cannot change that order. To complete $s$ to an alternating word that begins with R and ends with L, the exact componentwise minimum numbers of inserted symbols are

\[
\boxed{
\begin{aligned}
\operatorname{need}_R(s)
&=\mathbf1_{s_1=L}+\#\{i:s_i=s_{i+1}=L\},\\
\operatorname{need}_L(s)
&=\#\{i:s_i=s_{i+1}=R\}+\mathbf1_{s_m=R}.
\end{aligned}} \tag{23.1}
\]

For the empty word both needs are zero. If odd final classes are allowed, so the completed alternating word may end with R, the last indicator in $\operatorname{need}_L$ is omitted.

**Proof.** An initial L requires an R before it. Every adjacent LL pair requires an R inserted between those two fixed symbols, and these gaps are disjoint. Similarly every RR pair requires an inserted L. Finally an alternating word that must end with L needs an L after a terminal R. These requirements prove the lower bounds. Inserting exactly the listed symbol in each listed gap and at the listed endpoints produces an alternating word beginning with R and ending with L, proving simultaneous attainability and exactness. $\square$

Summing (23.1) over all current translation classes gives separate necessary lower bounds on the future R and L symbols. A search branch is impossible as soon as either exceeds the corresponding number of symbols still available. This dominates the older parity-only count of odd classes.

An exhaustive abstract-word audit through length eight checked the insertion formula. Adding it to the already-normalized zero-growth diagnostic search changed no certificate result and reduced the explored node counts as follows:

\[
\begin{array}{c|r|r|r}
\text{search}&\text{old nodes}&\text{new nodes}&\text{hits}\\ \hline
N=32\text{ complete}&245{,}883&42{,}180&0\\
N=40\text{ complete}&5{,}610{,}368&404{,}518&0\\
N=48\text{ same 16-rank sample}&1{,}108{,}925&37{,}908&0
\end{array}
\]

These are implementation diagnostics, not new exclusion claims. P15 already makes further zero-growth enumeration unnecessary. The odd-ending version remains useful for future positive-growth word searches.

### 23.2 Proof of P17

Assume $|B_t|\le K$ for all $t$. In the Tait graph, at most $2K$ vertices are incident to black edges. Section 16's exact boundary accounting gives total affected frozen-loop length $4V\le8K$. An unaffected loop is a pristine four-cycle. Hence every active frozen loop has length at most

\[
L_K=\max(4,8K). \tag{23.2}
\]

Suppose also that the ages of all reabsorbed non-pristine shed loops were bounded. P14's bounded-loop plus bounded-age theorem would force the orbit eventually to follow a translating periodic word with nonzero drift. Since the total black count remains bounded, that word would have net growth $g=0$. P15 excludes every such trace. Therefore the age bound is impossible:

\[
\boxed{
\sup\{t-s:\text{a non-pristine loop shed at }s
\text{ is reabsorbed at }t\}=\infty.} \tag{P17}
\]

This does not prove that black count must become unbounded. It proves exactly what a bounded-black-count counterexample would have to do: preserve and later recover arbitrarily old exterior memory. The bounded-side Jordan argument in P14 says that an unbounded-delay subsequence must use exterior-side excursions.

## 24. Exterior-memory continuation: local returns and the corrected split taxonomy

This section records rigorous partial progress on the principal entrance gap. It does **not** prove that bounded active-loop length forces bounded reabsorption age.

Retain P14's notation: $a_t=(p_t,q_t)$ is the directed ant state, $\bar a_t=(p_t,q_t+2)$ the opposite strand, and $\Gamma_t,\Lambda_t$ their cycles in the frozen permutation $\rho_{B_t}$.

### 24.1 The partner loop is short too

Assume $|\Gamma_t|\le L$ for every $t\ge T$. Then $|\Lambda_t|\le L$ for every $t\ge T$. At a merge, successor-swap surgery gives

\[
|\Gamma_{t+1}|=|\Gamma_t|+|\Lambda_t|,
\]

so in fact $|\Lambda_t|\le L-|\Gamma_t|$. At a split, $\Lambda_t=\Gamma_t$ before the successor swap. This proves the claim.

Both frozen strands through the current cell, the merge/split decision, and the new rooted active daughter are therefore determined within $\ell_1$ radius $L$ of $p_t$. This is a one-step locality statement, not finite memory: as the ant moves, new boundary data enter that radius-$L$ window.

### 24.2 Proof of P19: short self-avoiding temporal factors

Suppose

\[
p_s,p_{s+1},\ldots,p_{s+n-1}
\]

are pairwise distinct and $s\ge T$. No current cell in this interval was toggled earlier in the interval. Induction therefore compares the live path with the single frozen configuration at time $s$:

\[
a_{s+i}=\rho_{B_s}^{,i}(a_s),
\qquad0\le i<n. \tag{24.1}
\]

These directed states occur consecutively on $\Gamma_s$. If $n>|\Gamma_s|$, a directed state, hence its position, repeats before the interval ends. Thus

\[
\boxed{n\le|\Gamma_s|\le L.} \tag{P19}
\]

Every block of $L+1$ consecutive visited positions contains a spatial repeat. This establishes a positive density of local returns, but it does not bound radius: a path can concatenate many short loops while migrating through new territory.

### 24.3 Proof of P18: only black-cell lifetimes need finite memory

Assume there are constants $A,T$ with this property: whenever $t\ge T$ is an R visit and $p_t$ is later visited again, its next visit occurs by time $t+A$. That next visit is necessarily L because the R visit left the cell black.

Only finitely many initially black cells exist. Increase $T$ beyond the first-visit time of every initially black cell that is ever visited. At a time $s\ge T+A$, normalize at the current ant and record its heading, the last $A$ relative positions in temporal order, and the turn observed at each.

If $p_s$ occurs in the record, its last occurrence determines its present color: it is black after an R visit and white after an L visit. If it does not occur, it must be white. Otherwise it would either be an as-yet unvisited initially black cell, contrary to the choice of $T$, or its last visit would have been an R visit more than $A$ steps ago, making the present visit a forbidden late next visit.

The finite normalized record therefore determines the next turn and next record exactly. Every stored relative position has $\ell_1$ norm at most $A$, so only finitely many records exist. A record repeats, and translation-equivariant determinism makes all later records and turns periodic with a fixed displacement $d$. If $d=0$, the ant is confined to the finitely many positions of one period, contradicting P13. P15 excludes zero growth, negative growth cannot persist, and P4 makes the growth a positive multiple of four. Thus

\[
\boxed{\text{bounded R-to-L black lifetimes imply an eventual positive-growth translating word.}} \tag{P18}
\]

This is strictly stronger than bounding every cell-return gap. Arbitrarily old L-to-R returns are harmless for finite memory because an L visit leaves the cell white, locally indistinguishable from a virgin cell after the finite initial exceptions have passed. Every non-highway orbit must therefore contain R visits whose cells remain black for arbitrarily long times before the next visit.

### 24.4 Correct four-case taxonomy of a Tait split

Use the rotation convention from Section 16: an outer regular-neighborhood boundary has rotation $+1$, and an inner boundary of a bounded complementary face has rotation $-1$. The face containing a bridge matters. In particular, the tempting statement that every removed bridge has an outer parent and two outer daughters is false.

\[
\begin{array}{c|c|c|c|c}
\text{turn}&\text{graph operation}&\text{face}&\text{parent}&\text{daughters}\\ \hline
R&\text{add cycle edge}&\text{unbounded}&+1&+1,-1\\
R&\text{add cycle edge}&\text{bounded}&-1&-1,-1\\
L&\text{remove bridge}&\text{unbounded}&+1&+1,+1\\
L&\text{remove bridge}&\text{bounded}&-1&-1,+1
\end{array} \tag{24.2}
\]

**Proof.** An R split increases cycle rank by one without changing component count, so it creates exactly one inner boundary. In the unbounded face, the outer boundary becomes an outer and an inner boundary. In a bounded face, one bounded face is divided into two, so one inner boundary becomes two inner boundaries.

An L split occurs exactly when the removed edge is a bridge. For this local surgery, retain either endpoint that becomes isolated as a singleton vertex disk; its outer boundary is precisely the corresponding pristine four-cycle. With these endpoint disks retained, cycle rank stays fixed and component count rises by one, so exactly one outer boundary is added. In the unbounded face, one outer boundary becomes two outer component boundaries. In a bounded face—for example, a tree attached inside a cycle—the old inner boundary persists for one component while the component detached inside the face acquires its own outer boundary. This convention also covers deletion of a leaf or of an isolated one-edge component. $\square$

The marker geometry follows:

- For R in the unbounded face, shedding the outer daughter and following the inner daughter places the ant on the bounded side of the shed curve. Shedding the inner daughter and following the outer one creates an exterior inner-hole marker.
- For R in a bounded face, the daughters bound the two subfaces of the old bounded face. They are exterior to one another, but initially remain within the old bounded face until a later merger changes that relation.
- For L in the unbounded face, a shed daughter is the outer boundary of a detached island and the active daughter lies on its exterior side.
- For L in a bounded face, the new $+1$ daughter is the outer boundary of the component detached inside the old face. If it is shed, it is an exterior island marker. If the inherited $-1$ daughter is shed while the ant follows the detached $+1$ component, the ant is on the bounded side of the shed inner curve.

Thus genuinely exterior memory comes from inner hole markers created by R splits and outer island markers created by bridge-removing L splits, with bounded-face variants included.

### 24.5 Strongest safe reduction and the remaining loophole

An inner hole marker cannot move arbitrarily far while the active loop remains the outer boundary of the same Tait component: that active Jordan curve encloses the marker, and length at most $L$ keeps the curve within $O(L)$ of it. Likewise, following an inner daughter after shedding a short outer shell is P14's already-controlled bounded-side case until that shell is reabsorbed.

A far excursion relative to a persistent hole therefore requires the boundary/component relation to change. Bridge deletion can detach the marker behind a new outer shell, but it is **not** proved that one such shell must itself have unbounded lifetime. A hole-bearing component may dock, detach behind a short-lived shell, redock, and detach again. The docking edge can alternate L/R exactly as cell alternation requires. An old hole may acquire unbounded total age through unboundedly many individually short dock/undock episodes.

At the level of loop identity and planar topology alone, the safe reduction is:

> Unbounded exterior memory must be realized either by long-lived detached outer islands, or by persistent inner-hole markers undergoing unboundedly many changes of active boundary/component relation. Repeated bridge dock/undock cycles are a concrete unresolved mechanism. Any never-absorbed ancestral large boundary remains a finite but nonlocal exceptional environment.

Planarity, rotation signs, $(E,V,k,\beta)$, Jordan separation, and local alternation do not bound the number of dock/undock cycles. The successor-seam argument immediately below adds the needed history-sensitive anchor: for a non-highway under bounded active-loop length, unboundedly many uniformly short dock/undock episodes are not enough; at least one uninterrupted inactive seam episode must itself become unbounded. Repeating a short rooted contour still does not determine the future because old data can enter through the moving radius-$L$ boundary.

### 24.6 Proof of P20: the persistent successor seam

Let $\rho_t=\rho_{B_t}$ and put

\[
u_t=\rho_t(a_t)=a_{t+1}.
\]

The toggle at $p_t$ exchanges exactly the successor values based at $a_t$ and $\bar a_t$. Hence

\[
\boxed{\rho_{t+1}(\bar a_t)=a_{t+1}.} \tag{24.3}
\]

No later toggle away from $p_t$ changes either successor based at that cell. Thus, until the next visit to $p_t$, the directed arc

\[
e_t:\bar a_t\longmapsto a_{t+1} \tag{24.4}
\]

persists verbatim. Call it the successor seam of the visit.

Assume active frozen loops are bounded by $L$, let $t$ be an R visit after that bound begins, and let $\tau>t$ be the next visit to $p_t$. For $t+1\le s\le\tau$, let $C_s$ be the frozen cycle containing $e_t$. Initially (24.3) puts $C_{t+1}$ on the active cycle. Inductively:

- if a toggle does not touch $C_s$, the cycle is unchanged;
- if $C_s$ is the partner, it merges into a new active cycle of length at most $L$; and
- if $C_s$ is active, a merge leaves it active and a split puts the seam into one daughter, whose length is at most the parent's.

Therefore

\[
|C_s|\le L \quad(t+1\le s\le\tau). \tag{24.5}
\]

Whenever $C_s$ is active, both the ant state and the fixed state $\bar a_t$ based at $p_t$ lie on it, so

\[
\|p_s-p_t\|_1\le L. \tag{24.6}
\]

An *inactive seam episode* begins when a split sheds the daughter containing $e_t$ and ends when that unchanged daughter is reabsorbed as a partner. Because the R visit leaves $p_t$ black, every such cycle is non-pristine until $\tau$.

Suppose each inactive seam episode in this lifetime has duration at most $D$. At the split starting such an episode the ant is within $L$ of $p_t$, and speed one keeps it within $L+D$ throughout the episode. During active episodes (24.6) gives the smaller radius $L$. Arbitrarily many dock/undock episodes therefore still confine the **entire** interval $[t,\tau]$ to

\[
B_{L+D}(p_t).
\]

This ball has

\[
M=1+2(L+D)(L+D+1)
\]

lattice cells. The exterior coloring is unchanged during the interval, while inside the ball there are at most $4M2^M$ ant-position, heading, and coloring states. If one repeated before the first return to $p_t$, the complete global state would repeat and the intervening segment—none of which visits $p_t$—would recur forever, contradicting the assumed return. Hence

\[
\boxed{\tau-t\le4M2^M+1.} \tag{24.7}
\]

Combining (24.7) with P18 gives two exact conclusions:

1. bounded active-loop length plus bounded non-pristine reabsorption age forces an eventual positive-growth translating word, providing a second proof of P14's finite-memory implication; and
2. under bounded active-loop length, unbounded R-to-L black lifetimes force the duration of a **single uninterrupted inactive episode** of a non-pristine successor-seam loop to be unbounded.

The second statement handles arbitrarily many dock/undock cycles: if every inactive episode were uniformly short, (24.7) would bound the total lifetime regardless of their number. The universal gap is now localized to excluding a short, anchored, non-pristine seam loop that remains inactive while the ant makes an arbitrarily long exterior excursion and later returns near its anchor to reabsorb it.

For reference, a single uninterrupted *active* seam episode also has an explicit bound. It stays in $B_L(p_t)$, which has $m_L=1+2L(L+1)$ cells; full-state repetition gives

\[
H(L)=4m_L2^{m_L}. \tag{24.8}
\]

Thus the unbounded duration in P20 must genuinely occur while the seam is inactive.

### 24.7 Proof of P21: a long black lifetime cannot be isolated

This lemma needs no active-loop hypothesis. Fix $A\ge1$, work after the finite initial-black exceptions used in P18, and set

\[
m_A=1+2A(A+1),
\qquad S_A=4(2m_A)^A,
\]

where $S_A$ is a loose upper bound on normalized length-$A$ history records. Define

\[
F(A)=2S_A^2+3S_A+1. \tag{24.9}
\]

Suppose an R visit at time $t$ leaves $x=p_t$ black and its next visit is the L visit at time $\tau$. If

\[
\tau-t>F(A), \tag{24.10}
\]

then some other cell has an R-to-L lifetime longer than $A$ whose **ending time** lies strictly between $t$ and $\tau$.

**Proof.** Assume otherwise. At every time $s$ with $t<s<\tau$, the normalized last-$A$ history determines the current turn. If the current cell appears in the record, its last turn determines its color. If it is absent but black, its preceding R visit and the present L visit form a lifetime longer than $A$ ending inside $(t,\tau)$, unless the cell is $x$; but $x$ is not visited in the open interval. Initial-black exceptions have already been passed. Thus every absent current cell is white, and the history record evolves autonomously until $x$ is reached.

If $\tau>t+S_A+1$, two records repeat at times

\[
t<s_1<s_2\le t+S_A+1.
\]

Put $P=s_2-s_1\le S_A$ and $d=p_{s_2}-p_{s_1}$. Until $x$ is reached, translation covariance gives

\[
p_{s_1+nP+j}=p_{s_1+j}+nd,
\qquad0\le j<P. \tag{24.11}
\]

The displacement $d$ is nonzero; otherwise this repeated segment, which contains no visit to $x$, would avoid $x$ forever. Write $\tau=s_1+nP+j$ with $0\le j<P$. Since $p_\tau=x$ and $\|d\|_1\ge1$,

\[
\begin{aligned}
n
&\le n\|d\|_1
=\|x-p_{s_1+j}\|_1\\
&\le\|x-p_{s_1}\|_1+j
\le2S_A+1.
\end{aligned}
\]

Consequently

\[
\tau-t
\le(S_A+1)+(2S_A+1)S_A+S_A
=F(A),
\]

contradicting (24.10). $\square$

P21 says unbounded black lifetimes occur in arbitrarily deep temporal clusters. It does **not** give laminar nesting: the secondary lifetime may begin before the primary one. This crossing phenomenon occurs immediately on the blank orbit—the lifetimes $[0,4]$ at $(0,0)$ and $[3,15]$ at $(0,-1)$ satisfy $0<3<4<15$. Any attempted infinite-descent proof must control crossing interval chains rather than silently treating them as nested.

## 25. New exact computation: positive growth through period 40 and a long exterior witness

### 25.1 Complete positive-growth periodic search

P15 retired the zero-growth search branch, so the exact word search was redirected to positive growth. Give R weight $+1$ and L weight $-1$. Every cyclic word with total growth $g>0$ can be shifted to a phase immediately after a global minimum of its cumulative walk. Every relative prefix balance is then nonnegative and its first symbol is R. Phase shift preserves finite support, and rotation restores the initial heading convention. This normalization is exhaustive.

The independent Java implementation `PositiveGrowthSearch.java` uses only proved necessary conditions:

1. nonnegative prefix balance after the cyclic-minimum normalization;
2. exact alternation on repeated physical cells within the partial period;
3. reachability of a final $g\in4\mathbb Z_{>0}$;
4. endpoint reachability together with P16, $g\ge2\|d\|_\infty$; and
5. at selected depths, the odd-ending version of the exact completion deficit (23.1).

Every surviving leaf independently reconstructs its drift-translation classes and applies P3 exactly. No finite-time pattern matching or heuristic score accepts a leaf.

The complete uncapped primary executions are:

\[
\begin{array}{c|r|r|r|r|r}
N&\text{prefix ranks}&\text{nodes}&\text{deficit prunes}&\text{P3 leaves}&\text{hits}\\ \hline
34&512&9{,}726{,}176&137{,}855&295{,}495&0\\
36&1{,}024&19{,}781{,}050&502{,}306&1{,}194{,}951&0\\
38&2{,}048&41{,}972{,}884&1{,}551{,}467&1{,}469{,}976&0\\
40&4{,}096&201{,}924{,}597&0&10{,}313{,}586&0
\end{array} \tag{25.1}
\]

Period 40 used the simpler no-deficit mode. Periods 34, 36, and 38 were also run completely with the deficit disabled; those independent supersets visited 12,587,153; 31,132,389; and 81,275,925 nodes and again found zero hits.

Implementation cross-checks were exact:

- independent Python enumeration and the Java program produced identical per-shard P16-admissible leaf counts at period 16 (233 total) and period 20 (1,110 total), with zero P3 hits;
- the period-20 total was independently regenerated again during this continuation;
- the cyclic-minimum rotation of the genuine standard period-104 word is accepted by both implementations with $g=12$ and Java drift $(2,-2)$; and
- every compact run record has complete consecutive ranks, aggregate counts equal to the sums of rank records, empty hit lists, no node cap, and the exact source hash

  ```text
  f2fadea8b323bf7bc817505e36b83146e4489ee5954d98dc1a87b52adb8dbf8d
  ```

Conditional on P3, P4, P16, the written pruning proofs, the implementation, and the completed executions, periods 34, 36, 38, and 40 have no positive-growth finite-support periodic trace. Odd periods cannot restore heading; the older complete search covered every period through 32; and P15 excludes zero growth at all periods. Therefore

\[
\boxed{\text{No finite-support periodic Langton highway has period }N\le40.} \tag{25.2}
\]

This is a bounded-period computer-assisted theorem, not a proof that every orbit becomes periodic.

### 25.2 Exact 23,273-step exterior-memory witness

The adversarial loop search now optimizes realized reabsorption age, not censored age of debris still inactive at the horizon. Every inactive daughter is keyed by its complete directed-state set and receives an age only if that exact unchanged cycle is later the merge partner.

A complete search of all 512 centered $3\times3$ masks through 6,000 steps found mask `0x115` as the finite-horizon champion, with a realized non-pristine age 5,029. More importantly, the previously certified latest-gateway mask

```text
#.#
#.#
#.#
```

(`0x16d`, with rows shown from low to high $y$) yields a much longer exact witness:

\[
\begin{array}{c|l}
\text{initial black cells}
&(-1,-1),(1,-1),(-1,0),(1,0),(-1,1),(1,1)\\
\text{shed step}&14{,}989\\
\text{shed loop length}&8\\
\text{shed position/heading}&(-5,8),\ W\\
\text{reabsorbed step}&38{,}262\\
\text{age}&23{,}273\\
\text{return endpoint distance}&3
\end{array} \tag{25.3}
\]

The event is an R split of a length-20 parent in a bounded complementary face. The parent, shed length-8 daughter, and live length-12 daughter all have rotation $-1$, exactly the second row of (24.2). The ant follows the other inner boundary and is on the exterior side of the shed inner marker. Before reabsorption it reaches Manhattan distance 68 from the shed position at step 28,325, then returns within distance three.

The optimized tool redundantly retraced the other post-split daughter at every step, and the independent reference diagnostic agreed on every compared field through step 38,263: maximum active length 3,128, age 23,273, 18,352 splits, 19,911 merges, and all tracked-loop counts. A 50,000-step extension raised maximum active length to 3,288 but not the age record.

This is a concrete finite realization of the exact exterior-side mechanism left open by P20. It is **not** evidence that the delay is unbounded and is not a counterexample: this same seed is already certified to enter the standard highway later. Its value is that any proposed proof claiming small exterior delays must confront an exact 23,273-step near-return around an unchanged eight-state loop.

## 26. Status audit at the end of this continuation

The universal conjecture is **not proved or disproved**. No numerical completion percentage is defensible: the remaining statements are qualitative unboundedness problems, and either could require a new invariant rather than a longer version of the present argument.

What is now rigorous on paper, independently of the searches, is:

1. **P15 (even winding):** a clean finite-support translating period cannot have zero growth. Hence there are no nontrivial zero-growth periodic highways at any period.
2. **P16 (wake-strand bound):** every clean translating word with drift $d=(a,b)$ and growth $g$ obeys
   $$g\ge 2\max(|a|,|b|),$$
   with a positive even number of wake strands in every drift residue met by the trace.
3. **P18 (bounded lifetime reduction):** a uniform bound on the lifetime of every black inactive R-to-L loop would force an eventually positive-growth translating word whenever the active loop length is bounded.
4. **P20 (persistent successor seam):** after a daughter is shed, its marked successor state is carried unchanged by the active boundary; bounded active length gives a bounded seam cycle, and uniformly bounded inactive episodes give a finite lifetime bound. Thus a bounded-loop nonhighway would have to contain an individual inactive, non-pristine seam episode of arbitrarily long duration.
5. **P21 (long-lifetime clustering):** sufficiently old inactive black loops force many temporally nearby interactions in an explicit bounded neighborhood. This gives a quantitative concentration lemma, but the associated time intervals can cross rather than nest, so it does not yet yield an infinite descent.

What is computer-assisted rather than purely deductive is:

1. complete exact exclusion of every finite-support periodic highway of period at most 40, combining P15 with exhaustive positive-growth enumeration; and
2. the exact finite exterior-memory witness (25.3), whose unchanged length-eight loop survives 23,273 steps before reabsorption.

The implementation audit at this checkpoint succeeded: all Python sources compile; `PositiveGrowthSearch.java` compiles; all compact JSON records parse; period-34, 36, 38, and 40 records are uncapped and have complete rank coverage; their aggregate counters equal the rank sums; all hit lists are empty; the recorded source hashes match the current sources; and the normalized genuine period-104 standard highway remains an accepted positive control with growth 12 and drift $(2,-2)$.

Two indispensable gaps remain:

- **Global orbit gap.** Prove that every finite seed either has unbounded active-loop length in a controllable way or cannot sustain arbitrarily long exterior-side inactive seam episodes. P20 identifies the second behavior exactly, but (25.3) shows that any uniform estimate will need substantially more geometry than a small local bound.
- **Periodic classification gap.** Prove, without an a priori period cutoff, that every positive-growth clean translating word is the standard period-104 highway (up to symmetry and phase), or exhibit another one. Enumeration through period 40 cannot settle this unbounded statement.

Accordingly, the honest assessment is: the zero-growth periodic branch is closed and the bounded-loop obstruction is sharply localized, but the work is **not close to a complete universal proof** in the sense of having only routine details left. The next decisive advance must control entrance geometry across long exterior excursions, or discover a genuinely global invariant that makes such control unnecessary.

## 27. Signed mod-four wake-residue theorem

This section gives a new proof route to the conclusions of P15 and P16. It was derived from the complete additive-charge criterion in Section 12, independently rederived from the eight local R/L equations, attacked by a separate implementation, and partially formalized in Lean. It does not use the cylinder-winding proof.

### 27.1 Statement

Let a finite-support repeating trace have restored heading, nonzero drift

\[
d=(a,b),
\]

and canonical endpoint decomposition

\[
D=S+(T_d-1)A,
\qquad S=\sum_{i=1}^{g}\delta_{c_i}.
\tag{27.1}
\]

Here the $c_i$ are the bases of the $g$ growing black strands; equivalently, they correspond to the odd stabilized P3 translation classes. Put

\[
\chi(x,y)=(-1)^{x+y}.
\]

If $a\ne0$, then for every $r\in\mathbb Z/|a|\mathbb Z$,

\[
\boxed{
\sum_{i:c_{i,x}\equiv r\ (|a|)}\chi(c_i)\equiv2\pmod4.}
\tag{27.2}
\]

If $b\ne0$, then for every $s\in\mathbb Z/|b|\mathbb Z$,

\[
\boxed{
\sum_{i:c_{i,y}\equiv s\ (|b|)}\chi(c_i)\equiv2\pmod4.}
\tag{27.3}
\]

If $a=0$, the signed sum is $0\pmod4$ in every exact column; if $b=0$, it is $0\pmod4$ in every exact row.

### 27.2 Construction of the charge

Assume $a\ne0$ and let

\[
\alpha:\mathbb Z/|a|\mathbb Z\longrightarrow\mathbb Z/4\mathbb Z
\]

be arbitrary. Define

\[
w(x,y)=\chi(x,y)\alpha(x).
\tag{27.4}
\]

Then $4w=0$ and the four-corner sum vanishes:

\[
w(x,y)+w(x+1,y)+w(x,y+1)+w(x+1,y+1)=0.
\tag{27.5}
\]

The complete additive-charge criterion therefore supplies ant potentials $F_q$ for which

\[
F_{q+1}(z+u_{q+1})-F_q(z)=-w(z),
\qquad
F_{q-1}(z+u_{q-1})-F_q(z)=w(z).
\tag{27.6}
\]

These signs follow directly from the dynamics: R adds a black cell of weight $w$, whereas L removes one.

Combining an N-to-E R equation with an E-to-N L equation gives

\[
F_N(z+(1,1))-F_N(z)
=w(z+(1,0))-w(z)
=-\chi(z)(\alpha(x)+\alpha(x+1)).
\tag{27.7}
\]

The N/E/S equations and $F_S=F_N-2w$ give exactly the same increment along $(1,-1)$:

\[
F_N(z+(1,-1))-F_N(z)
=-\chi(z)(\alpha(x)+\alpha(x+1)).
\tag{27.8}
\]

The two endpoints in (27.7)--(27.8) differ by $(0,2)$, so $F_N$ is vertically two-periodic.

Restored heading gives $g\equiv0\pmod4$, hence the period length is even and $a+b$ is even. Translation by $d$ therefore preserves $\chi$, while periodicity of $\alpha$ gives $w(z+d)=w(z)$. Telescoping (27.7) across one complete horizontal residue cycle and using vertical two-periodicity yields, for either sign of $a$,

\[
F_q(z+d)-F_q(z)=2\sum_{r\bmod |a|}\alpha(r)
\qquad(q=N,E,S,W).
\tag{27.9}
\]

For negative $a$, reversing the horizontal telescoping changes the sign of a multiple of two; modulo four the result is unchanged. The formulas expressing $F_E,F_S,F_W$ through $F_N$ add only $d$-periodic $w$-terms, so every heading has the same monodromy.

### 27.3 Endpoint cancellation

Charge conservation over one period gives

\[
\sum_zD(z)w(z)+F_q(p+d)-F_q(p)=0.
\tag{27.10}
\]

The convention is $(T_dA)(z)=A(z-d)$. Since $w(z+d)=w(z)$,

\[
\sum_z(T_dA)(z)w(z)=\sum_zA(z)w(z),
\]

so the two widget terms in (27.1) cancel. Equations (27.9)--(27.10) reduce to

\[
\sum_i\chi(c_i)\alpha(c_{i,x})
+2\sum_r\alpha(r)=0.
\tag{27.11}
\]

Choosing $\alpha$ to be the indicator of one residue proves (27.2), because $-2\equiv2\pmod4$. Rotation proves (27.3).

When $a=0$, take an arbitrary finitely supported exact-column function $\alpha:\mathbb Z\to\mathbb Z/4\mathbb Z$. Then $b$ is even, $w$ is $d$-periodic, and vertical two-periodicity makes the potential monodromy zero. Exact-column indicators give the zero-coordinate statement; rotation gives exact rows.

### 27.4 Consequences and limits

A sum of $m$ signs $\pm1$ that is $2\pmod4$ is nonzero and has $m$ positive and even. Thus every nonzero $x$-drift residue contains at least two strands, as does every nonzero $y$-drift residue:

\[
\boxed{g\ge2|a|,\qquad g\ge2|b|.}
\tag{27.12}
\]

If $g=0$, at least one of (27.2)--(27.3) is impossible because $d\ne0$. This excludes zero-growth repeating traces directly and supplies an independent short proof of the conclusion previously obtained from P15. Unlike the cylinder proof, it does not first require axis alignment or a clean-packet reduction.

The signed statement is stronger than the unsigned P16 count. If a residue contains exactly two strands, their bases have the same checkerboard parity. For $g=4$ and $d=(\pm2,\pm2)$, the $2\times2$ residue-count matrix must be one of

\[
\begin{pmatrix}2&0\\0&2\end{pmatrix},
\qquad
\begin{pmatrix}0&2\\2&0\end{pmatrix};
\tag{27.13}
\]

all four bases then have the same checkerboard parity. For $g=4$ and $d=(\pm1,\pm1)$, the bases split $3$-to-$1$ between checkerboard parities. These restrictions do not yet rule out a chronological trace.

### 27.5 Independent audits

The explicit-potential audit checked 944,640 local R/L equations, 3,360,000 nonzero-$a$ monodromy equations including both signs of $a$, and 2,016,000 zero-$a$ equations. A separate implementation enumerated all 524,286 turn words through length 18; all 172,092 heading-reset, nonzero-drift words satisfied the direct signed-toggle identity before P3 was imposed. It independently checked 1,832 valid standard phase/power words and 6,656 dihedral transforms against the strand formula. No failure was found.

The result still does not bound even stabilized classes, translation levels, transverse span, or period. Static aggregate flows satisfying (27.2)--(27.3) can split into several transition circuits. The missing periodic ingredient is connectivity/interlacement of the single phase-ordered ant tour.

## 28. Exterior continuation: renewal flights and uniformly bounded islands

### 28.1 P23: finite-history flight renewal

Fix $A\ge1$ after all relevant first encounters with the finite initial black set. Let $H_A(s)$ be the normalized record of the preceding $A$ positions and turns together with the current heading. Call time $s$ $A$-quiet when either the current cell occurs in that record or it is white. Non-quiet times are exactly L visits whose preceding R visit was more than $A$ steps earlier.

On every interval of quiet times, the record evolves by a finite deterministic white-default map. If a record repeats at $r$ and $r+P$, then until the quiet interval ends there are phase positions $v_j$ and a drift $d=v_P$ with

\[
p_{r+nP+j}=p_r+nd+v_j.
\tag{28.1}
\]

If $d=0$ and a second full block survived, every absolute position, heading, and turn would repeat. Each visited cell must occur an even number of times in the block, or its starting color would change and its first turn in the second block would differ. The complete global state would therefore repeat in a finite region, contradicting P13. Hence omitted black memory is met within one additional period.

Suppose $d\ne0$ and the quiet flight survives through its first $P+1$ repetitions. If a later first non-quiet collision were with a cell made black during this repeated regime, its earlier R phase/level $(i,m)$ and L phase/level $(j,n)$ would satisfy

\[
(n-m)d=v_i-v_j.
\tag{28.2}
\]

The phase path has length $P$, so

\[
1\le n-m\le P.
\tag{28.3}
\]

Translating both levels down by $m$ would reproduce the same long R-to-L collision no later than the first $P$ repetitions, contradicting the assumed quiet warm-up. Thus every genuinely late interruption collides with black debris already present at time $r$.

This is a precise renewal theorem, not an entrance proof: a flight may create bounded obstacles for later flights, so collision ancestry is well founded locally without being monotone along the entire orbit.

### 28.2 P24: bounded active loops localize every black component

Assume $|\Gamma_s|\le L$ for all $s\ge T$. If a cell receives an R visit at $t\ge T$ and is not revisited, both frozen boundary arcs incident to its now-black Tait edge start on cycles of length at most $L$: a merge puts both on the new active cycle, and a split puts them on daughters no longer than the old active cycle. Tracking either fixed arc through later successor swaps shows that its carrier remains of length at most $L$ until the cell is revisited.

Call a presently black edge *new* when its last R visit was at or after $T$; every other presently black edge belongs to the fixed finite set $B_T$. Consider the outer boundary $O$ of any current nonempty black component.

- If an edge on the outer facial walk is new, its outer incident boundary arc is covered by the preceding two-sided fixed-arc lemma, so $|O|\le L$.
- If every black edge on the outer facial walk is old, every Tait vertex used by that walk is an endpoint of $B_T$. Each such vertex disk contributes at most four directed boundary states, so
  \[
  |O|\le4|V(B_T)|\le8|B_T|.
  \]

The earlier tempting assertion that an arbitrary internal new edge must touch the outer boundary is false (a theta graph already refutes it); the outer-boundary case split is the repaired proof. Put

\[
L_*:=\max(L,8|B_T|).
\]

There are only finitely many translated embedded lattice boundary cycles of length at most $L_*$, and each encloses only a bounded number of lattice edges. Hence every black component has edge count and diameter at most a constant $K(B_T,L)$. Unbounded black memory under bounded active loops can therefore reside only in an unbounded collection of uniformly small components, never in one growing component.

### 28.3 P25: stationary-island cores

During an inactive successor-seam episode, its black anchor edge persists. The component $J_s$ containing that edge has diameter at most $K(B_T,L)$ and remains within a fixed radius of the anchor. Outside a sufficiently large fixed ball $B_{R_0}$, the active boundary belongs to a different component, and the current toggle cannot touch or change $J_s$.

If such an episode reaches radius $R>R_0$, the outside-ball interval containing a farthest point has duration at least

\[
2(R-R_0)-2.
\tag{28.4}
\]

throughout which $J_s$ is detached and stationary. Finite-state counting says that realized episode duration is bounded when its radius is bounded. Therefore unbounded bad episodes have a subsequence with both stationary-core radius and duration tending to infinity.

The remaining bounded-loop obstruction is now exact: an unbounded spatial field of other uniformly small islands would have to guide the ant away from, and later back to, an old stationary seam island.

### 28.4 Counterexamples to two hoped-for shortcuts

The blank orbit through time 9,900 contains 35 R-to-next-L lifetime intervals that are pairwise crossing: after ordering by start time, every pair obeys

\[
l_i<l_j<r_i<r_j.
\]

Thus black-memory ancestry is not laminar or LIFO even in a genuine orbit.

There is also an exact one-obstacle reversal. Start at the origin heading north with the 13-cell immediate-highway seed

\[
\begin{aligned}
\{&(-6,0),(-5,0),(-5,1),(-4,0),(-4,2),(-3,-1),(-3,2),\\
&(-2,-1),(-2,1),(-1,1),(0,0),(0,1),(0,2)\}
\end{aligned}
\]

and add the isolated black cell $(-23,26)$. The trajectory agrees with the unobstructed highway for 1,173 steps, collides with that cell, reaches distance 66 from the origin, and returns exactly to the origin at time 6,636 heading north, 5,463 steps after collision. It later receives an exact standard-highway certificate at time 10,668, so it is not a counterexample. Its role is to refute the claim that one bounded ancestral island cannot deeply reverse a mature positive-growth flight.

A broader exact scan placed one black obstacle at every one of 22 certified leading-cell types and levels 0 through 30. All 682 cases eventually received an exact standard-highway certificate before the 200,000-step horizon; all four outgoing orientations occurred. The longest detection time was 65,290 for obstacle $(-22,16)$. This is finite scattering data, not a universal bound.

## 29. Lean 4 machine-checking checkpoint

A portable Lean 4.32.0/Lake 5.0.0 project now compiles under `work/lean_langton`. It contains no `sorry` or `admit`. The current clean build completes ten jobs. The axiom audit reports only standard logical dependencies such as `propext`, `Classical.choice`, and `Quot.sound`.

The compiled core includes:

1. exact finite-list-support Langton transition semantics;
2. departed-cell toggling and unchanged colors elsewhere;
3. exact finite runs and extracted turn words;
4. restored heading implies R-minus-L residue zero in $\mathbb Z/4\mathbb Z$;
5. the finite half-flow parity telescoping core of P15;
6. four-corner admissibility of the checker-signed weights used in P22;
7. $E_r+2=0\Rightarrow E_r=2$ in $\mathbb Z/4\mathbb Z$;
8. $E_r=2$ forces a positive even residue fiber with at least two bases;
9. the residue fibers partition the finite base list; and
10. if all $n$ residues satisfy the charge identity, then $g\ge2n$;
11. finite local potential differences telescope exactly to the endpoint potential difference;
12. a lifted checker-signed residue cycle has potential monodromy $2\sum\alpha$ in $\mathbb Z/4\mathbb Z$;
13. a translated finite widget has the same additive charge under a translation-periodic weight; and
14. a structured local residue certificate derives $E_r+2=0$, and one such certificate per residue derives the growth bound.

The new `Langton/ChargeTelescoping.lean` module removes the finite telescoping, cyclic $2\sum\alpha$ calculation, and $(T_d-1)A$ widget cancellation from the hypothesis boundary. It still requires an explicit `LocalResidueCertificate`. Constructing that certificate uniformly from an actual Langton trace requires the trace-to-strand/widget decomposition, drift-periodic physical weight, lifted complete residue path, local potential formula on that path, conserved endpoint equation, and strand/fiber identification. The quotient-cylinder geometry, the potential construction from exact ant dynamics, the P12 canonical endpoint decomposition, and the universal entrance problem are not yet formalized. Thus the project certifies a larger algebraic layer without pretending to certify P22 or the highway conjecture end to end.

## 30. Exact periodic continuation and status

### 30.1 Independent complete period-42 exclusion

The original audited `PositiveGrowthSearch.java` and a residue-aware derivative both performed complete uncapped length-14-prefix searches of period 42. Both covered ranks $0,\ldots,8191$ exactly once and reported

\[
528{,}451{,}911\text{ nodes},
\qquad
14{,}561{,}206\text{ leaves},
\qquad
0\text{ hits}.
\tag{30.1}
\]

Every per-rank node, leaf, growth-prune, endpoint-prune, and hit count agreed. The original implementation applied exact P3 to all 14,561,206 leaves. The derivative applied P22 plus the odd-class growth identity first, rejected 13,487,309 leaves, and applied P3 to the remaining 1,073,897. Both found zero certificates. Together with the previous period-through-40 theorem and the impossibility of odd heading-reset periods,

\[
\boxed{\text{No finite-support periodic Langton highway has period }N\le42.}
\tag{30.2}
\]

This is a bounded-period computer-assisted theorem. It says nothing by itself about aperiodic orbits or periods above 42.

### 30.2 Independent complete period-44 exclusion

The P22-aware engine and the original audited engine were freshly compiled and run over the same ten half-open shards of the length-15 prefix ranks $0,\ldots,16383$. Every shard reported `search_complete=true`, `node_cap=null`, and an empty hit list. Independent reconstruction verified exact interval coverage, prefix strings, prefix-validity flags, and every top-level sum. Both engines reported

\[
\begin{aligned}
1{,}319{,}080{,}456&\text{ nodes},\\
115{,}325{,}749&\text{ growth prunes},\\
319{,}099{,}477&\text{ endpoint prunes},\\
67{,}839{,}409&\text{ leaves},\\
0&\text{ hits}.
\end{aligned}
\tag{30.3}
\]

All shared counters agreed at every one of the 16,384 ranks; the mismatch count was zero. The original engine applied exact P3 to all 67,839,409 leaves. The residue-aware engine applied the signed P22 test to every leaf, rejected 65,050,414, and applied P3 to the remaining 2,788,995. Hence, conditional on P3, P4, P16/P22, the documented pruning proofs, the two source implementations, and the completed execution records,

\[
\boxed{\text{No finite-support periodic Langton highway has period }N\le44.}
\tag{30.4}
\]

This remains a bounded-period computer-assisted theorem, not an entrance theorem and not an unbounded classification of periodic words.

The deterministic audit is `work/p44_independent_audit.py` (SHA-256 `35d134a3f4bd98c51ce8a9bf3814e156e303adada3cda93881621a94fea0e0ba`). Its summary is `work/p44_independent_audit_summary_2026-07-14.json` (SHA-256 `682b9bf0118684f3c2595e7deae39c785dd5d31bf38812df0ac47ca8c4869ada`), and the audit note is `work/p44_independent_audit_note_2026-07-14.md` (SHA-256 `49aea8b22b068e04bb9d6d330acb229a13f2ef18e5b5a2c725fa1780673ab5c7`). Every shard and console hash is stored in the summary.

### 30.3 Closed-detour and standard-phase counterexample searches

The standard word has 58 directed-pose return intervals and 40 distinct closed subwords. An exact splice search deleted one return interval and inserted one closed standard subword at every surviving phase. Among 196,762 positive-growth candidates, 211 passed P3; every one was merely a cyclic rotation of the standard word. There were no nonstandard certificates.

All 10,816 concatenations of two cyclic standard phases were also checked. Exactly 104 passed P3, namely the identical-phase powers. Among 70,616 triples whose three phase blocks share a rotated drift, only constant-phase triples passed. A further 9,568 targeted mixed-drift triples extending every mixed pair with score at most 12 produced no hit. These computations show finite isolation of the known word inside structured families, not unbounded uniqueness.

### 30.4 Current distance from a universal solution

This continuation closes no entrance branch completely. It does, however, replace several vague gaps by precise smaller ones:

- the periodic problem now has a signed residue invariant and an independently extended exact frontier, but still lacks a single-tour interlacement theorem capable of handling unbounded period;
- the bounded-active-loop problem now has uniformly bounded black components and long stationary seam islands, but still permits an unbounded field of other small islands to redirect the ant; and
- the unbounded-active-loop branch still lacks a coercive invariant or geometric normalization.

Accordingly, the work is closer in the sense of stronger necessary conditions, machine-checked kernels, and a narrower obstruction. It is **not close in the sense of having a nearly complete proof**. The next decisive theorem must control the global ordering of island collisions or the single-tour chronology of positive-growth traces; additional finite horizons alone cannot supply that theorem.

## 31. Minimal-growth classification and the chronology barrier

### 31.1 Complete wake-residue skeletons when growth is four

Assume an exact finite-support repeating trace has growth $g=4$ and nonzero drift $d=(a,b)$. P16 and the parity of an even heading-reset period leave, up to signs and quarter turns, exactly

\[
(\pm1,\pm1),\qquad(\pm2,0),\qquad(0,\pm2),\qquad(\pm2,\pm2).
\tag{31.1}
\]

P22 completely determines the finite residue skeleton in each case, although it does not determine longitudinal levels or chronological order.

For primitive diagonal drift $(1,1)$, label a translation orbit by $t=y-x$; for $(1,-1)$ use $t=x+y$. The four strands occupy four distinct transverse integers. Their checkerboard signs have a $3$-to-$1$ split. The magnitudes and separations of those integers remain unbounded.

For axis drift $(2,0)$, the exact-row zero-charge equations pair the two $x$ residues on exactly two rows of equal parity. After a transverse translation and reflection the skeleton is

\[
\boxed{\{(0,0),(1,0),(0,2h),(1,2h)\},\qquad h\ge1.}
\tag{31.2}
\]

The phase path must span and return across the row separation, so

\[
\boxed{N\ge8h.}
\tag{31.3}
\]

The $(0,2)$ case is the rotated statement. For drift $(2,\pm2)$, the $2\times2$ residue-count matrix is one of the two doubled perfect matchings in (27.13); all four strand bases have the same checkerboard parity, while their transverse labels remain unbounded.

### 31.2 A kinematic period congruence

Normalize the period start to an even checkerboard cell with north heading and put $n=N/2$. Let $A$ be R-minus-L restricted to the even phases. Counting west, south, and even-phase L events gives the proved congruence

\[
\boxed{n+a+b+A\equiv0\pmod4.}
\tag{31.4}
\]

For a P3-valid trace, paired turns cancel within each stabilized class, so $A$ equals the number of odd classes on the even checkerboard. Combining this with the preceding skeletons yields

- $N\equiv0\pmod8$ for drift $(2,0),(0,2),(2,2)$, or $(2,-2)$;
- for drift $(1,1)$, $N\equiv2$ or $6\pmod8$ according to whether the minority or majority checker parity is even; and
- the two primitive-diagonal assignments reverse for $(1,-1)$.

The four distinct primitive-diagonal transverse integers have a $3$-to-$1$ parity split and hence range at least four. Combining the resulting variation bound with (31.4) gives analytic lower bounds $N\ge10$ in the mod-$2$ branch and $N\ge14$ in the mod-$6$ branch.

### 31.3 Exact countermodels to every incidence-only closure attempted so far

An exhaustive construction found a single heading-reset lattice tour for every drift type in (31.1) that has growth four, respects physical-cell alternation within one period, has translation-class excess only zero or one, and satisfies all signed residue equations, yet fails the cross-period P3 order:

| drift | period | turn word | P3 violation score |
|---|---:|---|---:|
| $(0,2)$ | 8 | `LRRLRRRR` | 1 |
| $(2,0)$ | 8 | `RLRRLRRR` | 1 |
| $(1,-1)$ | 14 | `LLLRLRRRRLRRRR` | 2 |
| $(1,1)$ | 14 | `LLRRRRLLRLRRRR` | 3 |
| $(2,-2)$ | 24 | `LLLRLRRRRLLLLRLRRRRLRRRR` | 1 |
| $(2,2)$ | 24 | `LLLRRRRLRLRLRLLRRRRLLRRR` | 6 |

The $(2,-2)$ period-24 tour misses P3 by only one stabilized adjacency. Therefore drift, growth, one-period kinematics, within-period alternation, local class excess, and every P22 residue charge still do not imply a valid periodic ant trace. Any successful $g=4$ impossibility proof must control cross-period level/phase chronology.

Targeted dissection of that sole defect found the class represented by $(0,-1)$. Its stabilized entries are

\[
(1,15,R),(1,19,L),(1,23,R),(0,3,R),(0,11,L),
\tag{31.5}
\]

where each pair is (translation level, phase, turn). The only bad adjacency is the level-1 phase-23 R followed four chronological steps later by the next-period level-0 phase-3 R at the same physical cell. The two arrivals have opposite headings. Thus the sharp near-model fails at one square-scale return crossing the period boundary; all within-period checks miss it. This identifies the obstruction exactly but does not prove that every hypothetical $g=4$ trace must contain such a return.

The reproducer is `work/g4_case_audit.py` (SHA-256 `0c7e001c68d7333e544f94f41ffe88d14f35d0b83b3bf34de3838e375ef06360`). Its rerun exited successfully and reproduced all six rows. The full derivation is in `work/translator_classification_notes.md` (SHA-256 `e0b643ca6d19ea6d8f6e4ccbfc2133bc40a2d2963f600d26b0457b3046a8c4d6`).

### 31.4 Lean moved-root verification

Moving the project exposed a defect in `work/lean_langton/build.ps1`: Lake inherited the caller's directory, and the wrapper could obscure its failure. The wrapper now enters its own project directory and checks both Lake exit codes. After adding the charge-telescoping module, a clean moved-root run reported `Build completed successfully (10 jobs)`, followed by the expected axiom audit, and a source scan found no `sorry` or `admit` declarations.

`Langton/ChargeTelescoping.lean` has SHA-256 `990adca871641dfbc3a4563d72e8a83f2e40ff21ed4c931cfc88b19b026b1da9`. The exact remaining interface is documented in `work/lean_langton/FORMALIZATION_BOUNDARY.md`, SHA-256 `b0d1d0054ae76a860c9bfc5a865364d26983e44e2bb820bf22a35e49fd9cfa06`.

## 32. Frontier escape and the exact exterior obstruction

### 32.1 P26 with explicit quantifiers

Fix a memory horizon $A$. Suppose normalized histories satisfy

\[
H_A(r)=H_A(r+P)
\]

and induce phase positions $v_0,\ldots,v_{P-1}$ and nonzero drift $d$. Assume every time in

\[
[r,r+(P+1)P)
\tag{32.1}
\]

is $A$-quiet, so complete translation levels $0,\ldots,P$ supply the self-wake warm-up. Let $n_0\ge P+1$, assume the flight stays quiet through $[r,r+n_0P)$, and choose an integer linear functional $\lambda$ with $\lambda(d)>0$. If

\[
\min_{0\le j<P}\lambda(p_r+n_0d+v_j)
>
\max_{z\in B_r}\lambda(z),
\tag{32.2}
\]

where the maximum is $-\infty$ when $B_r$ is empty, then the same record cycle repeats forever.

Indeed, at every later level $n\ge n_0$ the left side of (32.2) increases by $(n-n_0)\lambda(d)$, so no later phase position belongs to $B_r$. The hostile re-audit of P23 made its ancestry conclusion exact: if a first later non-quiet cell were not in $B_r$, its last R occurred at or after $r$. Shifting that R/next-L phase-level pair down by its creation level preserves the lack of an intervening visit and the lifetime gap exceeding $A$. The phase displacement bounds the level difference by $P$, so the same non-quiet collision would occur during the warm-up (32.1), a contradiction. Thus every possible late collision is in $B_r$, while (32.2) excludes all such coordinates. The flight never ends.

The resulting exact repeated trace cannot have negative growth because black count is nonnegative, and cannot have zero growth by P15; hence its growth is positive. Since every nonzero $d$ admits a signed coordinate functional with $\lambda(d)>0$ and $B_r$ is finite, a fixed warmed renewal flight has only two possible outcomes: ancestral debris interrupts it at a finite level, or it clears the ancestral frontier and escapes forever.

### 32.2 Consequence for a returning stationary seam island

A bad stationary-island core that eventually returns to its anchor cannot contain a final uninterrupted warmed renewal flight. It must instead exhibit either

1. an unbounded chronological chain of flight changes, each sufficiently late change caused by debris older than that particular flight; or
2. quiet intervals repeatedly cut off before any normalized history completes the required repetition and warm-up.

This is stronger than saying merely that old debris matters: it forbids one fixed translating local mechanism from wandering arbitrarily far and then returning. What remains is a collision transducer that repeatedly changes the local mechanism.

### 32.3 Why coarse bounded-island arguments cannot finish the proof

Two explicit abstract walkers provide hostile countermodels to proposed arguments that use only generic geometry rather than Langton's exact routing.

- A planar finite-state binary-counter walker stores separated unit islands, returns to a permanent anchor after every increment, and has unbounded return radii while support is finite at every time and every component has size one.
- A still smaller unary moving-reflector walker uses one permanent anchor and one unit marker. Each tour moves the marker from $n$ to $n+1$ and returns to the anchor. The reachable dynamics is injective, so locality, planarity, finite state, bounded components, finite support, a stationary anchor, and reversibility on the realized orbit still do not force bounded returns.

These are not Langton-ant orbits and therefore are not counterexamples to the conjecture. Their precise role is eliminative: P24/P25 plus a generic planar or finite-state monotonicity cannot close the bounded-loop branch. A successful proof must constrain the exact Langton island-collision transducer through successor-swap chronology, checkerboard/HV routing, strict R/L alternation, or a new Langton-specific invariant.

The full proof and hostile audit are in `work/exterior_gap_notes.md`, SHA-256 `0c773f16f96b648efb21068683a6de89698ea891a8da9e7c273600dfc6fbc5e0`.

## 33. Collision-chain parity and the chronology attack

### 33.1 P27: an exact two-endpoint defect theorem

For a finite cell set $D$, form its simple bipartite row-column incidence graph: a cell $(x,y)$ is the edge $C_xR_y$.  Work over $\mathbf F_2$ and write $\partial D$ for the set of odd-degree coordinate vertices.  For a directed ant state $s=(p,q)$ put

\[
\eta(s)=
\begin{cases}
C_{p_x},&q\text{ vertical},\\
R_{p_y},&q\text{ horizontal}.
\end{cases}
\tag{33.1}
\]

Then for every two times $s<t$,

\[
\boxed{\partial(B_s\mathbin\triangle B_t)=\eta(s)+\eta(t).}
\tag{33.2}
\]

The proof is one-step exact.  The departed cell $(x,y)$ toggles, contributing the incidence edge with boundary $C_x+R_y$.  Every Langton turn changes heading type.  If the old heading is vertical, the old token is $C_x$ and the new horizontal move preserves row $y$, so the new token is $R_y$; the horizontal case is rotated.  Summing the one-step identities cancels every intermediate token.

It follows that the incidence graph of $B_s\mathbin\triangle B_t$ has either zero or two odd vertices.  If there are two, the handshaking lemma puts them in the same component; every other nonempty component is Eulerian and contains a bipartite cycle of length at least four.  If the directed ant pose is identical at the endpoints, the tokens cancel.  The symmetric difference cannot be empty, because then the complete finite-support state would repeat and contradict P13.  Hence at least four cells differ.  In particular, a closed directed return cannot literally update a nonempty tape confined to one exact row or one exact column.

For arbitrary checkpoint times $t_0<\cdots<t_m$, the same argument gives the collision-chain identity

\[
\partial\left(\bigoplus_{i<m}(B_{t_i}\mathbin\triangle B_{t_{i+1}})\right)
=\eta(t_0)+\eta(t_m).
\tag{33.3}
\]

Thus intermediate collision defects cancel exactly.  There is at most one open incidence component across the whole chain; every other stored defect is a neutral incidence cycle.  This rules out the one-row embeddings of both coarse countermodels in Section 32 as literal Langton mechanisms, but it is a conservation law rather than a coercive energy.

### 33.2 P28: exact surgery at an L collision

At a black cell $z$, let $a=(z,q)$ and $\bar a=(z,q+2)$ be the two admissible incoming roots, and let $u=\rho_B(a)$ and $v=\rho_B(\bar a)$.  The two roots occupy the two sides of the occupied Tait edge $e_z$.

- If $e_z$ is a bridge, its two sides belong to the same regular-neighborhood boundary.  Thus $a,\bar a$ lie on one frozen cycle, and deleting $e_z$ swaps their successors and splits the cycle.  The actual next state is the old successor $u$, so $u$ selects the live daughter; the other daughter is shed.
- If $e_z$ is not a bridge, its sides belong to two distinct boundaries.  Thus the successor swap merges their frozen cycles.  The Tait component stays connected and its cycle rank decreases by one.

This proves an exhaustive instantaneous collision classification.  It does not select the next renewal flight or even constrain its eventual drift projection.

### 33.3 Exact reversal audit and the failed monotonicity

The immediate 13-cell highway seed plus the initially isolated black obstacle $(-23,26)$ gives a sharp counterexample to the hoped-for projection law.  At its first read, time 1,173, the obstacle edge has endpoint degrees $(3,1)$ and is a leaf bridge in a component with

\[
(E,V,k,\beta)=(34,33,1,2).
\]

The active and opposite roots lie on the same length-120 boundary of rotation $+1$.  The L deletion splits it into a pristine live four-cycle of rotation $+1$ and a non-pristine shed length-116 cycle, also of rotation $+1$.  Despite this maximally clean local exit, the ant returns to the launch directed pose at time 6,636 and reaches an exact opposite standard gateway at time 10,668:

\[
d_{\rm in}=(-2,2),\qquad d_{\rm out}=(2,-2).
\tag{33.4}
\]

The time-0/time-6,636 symmetric difference has 524 cells.  Its incidence graph is one Eulerian component on 81 coordinate vertices with cycle rank 444.  Hence the reversal stores all endpoint-neutral change in a large cycle packet and obeys (33.2) exactly.  This disproves the proposed extension that an ancestral leaf bridge followed by a pristine exit must preserve a nonnegative projection of drift.

The exact single-witness audit is `work/one_obstacle_collision_audit.py`, SHA-256 `21d77bbb8404ae75888341df7e55eb855680339d113091a2b16d46ba45960ecb`.  It was rerun at this checkpoint and asserted every value above.  The full derivation is in `work/exterior_gap_notes.md`, SHA-256 `1c9c1dd78edbf43393c30e5437b9607d9123d5cfd8235fdc0acb69bc99fbc0a1`.

### 33.4 Lean checkpoint and exact remaining limit

`Langton/CollisionParity.lean` formalizes the one-step boundary identity, preservation through an exact finite run, endpoint theorem (33.2), and checkpoint telescoping (33.3) directly from the duplicate-free finite black-list transition.  Its SHA-256 is `80a83a42be952d75870ccd55cbedbb2d8b44eb63767add5908430fe75f745be2`.

`Langton/DirectedPoseDiscrepancy.lean` constructs explicit exact-column and exact-row checker-signed mod-four potentials, verifies all eight R/L local equations, proves the unconditional same-directed-pose endpoint congruences used in (33.7), and machine-checks the four-corner sign propagation with arbitrary checker parity at the southwest corner.  Its SHA-256 is `ee53b7aa884effb94b42213affe37bab4762075cc672ba77a4fa3d2a763a7c17`.  The independent paper/Lean audit is `work/directed_pose_discrepancy_audit.md`; its hash is recorded in the continuation manifest because a typographical repair followed the mathematical audit.

The trace-geometry formalization also moved inward.  `NormalizedTrace.delta_sum_matches_phases` is now derived from exact finite per-level toggle aggregation, the canonical strand-plus-translated-widget decomposition is proved by a prefix scan, grouped phase charge is reduced to strand charge, and the residue alpha cycle is constructed from one certified physical residue traversal.  The remaining assumptions are precisely the endpoint binary normal form, the physical closed residue path, the local potential law, and exact trace-charge conservation.  `Langton/TraceGeometry.lean` has SHA-256 `4e58c91dcf272fe3cf06c2517fe303cc038921c0f5b062182309ae52f397d596`.

After all additions, an independent moved-root wrapper run completed 16 jobs, the axiom audit reported only Lean's standard logical dependencies, and a source scan found no `sorry` or `admit` declarations.  This supersedes the earlier ten- and fourteen-job checkpoints.

Neutral cycles can have arbitrary span: four rectangle corners form one incidence cycle while their Tait edges may be four isolated bounded islands.  Widely separated copies retain this defect.  Therefore P27 plus P24 does not bound island count, radius, or return time.  A successful exterior proof still needs a Langton-specific rate/order theorem showing that forced root chronology cannot manufacture enough neutral cycles to support infinitely many reversals.

### 33.5 P29: every R-to-L lifetime carries a cycle

Let $r<l$ be consecutive visits to one physical cell $z$, with R at $r$ and the necessarily following L at $l$.  The black symmetric differences satisfy

\[
B_r\mathbin\triangle B_l
=B_{r+1}\mathbin\triangle B_{l+1}=:S.
\tag{33.5}
\]

Indeed, the first interval toggles the departed cells at times $[r,l)$ and the second those at $(r,l]$; replacing the endpoint occurrence $p_r=z$ by $p_l=z$ leaves the parity set unchanged.  Since there is no intervening visit to $z$, that cell occurs exactly once and lies in $S$.  The ant arrives at any fixed cell with one fixed heading parity, so $\eta(r)=\eta(l)$ in (33.2).  Thus every row and column degree of $S$ is even.  Its component containing $z$ contains a bipartite cycle through $z$, proving

\[
\boxed{|S|\ge4.}
\tag{33.6}
\]

At least three distinct other cells therefore have odd visit count during every completed black lifetime.  This conclusion holds for both possible arrival relations and needs only the endpoint-boundary theorem.

The complete additive mod-four charges give a signed refinement.  If the arrivals are parallel, the directed poses just before the R and L turns agree, so compare $B_r$ with $B_l$ and give $z$ endpoint sign $\eta=+1$.  If the arrivals are opposite, the two post-move poses agree, so compare $B_{r+1}$ with $B_{l+1}$ and give $z$ sign $\eta=-1$.  In every exact row and column the sum of endpoint sign times checkerboard sign is $0\pmod4$.

If equality holds in (33.6), translate and reflect so the four cells are

\[
z=(0,0),\quad(a,0),\quad(0,b),\quad(a,b),\qquad a,b>0.
\]

Their endpoint signs are forced to be

\[
\boxed{\left(\eta,(-1)^{a+1}\eta,
(-1)^{b+1}\eta,(-1)^{a+b}\eta\right).}
\tag{33.7}
\]

The originally drafted claim of four **other** discrepant cells was false: the paired cell itself is one of the four.  The standard trace makes the corrected bound sharp; 11 of its 22 opposite-arrival physical pairs have a four-cell discrepancy, including a unit-square example at phases 44 to 48.

### 33.6 Matching-exchange audit outcome

The periodic matching construction in `work/chronology_pairing_notes.md` compares the global-minimum Dyck matching with the physical consecutive R/L matching forced by P3.  Its parity and mod-four exchange identities are correct, but a hostile audit proved that they hold for arbitrary within-class R/L bijections and therefore do not encode chronological adjacency.  All six fixed growth-four near-models satisfy them under deterministic surrogate matchings.  The genuinely chronological information is the lifted-time adjacency used by P29 and the voltage/touch-graph theorems in Section 34.

## 34. Voltage interlacement and the contracted touch graph

### 34.1 The physical P edge and its exact voltage

Fix one stabilized translation class and write each phase position as

\[
p_i=b+a_i d.
\]

Define the lifted time $\tau_i=i-Na_i$.  Phase $i$ visits the actual cell $b+nd$ in period $n-a_i$, at actual time

\[
i+N(n-a_i)=nN+\tau_i.
\tag{34.1}
\]

Thus the P3 order “decreasing level, then increasing phase” is exactly increasing lifted time.  Consecutive stabilized R,L entries are genuine consecutive physical-cell lifetimes after one sufficiently large common forward shift.  Heading contributions from the level offset are multiples of $g$, hence vanish modulo four because $g\equiv0\pmod4$.  This closes the phase-versus-actual-time gap in the matching construction.

### 34.2 The Dyck exchange formulas are bookkeeping, not the missing obstruction

The hostile audit confirmed the Dyck-versus-P matching parity and mod-four formulas, including their signs.  However, their proofs use only a bijection between R and L phases within each translation class; they do not use

\[
\tau_R<\tau_L
\quad\text{with no intervening same-cell occurrence.}
\tag{34.2}
\]

A deterministic nonchronological surrogate matching on each of the six fixed growth-four near-models satisfies every local, component, and global exchange equation, even though every model fails P3.  The two sides of the global congruence are respectively

\[
0=0, 0=0, 1=1, 3=3, 2=2, 2=2\pmod4.
\]

Consequently the exchange identity is retained as a correct normal form but rejected as an independent chronology obstruction.  This is a proved failure of that proposed closure route, not a computational conjecture.

### 34.3 P30: voltage chord rows and integer rotation

Let $E$ be the finite set of physical P pair types and $U$ the $g$ unmatched wake types.  Choose a level-zero pair $e$ with cell $c_e$ and lifted interval $(r_e,l_e)$.  Copy $n$ of type $f$ has endpoints $r_f+nN,l_f+nN$ at cell $c_f+nd$.  Over $\mathbf F_2$, put $A_{ef,n}=1$ when exactly one of those two endpoints lies strictly inside $(r_e,l_e)$, and put $U_{eu,n}=1$ when the unmatched event $u+nN$ lies inside.  Only finitely many coefficients in one row are nonzero.  P29 gives the exact odd-visit vector

\[
\boxed{
v_e=\delta_{c_e}
+\sum_{f,n}A_{ef,n}\delta_{c_f+nd}
+\sum_{u,n}U_{eu,n}\delta_{c_u+nd},
\qquad \partial v_e=0.}
\tag{34.3}
\]

The Laurent coefficients satisfy $A_{ef}(T)=A_{fe}(T^{-1})$.  Diagonal terms need not vanish because a long lifetime may interlace translated copies of its own type.

Orient a crossing coefficient by $+1$ when the other R endpoint is inside and its L endpoint outside, and by $-1$ in the reverse case.  Then

\[
K_{ef,n}=-K_{fe,-n}.
\tag{34.4}
\]

With $\eta_e=+1$ for parallel arrivals and $-1$ for opposite arrivals, the aligned-pose signed difference is

\[
\Delta_e=\eta_e\delta_{c_e}
+\sum_{f,n}K_{ef,n}\delta_{c_f+nd}
+\sum_{u,n}U_{eu,n}\delta_{c_u+nd}.
\tag{34.5}
\]

Close the lifetime walk at its base cell.  The closing corner has sign $\eta_e$, so its integer rotation number $\omega_e$ satisfies

\[
\eta_e+\sum_{f,n}K_{ef,n}+\sum_{u,n}U_{eu,n}=4\omega_e.
\tag{34.6}
\]

Summing (34.6) over all $m=(N-g)/2$ pair types cancels the skew pair terms and proves

\[
\boxed{m-2E+H_{\rm tot}=4\sum_e\omega_e,}
\tag{34.7}
\]

where $E$ is the number of opposite-arrival pairs and $H_{\rm tot}$ counts contained unmatched copies.  This is genuinely voltage-aware but is not by itself contradictory.  On the standard trace it reads $2+190=4\cdot48$.

### 34.4 P31: exact boundary touch-graph reduction

Identify the two phase occurrences of each physical P pair.  They become 4-valent vertices of the temporal phase circuit; the unmatched R events remain degree-2 switches.  At a paired vertex, the two arrivals have the same H/V type, so H/H and V/V smoothing pairs the two incoming half-edges and the two outgoing half-edges.  Relative to the temporal Euler circuit this is exactly Traldi's $\psi$ transition, whose modified interlacement column is the raw interlace column plus a diagonal one.

Cut the wake switches.  Smoothing produces $g/2$ open H paths, $g/2$ open V paths, and an arbitrary number $c$ of closed H/V backtracking circuits.  Form $T_{\rm boundary}$ with these components as vertices, paired lifetimes as ordinary H--V edges, and wake events as distinguished H--V edges.  Every open component has two wake ports, so the wake subgraph $W$ is 2-regular and is a union of $\kappa$ even cycles.

Suppressing the degree-2 wake switches in the temporal graph gives a connected 4-regular Euler system.  Its H/V circuit partition has touch graph

\[
\boxed{T_0=T_{\rm boundary}/W.}
\tag{34.8}
\]

The modified-interlacement/touch-graph theorem now applies without an analogy: after deleting wake coordinates, the lifetime fundamental-circuit rows span the entire cycle space of $T_0$.  Since $T_0$ has $m$ edges, $c+\kappa$ vertices, and one component,

\[
\boxed{\dim Z(T_0)=m-c-\kappa+1.}
\tag{34.9}
\]

The full boundary graph has cycle dimension $m-c+1$.  Contraction has kernel $Z(W)$ of dimension $\kappa$.  Thus the exact gap in the rank method is not the contracted graph; it is the lift through the wake-cycle kernel.

### 34.5 Sharp limit at growth four

For $g=4$, there are exactly two open H and two open V paths.  Their wake subgraph is either one four-cycle ($\kappa=1$) or two doubled H--V edges ($\kappa=2$).  Both are valid.  Moreover, the four wake ports do not bound $c$: finite exact-row or exact-column circuits can close by backtracking on parallel temporal edge copies.  These closed circuits encode data not bounded by the four odd stabilized classes.

The standard trace sharply checks the theorem:

\[
m=46,quad g=12,quad c=5,quad\kappa=1.
\]

Equation (34.9) predicts rank 41, and the projected lifetime matrix has rank 41.  The full boundary graph has rank 42, but the full lifetime-row matrix still has rank 41.  The missing dimension is exactly its wake cycle.  Hence the stronger claim that lifetime rows always span the uncontracted boundary graph is false for the standard highway itself.

The remaining periodic lemma is now precise: control the $Z(W)$ lift and the unbounded closed H/V circuits using translation voltage, square-lattice labels, or the signed mod-four charges strongly enough to exclude both growth-four wake graphs.  General circuit nullity alone cannot do this.

The hostile proof audit is `work/chronology_pairing_hostile_audit.md`, SHA-256 `9beb8d7882841276f1212a01b1dfddf0ef6111e711900a87984fb05649953c11`.  The deterministic narrow reproducer is `work/chronology_pairing_audit.py`, SHA-256 `e0b063427e30428c8d43b09bd8621bcf0456ee87c3292a721ff7025653f780e1`; its JSON output has SHA-256 `b7f50e83a77eccf0acccf60f82b235261bf1d23e094ad4f66f0680d5c45ed345`.  It checks only the standard word and the six already fixed near-models.  The touch-graph derivation is in `work/interlace_touchgraph_notes.md`, SHA-256 `66626ac1e12a6aac34fdc772b8efe2bac56c8dd00b06ebdbc528ce168a15c0f1`.

## 35. Continuation session: period 46/48 exclusion, Lean repair, and repository

**Working date:** 14 July 2026 (paper/repo continuation).

### 35.1 Exact periodic exclusion extended to period 48
**Supersession note (20 July 2026).** The two runs described immediately below are
the P16-pruned and P22-pruned conditional variants. They share one enumeration
framework and are not independent implementations. The theorem is now certified by
the later, larger residue-free variant, whose period-46 and period-48 totals are
15,483,269,352 and 41,710,394,384 nodes. Use Section 36.6 and
`records/independent_exclusion_summary.json`, not these older counts, when citing the
exclusion that does not assume P22.

Both search engines were recompiled and positive-controlled (each accepts the
normalized standard 104-word: growth 12, drift (2,-2), P16/residue/P3 all valid).

- **Period 46.** Two independent engines, 16 shards each over all 2^15 length-16
  prefix ranks. Identical totals: 3,463,441,745 nodes, 98,568,824 leaves, 0 hits.
  Residue engine pruned 92,436,632 leaves via P22, applied exact P3 to 6,132,192.
  All per-rank node/leaf/prune counters agree between engines.
- **Period 48.** Two independent engines, 16 shards each over all 2^16 length-17
  prefix ranks. Identical totals: 8,677,026,370 nodes, 451,962,870 leaves, 0 hits.
  Residue engine pruned 439,705,662 leaves, applied exact P3 to 12,257,208. All
  per-rank counters agree.

Combined with the earlier record (<=44), the impossibility of odd heading-reset
periods, and P15/P22's zero-growth exclusion at every period: **no finite-support
periodic highway of nonzero drift has period at most 48.** Shard directories:
`work/p46_{original,residue}_shards/`, `work/p48_{original,residue}_shards/`.
Aggregated summary: `langtons-ant-highway/results/period_exclusion_summary.json`.

### 35.2 Lean: P3Endpoint repaired and brought into the build graph
`Langton/P3Endpoint.lean` previously failed to elaborate (a `rw` with a
motive-not-type-correct error at `firstOneIndex_spec`, and the file was outside the
default build target so the failure was silent). Fixed the tactic (`rw [hindex]` ->
`simp only [hindex]`), imported the file from `Main.lean` and `Audit.lean`, and added
`#print axioms` lines for its key theorems. The whole project now builds clean (16
jobs) with every audited theorem depending only on `propext, Classical.choice,
Quot.sound`; no `sorry`.

### 35.3 Publication artifacts
Two self-contained LaTeX papers (embedded bibliographies, no external .bib) authored
under the name Atharva Jillhewar: a novel-results paper and a complete-ledger
companion, plus HTML renderings. A public repository skeleton was assembled at
`langtons-ant-highway/` (paper/, companion/, lean/, code/, results/, docs/,
research-notes/) with README, MIT+CC-BY licensing, CITATION.cff, and .gitignore
excluding the toolchain, build output, and bulk shard data.

### 35.4 Status unchanged
No proof or disproof of the highway conjecture. The period-48 result is a stronger
bounded-period frontier, not a resolution; the open branches of Sections 30-34
(single-tour chronology / bounded-retreat) remain.

## 36. Timed publication-preparation continuation

**Session start:** 20 July 2026, 18:33 CDT.  **Target research interval:** two
hours, through approximately 20:33 CDT, followed by final compilation, review,
and outreach packaging.  This timestamp is a workflow checkpoint, not a theorem.

### 36.1 Scope and truth discipline

This session continues only the two live mathematical fronts: the P3-to-endpoint
normal-form/formalization bridge and the signed/voltage constraints on the wake
cycle kernel.  It will not extend numerical horizons merely to accumulate tests.
The main paper is `paper/main.tex`; its LaTeX format and mathematical typography
will be preserved.  Three independent referee passes have been commissioned:

1. a hostile theorem-by-theorem mathematical audit;
2. an independent Lean and finite-computation boundary audit; and
3. a publication, citation, and exposition audit.

No result will be promoted to the paper merely because an agent suggested it.
Each substantive correction will be checked against the proof notes, exact
artifacts, or primary literature.  The highway conjecture remains open at the
start of this session.

### 36.2 Codebase reconstruction before editing

The committed repository at tag `v1.1` has four distinct evidentiary layers,
which must not be conflated in the paper:

1. `paper/main.tex` is the 18-page principal preprint; `companion/main.tex` is
   the longer technical ledger.  The principal paper is the only source to be
   edited for this publication pass.
2. `code/python/langton_research.py` contains the exact ant kernel, the
   constructive finite-seed checker, Tait-graph diagnostics, and gateway
   certificates.  `verify_criterion_indep.py` reimplements the literal P3
   criterion with pairwise union--find classes and checks the one-sort
   reduction independently of the Java implementation.
3. The three Java programs share an enumeration framework.  The program named
   `PositiveGrowthSearchIndep.java` is residue-theorem-free, but is not an
   implementation-independent engine: it omits P22/P16 pruning while retaining
   the common trace representation and criterion machinery.  The published
   period-48 counts are from this larger residue-free tree.  The P16- and
   P22-pruned variants are conditional cross-checks.
4. The Lean project checks the transition kernel and finite algebraic layers.
   `P3Endpoint.lean` proves binary endpoint-prefix bounds from an explicitly
   supplied stabilized alternating P3 word, but does not yet construct that
   word from every `ExactPeriodTrace`.  `RemainingPotentialGeometry` still
   supplies the lifted residue traversal, local potential law, and grouped
   conservation needed for P22.  Thus no end-to-end Lean claim is warranted.

The archived search certificate is `records/langton_search_records.tar.gz`,
with per-rank hashes in `records/RECORDS_MANIFEST.json`; the human-readable
totals are in `results/period_exclusion_summary.json`.  The paper and metadata
must use the larger residue-free totals, not the older P16-pruned counts.

Two definite paper corrections were identified before the full referee reports:

- the touch-graph span is a theorem for distinct lifetime labels.  Under the
  possibly noninjective physical row/column pushforward it spans only the image
  of that labelled cycle space, not necessarily the whole physical coordinate
  cycle space;
- the four-cell lifetime argument in the principal paper uses an imprecise
  post-R/pre-L state description.  It must be replaced by the exact aligned-pose
  dichotomy (parallel arrivals: compare pre-turn states; opposite arrivals:
  compare post-move states) proved in the directed-pose audit.

### 36.3 Lean bridge advanced and rebuilt from a clean toolchain

`StabilizedP3Word.toOrbitEndpointData` now constructs every algebraic field of
`OrbitEndpointData` from one explicitly supplied stabilized P3 word. Lean proves
that the first coefficient (+1) is the first positive strand, removes it, proves
the remaining coefficient sum is zero, and proves every prefix of the resulting
widget scan is binary. This removes the old practice of supplying those endpoint
facts independently. It does **not** extract the nonincreasing stabilized level word
from an arbitrary `ExactPeriodTrace`, or construct the physical lifted residue path
or local potential identity; those are the remaining geometric interfaces.

The Windows host executable was blocked by the machine's code-integrity policy, so
a clean Linux build was made from the official Lean 4.32.0 release through
`lean/Dockerfile`. All 18 jobs built. The added theorem depends only on `propext`
and `Quot.sound`; the complete audit lists only `propext`, `Quot.sound`, and where
used `Classical.choice`. A source scan finds no `sorry`, `admit`, custom axiom,
`native_decide`, or `unsafe` escape. The formerly hard-coded toolchain path in
`lean/build.ps1` was replaced by a PATH/environment-aware launcher.

### 36.4 Growth-four wake-kernel classification: exact result and exact limit

The narrow script `work/g4_wake_kernel_audit.py` enumerates only the three perfect
matchings of four labelled wake ports; it is not a period search. An independent
referee re-enumerated the cases. Coordinate compatibility forces:

1. axis drift ((2,0)): one H matching and one V matching, whose union is one
   alternating four-cycle, so (kappa=1);
2. even diagonal drift ((2,2)): the unique H and V matchings coincide, giving two
   doubled two-edge cycles, so (kappa=2);
3. primitive diagonal drift ((1,1)): three choices for each matching; six unequal
   pairs give one four-cycle and three equal pairs give two doubled cycles, so
   (kappa\in\{1,2\}).

The two even-diagonal residue-count matrices are

\[
\begin{pmatrix}2&0\\0&2\end{pmatrix}
\quad\text{and}\quad
\begin{pmatrix}0&2\\2&0\end{pmatrix},
\]

not one matrix "or its transpose." This topology lemma classifies compatible
abstract wake-port pairings only; it proves neither P3 chronology nor realizability
by an ant trace.

The script's `cycle_functionals` use alternating (+1,-1) circulation
coefficients. They are **not** the P22 sums, which place coefficient (+1) on each
wake base. No theorem says these oriented charges vanish on lifetime-row lifts. The
safe negative conclusion is only that these natural oriented coordinate functionals
are noninjective on (Z(W)); the even-diagonal kernel is entirely invisible. No
stronger P22-kernel claim was promoted to the paper.

### 36.5 Principal-paper correction pass

The `amsart` source was retained, while the table of contents and forced page breaks
were removed. The revised title is *Finite-Support Periodic Highways of Langton's
Ant: Necessary Conditions and Short-Period Exclusion*. The main corrections are:

- definitions of heading-reset period, eventual periodic trace, drift, growth,
  least trace period, and the admitted translations/rotations/phases;
- deletion of bare reflection as a claimed symmetry;
- a cycle-lemma proof of the nonnegative-prefix phase normalization used by the
  residue-free search;
- restriction of Proposition 4.4 to affine combinations of ((E,V,k,\beta)), the
  only quantities treated by its proof;
- removal of the unsupported clean-translator refinement about drift multiples,
  period divisibility, and an ambiguous norm bound;
- correction of the lifetime proof: the post-R token and pre-L token are the two
  endpoints of the departed cell, giving an avoiding path and a four-edge cycle;
- multigraph conventions and the warning that Traldi's ranks are for the labelled
  lifetime graph; physically pushed rows span only (pi_*Z(T/W));
- removal of the unsupported Hamming-isolation proposition;
- separation of the entrance and all-period classification gaps; and
- corrected Langton, Gajardo, and Traldi bibliography entries.

The endpoint-token collision proof supersedes the preliminary Section 36.2 wording
that suggested a directed-pose case split was required.

### 36.6 Search-certificate repair and fresh bounded rerun

The old archive (SHA-256
`c36e636914f7cbb9e0a2b892f32963cc74ad840e8bbf16d0dfe836db85c03a95`)
was internally consistent for its 416 hashed members but omitted the records behind
the period-at-most-32 row. Its 32 length-six prefixes also did not cover depths below
six.

All 32 prefix shards and an unprefixed depth-at-most-5 baseline were regenerated
under current `code/python/langton_research.py` (SHA-256
`b395ed3aac53bb9f43aea375ffd7257cd81ec3df5404df098783ed0656c4bcfc`).
The exact result is 59 nodes at depths 0--5 plus 46,185,421 nodes across all 32
disjoint `R` plus five-symbol prefixes at depths 6--32: 46,185,480 total nodes,
largest shard 2,623,020 under a cap of 100,000,000, every shard complete, zero hits.

`records/aggregate_indep.py` now checks all eight per-rank counters and fails closed
if any requested period is missing. Periods 34--48 passed exact rank coverage,
completion, null-cap, counter-sum, and zero-hit checks. Period 48 records 51,856.023
aggregate shard-seconds (14.404 shard-hours) and 1:28:48 wall time with 11 workers;
the old "few core-hours" wording was removed.

`records/make_archive.py` now hard-fails on missing inputs, builds to a temporary
archive, verifies every member and SHA-256, and only then replaces the release file.
The rebuilt 460-member archive has SHA-256
`da4dac9c5be182ebc5d0b6517aba03e8fd5025df72625b97e1a875242c7766b8`.
After fresh extraction, `audit_p32.py` and the strengthened
`aggregate_indep.py` both returned `all_checks_passed=true`.

### 36.7 Current distance from the conjecture

This session improves rigor, reproducibility, and the P3 algebraic Lean bridge, but
does not make the universal conjecture close to solved. The finite pairing
classification explains why the wake-cycle kernel survives at growth four; the
fresh bounded rerun strengthens only the period-at-most-48 theorem. A complete proof
still needs both (i) a global entrance mechanism for every finite seed and (ii) an
unbounded-period chronology theorem classifying all positive-growth periodic traces.
Neither has been derived, and no counterexample certificate has been found.

### 36.8 Adversarial paper audit and exact repairs

Between 18:33 and the 20:18 CDT finalization checkpoint, the principal manuscript,
companion, code-facing documentation, and release records were subjected to separate
internal adversarial audits. These were automated-agent referee passes, not external
peer review, and are not described as independent mathematical confirmation. Every
reported issue was checked in the current source before it was changed.

The main manuscript now states the conjecture behaviorally: after some time the
future path and turn trace must agree with the standard highway up to lattice
translation, quarter-turn rotation, and cyclic phase. It explicitly permits finite
stationary debris outside the future path and does not demand equality of the entire
colouring. Reflection is not used as a symmetry. The two unresolved obligations are
also stated behaviorally: a finite translated window must contain the ant and every
cell or Tait-boundary component capable of influencing the future, and every
positive-growth periodic highway must agree with the standard path and turn trace.

The following proof-level defects or overstatements were removed or repaired:

1. the periodic seed formula now includes
   `min_I a_i <= n < max_I a_i`, making every `S_{I,n}` defined and the seed finite;
2. the arithmetic coset checker now uses the complete Bézout invariant
   `(b'x-a'y, (rx+sy) mod gcd(a,b))`, not an incomplete single-coordinate residue;
3. the planar regular-neighbourhood proof specifies genus zero and derives
   `V-E=2k-b`, hence `b=E-V+2k=k+beta`;
4. an advanced record must lie strictly beyond the bounding box of the initial
   support before the untouched-endpoint bridge argument applies;
5. the affine-statistics proposition concludes only that no affine combination of
   `(E,V,k,beta)` is a monotone/Lyapunov potential even on the blank orbit;
6. the collision-chain proof now uses time-indexed endpoint tokens and the
   handshaking lemma, and the four-cell lifetime bound follows from a path joining
   the endpoints of the missing paired edge;
7. the charge cocycle, endpoint decomposition, and stationary-debris-to-clean-
   translator reduction have complete proofs rather than unsupported assertions;
8. an unsupported exterior-dynamics theorem block, the centered-3-by-3 theorem,
   the Hamming-isolation claim, the physical touch-graph rank claim, and an
   unproved minimum-rectangle claim were removed from the release manuscripts; and
9. the Lean description was narrowed throughout to selected algebraic kernels
   conditional on a structured periodic-trace certificate.

The companion was rebuilt as a self-contained 15-page technical report after these
repairs. A cold final referee pass found no remaining mathematical, claim-scope,
undefined-reference, duplicate-label, or missing-citation blocker. The principal
paper remains the 18-page submission manuscript and controls the claims.

### 36.9 Exact meaning of the period-at-most-32 certificate

The earlier phrase “complete legal trace tree” was too broad. The 32 long shards
begin with `R` and then cover all five-symbol `R/L` suffixes; the unprefixed baseline
covers depths zero through five. The exact theorem is nevertheless complete for the
positive-growth highway search: every positive-growth heading-resetting word contains
an `R`, and a cyclic shift starts at that `R`; this is the same periodic orbit at a
different phase and preserves finite-support realisability.

All paper, HTML, README, JSON, audit-script, and archive wording now says
“first-R cyclic-phase-normalised enumeration.” `records/audit_p32.py` emits schema
`langton-p32-exclusion-v2` with the field
`cyclic_phase_normalized_nodes_through_period_32=46185480` and an explicit coverage
sentence. Its cold audit again returned 46,185,421 sharded nodes plus the 59-node
baseline, zero hits, all 32 prefixes exactly once, and no reached node cap.

### 36.10 Frozen search archive and cold verification

Because the corrected audit script, Java provenance comments, and reproduction
working-directory instructions are themselves archived, the search record archive was
rebuilt once more. The final archive is
`records/langton_search_records.tar.gz`, contains exactly 460 unique members, and has
SHA-256

`7052f3070829bf804ae317a40379f6bb045b00775aff826b4e347880747bcc1a`.

The archive constructor recomputed every inner SHA-256, compared the exact member
set, rejected duplicates, and atomically installed the verified temporary archive. A
fresh extraction then ran the packaged `audit_p32.py` and `aggregate_indep.py`.
The former passed the first-R period-at-most-32 certificate; the latter passed every
period 34, 36, ..., 48 with exact rank coverage, `search_complete=true`, no node cap,
all eight counters summed, `p3_checks=leaves`, and zero hits. The residue-free engine
source remains SHA-256
`dacd32f6ab2f0c033c4e8226987333f21582e5aecad25322863439065645d68f`.

### 36.11 PDF, metadata, and outreach checks

Both LaTeX documents compile twice with no undefined citation/reference, overfull or
underfull box, or LaTeX warning. The main PDF is 18 pages; the companion is 15 pages.
Every page of the companion and every changed page of the already fully inspected
main paper was rendered at 110 dpi and visually checked for clipping, overlap,
orphaned lines, malformed mathematics, and bibliography overflow. Both PDFs carry
explicit title and author metadata. The accessible HTML summaries use the same
behavioral conjecture and the stronger bounded-active-core formulation.

`docs/professor_outreach_email.md` asks for one targeted technical check, states that
the conjecture is not solved, distinguishes the concept DOI from an exact version
DOI, and forbids describing internal AI-assisted audits as peer review. Before any
email is sent, the author must fill the address/affiliation and professional-email
placeholders and mint or identify an exact version DOI whose files match the final
artifact manifest.

### 36.12 Honest final mathematical distance

No step in this publication pass supplies either missing infinite theorem, and no
counterexample certificate was found. The new Lean constructor is a real reduction
in the algebraic interface, the wake-port enumeration is a real finite topology
classification, and the period-at-most-48 exclusion is an exact bounded theorem;
none implies universal entrance or all-period uniqueness.

The touch-graph audit sharpened the negative boundary: distinct lifetime labels may
support a cycle-space statement, but the physical row/column pushforward can identify
labels and is not injective. Likewise, natural alternating oriented wake-cycle
functionals have a nontrivial kernel and are not the all-`+1` P22 charges. Therefore
the most promising remaining proof obligations are still:

1. prove that all future-influencing state eventually lies in one finite translated
   active window, with discarded debris permanently inert; and
2. derive an unbounded-period single-tour chronology/interlacement theorem strong
   enough to classify every positive-growth periodic highway.

A disproof still requires an infinite certificate: either a nonstandard periodic
word passing the exact criterion with its constructed finite seed, or a finite
self-enlarging gadget with an inductive recurrence. Near-infinite compute is useful
only when aimed at one of those certificates or at a precisely stated finite theorem.

### 36.13 Final executable and cross-platform checksum audit

A fresh six-way executable cross-check was run after the prose freeze. The independent
literal P3 verifier and the Java one-sort checker agreed on all 524,286 nonempty words
through length 18, including 174,762 heading-reset words and 172,092 nonzero-drift
ones; none of the latter passed P3. The standard 104-word passed with drift `(2,-2)`,
growth 12, and the exact 11-cell seed. The direct residue audit passed all local and
standard-family checks, and the affine-statistics script observed all eight centrally
symmetric increment vectors with rational span three.

The collision diagnostic initially printed `len(G)>=4`, which was the wrong set: the
paired cell `z` is black at both endpoints and therefore is deliberately absent from
the symmetric-difference graph `G`. The theorem proves that `G` supplies an avoiding
three-edge path and that adjoining the missing paired edge/cell closes a four-cycle.
`verify_collision_tokens.py` now checks `|G union {z}|>=4` and asserts it. This was a
diagnostic-display bug, not a change to the paper proof.

The final cold release audit also caught a cross-platform reproducibility defect:
several Windows working files and the archived manifest used CRLF even though
`.gitattributes` requires LF. Such files would hash differently after a Git clone.
All release text was normalized to LF; `aggregate_indep.py`, `audit_p32.py`,
`make_archive.py`, and the period-44 audit writers now request `newline="\n"`
explicitly. The archive was rebuilt after normalization. This supersedes the
intermediate `d877...` archive checksum; the canonical archive checksum is the
`7052...` value recorded in Section 36.10 and the paper.

After that rebuild, a genuinely new extraction at 20:32 CDT on 20 July 2026 ran the
packaged auditors, rather than importing repository-side results. `audit_p32.py`
returned `all_checks_passed=true`, all 32 prefixes exactly once, 46,185,421 sharded
nodes plus the 59-node baseline, largest shard 2,623,020 below the 100,000,000 cap,
and zero problems. `aggregate_indep.py` returned `[OK]` for every even period
34--48 and `all_checks_passed = True`, with zero hits. The extracted archive hash was
again
`7052f3070829bf804ae317a40379f6bb045b00775aff826b4e347880747bcc1a`,
and its `RECORDS_MANIFEST.json` contained zero CRLF byte pairs. This closes the
post-normalisation archive-verification loop.

## 37. Transverse rigidity: the extremal-line theorem and a period-unbounded exclusion

Session of 21 July 2026. Target: obligation 2 (the unbounded-period chronology
obligation). Section 31.3 established that no *incidence-only* argument can close
even the growth-four case, because explicit countermodels satisfy every residue
equation, every within-period alternation check, and every drift/growth skeleton
constraint while still failing cross-period order. The results below are the first
in this journal that are genuinely chronological: both proofs use P3 condition (ii)
(the stabilised word begins with R) as an *ordering* hypothesis rather than as a
counting hypothesis, and both hold for **every period, with no bound**.

### 37.1 Setting: the transverse functional

Let $w$ be a finite-support-realisable periodic trace of length $N$ with drift
$d=(a,b)\neq0$. Call the drift **diagonal** when $|a|=|b|=m\ge1$; write $d=me$ with
$e$ primitive, and let $t(x,y)=x+y$ when $ab<0$ (so $e=\pm(1,-1)$), and
$t(x,y)=x-y$ when $ab>0$ (so $e=\pm(1,1)$).

Then $t(d)=0$, so $t$ is constant on translation classes and the transverse range of
the trace is the same in every period; and **every unit step changes $t$ by exactly
$\pm1$**. The latter is where diagonality is used: for an axis drift the transverse
functional is $y$ (or $x$), which is unchanged by two of the four moves, and the
arguments below fail. The standard highway has $d=(2,-2)$, hence $m=2$, $e=(1,-1)$,
$t=x+y$.

Put $T=\max_i t(p_i)$ and $T'=\min_i t(p_i)$, and call $W=T-T'$ the **transverse
width**. The standard highway has $T=5$, $T'=-5$, $W=10$.

### 37.2 The extremal-line theorem

**Theorem A.** For a finite-support-realisable periodic trace with diagonal drift:

1. every cell on the line $t=T$, and every cell on the line $t=T'$, that the ant
   reaches at all is visited **exactly once in the entire trajectory** (equivalently,
   every translation class meeting an extremal line is a singleton);
2. all arrivals on those two lines are horizontal - on $t=T$ the arrival heading is
   the horizontal heading that increases $t$, and on $t=T'$ the one that decreases it;
3. every turn on those two lines is R;
4. $W=T-T'$ is even;
5. consequently every visited cell of the two extremal lines is permanently black,
   i.e. belongs to the wake.

*Proof.* All cells on a line $t=c$ share the checkerboard parity of $c$, so by the
HV partition their arrivals share one axis: on each extremal line the arrivals are
either all vertical or all horizontal. The ant reaches $t=T$ from $t=T-1$, so its
arrival heading increases $t$; and it may not leave the strip, so its departure
heading does not increase $t$.

Suppose the line $t=T$ were vertical. Its arrival is then the vertical heading
increasing $t$ (write it N), and the clockwise image of N is the horizontal
heading E, which also increases $t$ and would leave the strip. Hence every turn on
the line is L. But P3(ii) makes the stabilised word at each cell begin with R, a
contradiction. So $t=T$ is horizontal, its arrival is the horizontal heading E
increasing $t$, and the anticlockwise image N of E again increases $t$; therefore
every turn on the line is R. By P3(i) the stabilised word alternates, so a cell
visited twice would read RR. Hence each cell of $t=T$ is visited exactly once, and
the same argument applies verbatim at $t=T'$. Both extremal lines are horizontal,
hence carry the same checkerboard parity, so $T\equiv T'\pmod 2$. A singleton class
is odd, so its cell ends black. $\square$

Note the shape of the argument: it is P3(ii), the *first-turn* condition, that
eliminates the vertical case, and P3(i), *alternation*, that forces single visits.
Neither is available to an incidence-only argument, which is exactly why Section 31.3
could not be closed.

### 37.3 Verification of Theorem A

`work/verify_extremal.py` (SHA-256
`7796d5c6966ece905c0a21dda29af6d2d950b657676014fd85d630e0f690221e`) checks the
theorem directly and, more usefully, its contrapositive.

On the standard highway: $t$-range $[-5,5]$, width $10$ (even); the line $t=5$ carries
$2$ phases on $2$ distinct cells, each visited once, all arrivals E, all turns R;
the line $t=-5$ likewise with all arrivals W. On the square of the standard word
(period $208$, drift $(4,-4)$) the same lines carry $4$ once-visited cells each. On
the R/L-swapped reflection the extremal turns are all L and the word is
correctly reported P3-invalid, which is the mirror image of the excluded vertical
case.

Exhaustively over every diagonal-drift heading-resetting word of length at most $18$:

| quantity | count |
|---|---:|
| diagonal-drift heading-resetting words | 60,854 |
| of those, with a repeated cell on an extremal line | 18,946 |
| of those, P3-valid (Theorem A forces 0) | **0** |

### 37.4 A period-unbounded exclusion: no highway of transverse width two

Theorem A collapses a narrow strip to a one-dimensional system, and that system can
be refuted for *all* periods simultaneously. This is the first exclusion in this
project that is not bounded by a period cutoff.

**Theorem B.** No finite-support periodic highway with diagonal drift has transverse
width $W=2$. Consequently $W$ is even and $W\ge4$.

*Proof.* Label the three occupied lines $0,1,2$ for $t=T,T-1,T-2$. Lines $0$ and $2$
are extremal, hence horizontal and once-visited with turn R (Theorem A); line $1$ is
vertical. Each step changes $t$ by $\pm1$, so the ant alternates between line $1$ and
lines $\{0,2\}$: consecutive visits to line $1$ are separated by exactly one excursion.

By Theorem A the excursions are forced. From a line-$1$ cell $z$, the upward
excursion is $z\to z+\mathsf{E}\to z+\mathsf{E}+\mathsf{S}=z+e$, and the downward one
is $z\to z+\mathsf{W}\to z+\mathsf{W}+\mathsf{N}=z-e$. So line-$1$ cells carry a
longitudinal index $\ell\in\mathbb{Z}$ and every excursion changes $\ell$ by $\pm1$.

The line-$0$ cell used by an upward excursion from site $\ell$ depends only on $\ell$;
call it $U_\ell$, and likewise $D_\ell$ on line $2$. By Theorem A each of $U_\ell$ and
$D_\ell$ is visited at most once in the whole trajectory, so site $\ell$ admits at
most one upward and at most one downward excursion. Every visit to $\ell$ produces
exactly one excursion, so **each site is visited at most twice, ever**.

By P3 the turns at a site alternate from R, so visit $1$ is R and visit $2$ is
L. Reading the four cases at a vertical cell (S,R to W; S,L to E;
N,R to E; N,L to W) and noting that arrival S means the ant came from
$\ell-1$ and arrival N that it came from $\ell+1$: **R reverses the longitudinal
direction of travel and L continues it.**

Now suppose such a highway exists; its drift is $\pm m\neq0$ along $\ell$, say $+$.
At any finite time the visited sites form a contiguous interval $[A,B]$. Since the
ant reaches arbitrarily large $\ell$, it arrives at a fresh site $B+1$ moving $+$
infinitely often. There it takes visit $1$, turn R, and reverses to $-$, returning
to $B$. If $B$ already has two visits this is a third, a contradiction; otherwise it
is visit $2$, turn L, which continues the ant to $B-1$. Inductively the ant walks
left through sites that must each have had exactly one prior visit, converting each to
two. On reaching $A$ it either finds two visits (contradiction) or takes visit $2$,
turn L, and continues to the fresh site $A-1$, where visit $1$ is R and reverses
it back onto $A$ - which now has two visits, a third arrival, again a contradiction.
Every branch contradicts the two-visit bound. $\square$

`work/verify_width.py` (SHA-256
`e36c77d512ba14ee61eb729f21662b8eb016c480a2984439c646b8ec7eeb3ca4`) runs the forced
automaton from both initial directions; each reaches a third visit at step $4$. The
brute-force scan over all diagonal-drift heading-resetting words of length at most
$18$ found no P3-valid word of any width, consistent with (and not evidence beyond)
the period-at-most-48 exclusion.

### 37.5 What this does and does not settle

Theorem B removes an infinite family of candidate periods, which no earlier result in
this project did: every previous exclusion was a finite search bounded by period $48$.
It does not approach the standard highway's own width of $10$. The natural next step
is width $4$: lines $0,2,4$ are horizontal and lines $1,3$ vertical, the extremal
lines $0$ and $4$ remain once-visited, but the interior horizontal line $2$ may be
visited repeatedly, so the one-dimensional collapse of Theorem B does not apply. The
width-$W$ problem is a Turing-machine-style question on a tape of columns with
alphabet $2^{\lceil (W+1)/2\rceil}$, and is finite-state for each fixed $W$; widths
$4,6,8$ are therefore a well-posed decidable target, and settling them would prove
that the standard highway is the narrowest possible.

Neither theorem uses the residue theorem of Section 27 or any of its corollaries, so
both are independent of that development. Both do use the periodic-realisability
criterion of Section 3 and the HV partition, and nothing else.

### 37.6 Adversarial audit: two real defects, both repaired

Two independent adversarial referees were run against Section 37 before release, one
per theorem, each instructed to assume the theorem false. Both found genuine errors.
The statements in 37.2 and 37.4 above are superseded by the corrected forms recorded
here and in the paper; they are left in place because this journal is an audit trail.

**Defect 1 (Theorem A, fatal to the statement as printed).** The transverse
functional was defined by a case split, $t=x+y$ when $ab<0$ and $t=x-y$ when $ab>0$,
and the proof was then written in the first frame only. The increments are

| heading | N | E | S | W |
|---|---|---|---|---|
| $t=x+y$ | $+1$ | $+1$ | $-1$ | $-1$ |
| $t=x-y$ | $-1$ | $+1$ | $+1$ | $-1$ |

so for $t=x+y$ the $t$-increasing vertical heading is north and its clockwise image
east also increases $t$, which is what kills the vertical case. For $t=x-y$ the
$t$-increasing vertical heading is *south*, whose clockwise image is *west* and
decreases $t$: the vertical case survives and the **horizontal** case dies instead.
The proof's phrase "call it north" is a $180^\circ$ relabelling, but the two frames
differ by a $90^\circ$ rotation, which exchanges the two axes. Conclusion (i), that
the extremal lines are horizontal, is therefore false for exactly half of the drifts
covered.

The counterexample is the paper's own running example: the standard word read from an
east-facing start is the same highway rotated a quarter turn, has drift $(-2,-2)$ with
$ab>0$, and its extremal lines are **vertical**, with arrivals south at $t=T$ and
north at $t=T'$. Verified directly:

| start | drift | $ab$ | $t$ | extremal arrivals | turns | horizontal? |
|---|---|---|---|---|---|---|
| N | $(2,-2)$ | $<0$ | $x+y$ | E / W | R | yes |
| E | $(-2,-2)$ | $>0$ | $x-y$ | S / N | R | **no** |
| S | $(-2,2)$ | $<0$ | $x+y$ | E / W | R | yes |
| W | $(2,2)$ | $>0$ | $x-y$ | S / N | R | **no** |

Repair: since a quarter-turn rotation sends $\drift=(a,b)$ to $(-b,a)$ and hence $ab$
to $-ab$, and highways are identified up to quarter-turn rotation, normalise to
$ab<0$ and take $t=x+y$ throughout. The proof is then rewritten with explicit compass
directions and no relabelling, which removes the entire class of error. Everything
that does not name an axis survives untouched: every extremal turn is $\turnR$,
extremal cells are entered at most once, and $W$ is even. The unnormalised form is now
recorded as a separate remark.

**Defect 2 (Theorem B, serious gap; theorem still true).** The proof asserted that
"the turns at $\ell$ alternate from $\turnR$, so the first visit turns $\turnR$". That
is false. Criterion (ii) constrains only the *stabilised* word of a class, and the
seed construction of Theorem 3.1 deliberately blackens cells below their class's
maximal level, so a first visit may perfectly well turn $\turnL$. Unvisited does not
mean white. The subsequent case analysis inherited the error and was also not
exhaustive: it never considered the ant walking into a fresh site that is black, in
which case the ant continues rather than reversing. `verify_width.py` hard-coded the
same false assumption (`turn = 'R' if visits % 2 == 1 else 'L'`), so the script could
not have detected it -- a reminder that a checker sharing an assumption with the proof
checks nothing about that assumption.

Repair (due to the referee, and adopted): argue on edges rather than sites. An upward
excursion out of site $\ell$ consumes the extremal cell $U_\ell$ and a downward
excursion out of $\ell$ consumes $D_\ell$; distinct sites consume distinct cells, and
Theorem A bounds each at one use. So the gap $(\ell,\ell+1)$ is crossed at most once
upward and at most once downward. Drift $+m$ forces the net crossing number of every
gap above the start to be exactly $+1$, and with both counts bounded by one this
forces one upward crossing and **no** downward crossing. Hence every site above the
start is entered exactly once, arriving heading south and departing east, so its
unique turn is $\turnL$; its translation class is then a singleton whose stabilised
word is the single letter $\turnL$, contradicting criterion (ii). No interval, no
descent, no first-turn assumption.

`verify_width.py` was rewritten accordingly. It now checks the geometric inputs and
runs an adversarial search in which the colour of every not-yet-visited site is chosen
by an opponent; with at most $k$ black seeds no opponent survives more than $k+4$
steps before some gap must be crossed twice in one direction. That is independent
confirmation which the previous script structurally could not provide.

**Assessment.** The audit was worth more than the original derivation. Defect 1 would
have been caught by any referee who tried the standard highway in a rotated frame, and
Defect 2 by anyone who took the seed construction seriously; both were in the first
written version and neither was detected by the checks I wrote, because those checks
shared the proofs' assumptions. The pattern to carry forward is that a verification
script written from the same mental model as the proof is not an independent check,
and that the useful adversarial question is "which hypothesis is being used where it
was not established" rather than "does the example work".

## 38. Width-four research session (21 July 2026)

This section is the chronological audit record for the research performed before the
19:00 CDT manuscript cutoff (extended by the user at 17:27). The polished derivations and complete bounded-search
tables are also kept in `research-notes/width4_research_2026-07-21.md`; the machine
summary is `results/width4_drift_exclusion_summary.json`.

### 38.1 Scope and normalization

The target was the first unresolved even width, not the universal eventual-highway
conjecture directly. Rotate the diagonal drift to `(m,-m)`, `m>0`, take transverse
coordinate `t=x+y`, shift the five occupied lines to `t=0,1,2,3,4`, and use a
longitudinal integer `ell`. The extremal-line theorem makes lines 0 and 4 singleton
`R` lines. Lines 1 and 3 have vertical arrivals; line 2 is the revisitable interior
horizontal line.

No result in this section asserts that every Langton-ant configuration becomes a
highway, that width four is impossible for all `m`, or that fixed width alone is a
finite-state problem.

### 38.2 General width--growth sandwich

For normalized diagonal drift `(m,-m)`, a translation class is labelled by
`(t,x mod m)`. In each residue the signed residue theorem forces a positive even
number of odd classes. Since the transverse width `W` is even, there are `W+1` level
lines, so an even subset has cardinality at most `W`. Summing over the `m` residues
gives

```
2m <= g <= mW.
```

This is valid for every diagonal periodic highway, not just width four. For the
standard highway `(m,g,W)=(2,12,10)` it gives only `W>=6`.

### 38.3 Six possible odd masks at width four

Solving the five-bit signed mod-four equation with positive even cardinality gives,
for each `x` residue and independently for each `y` residue, exactly

```
{0,2}, {1,3}, {0,4}, {2,4}, {0,1,2,4}, {0,2,3,4}.
```

If `h` of the `m` masks have four elements, then `g=2m+2h`. Since `g` is a
multiple of four, `h congruent m (mod 2)`. Enumerating compatible vertical and
diagonal masks gives `6,14,30,70,146,302,650,1422` skeletons for `m=1,...,8`.
This is a finite-memory shift-of-finite-type statement about the *odd skeleton only*.
It is not a chronological realization theorem.

### 38.4 Exact four-state macro automaton

Observing the ant on odd lines after every two ant turns gives states `LN,LS,UN,US`.
The complete transition table is

```
LN -> LS  +1 RR centre      LN -> UN  +1 RL centre
LN -> LN  -1 LR bottom      LS -> LN  -1 RR bottom
LS -> LS  +1 LR centre      LS -> UN  +1 LL centre
UN -> US  +1 RR top         UN -> UN  -1 LR centre
UN -> LS  -1 LL centre      US -> UN  -1 RR centre
US -> LS  -1 RL centre      US -> US  +1 LR top.
```

The pair is `(odd-line turn, even-line turn)`. A based tour starts immediately after
a bottom visit in `LN`, returns to `LN` shifted by `m`, and must use the top line.
Each macro contributes exactly two ant turns, so `N=2P`.

### 38.5 All-period bound at fixed drift

Name the transition counts

```
x,a,b from LN;  c,d,e from LS;  f,q,h from UN;  i,j,y from US,
```

in the order displayed in 38.4. Flow gives `c=a+b` and `f=i+j`. Extremal
singleton rigidity gives `x+c<=m` and `f+y<=m`. Put
`L1=x+d+e`, `L3=q+h+y`. P3 alternation on each odd-line translation class implies
nonnegative total turn excess, hence `L1<=2c` and `L3<=2f`. Direct counting gives

```
P = 2c+2f+L1+L3,
m = L1-L3-2x+2y.
```

Eliminating `L3`, then using `L1<=2c<=2(m-x)`, `c<=m-x`, and `f<=m-y`, yields the
strictly recorded form

```
P + 8x <= 7m.
```

Therefore `P<=7m`, `N<=14m`, and `P congruent m (mod 2)`. Combining with
`g>=2m` gives `N<=7g`. The period--drift bound itself does not use the residue
theorem; the last speed corollary does.

The incidence family `v^m`, `v=RRLRLLRRRRLLRR`, saturates `P=7m`, `g=4m`, and the
six-mask constraints. It is not a structural counterexample: for `m>=2`, phases 9
and 17 revisit `(3,-2)` with two successive `R` turns. Thus transition counts and
odd masks cannot improve the constant seven; local ordering must enter.

### 38.6 Primitive drift excluded without a period cutoff

For `m=1`, unique bottom and top classes force `c=f=1`, `a+b=i+j=1`, and `x=y=0`.
Growth is a positive multiple of four but there are only five classes, hence `g=4`.
The two odd-line left totals are `1` and `2` in some order, so `P=7`. The six
state-compatible ant words are

```
RRLRLLRRRRLLRR   RRLRLLLRRRRLRR   RRLLRRRRLLLRRR
RRLLLRRRRLLRRR   RLRRRRLLLRLRRR   RLLRRRRLLRLRRR.
```

Their displayed bad class words are respectively `LRLR, LRLR, RLLR, RLLR, RRL,
LRR`; each starts `L` or has equal adjacent turns. Hence width four with primitive
diagonal drift is impossible at every period.

### 38.7 Exact finite fixed-drift exclusion through m=9

`code/java/WidthFourSearch.java` enumerates the complete based macro automaton,
enforces ordinary same-physical-cell alternation, endpoint reachability, displacement
parity, and extremal-residue uniqueness, then checks growth/odd-class equality and
the exact start-`R` alternating P3 words. Its SHA-256 during these runs was
`51FE7C1DC12B00FD7065ACB78F1F0A6E8FBDCFC1DE4FEED643F602F30A22D820`.

The theorem `P<=7m` makes each fixed `m` range finite. All admissible periods for
`m=1,...,9` have zero hits. The final targeted `m=9` rows were:

| P | nodes | structural leaves | hits |
|---:|---:|---:|---:|
| 39 | 52,741,069 | 5,872 | 0 |
| 41 | 89,958,533 | 1,955 | 0 |
| 43 | 152,553,888 | 1,397 | 0 |
| 45 | 256,588,299 | 163 | 0 |
| 47 | 427,374,080 | 180 | 0 |
| 49 | 703,623,405 | 0 | 0 |
| 51 | 1,144,886,139 | 9 | 0 |
| 53 | 1,841,115,126 | 0 | 0 |
| 55 | 2,930,455,631 | 0 | 0 |
| 57 | 4,623,723,311 | 0 | 0 |
| 59 | 7,245,814,177 | 0 | 0 |
| 61 | 11,294,947,821 | 0 | 0 |
| 63 | 17,532,472,230 | 0 | 0 |

The existing all-highway computation supplies `P<=24`; the unrestricted width-four
run supplies `25<=P<=38`; the table supplies every remaining admissible odd period.
This proves only `1<=m<=9`, not unbounded `m`.

### 38.8 Spatial block form of chronological P3

For a fixed line and residue `r mod m`, write an occupied physical cell as
`ell=r+qm` and let `B_q` be its ordinary phase-ordered turn word. An occurrence at
phase `i` has stabilized key `i-Nq`. If `q'>q`, every key from `q'` is smaller than
every key from `q`; therefore the stabilized class word is the concatenation of the
nonempty `B_q` in strictly decreasing `q`.

P3 is thus equivalent to: each block alternates; the rightmost block starts `R`; and
neighboring nonempty blocks have different boundary turns. Equivalently, with
`R=0,L=1`,

```
first(B_q) = parity(number of visits in all blocks strictly to the right of q).
```

This isolates the unexploited ordering content at spatial joins. It is exact and
all-period, but no global contradiction has yet been extracted from it.

Equivalently, let `chi(q)=#R(B_q)-#L(B_q)`. Every alternating even block has charge
zero; an odd block has charge `+1` or `-1` according to its first turn. The join
propagation therefore makes the nonzero charges, from right to left,
`+1,-1,+1,-1,...`. Every right-hand prefix of a translation class consequently has
charge in `{0,1}`. The full-class sum is only the previously known odd-class
identity; the prefix bound is the genuinely ordering-sensitive strengthening. The
current analytic target is to localize the width-four flow/displacement identities
at a longitudinal cut and combine them with these prefix bounds.

Audit note: the alternating-list part was already present in Lean as
`StabilizedP3Word.raw_prefix_bound` in `P3Endpoint.lean`. What is new here is the
geometric proof that the formal decreasing levels are exactly the right-to-left
physical-cell blocks in the width-four frame. Do not market the prefix algebra itself
as a new theorem.

### 38.9 Independent checks and discarded routes

Lean 4.32.0 checks the six-mask enumeration, the even-fiber growth bound, the
arithmetic implication `P+8x<=7m`, parity, `N<=7g`, and primitive `P=7` in
`lean/Langton/WidthFour.lean`. The current source hash is
`E0A4C88394FC5D08991F4C9432564B6AEDF7EBC03994A01B24BAC5CBDDF886B7`; the build uses
only standard Lean axioms and contains no `sorry` or `admit`. The macro geometry is
still a paper hypothesis, not an end-to-end formalization.

The independent Z3 model returned exact UNSAT at `(m,P)=(1,7),(2,6),(2,8),(2,10),
(3,9)` and `(9,9),(9,11),(9,13),(9,15)`. It timed out at `(2,12),(9,17),(9,19)`;
those timeouts were never counted as exclusions.

Three failures were retained:

1. `starts R` alone is false as a universal obstruction. At ant period 50, three
   structural cycles start `R` in every class but fail inter-block alternation.
2. Deleting `LN->LN` and `US->US` as alleged boundary-`L` moves was wrong: the pair
   label had been read backwards; both boundary turns are `R`.
3. An incremental P3 arithmetic prune was sound but slower. At `(9,57)` it reduced
   nodes by only `0.054%` and increased time from `329.221` to `410.472` seconds, so
   it was removed.

A fourth attempted reduction localized the new prefix-charge theorem. The integer
model `code/python/width4_prefix_flow.py` imposes vertexwise macro-flow conservation,
`P<=7m`, extremal uniqueness, positive growth, every prefix charge in `{0,1}`, and a
rank certificate making the nonzero support weakly connected. It is UNSAT for
`m=1`, but SAT for `m=2` at `(P,g)=(12,4)` and for `m=3` at `(19,8)`. The `m=2`
support has an Euler ordering `b f i h d d c b h d d c`; replaying it produces two
successive `R` turns at physical cell `(1,0)`. Hence aggregate connected flow plus
all spatial-prefix charges still forgets the order in which each cell's turns occur.
This is a countermodel to the proposed linear proof, not a highway.
The strengthened `m=4` query with `P>=5m+7` ran for roughly fourteen CPU minutes
without resolving and was terminated; it contributes no mathematical result.

The period bound nevertheless gives a different finite-reduction foothold. For each
of the `m` cut residues modulo longitudinal translation, count crossings of every
lifted cut in that residue. The quotient path winds once, so each count is positive
odd, and the counts sum exactly to `P<=7m`. If `L` cuts have count
at most seven, the others have count at least nine, so
`7m >= L+9(m-L)` and `L>=m/4`. A positive density of cuts therefore has a crossing
sequence of length at most seven over a finite alphabet. A standard crossing-sequence
pumping argument would try to splice between two identical such cuts and reduce
`m`. The density statement is proved (its arithmetic endpoint is checked in Lean),
but the necessary splice theorem preserving tape colours and the P3 seed/wake
relation is not. It is a concrete future route, not a present decidability claim.

The exploratory `width4_crossing_signatures.py` confirms the expected mechanism on
the explicit endpoint near-model. For `m=10`, modular cut residues `3,...,9` all carry the same five
events `d(+),c(-),b(+),h(-),d(+)`; removing the slab between consecutive equal cuts
deletes one repeated five-transition block and produces the `m-1` family. This only
validates the naive signature on a known pumpable word. Arbitrary P3 traces still
require the decorated splice theorem.

Correction made immediately: the first checker used only absolute cuts `0,...,m-1`
and omitted overshoot crossings. The correct signature groups every lifted cut
`r+qm+1/2` by residue `r`; in the endpoint example, the six overshoot steps at cuts
`10,11,12` augment residues `0,1,2`. All density and pumping statements above use
this corrected modular definition.

### 38.9a Candidate splice theorem and explicit finite cutoff

The corrected signature requires a second ordering correction. A phase `i` event on
lifted cut `r+qm+1/2` occurs at the representative cut at stabilised time `i-Pq`.
Thus each modular signature is sorted by `i-Pq`, exactly as cell-class P3 words are.
The earlier raw-phase output is superseded.

The proof draft now says: if two residues have equal decorated signatures (macro
source/target states and the two turns), delete the slab between them in every
translated period and pair boundary crossings in stabilised order. Equal transition
types make each glued crossing legal and preserve the turn history of every retained
cell. The periodic compression `phi` obeys `phi(ell+m)=phi(ell)+m'`, so retained
old classes modulo `m` biject with new classes modulo `m'` and their P3 words are
unchanged. The exact criterion then gives a smaller-drift width-at-most-four highway;
even width and the width-two exclusion make it width four.

This is a specialised form of the classical one-tape crossing-sequence cut-and-paste
lemma (Hennie; see Jeandel, STACS 2014, Section 3.3). It still requires independent
audit of the equivariant infinite deletion and P3-class bijection before use in the
paper.

First adversarial issue discharged in the draft: a negative stabilised key does not
license a negative-time ant step. Move the representative cuts to `r+Qm+1/2` with
`Q` larger than every lift used in the period. Its events occur at actual forward
times `QP+(i-Pq)` in the same order. Splice only that far-ahead periodic tail, then
apply P3 to the extracted smaller-drift word to construct a fresh finite seed. This
avoids importing a formal backward orbit or infinite wake.

A second precision improvement replaces the informal atomic-macro splice by a
literal deterministic one-tape encoding. A tape cell is one longitudinal column
with its five colour bits; finite control stores transverse line and heading;
vertical ant moves are stay-put moves. Equality of decorated macro signatures
therefore implies equality of ordinary control crossing sequences. The classical
splice induction preserves every read and write on both retained halves, including
the cells adjacent to the new boundary.

The infinitely many periodically repeated slab deletions are defined as a finite-
time direct limit. Start beyond the finite seed. Every finite computation prefix
meets only finitely many slabs and hence follows from finitely many ordinary
disjoint splices; determinism makes the prefixes compatible. The compressed
initial tape is still finite support because the entire deleted far tail was blank
at time zero. The old `(2P,m)` tail translation becomes spatial translation by
`m'=m-(s-r)`. The last serious self-audit point is proving that this equivariance
advances the oriented spliced event path by a fixed positive finite event count;
the nonempty net-right crossing sequence at a retained cut is the proposed
certificate. The cutoff remains conditional until an independent referee checks
this point.

The direct one-tape encoding sharpens the alphabet. At a horizontal crossing, the
finite control immediately after the move is its direction and the even transverse
destination line `0`, `2`, or `4`. Hence equality of projected control signatures
already suffices for the classical splice; the macro transition type is unnecessary
decoration. If the splice lemma survives, minimality makes the low control
signatures distinct. A transition-table audit further shows two, not three, possible
destination lines per fixed direction: rightward gives `2` or `4`, leftward gives
`0` or `2`. There are therefore at most `2+2^3+2^5+2^7=170` low signatures, while
at least `m/4` cuts are low, giving `m<=680`. Using the entire average-length budget
is sharper: short signatures contribute at most
`6*2+4*8+2*32=108` units below length seven, while each signature of length at least
nine costs two or more. Thus there are at most 54 long signatures and
`m<=2+8+32+128+54=224`. Together with `P<=7m`, width-four existence becomes a finite decidable
problem. This is a candidate finite-reduction theorem, not an all-width-four
exclusion and not a result yet approved for the manuscript.

Extremal singleton rigidity sharpens the same count again. In a length-`2n+1`
signature, at most one rightward crossing may land on top line `4`, and at most one
leftward crossing may land on bottom line `0`; repetitions would be two phases in
one extremal class. All other landings are on the centre line. Thus the capacity is
at most `(n+2)(n+1)`, giving `2,6,12,20` at lengths `1,3,5,7`. Their below-seven
budget is `6*2+4*6+2*12=60`, paying for at most 30 length-at-least-nine signatures.
The strongest current conditional cutoff is therefore `m<=2+6+12+20+30=70`.

Finally, Section 37.5's sentence that fixed width is automatically finite-state is
withdrawn. A finite alphabet on an unbounded tape can retain unbounded memory. Only
the odd-skeleton SFT and each fixed-drift range are currently proved finite.

### 38.10 Honest distance from the conjecture

The session produced a genuine all-period period bound at fixed drift, an all-period
primitive-drift exclusion, and an exact exclusion for nine drift magnitudes. It did
not prove all-width-four exclusion, highway uniqueness, or the universal convergence
conjecture. The next proof target is a global invariant for the spatial block joins
in 38.8; the empirical but unproved endpoint `P=5m+6` may help locate it, but it must
not be cited as a theorem.

An exact endpoint near-model explains why that empirical bound would be sharp. For
every `m>=3`, the macro word

```
(b q f j d d c) (b h d d c)^(m-2) (b h d d e f i h c)
```

has drift `m`, period `5m+6`, growth four, ordinary physical-cell alternation, and
distinct extremal residues. It is not a P3 counterexample: the lower-odd-line cells
`ell=m+1` and `ell=1` have blocks `LR` and `LRL`, whose stabilized concatenation
`LRLRL` starts `L`; the family also misses growth/odd-class equality. Thus it is a
sharpness witness only for the ordinary-alternation/extremal structural layer.

The `m=10` continuation confirmed ten such leaves at `P=56=5m+6`; none passes the
odd-class identity. Rows `P=58` and `P=60` have no structural leaf; the latter
visited `19,138,313,024` nodes in `1108.564` seconds. All completed even rows
`40,42,...,66` have zero P3 hits. The newly completed `P=62` row visited
`30,238,836,043` nodes in `1680.264` seconds and had no structural leaf. Workers
`P=64` then completed `47,442,673,612` nodes in `2738.439` seconds with no structural
leaf. Workers `P=66,68,70` continue under the user-extended 19:00 research cutoff and contribute
no result until individually completed. Subsequently `P=66` completed
`74,038,045,927` nodes in `3995.586` seconds with no structural leaf. The `P=68`
and `P=70` workers were stopped unfinished at 18:56:13 CDT and returned no completed
row, so both remain uncounted and the fixed-drift theorem remains `m<=9`.

### 38.11 Crossing-sequence graph form of the candidate splice

The remaining equivariance point in 38.9a has a finite graph formulation. Encode a
longitudinal column as a five-bit tape symbol and place the finite control sequence
at each boundary. Consecutive boundary sequences plus the initial column symbol form
an edge in the classical one-tape crossing-sequence graph. Beyond the finite seed
every symbol is all-white, and the old highway supplies a closed spatial walk of
length `m`. Equal projected control signatures `Gamma_r=Gamma_s` are equal vertices;
delete the intervening closed subwalk to obtain length `m'=m-(s-r)`.

The actual infinite computation is still defined by finite splices, not merely by
the graph's existence statement: the first `K` repeated slabs give a genuine run,
and every finite prefix stabilises as `K` grows. In the limit, translation by one
shortened graph cycle sends each retained local column transcript and each `j`-th
crossing occurrence to its translate. It therefore preserves the successor relation
on the oriented tail event path. Any such map is `n -> n+k`; here `k` is finite and
positive because the spatial coordinate changes by `m'>0`. This proves eventual
translation by `(m',-m')`, subject to the remaining audit that no crossing sequence
can be truncated only at the infinite-limit stage. Finite-prefix stabilisation is
the proposed discharge. The result remains candidate until independent review.

The proposed discharge is now sharpened to monotonicity. At matched rightward
crossings the left cut occurs first; at matched leftward crossings the right cut
occurs first. The splice always jumps forward in the old chronology, so each new
farther splice only deletes events. A fixed retained crossing has a nonincreasing
natural event index and therefore stabilises, while the finite one-cut lemma ensures
it exists at every stage. Extra finite-index crossings likewise cannot appear only
in the limit. This removes the known truncation mechanism; independent review is
still required before the pumping theorem is promoted.

### 38.12 Candidate P32: the all-white width-four crossing graph is acyclic

The splice analysis exposes a stronger local obstruction. Encode a boundary
crossing state by direction and even destination line; direction is implicit in the
alternating index. For one initially white five-cell column, exact left/right
boundary sequences determine its entire read/write history. Extremal singleton
rigidity permits at most one rightward top landing and one leftward bottom landing
on each boundary.

An exhaustive finite-state recursion over the 32 column masks, entry state, and four
exceptional-event flags produces exactly 12 compatible all-white edges:

```
202       -> 4
4220222   -> 2, 202, 20222, 2022224
2042222   -> 2, 202, 20222, 2022224
202242222 -> 422, 42202, 4220222.
```

Only ten vertices occur. The graph is acyclic, with longest path
`202242222 -> 4220222 -> 202 -> 4`. Every width-four finite-seed highway would supply
an infinite path from the infinitely many initially white tail columns, a
contradiction. This is therefore a candidate all-period width-four exclusion.

`code/python/width4_crossing_graph.py` obtains the table both by an unbounded
finite-state generator (12 terminals, zero reachable entry cycles) and by pairwise
checking all 910 extremal signatures through length 25; the edge sets agree. It
then independently checks directed acyclicity and longest path three. SHA-256 is
`2AF99EDCBC355945B547AB1F80CAEE6927FA75D6C1C064C5ADC41D13B5FE3E33`.
The unbounded generator reaches 22 entry states, has maximum entry depth eight, and
finds no reachable entry cycle.
This was the pre-promotion status at the time of discovery: an independent audit
still had to verify the one-tape state projection, white/black turn convention,
boundary event indices, completeness of the exceptional flags, and repeated-state
logic.  Section 38.16 records the completed audit and repair.  The promoted
computer-assisted theorem upgrades the diagonal transverse lower bound from `W>=4`
to `W>=6`; widths six and eight remain open below the standard highway's width ten.

Lean separately checks the finite graph implication in
`lean/Langton/WidthFourCrossing.lean`: every listed edge lowers an explicit rank and
there is no four-edge chain. The source hash is
`548DF94E2B8B60CE23269153EE446CFF824AC1DB6AA1A41773F4E605205324FF`.
The file states plainly that it does not formalise completeness of the local
classifier.

A second implementation,
`code/python/verify_width4_crossing_graph_indep.py`, uses compass-letter headings,
set-valued black rows, and a separately written recursion, with no imports from the
search or crossing-graph modules. It reproduces exactly the same 12 edges. SHA-256:
`694C1178B00FA8AB929A5375255E53762C403DE02FC1D2958A4409EF9B84AFE0`.
The same verifier simulates the documented finite seed of the standard highway,
extracts far-cut sequences of lengths 31 and 21 at cuts 100 and 101, and exactly
replays the intervening initially white column. This checks the direction, landing
line, and boundary-index convention on a genuine highway of another width.

The wider-strip test supplies an exact boundary of the argument. A generic local
entry-state generator finds no cycle at width four, but at widths six and eight it
finds the reachable two-cycle
`({1,2},line 2,E) <-> ({1,3},line 2,W)` without consuming either extreme twice.
Thus the local state graph becomes recurrent as soon as another interior horizontal
line is available. This is not a highway counterexample; it is a counterexample to
extending the acyclic-column proof unchanged. Script:
`code/python/explore_even_width_crossing_cycles.py`, SHA-256
`760CD63D8CCC0292AD5FF2A3134CAE7A4E2CDD1AA16758527BFF5F706806F327`.

### 38.13 Manual bridge audit before manuscript promotion

I re-derived the direct argument from the lattice coordinates rather than from the
program output.  Put the normalised strip on transverse coordinates
`t=x+y in {0,1,2,3,4}` and use `x` as the longitudinal tape coordinate.  A north or
south step stays in one tape column; an east or west step crosses one tape boundary.
Immediately after any boundary crossing the destination transverse coordinate is
even.  Thus a rightward event has label `2` or `4`, and a leftward event has label
`0` or `2`; direction is recovered from the alternating position in the sequence.
This verifies that the projected label used by both classifiers is the complete
finite control needed to restart the deterministic within-column computation.

For a fixed far-ahead boundary, the ant is initially on its left and eventually on
its right.  Periodicity with positive longitudinal drift and a finite set of phase
offsets makes the number of its crossings finite.  Consequently its exact sequence
has positive odd length and alternates right, left, ..., right.  A repeated label
`4` in a rightward slot would enter the same top-extremal cell twice; a repeated
label `0` in a leftward slot would enter the same bottom-extremal cell twice.
Extremal-line rigidity forbids both repetitions.  These are exactly the four
boundary flags used by the generator (one top/right and one bottom/left event on
each side); no colour or chronological data are discarded inside the column.

At the start of the periodic tail only finitely many cells have been visited, and
the initial black support is finite.  Therefore all sufficiently far longitudinal
columns consist of five white cells and have never been touched.  The exact
crossing sequences at their consecutive boundaries give an edge of the classified
blank-column graph for every such column.  Infinitely many consecutive columns
would therefore give an infinite directed path.  Since the 12-edge graph has rank
at most three and every edge strictly lowers rank, this is impossible.

This audit identifies the precise computer-assisted boundary.  The mathematical
reduction from a width-four highway to an infinite graph path and the rank
contradiction are proofs on paper (the latter also in Lean).  The finite claim that
the 12 displayed edges are all compatible blank-column pairs is established by two
independent literal enumerators, not yet by an end-to-end Lean theorem.  The paper
must say this explicitly and call the result computer-assisted unless that last
enumeration is formalised.

### 38.14 Why the width-six local cycle survives the ordering test

The two-state recurrence reported in 38.12 is not merely an incidence artefact.
Write its states, suppressing unchanged extreme flags, as

```
A = (black rows {1,2}, enter row 2 east),
B = (black rows {1,3}, enter row 2 west).
```

From `A`, row 2 is black and turns `L`, sending the ant north to row 3; row 3 is
white and turns `R`, sending it east out of the column.  The new mask is `{1,3}`.
After an external return at row 2 from the right, state `B` turns `R` on the now
white row 2, goes north, then turns `L` on the now-black row 3 and exits west,
restoring mask `{1,2}`.  Thus both repeatedly used cells have alternating turn
histories (`...LRLR...` in opposite phases).  The cycle uses neither extremal line.

Consequently the width-four acyclicity proof fails at width six for a genuinely
chronological reason: one extra interior horizontal line supports a local rotor
oscillator that already respects ordinary same-cell alternation.  This is still
only a local transcript, not a global highway or a counterexample to the
finite-support conjecture.  Any width-six exclusion must couple neighbouring
columns or use the stabilised *start-with-R* ordering across translation classes;
extremal singleton flags plus per-cell alternation cannot suffice.

### 38.15 Research cutoff and frozen status

The user-extended research phase ended at 19:00:02 CDT on 21 July 2026.  At the
cutoff, both exact blank-column classifiers again returned the same twelve edges;
the primary generator reported 22 reachable states, maximum depth eight, and no
cycle, and the standard-highway convention replay passed.  The Docker-pinned Lean
4.32.0 build completed all 22 targets; the finite graph rank certificate compiled.
The `m=10` rows `P=68,70` had already been stopped unfinished at 18:56:13 and are
not results.  Manuscript work begins only after this checkpoint.

Frozen claim discipline for the rebuild:

- the universal finite-support highway conjecture remains open;
- the width-four result is a computer-assisted theorem only if the independent
  referee accepts the local-classifier completeness argument;
- Lean checks the twelve-edge rank consequence, not the classifier completeness;
- the rigorous fixed-drift exhaustive theorem remains `1<=m<=9`;
- widths six and eight, non-diagonal periodic highways, and universal entrance are
  not settled.

### 38.16 Post-cutoff independent referee and promotion audit

After the manuscript rebuild, an independent adversarial model re-derived the
coordinate projection, turn convention, four exceptional flags, no-cycle recursion,
and the passage from infinitely many untouched columns to an infinite boundary-graph
path.  It accepted all five mathematical points and reran both Python classifiers:
12 edges, 22 reachable entry states, maximum depth eight, no local cycle, longest
graph path three, and a successful standard-highway convention replay.

The referee found one real precision error in the first rebuilt manuscript.  The
blank-column lemma said that directions alternate and the extreme labels occur at
most once, but omitted the hypothesis that rightward destination labels lie in
`{2,4}` and leftward labels in `{0,2}`.  Without it the literal statement was false;
for example `(3,1,4) -> (4)` is compatible with a blank column but lies outside the
width-four HV geometry.  The global theorem already derived the even-label
restriction, so its argument was salvageable.  Both lemma statements now include
the restriction explicitly.  The companion proof was also repaired to invoke finite
black support, not only finite past visitation, when choosing the untouched tail.

The same referee identified a future-divergence hazard in Lean: the twelve edges
were duplicated as a list and as a proposition.  `BlankEdge` is now defined as
membership in `blankEdges`, and `blankEdge_cases` proves the explicit case split.
The Docker-pinned Lean 4.32.0 build again completed 22/22 targets.  Current Lean
source SHA-256 is
`548DF94E2B8B60CE23269153EE446CFF824AC1DB6AA1A41773F4E605205324FF`.

Promotion status: the result is accepted in the manuscripts as a
**computer-assisted all-period exclusion of diagonal transverse width four**.  It is
not called a fully formalised theorem: completeness of the 12-edge local classifier
is supported by two independent exact enumerators, while Lean checks membership in
that displayed edge list and the rank/acyclicity consequence.
