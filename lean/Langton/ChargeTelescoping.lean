import Langton.ResidueCharge

namespace Langton.ChargeTelescoping

abbrev ZMod4 := Fin 4

/-! ## Generic finite-path telescoping -/

/-- The final element of `a :: rest`, expressed without a partial operation. -/
def lastFrom (a : α) : List α → α
  | [] => a
  | b :: bs => lastFrom b bs

/-- Sum a local edge quantity over all consecutive pairs of a finite path. -/
def edgeSum (delta : α → α → ZMod4) : List α → ZMod4
  | [] => 0
  | [_] => 0
  | a :: b :: rest => delta a b + edgeSum delta (b :: rest)

/-- A predicate holds on every consecutive pair of a finite path. -/
def OnEdges (P : α → α → Prop) : List α → Prop
  | [] => True
  | [_] => True
  | a :: b :: rest => P a b ∧ OnEdges P (b :: rest)

/-- Local potential differences telescope to the endpoint difference. -/
theorem edgeSum_of_potential (delta : α → α → ZMod4) (potential : α → ZMod4)
    (a : α) (rest : List α)
    (hlocal : OnEdges (fun u v => delta u v = potential v - potential u)
      (a :: rest)) :
    edgeSum delta (a :: rest) = potential (lastFrom a rest) - potential a := by
  induction rest generalizing a with
  | nil => simp [edgeSum, lastFrom]
  | cons b bs ih =>
      have hab := hlocal.1
      have htail := hlocal.2
      simp only [edgeSum, lastFrom]
      rw [hab, ih b htail]
      grind

/-- Mapping path vertices commutes with summing a local edge quantity. -/
theorem edgeSum_map (delta : β → β → ZMod4) (f : α → β) (path : List α) :
    edgeSum delta (path.map f) = edgeSum (fun u v => delta (f u) (f v)) path := by
  induction path with
  | nil => rfl
  | cons a rest ih =>
      cases rest with
      | nil => rfl
      | cons b bs =>
          simp only [List.map_cons, edgeSum]
          congr 1

/-! ## Cyclic checker-potential increment -/

/-- Append the initial value to close a nonempty cycle. -/
def closeCycle : List α → List α
  | [] => []
  | a :: rest => (a :: rest) ++ [a]

theorem edgeSum_append_singleton (delta : α → α → ZMod4)
    (a z : α) (rest : List α) :
    edgeSum delta ((a :: rest) ++ [z]) =
      edgeSum delta (a :: rest) + delta (lastFrom a rest) z := by
  induction rest generalizing a with
  | nil => simp [edgeSum, lastFrom]
  | cons b bs ih =>
      simp only [List.cons_append, edgeSum, lastFrom]
      have hih := ih b
      simp only [List.cons_append] at hih
      rw [hih]
      exact (Lean.Grind.Fin.add_assoc _ _ _).symm

def pairEdge (u v : ZMod4) : ZMod4 := u + v

def cyclicPairSum (values : List ZMod4) : ZMod4 :=
  edgeSum pairEdge (closeCycle values)

theorem cyclicPairSum_singleton (a : ZMod4) : cyclicPairSum [a] = a + a := by
  simp [cyclicPairSum, closeCycle, edgeSum, pairEdge]

theorem cyclicPairSum_cons_cons (a b : ZMod4) (rest : List ZMod4) :
    cyclicPairSum (a :: b :: rest) = (a + a) + cyclicPairSum (b :: rest) := by
  simp only [cyclicPairSum, closeCycle, List.cons_append, edgeSum]
  have ha := edgeSum_append_singleton pairEdge b a rest
  have hb := edgeSum_append_singleton pairEdge b b rest
  simp only [List.cons_append] at ha hb
  rw [ha, hb]
  simp only [pairEdge]
  grind

/-- Every cyclic adjacent-pair sum counts every value exactly twice. -/
theorem cyclicPairSum_eq_two_mul_sum (values : List ZMod4) :
    cyclicPairSum values = 2 * values.sum := by
  induction values with
  | nil => rfl
  | cons a rest ih =>
      cases rest with
      | nil =>
          rw [cyclicPairSum_singleton]
          simp only [List.sum_cons, List.sum_nil]
          grind
      | cons b bs =>
          rw [cyclicPairSum_cons_cons, ih]
          simp only [List.sum_cons]
          grind

