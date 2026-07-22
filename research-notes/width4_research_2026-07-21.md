# Width-four research log - 21 July 2026

## Scope and status

**Current status after the post-cutoff audit.**  The direct blank-column result in
this log was promoted to a computer-assisted theorem: no diagonal finite-support
periodic highway has transverse width four.  Two independent exact enumerators
certify the complete 12-edge local graph, and Lean checks its rank consequence.
Journal \S38.16 records the referee-discovered label-hypothesis repair and the exact
formalisation boundary.  The time-stamped prose below preserves the discovery process
and therefore sometimes says ``candidate'' or ``not yet proved.''

This session follows the classification-side route, not the universal entrance
route.  The extremal-line theorem and the period-unbounded exclusion of transverse
width two were taken as established inputs.  The initial target was the next case,
transverse width four; at the beginning of the interval no all-period width-four
exclusion had yet been proved.

The manuscript is deliberately not being edited during the 90-minute research
interval.  This file records derivations and bounded experiments that may later be
promoted only after audit.

## Normalised geometry

Normalise a diagonal drift to

\[
d=(m,-m),\qquad m>0,\qquad t(x,y)=x+y,
\]

and shift the transverse range to the five lines `0,1,2,3,4`.  Lines 0, 2, and 4
have horizontal arrivals; lines 1 and 3 have vertical arrivals.  Extremal rigidity
makes every visited cell on lines 0 and 4 a once-used `R` cell.

Use the longitudinal coordinate `ell=x`.  Observe the ant only when it is on one of
the odd lines.  There are four states:

- `LN`: lower track, arrival north;
- `LS`: lower track, arrival south;
- `UN`: upper track, arrival north;
- `US`: upper track, arrival south.

Every macro move contains two ant turns, first at an odd-line cell and then at an
even-line cell.  Direct evaluation of the turn rule gives the complete transition
table:

| state | next state | delta ell | turns | even line |
|---|---|---:|---|---:|
| LN | LS | +1 | RR | 2 |
| LN | UN | +1 | RL | 2 |
| LN | LN | -1 | LR | 0 |
| LS | LN | -1 | RR | 0 |
| LS | LS | +1 | LR | 2 |
| LS | UN | +1 | LL | 2 |
| UN | US | +1 | RR | 4 |
| UN | UN | -1 | LR | 2 |
| UN | LS | -1 | LL | 2 |
| US | UN | -1 | RR | 2 |
| US | LS | -1 | RL | 2 |
| US | US | +1 | LR | 4 |

Completeness of the based reduction: choose any bottom-extremal visit and cyclically
start immediately after it.  Its forced `R` turn leaves the bottom line heading
north, so the new initial state is `LN`.  After one trace period the state is again
`LN`, translated by `m`; a top-line transition must occur because the width is four.
Conversely, every such closed macro path expands uniquely to a turn word in the
five-line strip.  No cyclic-minimum normalisation is used, so choosing the bottom
visit does not discard positive-growth cycles.

## A general width-growth sandwich

The residue theorem and extremal parity combine to give a useful all-period bound
that is not special to width four.

**Theorem (diagonal width-growth sandwich).** Let a finite-support periodic highway
have diagonal drift `d=(m,-m)` after normalisation, with `m>0`, growth `g`, and
transverse width `W`.  Then

\[
W\text{ is even},\qquad 2m\le g\le mW.
\]

**Proof.** Translation classes have the complete labels `(t,x mod m)`.  For a fixed
`x`-residue there is therefore at most one odd class on each of the `W+1` transverse
levels.  The signed residue identity says that the number of odd classes in that
fiber is positive and even.  Extremal rigidity says `W` is even, so `W+1` is odd and
the largest possible even fiber size is `W`.  Summing the upper bound over all `m`
residues gives `g<=mW`, because growth is the number of odd classes.  The lower bound
`g>=2m` is the strand-density bound.  QED.

Equivalently, every such highway satisfies `W>=g/m`, rounded upward to the next even
integer.  For the standard highway `(m,g,W)=(2,12,10)`, this alone gives only
`W>=6`; it is a genuine constraint but not a uniqueness argument.

## The six-mask odd-skeleton theorem

For `j in {0,1,2,3,4}` and `r in Z/mZ`, let

\[
o_{j,r}=1
\]

exactly when the translation class on level `t=j` with `x=r (mod m)` has odd
stabilised length.  The pair `(t, x mod m)` is a complete translation-class label:
equal labels imply that the coordinate difference is `(km,-km)=k d`.

**Theorem (six-mask constraint).** For every longitudinal residue `r`, the set

\[
M_r=\{j:o_{j,r}=1\}
\]

is one of

\[
\{0,2\},\ \{1,3\},\ \{0,4\},\ \{2,4\},\
\{0,1,2,4\},\ \{0,2,3,4\}.
\]

For every `y`-residue `s`, the diagonal set

\[
D_s=\{j:o_{j,j-s}=1\}
\]

belongs to the same list.

**Proof.** One odd class supplies one wake-strand base.  Checkerboard sign is
`(-1)^j` on level `j`.  The signed mod-four wake-residue theorem, applied to the
`x`-residue `r`, gives

\[
o_{0,r}-o_{1,r}+o_{2,r}-o_{3,r}+o_{4,r}=2\pmod 4.
\]

There are only five binary variables.  Exhausting their values gives exactly the six
sets displayed above: the three positive two-subsets `{0,2}`, `{0,4}`, `{2,4}`;
the negative two-subset `{1,3}`; and the two four-subsets obtained by deleting level
3 or level 1 from `{0,1,2,3,4}`.  For a fixed `y`-residue `s`, the class `(j,r)` has
`y=j-r=s (mod m)`, hence `r=j-s`; the `y`-residue identity gives the same calculation
for `D_s`.  QED.

