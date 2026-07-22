# Lean Langton kernel

This is a dependency-light Lean 4 formalization of the finite-support Langton
ant transition kernel and two exact invariant components used in the current
P15/P16 research chain.

## Reproduce

From PowerShell in this directory:

```powershell
.\build.ps1
```

The project is pinned to Lean 4.32.0 by `lean-toolchain`.  `build.ps1` uses `lake`
from `PATH`, an optional sibling portable toolchain, or the executable named by
`LANGTON_LEAN_LAKE`.

For a clean Linux build with no host Lean installation:

```powershell
docker build -t langton-lean:4.32.0 .
docker run --rm --mount "type=bind,source=${PWD},target=/src" `
  langton-lean:4.32.0 bash -lc "lake build && lake env lean Audit.lean"
```

## What is formalized

- Integer lattice positions, four headings, finite black support, and the exact
  white/right/black versus black/left/white transition.
- Extensional toggle lemmas: the departed cell flips and every other cell is
  unchanged.
- Exact iteration and extraction of the chronological turn word.
- The heading-reset theorem `headingReset_trace_modFour`: an actual finite run
  that restores its heading has signed R-minus-L residue zero modulo four.
- The finite telescoping theorem `evenWindingParityCore`: adjacent half-flow
  parities with zero exterior values have even aggregate seam parity.
- The contradiction wrapper `noOddWindingFromFiniteHalfFlow`.
- An exact four-step blank-grid transition certificate.
- The cyclic mod-four checker weight
  `checkerWeight alpha r odd = (-1)^odd * alpha(r)` and its exact
  `fourCornerAdmissible` mixed-difference identity for arbitrary `alpha`.
- The finite signed residue sum `fiberCharge`, its reduction modulo two to
  unsigned `fiberCard`, and the implication `E_r = 2` gives a positive even
  residue fiber of cardinality at least two.
- An exact proof that residue fibers partition the complete base list.
- `cyclicCharge_implies_growth_bound`: if every one of `n` cyclic residue
  fibers satisfies `E_r + 2 = 0` in `Z/4Z`, then the total number of bases is
  at least `2*n`.
- Generic finite-path potential telescoping over consecutive edges.
- The cyclic local-potential calculation: summing
  `-checkerSign * (alpha(r) + alpha(r+1))` over one residue cycle gives
  `2 * sum alpha` in `Z/4Z`.
- Exact cancellation of a finite translated widget whenever its cell weight is
  translation-periodic.
- `LocalResidueCertificate`, which names every remaining geometric input, and
  `localCertificate_implies_residueIdentity`, which derives `E_r + 2 = 0`
  from local potential increments, additive conservation, widget cancellation,
  strand identification, and a delta-alpha cycle.
- `localCertificates_imply_growthBound`: one such certificate for every
  residue mechanically implies the global `2*n` strand-density bound.
- `ExactPeriodTrace`: a candidate period whose positions and turns are the
  actual finite kernel run, with restored heading, displacement, and a checked
  drift-orbit address for every phase.
- Exact finite aggregation of signed phase visits by orbit level.
  `aggregateToggles_sum` proves that a covering level window preserves the
  total signed turn count.
- A canonical endpoint normal form.  A prefix scan reconstructs finite widget
  coefficients and proves `D = S + (T - 1)A` together with terminal zero.
- Reduction of exact grouped phase charge to canonical strand charge, followed
  by automatic translated-widget cancellation.
- A canonical residue delta-alpha function.  A certified closed traversal of
  the finite residues supplies `cycle_values` and `alphaCycle.sum = 1`
  mechanically.
- `toLocalResidueCertificate`, which constructs all algebraic certificate
  fields from a normalized exact trace and the remaining lifted-potential
  geometry.
- `StabilizedP3Word.toOrbitEndpointData`, which derives the first positive
endpoint, the balanced remainder, and binary widget scan from a stabilized,
decreasing-level P3 word instead of assuming those endpoint fields.
- Width-four arithmetic kernels: the six-mask finite enumeration, the upper step in
  `g <= mW`, the macro period bound `P <= 7m`, period parity, the primitive-drift
  arithmetic reduction, spatial block ordering, and explicitly labelled candidate
  crossing-signature cutoff arithmetic.
- The 12-edge blank-column graph as one literal list, with `BlankEdge` defined by
  list membership, an explicit rank decrease for every edge, and a theorem excluding
  four-edge chains. Completeness of the Python-generated edge list is not formalized
  in Lean.

## Scope and assumptions

Black support is represented by a finite list and interpreted extensionally;
duplicates do not affect colour.  Whitening removes every duplicate, making
the transition exact at the represented-set level.

This checkpoint does **not** formalize the geometric reduction from a clean
translator to the finite half-flow profile.  In particular, it does not yet
formalize quotient cylinders, the local HV edge formulas, or the theorem that a
translator winds once.  Therefore it is not by itself a Lean proof of P15, P16,
or the universal highway conjecture.  It mechanically verifies the transition
kernel, P4's mod-four heading component, and the finite algebraic cancellation
at the heart of P15 once the geometric hypotheses have been established.

The earlier residue-density theorem still exposes
`forall r, fiberCharge r bases + 2 = 0` directly.  The newer trace theorem
removes the finite additive-algebra layer and constructs periodicity, widget
cancellation, strand identification, and the delta-alpha cycle.  It still does
not produce a normalized periodic-trace certificate from an arbitrary Langton
orbit.  The
remaining explicit inputs are: a geometric construction of the stabilized P3 word
for each drift orbit and its identification with the aggregated exact phase toggles;
a physical lifted path
making one closed residue traversal; the local potential formula on that path;
and conservation of exact grouped phase charge plus potential drift.

Thus the new theorem is a machine-checked conditional bridge, not a full proof
of P22/P16.  No P12 decomposition assumption or geometric entrance statement is
hidden in it.  See `FORMALIZATION_BOUNDARY.md` for the exact interface.

The width-four crossing module has a separate, narrower boundary: Lean checks the
finite graph implication once the 12 edges are supplied. Two independent Python
enumerators establish completeness of that local table. Neither the table
enumeration nor the reduction from an arbitrary periodic ant trace to an infinite
blank-column path is formalized end to end.
