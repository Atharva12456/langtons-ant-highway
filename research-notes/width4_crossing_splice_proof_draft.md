# Width-four crossing-sequence splice: proof draft

**Date:** 21 July 2026  
**Status (updated after release audit):** This draft has two distinct results, at
different maturity levels — do not conflate them.
- The **all-white blank-column crossing graph is acyclic** (Section 9 here) was
  **promoted** after the §38.16 referee audit to a stated result: it is
  Lemma 9.4 (blank-column classification) and Theorem 9.5 (no width-four highway,
  hence W>=6) in `paper/main.tex`, computer-assisted with a Lean-checked rank
  consequence. Where this draft still says "candidate" about that acyclicity claim,
  read it as superseded by the promoted theorem.
- The **m<=70 splice / pumping cutoff** (the draft's primary subject) remains a
  **candidate** decidability route and is NOT claimed in the paper. Its Lean endpoints
  are named `drift_le_candidate_*_cutoff` precisely to mark them as unproven kernels.
**Purpose:** reduce all width-four periodic highways to a finite drift range

## 1. Macro trace and notation

Normalize the drift to `(m,-m)`, `m>0`, and use transverse lines `0,...,4`.
A width-four trace has a macro presentation

```
(s_i, ell_i) --tau_i--> (s_(i+1), ell_(i+1)),   0<=i<P,
```

where `s_i` is one of `LN,LS,UN,US`, every `tau_i` is one of the twelve transitions
in `WidthFourSearch`, and `ell_(i+1)-ell_i` is `+1` or `-1`. After a cyclic phase
choice, `(s_0,ell_0)=(LN,0)` and `(s_P,ell_P)=(LN,m)`. The ant period is `2P`.

Each transition crosses exactly one longitudinal cut. It also turns one odd-line
cell in its source column and one even-line cell in its target column. Thus a
transition type specifies:

- source and target macro states;
- crossing direction;
- the two transverse endpoint lines; and
- the two turn symbols.

There are six transition types in each direction.

## 2. Infinite lift and the correct cut order

Extend the geometric macro path formally by translation: period `n` uses phase `i` at
`ell_i+nm` and global macro time `i+nP`. This is a continuous bi-infinite geometric
path. Finite-seed realizability is imposed only in forward time, so the proof must
not use a formal negative-period turn as though it were an executed ant step.

For cut residue `r in {0,...,m-1}`, a phase-`i` transition may cross the lifted cut

```
r + qm + 1/2.
```

Translate that event by `-q` periods to the representative cut `r+1/2`. Its global
time there is

```
kappa = i - Pq.
```

The decorated crossing signature `Sigma_r` is the list of transition types crossing
the cut orbit `r mod m`, sorted by `kappa`. Raw phase order is wrong when the trace
overshoots the fundamental interval.

Its **control projection** `Gamma_r` retains only the crossing direction and the
even transverse line on which the ant lands.

Because the lifted path crosses a fixed representative cut continuously, directions
in `Sigma_r` alternate and begin and end with `+`. Hence `|Sigma_r|` is positive odd.
Every macro phase crosses one cut orbit, so

```
sum_r |Sigma_r| = P.
```

To realise this signature in the genuine forward orbit, choose `Q` larger than every
lift index `q` appearing in the one-period trace. At the far-ahead physical cut
`r+Qm+1/2`, the same event occurs in period `Q-q` at actual time

```
QP + (i-Pq) >= 0.
```

Thus `Sigma_r` is the actual chronological crossing sequence at every sufficiently
far representative cut, shifted by a constant time. No backward extension of the
finite-seed dynamics is used.

Also choose the splice start beyond the finite seed and with a backtracking margin.
The one-period set `{ell_i}` has a finite minimum, so after a sufficiently large
period index the forward trace never returns to the uncompressed prefix. The tail
surgery can therefore be separated from the untouched finite prefix by a cut which
is crossed for the last time before surgery begins.

## 3. Density of short signatures

The proved width-four bound is `P<=7m`. Let `L` be the number of residues whose
signature length is at most seven. Non-short signatures have positive odd length at
least nine. Therefore

```
7m >= P >= L + 9(m-L) = 9m-8L,
```

so `m<=4L`. The final arithmetic implication is theorem
`many_low_crossing_cuts` in `lean/Langton/WidthFour.lean`.

## 4. Candidate splice lemma

### Statement

If `Gamma_r=Gamma_s` for two distinct cut residues, a P3-valid width-four trace can
be replaced by a P3-valid trace of strictly smaller positive drift and transverse
width at most four.

### Direct one-tape encoding

There is a useful way to avoid treating a two-turn macro transition as an atomic
black box.  Regard the longitudinal coordinate `ell=x` as a one-dimensional tape
coordinate.  One tape symbol is the five-bit colour vector of the cells on
transverse lines `0,...,4` in that column.  The finite control stores the transverse
line, compass heading, and (if a conventional Turing-machine model without a
stay-put move is desired) one auxiliary phase bit.  A vertical ant move is a
stay-put tape move and a horizontal ant move crosses one tape boundary.  This is a
deterministic one-tape machine with alphabet of size at most `2^5` and finite
control.  A finite black ant seed is a finite nonblank tape.

For a tape boundary `u+1/2`, record immediately after each crossing the crossing
direction and finite-control state.  Call this the **control crossing sequence**.
The decorated macro type used in `Sigma_r` determines this datum: it specifies the
source and target odd-track states, direction, even endpoint line, and both turns.
In fact `Gamma_r` is exactly the control crossing sequence.  The direction is the
horizontal heading `E` or `W`. A rightward move lands on line `2` or `4`, and a
leftward move on line `0` or `2`; these are all the finite-control data immediately
after the crossing. Equality of `Gamma`
therefore suffices.  The decorated alphabet is a strict over-refinement.

The ordinary crossing-sequence splice lemma now applies without an extra assumption
about endpoint colours.  If two boundaries of one deterministic computation have
the same control crossing sequence, keep the initial tape to the left of the first
boundary and to the right of the second, delete the intervening cells, and glue.
Between successive crossings the new computation copies the appropriate old
half-tape computation.  At the next boundary crossing the equal control state lets
it switch halves.  Induction on the crossing number proves that every read, write,
turn, and move is legal.  This is the precise content needed here from the classical
one-tape crossing-sequence lemma.

Equivalently, form the classical crossing-sequence graph.  A vertex is a finite
control crossing sequence; the column between two consecutive boundaries is an
edge labelled by its initial five-bit tape symbol, and the two endpoint sequences
are compatible exactly when the deterministic local column history exists.  Far
ahead of the finite seed every edge label is the all-white symbol.  The old
width-four highway supplies a spatially periodic closed walk of length `m` in this
graph, with vertex at cut residue `r` equal to `Gamma_r`.  If
`Gamma_r=Gamma_s`, the portion between the two equal vertices is a closed subwalk;
deleting it leaves a closed walk of length `m-(s-r)`.  This graph picture is the
finite combinatorial core of the simultaneous splice below.

### Periodic spatial deletion

Orient the residue circle so `0<=r<s<m`, put `Delta=s-r`, and set `m'=m-Delta`.
Choose the far-ahead `Q` above. For every integer `q>=Q`, delete the slab of
longitudinal columns strictly between the
lifted cuts

```
r+qm+1/2  and  s+qm+1/2.
```

Let `S` be the remaining columns. The order-preserving compression `phi:S->Z`
satisfies

```
phi(ell+m)=phi(ell)+m'.
```

Choose `Q` so far ahead that the original finite seed lies wholly to the left of
the first deletion.  The compressed initial tape therefore still has finite
nonblank support: the operation deletes infinitely many columns, but every deleted
or shifted far-tail column is initially blank.

The infinitely many splices are defined by a finite-time direct limit.  Up to any
fixed time, a one-head computation visits only finitely many columns, so only
finitely many deleted slabs can affect that prefix.  Apply the ordinary splice
lemma to those finitely many disjoint slabs.  Increasing the finite set cannot
change the already constructed prefix, by determinism and locality.  The compatible
prefixes therefore define one infinite legal computation on the compressed finite
seed.  This is stronger and cleaner than postulating an infinite pre-existing wake.

There is also a monotonicity proof ruling out truncation at infinity.  For cuts
`A<B`, the matching rightward crossing occurs at `A` before it occurs at `B`, while
the matching leftward crossing occurs at `B` before it occurs at `A`.  Each splice
therefore jumps forward in the old chronological execution and deletes an interval;
it never inserts, duplicates, or reverses events.  After adding the `(K+1)`-st
farther splice, the retained event list is a subsequence of the `K`-splice event
list.  The index of any fixed retained crossing occurrence is consequently a
nonincreasing natural number and eventually stabilises.  Every prescribed occurrence
exists in every finite splice by the one-cut lemma, so none can disappear only in
the limit.  Conversely, any alleged extra limit crossing would occur at a finite
event index and hence already occur in a sufficiently large finite splice.  Thus the
limit has exactly the stated crossing sequences.

### Equivalent macro description

At each deleted slab, pair its left- and right-boundary crossings in the order given
by the stabilised control signatures. The directions alternate, so a rightward entrance is
paired with the corresponding rightward exit, and similarly in the reverse
direction.

The literal one-tape proof switches half-computations immediately after the
horizontal crossing and uses only equality of destination line and direction.  It
then reads the retained destination-column symbol and continues by the actual ant
rule. Regrouping this legal ant computation into pairs recovers transitions in the
twelve-entry macro table.

When the stronger decorated signatures agree, there is also a direct macro
visualisation: equality gives the same source/target state and the same odd/even
endpoint lines and turns, so one may replace the two boundary events and intervening
slab segment by one transition across the glued boundary.

- On a rightward splice, retain the odd-cell turn from the old left event and the
  even-cell turn from the old right event.
- On a leftward splice, retain the odd-cell turn from the old right event and the
  even-cell turn from the old left event.

Under that stronger equality the combined pair is exactly the common legal macro
transition type. This paragraph is only a visualisation; legality for the weaker
control-signature hypothesis comes from the one-tape induction, not from equality
of the turn pairs.

This is exactly the one-tape splice above, expressed in the two-turn macro language.
The one-tape encoding supplies the formal intermediate states and removes any need
to assume that an atomic two-cell update can simply be split.

### Eventual periodicity and the new drift

Beyond the untouched finite prefix, both the original executed history and the
family of deleted slabs are invariant under translation by one old period:

```
(time, ell) -> (time+2P, ell+m).
```

After compression the same spatial symmetry is `ell -> ell+m'`.  The direct-limit
splice is equivariant under this symmetry.  More explicitly, translate each retained
local column transcript and its ordered boundary-crossing occurrences by one new
closed-walk cycle.  Compatibility identifies the same local read/write transcript,
and the `j`-th occurrence at a boundary maps to the `j`-th occurrence at its
translate.  This defines a successor-preserving self-map of the oriented tail event
path.  A successor-preserving self-map of a one-way discrete path has the form
`n -> n+k`; here `k` is finite, and it is positive because the map changes the
longitudinal coordinate by `m'>0`.  Write `k=2P'` (it is even because the translated
state returns to the same odd-track macro phase).  Hence the symmetry maps the event
path to itself forward by a fixed positive finite number `2P'` of ant events.
Starting at a tail event after the first deletion gives a repeating finite word
whose heading/control state resets and whose displacement is `(m',-m')`.

The positivity and finiteness of `P'` can also be seen at one retained cut: its
control crossing sequence is nonempty and has net one rightward crossing.  Between
that cut and its translate by `m'` the spliced head executes a finite nonempty
segment, and equivariance repeats that segment.

## 5. Preservation of local turns and P3

Every physical cell outside the deleted slabs maps to one compressed cell.  In the
one-tape proof, a retained column is always run by one of the two original half-tape
computations.  Induction on successive boundary crossings shows that its reads and
writes occur in exactly their old order.  Thus each retained ant cell has exactly
its old chronological turn word, including the two cells adjacent to a glued
boundary.  This establishes, rather than assumes, the boundary-history assertion in
the macro description.

On the periodic tail, the compression respects translation. Retained residues modulo `m` map
bijectively to residues modulo `m'`; explicitly, for retained cells,

```
ell_2 = ell_1 (mod m)  iff  phi(ell_2)=phi(ell_1) (mod m').
```

Since `phi` is increasing, it preserves the front-to-back order of physical-cell
blocks in every translation class. Thus the stabilized word of every new class is
identical to the stabilized word of its old retained class. P3 start-`R` and
alternation are preserved.

The direct-limit construction already supplies a finite seed.  Equivalently, apply
the exact periodic-trace criterion directly to the extracted tail word: the class
words above are unchanged, so P3 holds and the criterion constructs a fresh finite
seed without an infinite black background.  The trace is nonempty and has nonzero
diagonal drift.  Its transverse width is even and at most four; nonzero diagonal
motion cannot have width zero, and width two has already been excluded.  Hence the
result is again width four.

## 6. Explicit candidate cutoff

Choose a hypothetical width-four highway with minimal drift `m`. By the splice
lemma, all `Gamma_r` are distinct. A short signature has odd length `1,3,5`, or `7`.
At every event its direction is fixed by alternation, and the destination even line
has two geometrically possible values. Therefore the number of short control signatures is at most

```
F = 2 + 2^3 + 2^5 + 2^7 = 170.
```

Since `L<=F` and `m<=4L`,

```
m <= 680.
```

The full average-length budget improves this.  Let `n_k` count signatures of length
`k` for `k=1,3,5,7`, and let `n_+` count the remaining signatures, each of length at
least nine. Distinctness gives

```
n_1<=2,  n_3<=8,  n_5<=32,  n_7<=128.
```

Relative to average length seven, the maximum deficit supplied by the short
signatures is

```
6*2 + 4*8 + 2*32 = 108.
```

Every long signature costs at least two units above seven, so `n_+<=54`. Hence the
stronger, counting-optimal bound is

```
m <= 2+8+32+128+54 = 224.
```

Extremal singleton rigidity improves the signature capacities. In a signature of
length `2n+1`, there are `n+1` rightward slots and `n` leftward slots. The exceptional
rightward landing on top line `4` can occur at most once: two such phases would lie
in the same top extremal translation class. Likewise the exceptional leftward
landing on bottom line `0` can occur at most once. All other landings are on line
`2`. Hence the number of signatures is at most

```
(n+2)(n+1),
```

the product of the choice of no top event or one of `n+1` slots and the choice of no
bottom event or one of `n` slots. At lengths `1,3,5,7` the capacities are therefore
`2,6,12,20`. Their maximum deficit below average length seven is

```
6*2 + 4*6 + 2*12 = 60.
```

Thus there are at most 30 signatures of length at least nine, and the strongest
present counting bound is

```
m <= 2+6+12+20+30 = 70.
```

For each fixed `m`, `P<=7m` makes exact word enumeration finite. The candidate splice
lemma would therefore prove that width-four existence is decidable by a finite
search. It does not prove that no width-four highway exists.

The cutoff arithmetic is checked by
`drift_le_candidate_extremal_control_cutoff` in Lean. The cruder bounds `224`, `680`
and the older decorated `1151736` remain valid but are superseded. The splice itself
is not formalized.

## 7. Evidence and sources

`code/python/width4_crossing_signatures.py` implements the stabilized key, both
signature projections, and checks that modular signatures partition all macro phases and alternate directions. On the
explicit endpoint near-model with `m=10`, cut residues `3,...,9` have identical
five-event signatures `d(+),c(-),b(+),h(-),d(+)`; deleting a slab removes one repeated
five-transition block and yields the `m-1` family.

The classical information-exchange statement appears in Emmanuel Jeandel,
*Computability of the entropy of one-tape Turing machines*, STACS 2014, Section 3.3,
following F. C. Hennie's crossing-sequence method. Jeandel states that equal crossing
sequences allow the tape to be cut at one boundary and pasted to the shifted tape at
another while preserving the machine's behavior.

## 8. Adversarial audit checklist

Before promotion, a referee must try to break each of these points:

1. Does the `i-Pq` order exactly equal chronological order at a representative cut
   in the translated lift?
2. Does equal decorated signature pair entrances/exits of every periodically deleted
   slab without a lift-index mismatch?
3. Can the two-cell macro update always be represented by the claimed boundary
   splice, or is an additional tape symbol/state needed in the signature? Proposed
   discharge: use the explicit five-bit-column one-tape encoding above; decorated
   macro equality over-refines the ordinary control crossing sequence.
4. Is every retained cell's turn history unchanged, including the two cells adjacent
   to a glued boundary?
5. Is the translation-class bijection modulo `m` versus modulo `m'` exact?
6. Does finite-support realizability survive periodic compression without importing
   an infinite black background? Proposed discharge: start all deletions beyond the
   finite seed, define the simultaneous splices as a finite-time direct limit, and
   independently apply the exact criterion to the extracted tail word.
7. Is positive growth guaranteed after a splice that deletes all visits to an old
   extreme line?
8. Does cyclic choice of time zero preserve the based macro assumptions used by the
   width-four reduction?

Until all eight are discharged, `70` is a candidate cutoff, not a theorem of
the paper.

## 9. Stronger candidate: the all-white crossing graph is acyclic

The pumping argument led to a direct local classifier which, if its finite
enumeration survives audit, excludes width four completely and makes the cutoff
unnecessary.

Choose a longitudinal column beyond the finite initial seed. Its five strip cells
are initially white. Let `u` and `v` be the control crossing sequences at its left
and right boundaries. Directions are implicit: positions `0,2,...` are rightward
and `1,3,...` leftward. Store only the destination even line. Extremal singleton
rigidity gives at most one `4` in a rightward slot and at most one `0` in a leftward
slot of each boundary sequence.

The column compatibility test is deterministic. Start with the first left-boundary
entry, toggle the indicated cell, turn, and follow vertical moves within the column
until the next horizontal exit. Match that exit against the next event of the
appropriate boundary sequence. If the head returns, consume the next entry event
from the same boundary and continue. The column has only five colour bits. Tracking
those bits, the current entry state, and the four flags recording whether each
boundary has already used its exceptional top/bottom event gives a finite exhaustive
recursion.

Writing a sequence by concatenating its line numbers, the complete list of
all-white compatible directed edges is

```
202       -> 4
4220222   -> 2, 202, 20222, 2022224
2042222   -> 2, 202, 20222, 2022224
202242222 -> 422, 42202, 4220222.
```

There are exactly 12 edges on 10 occurring vertices. The graph is acyclic; its
longest directed path is

```
202242222 -> 4220222 -> 202 -> 4,
```

of length three.

Any finite-support width-four highway has infinitely many initially white columns
ahead of its seed. Every adjacent pair of their exact boundary crossing sequences
must be one of the twelve edges above, producing an infinite directed path in this
finite graph. No such path exists. Therefore the finite table implies:

> **Candidate theorem.** No finite-support periodic Langton highway has transverse
> width four.

`code/python/width4_crossing_graph.py` independently obtains the table in two ways:
pairwise checking of all extremal signatures through length 25, and an unbounded
finite-state generator. The pairwise and generated edge sets agree. It then checks
graph acyclicity and longest path three. The unbounded generator reaches 22 entry
states, has maximum entry depth eight, and
finds no reachable entry cycle. Source SHA-256:
`2AF99EDCBC355945B547AB1F80CAEE6927FA75D6C1C064C5ADC41D13B5FE3E33`.

The key audit obligations are: the crossing state must really be only direction and
destination line; the local simulator's turn convention and left/right event
indices must match the ant; the four exceptional-event flags must exactly encode
extremal singleton rigidity; and the unbounded recursion must treat repeated states
soundly. Until those are checked independently (preferably also formalised), this
remains a candidate theorem rather than a manuscript result.

`lean/Langton/WidthFourCrossing.lean` separately records the twelve-edge table and
proves that every edge lowers the displayed rank, hence no four-edge chain exists.
Its SHA-256 is `548DF94E2B8B60CE23269153EE446CFF824AC1DB6AA1A41773F4E605205324FF`.
This formalises graph acyclicity, not exhaustiveness of the Python local classifier.

`code/python/verify_width4_crossing_graph_indep.py` is a separately written literal
verifier using compass-letter headings and a set of black rows; it imports none of
the search or crossing-graph code and reproduces the same 12 edges. SHA-256:
`694C1178B00FA8AB929A5375255E53762C403DE02FC1D2958A4409EF9B84AFE0`.
As a convention check, it also simulates the documented finite seed of the genuine
standard highway, extracts crossing sequences at far cuts 100 and 101, and exactly
replays the intervening initially white column (sequence lengths 31 and 21).

## 10. Current self-audit status (18:23 CDT)

The direct one-tape encoding discharges the earlier ambiguity about splitting a
two-cell macro update and gives a local proof of finite-support preservation.  The
crossing-sequence graph and the successor-preserving event-path argument now give an
explicit proof of the equivariance step.  The chronological-subsequence monotonicity
argument rules out truncation or creation of crossings at the infinite-limit stage.
All eight listed issues now have proposed discharges in this draft, but no manuscript
claim should depend on the lemma until an independent referee has checked those
discharges adversarially.