**Consequences.** If `h` longitudinal residues use a four-element mask, then

\[
g=2m+2h,\qquad 0\le h\le m,
\]

so

\[
2m\le g\le4m,\qquad h\equiv m\pmod2
\]

because `g` is a positive multiple of four.  Both extreme levels occur at least
once.  By extremal rigidity, every odd class on levels 0 and 4 is represented by one
phase and every visited extremal class is odd.

This is an all-period structural theorem, but it does not exclude width four.  Many
binary cylinders satisfy both six-mask rules.  The exact counts for circumference
`m=1,...,8`, before imposing chronology, are `6,14,30,70,146,302,650,1422`; hence
residue incidence alone leaves a large family of countermodels.

## Exact macro search

`code/python/search_width4.py` enumerates the complete based macro table, enforces
same-physical-cell alternation during the depth-first search, and applies the full
translation-class criterion at every structural leaf.  Its fast leaf checker uses
the exact class key `(t,x mod m)` and chronological key `i-N*((x-r)/m)`.  It was
cross-checked against the general criterion on the standard period-104 word, its
square, and all 791 positive-normalised diagonal heading-reset words through length
14; there were zero disagreements.

Current completed zero-hit rows:

| macro period | ant period | nodes | structural leaves | P3 hits |
|---:|---:|---:|---:|---:|
| 20 | 40 | 315,115 | 18,884 | 0 |
| 21 | 42 | 547,153 | 32,827 | 0 |
| 22 | 44 | 923,385 | 57,003 | 0 |
| 23 | 46 | 1,599,297 | 98,995 | 0 |
| 24 | 48 | 2,715,756 | 171,745 | 0 |
| 25 | 50 | 4,694,674 | 297,730 | 0 |
| 26 | 52 | 8,005,882 | 515,706 | 0 |
| 27 | 54 | 13,821,690 | 892,915 | 0 |
| 28 | 56 | 23,641,165 | 1,545,598 | 0 |
| 29 | 58 | 40,779,962 | 2,674,711 | 0 |
| 30 | 60 | 69,894,284 | 4,626,994 | 0 |
| 31 | 62 | 120,486,560 | 8,001,133 | 0 |
| 32 | 64 | 206,786,094 | 13,830,708 | 0 |
| 33 | 66 | 356,298,082 | 23,900,914 | 0 |
| 34 | 68 | 612,059,978 | 41,293,786 | 0 |
| 35 | 70 | 1,054,244,055 | 71,328,579 | 0 |
| 36 | 72 | 1,812,117,741 | 123,182,155 | 0 |
| 37 | 74 | 3,120,499,770 | 212,684,599 | 0 |
| 38 | 76 | 5,365,871,341 | 367,141,131 | 0 |

The period-50 through period-76 rows go beyond the general paper search cutoff, but they
remain bounded computations and must not be described as an all-period exclusion.  The
Java and Python engines agree on the overlapping rows; the Java run is the source of
the period-58 through period-76 counts.

## A period bound at fixed drift

The four-state reduction also gives an all-period theorem which was not visible in
the unrestricted period search.

**Theorem (width-four period--drift bound).**  If a P3-valid width-four highway has
normalised drift `(m,-m)`, `m>0`, macro period `P`, and ant period `N=2P`, then

```
P <= 7m,   N <= 14m,   and   P = m (mod 2).
```

**Proof.**  Name the macro-transition counts as follows:

```
x: LN->LN,  a: LN->LS,  b: LN->UN,
c: LS->LN,  d: LS->LS,  e: LS->UN,
f: UN->US,  q: UN->UN,  h: UN->LS,
i: US->UN,  j: US->LS,  y: US->US.
```

Flow conservation at `LN` and `US` gives `c=a+b` and `f=i+j`.  The visits to
the bottom extremal line are exactly the `x+c` transitions, and the visits to the
top line are the `f+y` transitions.  Extremal singleton rigidity gives

```
x+c <= m,   f+y <= m,
```

because an extremal translation class is labelled by its `x`-residue modulo `m`
and no such class can occur twice.  In particular `c<=m` and `f<=m`.

On the lower odd line, `a,b,c` turn `R`, whereas `x,d,e` turn `L`.  Summing the
alternating P3 words of all translation classes on that line shows that their total
turn excess is nonnegative.  Hence

```
x+d+e <= a+b+c = 2c <= 2m.
```

Similarly the upper odd line has `2f` right turns and `q+h+y` left turns, so

```
q+h+y <= 2f <= 2m.
```

Let `L1=x+d+e` and `L3=q+h+y` be the lower and upper odd-line left-turn totals.
Summing all transition counts and using the flow identities gives

```
P = 2c + 2f + L1 + L3.
```

The signed longitudinal displacement is

```
m = L1 - L3 - 2x + 2y,
```

because `a+b-c=0` and `f-i-j=0`.  Since `L1<=2c<=2(m-x)`, this identity gives

```
L3 <= m - 4x + 2y,
L1+L3 <= 3m - 6x + 2y.
```

Using also `c<=m-x` and `f<=m-y`,

```
P <= 2(m-x)+2(m-y)+3m-6x+2y
  = 7m-8x
  <= 7m.
```

Every macro transition changes the longitudinal coordinate by `+1` or `-1`, while
the total change is `m`; therefore `P` and `m` have the same parity.  QED.

The constant seven cannot be improved by transition counts, odd-class counts, or
the six-mask residue theorem alone.  Let