/-- The local increment supplied by the checker-signed potential formula. -/
def checkerEdgeIncrement (odd : Bool) (u v : ZMod4) : ZMod4 :=
  -ResidueCharge.signed odd (u + v)

def cyclicCheckerIncrement (odd : Bool) (values : List ZMod4) : ZMod4 :=
  edgeSum (checkerEdgeIncrement odd) (closeCycle values)

theorem edgeSum_checker_eq_signed_pairSum (odd : Bool) (values : List ZMod4) :
    edgeSum (checkerEdgeIncrement odd) values =
      -ResidueCharge.signed odd (edgeSum pairEdge values) := by
  induction values with
  | nil => cases odd <;> simp [edgeSum, ResidueCharge.signed] <;> grind
  | cons a rest ih =>
      cases rest with
      | nil => cases odd <;> simp [edgeSum, ResidueCharge.signed] <;> grind
      | cons b bs =>
          simp only [edgeSum]
          rw [ih]
          cases odd <;> simp [checkerEdgeIncrement, pairEdge, ResidueCharge.signed] <;> grind

/--
Summing the local potential increments around a cyclic residue list gives
`2 * sum alpha`; the checker sign disappears because `-2 = 2` modulo four.
-/
theorem cyclicCheckerIncrement_eq_two_mul_sum (odd : Bool) (values : List ZMod4) :
    cyclicCheckerIncrement odd values = 2 * values.sum := by
  unfold cyclicCheckerIncrement
  rw [edgeSum_checker_eq_signed_pairSum, ← cyclicPairSum]
  rw [cyclicPairSum_eq_two_mul_sum]
  cases odd <;> simp [ResidueCharge.signed] <;> grind

/--
If a lifted finite path reads one complete cyclic alpha list and each local
potential difference is the checker formula, then its endpoint potential drift
is exactly `2 * sum alpha`.
-/
theorem potentialDrift_of_checkerCycle
    (potential : α → ZMod4) (alphaAt : α → ZMod4)
    (a : α) (rest : List α) (alphaCycle : List ZMod4) (odd : Bool)
    (hcycle : (a :: rest).map alphaAt = closeCycle alphaCycle)
    (hlocal : OnEdges
      (fun u v => checkerEdgeIncrement odd (alphaAt u) (alphaAt v) =
        potential v - potential u)
      (a :: rest)) :
    potential (lastFrom a rest) - potential a = 2 * alphaCycle.sum := by
  have htel := edgeSum_of_potential
    (fun u v => checkerEdgeIncrement odd (alphaAt u) (alphaAt v))
    potential a rest hlocal
  calc
    potential (lastFrom a rest) - potential a =
        edgeSum (fun u v => checkerEdgeIncrement odd (alphaAt u) (alphaAt v))
          (a :: rest) := htel.symm
    _ = edgeSum (checkerEdgeIncrement odd) ((a :: rest).map alphaAt) := by
      rw [edgeSum_map]
    _ = cyclicCheckerIncrement odd alphaCycle := by rw [hcycle]; rfl
    _ = 2 * alphaCycle.sum := cyclicCheckerIncrement_eq_two_mul_sum odd alphaCycle

/-! ## Finite translated-widget cancellation -/

def additiveCharge (weight : α → ZMod4) : List α → ZMod4
  | [] => 0
  | z :: zs => weight z + additiveCharge weight zs

theorem additiveCharge_map_of_periodic (weight : α → ZMod4) (translate : α → α)
    (widget : List α) (hperiodic : ∀ z, weight (translate z) = weight z) :
    additiveCharge weight (widget.map translate) = additiveCharge weight widget := by
  induction widget with
  | nil => rfl
  | cons z zs ih =>
      simp only [List.map_cons, additiveCharge]
      rw [hperiodic, ih]

theorem translatedWidgetDifference_eq_zero
    (weight : α → ZMod4) (translate : α → α) (widget : List α)
    (hperiodic : ∀ z, weight (translate z) = weight z) :
    additiveCharge weight (widget.map translate) - additiveCharge weight widget = 0 := by
  rw [additiveCharge_map_of_periodic weight translate widget hperiodic]
  grind

