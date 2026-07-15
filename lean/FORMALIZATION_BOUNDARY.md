# Formalization boundary: exact trace geometry and mod-four residue charge

`Langton/ChargeTelescoping.lean` removes the finite additive-algebra step
between local potential increments and the residue identity.
`Langton/TraceGeometry.lean` now constructs most of that certificate from an
exact finite ant trace plus a sharply stated normalized-orbit interface.

## Proved by Lean

1. `edgeSum_of_potential`: local differences on every consecutive pair of a
   finite path telescope exactly to the endpoint potential difference.
2. `cyclicCheckerIncrement_eq_two_mul_sum`: the checker-signed cyclic increment
   is `2 * alphaCycle.sum` in `Fin 4`; the sign disappears because `-2 = 2`.
3. `potentialDrift_of_checkerCycle`: a lifted path whose alpha labels make one
   closed residue cycle and whose local potential differences have the required
   form has endpoint drift `2 * alphaCycle.sum`.
4. `translatedWidgetDifference_eq_zero`: a finite widget and its translate
   have equal additive charge under a translation-periodic weight.
5. `strandCharge_from_localCycle_and_periodicWidget`: conservation plus the
   preceding two facts removes the widget and leaves the strand charge.
6. `localCertificate_implies_residueIdentity`: a delta-alpha certificate gives
   `fiberCharge r bases + 2 = 0` rather than assuming that identity.
7. `localCertificates_imply_growthBound`: one certificate per residue gives
   `2*n <= bases.length` through the previously checked fiber-parity theorem.
8. `phasePositions_eq_addressPositions`: every phase position in an
   `ExactPeriodTrace` is the actual kernel state `run i initial` and equals its
   certified orbit-base-plus-level-times-drift address.
9. `aggregateToggles_sum`: grouping the exact signed phase toggles into any
   finite level window that covers them preserves their total signed turn sum.
   Consequently `NormalizedTrace.delta_sum_matches_phases` is now a theorem;
   it is no longer a structure field.
10. `OrbitEndpointData.canonical_decomposition`: the finite endpoint
    coefficient list is exactly one canonical strand (when growth is true)
    plus a translated-widget difference.  The widget is reconstructed by a
    prefix scan and its terminal coefficient is proved to be zero.
11. `orbitPhaseCharge_eq_strandCharge` and
    `groupedPhaseCharge_eq_strandCharge`: exact per-orbit signed phase charges
    reduce to the canonical strand charge; this uses the proved aggregate-sum
    theorem rather than assuming a strand charge equation.
12. `residueAlpha_cycle_values`: once the physical lifted path is certified to
    traverse `finRange n` and close, its delta-alpha values form the required
    closed cycle automatically.  `alphaAt`, `odd`, and `cycle_values` are no
    longer arbitrary fields of the remaining interface.
13. `toLocalResidueCertificate`: translation-periodicity, widget cancellation,
    strand/fiber identification, the delta-alpha sum, and the old conserved
    decomposition field are all constructed.  In particular, the old widget
    decomposition is not retained as an assumption.

## Still explicit assumptions

The remaining interface is now `NormalizedTrace` plus
`RemainingPotentialGeometry`.  Its non-definitional inputs are:

- an exact repeated trace, including its period, drift, restored heading, and a
  drift-orbit address for every actual kernel phase;
- for each orbit, a finite level window covering all its exact phase toggles and
  equality of the endpoint coefficient list with the mechanically aggregated
  toggle list;
- the endpoint normal-form conditions: after removing the first positive
  strand endpoint, the coefficient sum is zero and its prefix scan is binary;
- a physical lifted path whose residue sequence is exactly one closed traversal
  of `finRange n`;
- the local potential-increment identity along every consecutive path edge;
- conservation of the exact grouped phase charge plus the endpoint potential
  drift.

The finite widget, periodic residue weight, fiber identification, alpha labels,
closed alpha cycle, and certificate conservation equation are then derived.
What is still missing is a theorem producing the normalized endpoint conditions
and the lifted potential geometry from every relevant clean translator, followed
by an entrance theorem taking every finite initial coloring to such a
translator.  Consequently neither P22/P16 nor the universal highway conjecture
is claimed as an unconditional Lean theorem.