```
v = RRLRLLRRRRLLRR
```

be the first primitive period-seven near-model in the table below and take `v^m`.
It has drift `(m,-m)`, macro period `7m`, growth `4m`, exactly `4m` odd classes,
and the mask `{0,2,3,4}` in every longitudinal residue.  Thus it saturates the new
bound while satisfying the incidence/residue skeleton.  For `m=1` it also satisfies
ordinary same-cell alternation.  For every `m>=2`, phases 9 and 17 of `v^m` are
successive visits to the same physical cell `(3,-2)` and both turn `R`, so
concatenating the translated blocks already fails same-cell alternation in the first
two copies.  This family is therefore
an incidence-level sharpness witness, not a highway and not a structural counterexample
for general `m`.  Any improvement below `7m` must use local or stabilised ordering.

Combining `N<=14m` with the strand-density inequality `g>=2m` gives the useful
speed form

```
N <= 7g.
```

Thus a hypothetical width-four highway must create at least one net black cell per
seven ant steps.  This corollary does use the residue/strand theorem through
`g>=2m`; the period--drift bound itself does not.

This is the missing boundedness statement for a *fixed drift*, not a proof that the
whole fixed-width problem is finite-state: the parameter `m` remains unbounded.

### Primitive diagonal drift is impossible at every period

For `m=1`, the preceding proof becomes a short hand classification rather than a
computer search.  Each extreme line is visited exactly once.  A unique bottom visit
must be `LS->LN` (otherwise a tour which leaves `LN` cannot return), and a unique top
visit must be `UN->US` (otherwise `US` cannot first be reached).  Thus `c=f=1`,
`a+b=i+j=1`.  There are only five translation classes, one on each transverse line.
Growth is their number of odd classes, is positive, and lies in `4 Z`; hence growth
is four.  The two extreme singleton classes already contribute two.  Let the three
interior class excesses be `epsilon_1,epsilon_2,epsilon_3 in {0,1}`; they sum to two.
On the lower and upper odd lines the excesses are respectively
`2-(d+e)` and `2-(q+h)`, so both left-turn totals lie in `{1,2}`.  Moreover

```
P = 4 + (d+e) + (q+h)
```

and `P` is odd because `m=1`.  Thus the two left-turn totals have odd sum; they are
`1` and `2` in one order or the other, and `P=7`.  This derivation does not use the
residue theorem.

Flow conservation leaves the following six state-compatible ant words.  The last
column gives one stabilised interior class, in chronological order; each violates
P3 immediately.

| ant word | bad stabilised class | failure |
|---|---|---|
| `RRLRLLRRRRLLRR` | `LRLR` | starts `L` |
| `RRLRLLLRRRRLRR` | `LRLR` | starts `L` |
| `RRLLRRRRLLLRRR` | `RLLR` | adjacent `LL` |
| `RRLLLRRRRLLRRR` | `RLLR` | adjacent `LL` |
| `RLRRRRLLLRLRRR` | `RRL` | adjacent `RR` |
| `RLLRRRRLLRLRRR` | `LRR` | starts `L` |

Therefore no width-four periodic highway has primitive diagonal drift
`(|a|,|b|)=(1,1)`, at any period.

### Drift-targeted exact search

`code/java/WidthFourSearch.java` now accepts an optional fixed drift.  It prunes an
endpoint which cannot reach that drift, rejects the wrong period parity, and, when
the drift is fixed, rejects a repeated extremal residue as soon as it occurs.  The
last prune is exactly Theorem (extremal-line rigidity), not a heuristic.  On shared
test ranges its surviving leaf counts equal the `ext` counts of the unpruned search.
The finite range `P<=7m` can therefore be searched exhaustively for each specified
`m`.

The completed finite ranges have zero P3 hits for `m=1,...,9`.  For `m<=6` the
fixed-drift engine was run over the entire interval.  For `m=7,8`, the paper's
all-highway result supplies `P<=24`, and the fixed-drift runs supply respectively
`P=25,27,...,55` and `P=26,28,...,64`.  Thus the present exact finite-drift theorem
is:

> No width-four periodic highway has normalised drift `(m,-m)` for `1<=m<=9`.

The machine-readable summary is `results/width4_drift_exclusion_summary.json`.
This is not an all-drift width-four theorem.

For `m=9`, the existing all-highway search covers `P<=24`, the unrestricted
width-four search covers `25<=P<=38`, and the fixed-drift engine covers every
admissible odd `P` from `39` through the theorem limit `63`.  The final row
`(m,P)=(9,63)` visited `17,532,472,230` nodes in `435.052` seconds and had zero
structural leaves (hence zero P3 checks and zero hits).

## Spatial block form of the P3 ordering

The chronology criterion admits a useful ordering-sensitive reformulation.  Fix a
transverse line and a longitudinal residue `r mod m`.  Write each occupied physical
cell in that translation class as `ell=r+qm`, and let `B_q` be the word of turns made
at that one physical cell during the period, in ordinary phase order.  Then the
stabilised translation-class word is exactly

```
B_qmax B_(qmax-1) ... B_qmin,
```

with empty blocks omitted.  Indeed an occurrence at phase `i` in cell `q` has
ordering key `i-Nq`.  If `q'>q`, then
`i'-Nq' <= N-1-N(q+1) < -Nq <= i-Nq`, so every occurrence in the higher cell
precedes every occurrence in the lower cell; equal-`q` occurrences retain phase
order.

Consequently P3 is equivalent to three local block conditions: every nonempty
`B_q` alternates; the rightmost nonempty block begins with `R`; and the last turn of
each block differs from the first turn of the next nonempty block to its left.  In
bit notation (`R=0`, `L=1`), if `F_q` is the first turn of a block, this says