/--
The finite moving widget cancels from an additive conserved charge.  This is
the algebraic content of the `(T_d - 1)A` cancellation; the decomposition itself
is deliberately an explicit premise.
-/
theorem strandCharge_after_widgetCancellation
    (weight : α → ZMod4) (translate : α → α)
    (strands widget : List α) (potentialDrift : ZMod4)
    (hperiodic : ∀ z, weight (translate z) = weight z)
    (hconservation :
      additiveCharge weight strands +
        (additiveCharge weight (widget.map translate) - additiveCharge weight widget) +
        potentialDrift = 0) :
    additiveCharge weight strands + potentialDrift = 0 := by
  have hw := translatedWidgetDifference_eq_zero weight translate widget hperiodic
  rw [hw] at hconservation
  simpa using hconservation

/-- Local potential increments plus widget cancellation give the strand charge. -/
theorem strandCharge_from_localCycle_and_periodicWidget
    (weight : α → ZMod4) (translate : α → α)
    (strands widget : List α)
    (potential alphaAt : α → ZMod4)
    (a : α) (rest : List α) (alphaCycle : List ZMod4) (odd : Bool)
    (hperiodic : ∀ z, weight (translate z) = weight z)
    (hcycle : (a :: rest).map alphaAt = closeCycle alphaCycle)
    (hlocal : OnEdges
      (fun u v => checkerEdgeIncrement odd (alphaAt u) (alphaAt v) =
        potential v - potential u)
      (a :: rest))
    (hconservation :
      additiveCharge weight strands +
        (additiveCharge weight (widget.map translate) - additiveCharge weight widget) +
        (potential (lastFrom a rest) - potential a) = 0) :
    additiveCharge weight strands + 2 * alphaCycle.sum = 0 := by
  have hd := potentialDrift_of_checkerCycle potential alphaAt a rest alphaCycle odd hcycle hlocal
  have hc := strandCharge_after_widgetCancellation weight translate strands widget
    (potential (lastFrom a rest) - potential a) hperiodic hconservation
  rw [hd] at hc
  exact hc

/-! ## Explicit certificate boundary for the residue identity -/

structure LocalResidueCertificate (n : Nat) (α : Type)
    (bases : List (ResidueCharge.Base n)) (r : Fin n) where
  weight : α → ZMod4
  translate : α → α
  strands : List α
  widget : List α
  potential : α → ZMod4
  alphaAt : α → ZMod4
  start : α
  rest : List α
  alphaCycle : List ZMod4
  odd : Bool
  weight_periodic : ∀ z, weight (translate z) = weight z
  cycle_values : (start :: rest).map alphaAt = closeCycle alphaCycle
  local_potential : OnEdges
    (fun u v => checkerEdgeIncrement odd (alphaAt u) (alphaAt v) =
      potential v - potential u)
    (start :: rest)
  conserved_decomposition :
    additiveCharge weight strands +
      (additiveCharge weight (widget.map translate) - additiveCharge weight widget) +
      (potential (lastFrom start rest) - potential start) = 0
  strand_identification :
    additiveCharge weight strands = ResidueCharge.fiberCharge r bases
  delta_alpha_sum : alphaCycle.sum = 1

/-- A local certificate derives, rather than assumes, `E_r + 2 = 0`. -/
theorem localCertificate_implies_residueIdentity
    (cert : LocalResidueCertificate n α bases r) :
    ResidueCharge.fiberCharge r bases + 2 = 0 := by
  have hc := strandCharge_from_localCycle_and_periodicWidget
    cert.weight cert.translate cert.strands cert.widget cert.potential cert.alphaAt
    cert.start cert.rest cert.alphaCycle cert.odd cert.weight_periodic
    cert.cycle_values cert.local_potential cert.conserved_decomposition
  rw [cert.strand_identification, cert.delta_alpha_sum] at hc
  simpa using hc

/-- One local certificate per residue implies the global density bound. -/
theorem localCertificates_imply_growthBound
    (bases : List (ResidueCharge.Base n))
    (cert : ∀ r : Fin n, LocalResidueCertificate n α bases r) :
    2 * n ≤ bases.length := by
  apply ResidueCharge.cyclicCharge_implies_growth_bound bases
  intro r
  exact localCertificate_implies_residueIdentity (cert r)

end Langton.ChargeTelescoping