```
F_q = parity(total visits in all occupied blocks strictly to its right).
```

Ordinary same-cell alternation supplies the first condition for an actual ant
trace, so the unexploited content is now isolated at the spatial joins.  The three
period-50 countermodels that start `R` fail exactly at these joins.  This lemma is
exact and all-period, but it has not yet yielded a global contradiction; it is the
current route toward replacing the finite `m<=9` computation by an all-`m` proof.

There is an equivalent charge form which is stronger than the aggregate class
identity.  Define the one-period physical-cell charge

```
chi(q) = (# R turns in B_q) - (# L turns in B_q).
```

An alternating block has `chi=0` when its length is even and `chi=+1` or `-1`
when its length is odd, according to its first turn.  The join rule therefore says
that the nonzero charges, read from largest `q` to smallest `q`, are exactly

```
+1, -1, +1, -1, ... .
```

Equivalently, every forward prefix sum of physical-cell charges in one translation
class belongs to `{0,1}`.  Summing the entire class recovers the old odd-class
identity, but the prefix statement is strictly ordering-sensitive and is violated
by incidence countermodels.  Localising the width-four transition-count equations
at a longitudinal cut and combining them with this prefix bound is the most concrete
remaining analytic route.

The alternating-list algebra behind this charge statement was already formalised in
`lean/Langton/P3Endpoint.lean` as `StabilizedP3Word.raw_prefix_bound`. The new step in
this session is the geometric block-order lemma identifying those formal decreasing
levels with ordinary visit blocks of physical cells in the width-four coordinate.
Accordingly this should be presented as a spatial reformulation/bridge, not as an
independent new algebraic theorem.

### Prefix-flow relaxation: useful failure

`code/python/width4_prefix_flow.py` tests that route without silently assuming a
chronological order. It keeps integer flow conservation on every `(state,ell)`
vertex, `P<=7m`, positive growth, extremal-residue singleton bounds, and every
`{0,1}` prefix-charge inequality. A second version also forces the support of the
directed multigraph to be weakly connected, which together with the degree equations
is enough for some Euler trail to exist.

The disconnected relaxation was SAT already at `m=1`. Adding support connectivity
makes `m=1` UNSAT but remains SAT at `m=2` (`P=12,g=4`) and `m=3`
(`P=19,g=8`). One Euler ordering of the `m=2` flow is

```
b f i h d d c b h d d c,
```

and fails ordinary same-physical-cell alternation at `(1,0)` with successive `R`
turns. This identifies the remaining gap exactly: prefix charges constrain the
*multiset* of local turns, but a connected Euler flow need not realise those turns in
the locally alternating order. Thus the present flow and prefix inequalities alone
cannot prove width-four exclusion; an order-compatible Euler-trail obstruction is
still required. The SAT outputs are countermodels to a proof strategy, not highways.
An additional connected-relaxation query imposing `P>=5m+7` at `m=4` was stopped
after about fourteen CPU minutes without a solver answer; it is recorded as a
timeout, not as evidence for or against the empirical `5m+6` bound.

### Low crossing-sequence density and a possible pumping route

There is one more exact consequence of `P<=7m`. Work modulo translation by `m`.
For each cut residue `r=0,...,m-1`, let `C_r` count macro steps crossing any lifted
cut `r+qm+1/2`. The quotient path winds once, so forward crossings minus backward
crossings at every cut residue equals one. Hence every `C_r` is positive and odd.
Every macro step crosses exactly one lifted cut, so

```
sum_r C_r = P <= 7m.
```

Let `L` be the number of cuts with `C_r<=7`. Every other cut has `C_r>=9`, while a
low cut still has `C_r>=1`; therefore

```
7m >= sum_r C_r >= L + 9(m-L) = 9m-8L,
```

and `L>=m/4`. Thus a positive density of cuts have crossing sequences of length at
most seven over a finite transition alphabet. This is the standard raw material for
a crossing-sequence pumping lemma: in a sufficiently large minimal counterexample,
two low cuts should have identical signatures and the intervening slab might be
spliced out to reduce `m`.

This is not yet a decidability theorem. A valid signature must include enough tape
colour, row/state, direction, and period-boundary data to make the splice preserve
the ant computation and P3 seed/wake relation. Proving that two equal signatures
really can be spliced is the missing obligation. The density lemma does, however,
turn the previously vague bounded-memory hope into a precise finite-signature
research program.

`code/python/width4_crossing_signatures.py` computes the modular cut signatures and
a deliberately under-decorated
chronological signature (crossing direction, macro states, transition, and turn
pair). On the exact endpoint near-model at `m=10`, cut residues `3,...,9` have
the same five-event phase-free signature

```
d(+) c(-) b(+) h(-) d(+).
```

Residues `0,1,2` correctly receive the six overshoot steps crossing lifted cuts
`10,11,12`; this is why absolute-cut signatures would be wrong. Deleting the
five-transition slab between consecutive repeated cuts turns the explicit
`m` endpoint family into the same family at `m-1`. Thus the naive splice works on
the repeated-block witness and explains its linear form. This is a sanity check for
the crossing-sequence program, not proof that this under-decorated signature is
sufficient on arbitrary traces.

### Candidate crossing-sequence splice theorem (proof draft)

**Status at 17:45 CDT:** complete proof draft, awaiting adversarial review. Do not
promote the resulting cutoff to the manuscript until the periodic splice/P3 bridge
has been checked independently.

For a macro phase `i` crossing the lifted cut `r+qm+1/2`, define its stabilised cut
key to be `i-Pq`. The **decorated crossing signature** `Sigma_r` is the sequence of
macro transition types at cut residue `r`, sorted by that key. A transition type
records source and target macro states and the two turns; it therefore records which
transverse cells on the two endpoint columns are toggled and with which turns. The
directions in `Sigma_r` alternate `+,-,+,...,+` because the translated infinite path
has signed winding one across the cut.

Let `Gamma_r` be the control projection retaining only direction and the even
transverse line on which the ant lands. It is the actual one-tape control crossing
sequence.

**Candidate splice lemma.** If `Gamma_r=Gamma_s` for two residues `0<=r<s<m`, a
width-four P3-valid trace of drift `m` can be spliced to a P3-valid trace of drift
`m'=m-(s-r)` and transverse width at most four.

**Proof draft.** In every translated longitudinal period, remove the slab of columns
between the lifted cuts `r+qm+1/2` and `s+qm+1/2`. Pair the crossings of its two
boundary cuts in their stabilised chronological order. On a rightward pair, switch
from the old left-half computation immediately after crossing the left boundary to
the old right-half computation immediately after the matching crossing of the right
boundary; do the symmetric operation for a leftward pair. Equality of `Gamma`
supplies the same horizontal heading and destination transverse line, exactly the
finite control needed for this switch. The deterministic one-tape induction below
then shows that all retained events are legal and every retained physical cell has
exactly its old chronological turn history. If the stronger decorated signatures
agree, the same operation can also be visualised as combining equal macro boundary
transitions, but that extra equality is not required.

Let `S` be the remaining set of longitudinal columns and let `phi:S->Z` be the
order-preserving compression. Periodic deletion gives

```
phi(ell+m) = phi(ell) + m'.
```

Hence `phi` bijects retained translation classes modulo `m` with translation classes
modulo `m'`, preserves their front-to-back physical-cell order, and (by the preceding
turn-history observation) preserves every stabilised P3 word. The spliced macro path
has the same start/end state and nonzero drift `m'`. It is nonempty; on its own
extreme transverse line the geometry plus start-`R` forces a singleton `R` class, so
growth is positive. The exact periodic-trace criterion therefore supplies a finite
seed. Its width is even and at most four; width two is already impossible, so it is
again width four. This is the usual crossing-sequence cut-and-paste principle applied
to the two-column macro machine. A standard one-tape formulation can simulate each
macro transition with a finite intermediate state carrying the turn pair.

Finite-seed subtlety: keys `i-Pq` may be negative, and the formal negative-period
path need not be dynamically realised. Choose a physical representative cut
`r+Qm+1/2` far enough ahead that every event occurs at the genuine forward time
`QP+(i-Pq)>=0`, and splice only the future periodic tail. The extracted smaller-
drift tail word is then checked by P3 and receives a fresh finite seed from the exact
criterion; no infinite backward wake is imported.

The information-exchange step is consistent with the classical one-tape crossing-
sequence lemma: equal boundary state sequences permit the left half of one tape
computation to be glued to the shifted right half of another. Jeandel's formulation
states this explicitly in Section 3.3 of *Computability of the entropy of one-tape
Turing machines* (STACS 2014), following Hennie. What remains to audit here is not
that classical lemma, but the equivariant deletion of every translated slab and the
claim that the compressed P3 words are exactly preserved.

The boundary-colour issue can be formulated without any macro-level handwave.
Encode the width-four ant as a deterministic one-tape machine: longitudinal columns
are tape cells with five-bit colour symbols, and the finite control records the
transverse line and heading. Vertical ant moves are stay-put tape moves (or a
two-state simulation of one), while horizontal ant moves cross tape boundaries.
The control projection `Gamma` is the ordinary control crossing sequence. Thus the
classical splice lemma preserves the complete reads and writes on each
retained half, including the two cells next to the join.

For all translated slabs at once, start beyond the finite seed and take a finite-
time direct limit. Any finite execution prefix visits only finitely many slabs, so
it is produced by finitely many ordinary disjoint splices; determinism makes these
prefixes compatible. The compressed initial tape is still finite support because
all far-tail columns are initially blank. Translation of the old tail by `(2P,m)`
preserves the splice pattern and becomes a translation by `m'=m-(s-r)` after
compression. The remaining self-audit obligation is to state completely why this
equivariance advances the spliced oriented event path by one positive finite number
of events. A retained cut with nonempty net-right crossing sequence supplies the
proposed proof. The theorem remains labelled candidate pending hostile review.

That last step has now been rewritten in the crossing-sequence graph. Far beyond the
seed, each longitudinal column is initially the all-white five-bit symbol; its two
boundary crossing sequences form a compatible labelled edge. The highway therefore
gives a closed walk of length `m` in the graph. Equal vertices `Gamma_r=Gamma_s`
allow the intervening closed subwalk to be deleted, leaving a closed walk of length
`m'`. In the direct-limit computation, translating every retained local column
transcript by one new cycle maps each `j`-th boundary occurrence to the corresponding
`j`-th occurrence. It is therefore a successor-preserving self-map of the one-way
tail event path, hence `n -> n+k`; `k` is finite and positive because the spatial
coordinate changes by `m'>0`. This gives the required time period. The remaining
review target is whether the direct limit could truncate a nominal crossing
sequence at infinity; the finite-prefix compatibility argument is intended to rule
that out.

The truncation issue has a monotone resolution. For two cuts `A<B`, a paired
rightward crossing occurs at `A` before `B`, and a paired leftward crossing at `B`
before `A`. Every splice therefore jumps forward in the old execution and only
deletes a chronological interval. Adding a farther splice makes the retained event
list a subsequence of the previous one. The event index of a fixed retained crossing
is a nonincreasing natural number and stabilises; the finite one-cut lemma guarantees
the occurrence exists at every stage. No crossing can vanish only at infinity, and
an extra crossing at a finite limit index would already occur at a finite stage.
This completes the present self-audit of the direct limit, still subject to an
independent adversarial check before manuscript promotion.

Assuming the splice lemma, choose a width-four highway of minimal drift magnitude
`m`. Its control signatures are pairwise distinct. At least `m/4` have length at most
seven. For a rightward crossing the destination is line `2` or `4`; for a leftward
crossing it is line `0` or `2`. The direction pattern is fixed at odd lengths, so
there are two choices per event. Therefore the number
of possible low control signatures is at most

```
F = 2 + 2^3 + 2^5 + 2^7 = 170.
```

The density lemma gives the first cutoff `m <= 4F = 680`. The full average-length
budget is stronger. Distinct length-`1,3,5,7` signatures have capacities
`2,8,32,128`. Relative to average seven, their total available deficit is
`6*2+4*8+2*32=108`. Every other signature has length at least nine and costs at
least two units, so there are at most 54 of them. Therefore

```
m <= 2+8+32+128+54 = 224.
```

Extremal singleton rigidity makes the count polynomial rather than binary. In a
length-`2n+1` signature, the exceptional rightward top landing `(+ ,4)` can occur at
most once, and the exceptional leftward bottom landing `(- ,0)` can occur at most
once; otherwise two phases occupy the same extremal translation class. All other
landings are on line `2`. Hence there are at most `(n+2)(n+1)` signatures of that
length. The short capacities become `2,6,12,20`, with total deficit
`6*2+4*6+2*12=60`; at most 30 signatures can have length at least nine. Therefore

```
m <= 2+6+12+20+30 = 70.
```

Combining this explicit drift cutoff
with `P<=7m` would make width-four existence decidable by a finite search. It would
not itself exclude width four, and the present exact search through `m=9` is nowhere
near the new cutoff.

The first implementation sorted a modular signature in raw phase order. That was
also insufficient: an event at phase `i` on the lifted cut `r+qm+1/2` occurs at the
representative cut at time `i-Pq`. The checker now sorts on this stabilised key. All
raw-phase signature output is superseded.

An earlier count used all six decorated macro transition types available in each
direction and gave the weaker conditional cutoff `1,151,736`. The literal one-tape
encoding shows that decoration is unnecessary for splicing: fixed direction plus
destination even line is the complete crossing control. The older number remains a
valid over-refined conditional bound but is superseded by the extremal-weighted
bound `70`.

### Candidate all-period width-four exclusion from the blank-column graph

The control projection makes a stronger finite local test possible. For an initially
white longitudinal column, simulate its five cells using the exact crossing
sequences at the left and right boundaries. Each sequence alternates direction,
starts and ends rightward, and by extremal singleton rigidity contains at most one
rightward top landing `4` and at most one leftward bottom landing `0`.

`code/python/width4_crossing_graph.py` performs the literal column simulation. Its
unbounded finite-state generator tracks the 32 colour masks, current entry line and
heading, and four exceptional-event flags. It finds no reachable entry-state cycle
and exactly these compatible edges (line numbers concatenated):

```
202       -> 4
4220222   -> 2, 202, 20222, 2022224
2042222   -> 2, 202, 20222, 2022224
202242222 -> 422, 42202, 4220222.
```

The 12-edge, 10-vertex graph is acyclic; its longest path has length three,
`202242222 -> 4220222 -> 202 -> 4`. A finite-support width-four highway would have
infinitely many initially white columns beyond its seed, and their adjacent exact
boundary sequences would form an infinite path in precisely this graph. Thus the
finite table is a candidate proof that width four is impossible at every period.

The script cross-checks the generator against independent pairwise compatibility
tests for every extremal signature through length 25. Source SHA-256 is
`2AF99EDCBC355945B547AB1F80CAEE6927FA75D6C1C064C5ADC41D13B5FE3E33`.
The generator reaches 22 entry states, has maximum entry depth eight, and finds no
reachable entry cycle.
At the time of discovery this was a promotion gate: a referee still had to attack
the control-state projection, turn convention, boundary indexing, exceptional flags,
and repeated-state logic.  That gate was discharged after the 19:00 cutoff; the
details and one repaired statement-level omission are in Journal \S38.16.
`lean/Langton/WidthFourCrossing.lean` checks the rank-decrease certificate and
impossibility of a four-edge chain, but explicitly assumes the 12-edge table is
complete. Its SHA-256 is
`548DF94E2B8B60CE23269153EE446CFF824AC1DB6AA1A41773F4E605205324FF`.
An independent literal verifier using compass-letter headings and set-valued black
rows, importing no project search code, reproduces the same 12 edges:
`code/python/verify_width4_crossing_graph_indep.py`, SHA-256
`694C1178B00FA8AB929A5375255E53762C403DE02FC1D2958A4409EF9B84AFE0`.
It also validates the boundary convention on the genuine standard finite seed by
replaying an initially white far-ahead column between cuts 100 and 101; the extracted
boundary lengths are 31 and 21 and the replay is exact.

The mechanism is genuinely width-four-specific. The generic exploratory generator
`code/python/explore_even_width_crossing_cycles.py` finds no reachable local entry
cycle at width four, but at both widths six and eight finds the same two-state cycle

```
(black rows {1,2}, entry line 2 east)
  <-> (black rows {1,3}, entry line 2 west),
```

without reusing either exceptional extreme event. Wider strips therefore recover
unbounded interior memory, so the acyclic-column proof does not extend directly.
SHA-256: `760CD63D8CCC0292AD5FF2A3134CAE7A4E2CDD1AA16758527BFF5F706806F327`.

#### Paper-grade lemma chain for the direct exclusion

The following formulation survived the final pre-manuscript self-audit.

1. **Far-cut lemma.**  After a 180-degree rotation if necessary, take drift
   `(m,-m)` with `m>0`, longitudinal coordinate `x`, and shift the five transverse
   lines to `t=x+y in {0,...,4}`.  For every sufficiently large half-integer cut
   `x=k+1/2`, the complete future crossing sequence is finite, has positive odd
   length, and alternates east, west, ..., east.  This follows because the periodic
   path has only finitely many phase offsets from `nm`, while its longitudinal
   coordinate tends to `+infinity`.
2. **Control-projection lemma.**  Record the transverse coordinate immediately
   after each horizontal crossing.  Eastward records lie in `{2,4}` and westward
   records in `{0,2}`.  Event parity supplies the direction.  This record is the
   full control state with which the deterministic ant computation enters the next
   tape column; vertical moves stay in that column.
3. **Extremal-signature lemma.**  In one cut sequence, eastward label `4` and
   westward label `0` each occur at most once.  Either repetition would enter the
   same extremal cell at the fixed destination column twice, contrary to
   extremal-line rigidity.
4. **Blank-column classification lemma (computer-assisted).**  Starting from five
   white cells, the exact deterministic within-column simulation, under the two
   singleton restrictions on each boundary, permits exactly the twelve displayed
   ordered pairs of boundary sequences.  The exhaustive recursion has 22 reachable
   entry states, no reachable state cycle, and maximum depth eight.  A separately
   written recursion returns the same edge set.
5. **Rank lemma.**  Assign rank 3 to `202242222`, rank 2 to `4220222` and
   `2042222`, rank 1 to `202`, and rank 0 to all other occurring signatures.  Every
   one of the twelve edges strictly lowers rank.  Hence there is no directed path
   of four edges.  This finite implication is checked in Lean.
6. **Tail contradiction.**  At the time the periodic tail begins, only finitely
   many cells have been visited and only finitely many are black.  Every sufficiently
   far column is therefore an untouched white five-cell column.  Its two exact cut
   sequences are an edge in the classified graph.  Consecutive far columns would
   give arbitrarily long, indeed infinite, directed paths, contradicting the rank
   lemma.

The theorem is scoped to diagonal-drift finite-support periodic highways.  It does
not exclude non-diagonal translators, does not exclude widths six or eight, and does
not prove that arbitrary finite seeds ever enter a periodic tail.  The only
computer-assisted premise is item 4; the paper must not describe the current Lean
artifact as an end-to-end formalisation of that premise.

The width-six two-cycle was also decoded by hand.  In mask `{1,2}`, an eastward
entry on centre line 2 turns `L` at black row 2 and then `R` at white row 3, exiting
east with mask `{1,3}`.  A westward return on line 2 turns `R` at white row 2 and
then `L` at black row 3, exits west, and restores `{1,2}`.  Hence the repeated cells
themselves alternate perfectly and no extreme is reused.  This proves that the
failure of the width-four method at width six is not removed by ordinary local
alternation; a wider proof must couple columns or exploit the first-letter order of
whole translation classes.  The oscillator remains a local obstruction, not a
global highway.

### A sharp but unproved structural pattern

For every tested `m=3,...,9`, the *last* macro period having even a
same-cell-alternating, extremal-singleton structural leaf is

```
P = 5m + 6,
```

and there are exactly `m` leaves at that endpoint.  One family has a transparent
five-macro repeated block and growth four.  The same runs show longitudinal
overshoot bounds `min ell >= 1-m` and `max ell <= 2m+1` for every structural leaf
through `m=8`.  These two regularities strongly suggest a rotor/odometer lemma that
would improve `P<=7m` to roughly `P<=5m+6`.

Neither regularity is proved.  The completed `m=9` theorem-bound range confirms the
period endpoint, but the overshoot observation was recorded only through `m=8`.
Do not use `5m+6`, the `m`-leaf count, or the overshoot bounds in the manuscript as
theorems; they are research targets for a future local-alternation argument.

One endpoint leaf does have an exact formula, although it is only a near-model. In
transition-count notation, for every `m>=3` take

```
(b q f j d d c) (b h d d c)^(m-2) (b h d d e f i h c).
```

Each displayed transition is valid in the four-state automaton. The first block,
each repeated block, and the last block have net longitudinal displacement one, so
the total drift is `m`; their lengths give `P=5m+6`. Grouping the cells in the three
block types shows ordinary same-physical-cell alternation. The bottom visits occupy
`m` distinct residues and the two top visits occupy distinct residues for `m>=3`,
so it also has extremal singleton rigidity. Its growth is four. It is not P3-valid:
on the lower odd line the two cells `ell=m+1` and `ell=1` in one residue have
ordinary words `LR` and `LRL`, so their right-to-left stabilised concatenation is
`LRLRL` and starts with `L`. It also fails the aggregate odd-class identity. This
family proves that an eventual upper bound `P<=5m+6`, if established, would already
be sharp at the ordinary-alternation/extremal level.

The next fixed-drift run confirmed this structural pattern at `m=10`: `P=56` has
exactly ten extremal-singleton, ordinary-alternating leaves, all with growth four and
none satisfying growth/odd-class equality; `P=58` has no structural leaf. Completed
zero-hit rows at this checkpoint cover every even `P=40,42,...,60`. The `P=60` row
visited `19,138,313,024` nodes and had no structural leaf. Higher theorem-
range rows were still running and are not counted until completion. At the extended
checkpoint, `P=62` also completed: `30,238,836,043` nodes, no structural leaf, and
no P3 hit. Then `P=64` completed `47,442,673,612` nodes with no structural leaf or
P3 hit. `P=66` then completed `74,038,045,927` nodes with no structural leaf or P3
hit. The `P=68` and `P=70` workers were stopped unfinished at 18:56:13 CDT; neither
returned a completed row, so both remain uncounted. The completed
rows are preserved in `results/width4_m10_partial_2026-07-21.json`.

## Lean arithmetic checkpoint

`lean/Langton/WidthFour.lean` machine-checks deliberately delimited arithmetic
kernels:

1. the exhaustive six-mask classification from five binary variables and the signed
   mod-four equation;
2. `P<=7m` from the boundary, displacement, and odd-line count inequalities;
3. `P congruent to m (mod 2)` from the numbers of `+1` and `-1` macro moves; and
4. `P=7` in the primitive case once the two odd-line left-turn totals are `1` and
   `2`;
5. the even-fiber step and finite summation step in the upper bound `g<=mW`;
6. the arithmetic ordering of phase keys in distinct physical-cell blocks; and
7. the one-quarter lower bound for cuts crossed at most seven times.

The pinned Lean 4.32.0 build completes 22 jobs, the audit reports only the standard
Lean axioms, and a source scan finds no `sorry` or `admit`.  This is not an
end-to-end formalisation of the geometry: extremal rigidity, the macro transition
table, flow identities, and the passage from P3 alternation to the count inequalities
remain explicit mathematical inputs.

## Independent SMT formulation

`code/python/width4_smt.py` encodes a fixed `(m,P)` instance directly in Z3.  Its
symbolic variables are the macro state, longitudinal coordinate, and transition at
each time.  For every phase it forms the exact class key

```
phase - 2P * floor(ell/m)
```

and counts how many same-class phases have smaller keys.  Even rank is constrained
to `R` and odd rank to `L`, which is the stabilised P3 condition without calling the
enumerator's checker.  Any SAT word is replayed through the independent Python walk
and P3 implementation before being reported.

Z3 5.0.0 returned exact `unsat` for `(m,P)=(1,7),(2,6),(2,8),(2,10),(3,9)` and
for `m=9`, `P=9,11,13,15`.  It timed out rather than returning `unsat` at the harder
instances `(2,12)`, `(9,17)`, and `(9,19)`.  Therefore the SMT work is presently a
bounded cross-check, not a stronger exclusion and not a proof certificate.  The
timeouts are recorded as timeouts, never as negative results.

### Failed optimisation: incremental class arithmetic

A proposed Java prune tracked partial class parities and transverse-line turn
excesses, rejecting a branch when the remaining phases could not make each line's
excess equal its number of odd classes.  The condition was sound and reproduced the
small rows, but on the completed benchmark `(m,P)=(9,57)` it visited
`4,621,247,456` nodes in `410.472` seconds, versus `4,623,723,311` nodes in
`329.221` seconds without the bookkeeping.  A `0.054%` node reduction did not pay
for per-node array updates.  The optimisation was removed from the final source.

## Important limitation

The phrase "fixed width is finite-state, therefore decidable" has not been proved.
A finite alphabet on an unbounded longitudinal tape is not itself a finite state
space and can support Turing-machine behaviour.  What is proved finite-state here is
only the odd-skeleton residue constraint: the vertical and diagonal six-mask rules
form a finite-memory shift of finite type.  Turning that skeleton into a complete
chronological highway classifier still requires a bounded-memory theorem that is
currently missing.

## Next mathematical target

The bounded data suggest a universal start-order obstruction: among structural
width-four cycles, the odd-class identity has survivors, but every survivor still
has at least one translation class whose stabilised sequence starts with `L` or
fails alternation.  The useful target is therefore not another incidence equation.
It is a proof that every single tour of the four-state ladder with nonzero winding
forces one such bad chronological class.

### Failed strengthening: condition (ii) alone is not enough

Through ant period 48, no structural leaf even satisfied the condition that every
stabilised class starts with `R`.  It was tempting to conjecture that the first-turn
condition alone excludes width four.  Period 50 disproves that strengthening: there
are exactly three based structural cycles with every class starting in `R`.  Their
drift is `(1,-1)`; two have growth 8 and one has growth 4.  They fail alternation in
respectively 5, 4, and 5 classes.  The growth-4 example also satisfies the aggregate
odd-class identity (`growth = 4 = number of odd classes`), so even the first-turn
condition plus that incidence identity is insufficient.

One of the three countermodels is

`LRLRLRLRLRLRLRLRLRLRRLRRLRLRLRLRLRLRLRLRLRLRRLLRRR`.

Its five transverse classes have sizes `3,11,11,12,13`; all start with `R`, but
their stabilised sequences include long constant blocks and violate alternation.
This is a useful negative result: any all-period width-four proof must use both
ordering clauses of the exact criterion, not merely the first-turn clause that was
enough to establish the extremal-line theorem.

### Discarded boundary-transition reduction

An attempted ten-transition reduction was rejected during this session.  I initially
read the pair labels as though the first symbol were the even-line turn and deleted
`LN->LN` and `US->US`.  In fact the macro pair is `(odd turn, even turn)`; those two
transitions are `LR`, so their *boundary* turn is `R`, exactly as extremal rigidity
requires.  The deleted `L` occurs on the adjacent odd line.  No statement or search
depending on that false reduction is retained.
