import Langton.ChargeTelescoping
import Init.GrindInstances.Ring.Fin

namespace Langton.TraceGeometry

open Fin.IntCast

abbrev ZMod4 := Fin 4

/-! ## An exact finite trace with translation-orbit addresses -/

def posAdd (p q : Pos) : Pos := { x := p.x + q.x, y := p.y + q.y }

def posScale (k : Int) (p : Pos) : Pos := { x := k * p.x, y := k * p.y }

structure OrbitSite (n orbitCount : Nat) where
  residue : Fin n
  odd : Bool
  orbit : Fin orbitCount
  level : Int
deriving DecidableEq, Repr

def translateSite (s : OrbitSite n orbitCount) : OrbitSite n orbitCount :=
  { s with level := s.level + 1 }

/--
One candidate period of the exact ant kernel.  Phase positions and turns are
not free data: they are `run i initial` and `turnAt (run i initial)`.
`address_position` certifies the orbit/level address of every exact phase.
-/
structure ExactPeriodTrace (n orbitCount : Nat) where
  initial : State
  period : Nat
  drift : Pos
  orbitBase : Fin orbitCount → Pos
  address : Fin period → OrbitSite n orbitCount
  final_position : (run period initial).pos = posAdd initial.pos drift
  final_heading : (run period initial).dir = initial.dir
  address_position : ∀ i : Fin period,
    (run i.val initial).pos =
      posAdd (orbitBase (address i).orbit) (posScale (address i).level drift)

def phasePositions (trace : ExactPeriodTrace n orbitCount) : List Pos :=
  (List.finRange trace.period).map fun i => (run i.val trace.initial).pos

def phaseTurns (trace : ExactPeriodTrace n orbitCount) : List Turn :=
  (List.finRange trace.period).map fun i => turnAt (run i.val trace.initial)

theorem phasePositions_length (trace : ExactPeriodTrace n orbitCount) :
    (phasePositions trace).length = trace.period := by
  simp [phasePositions]

theorem phaseTurns_length (trace : ExactPeriodTrace n orbitCount) :
    (phaseTurns trace).length = trace.period := by
  simp [phaseTurns]

theorem phasePositions_eq_addressPositions (trace : ExactPeriodTrace n orbitCount) :
    phasePositions trace =
      (List.finRange trace.period).map fun i =>
        posAdd (trace.orbitBase (trace.address i).orbit)
          (posScale (trace.address i).level trace.drift) := by
  unfold phasePositions
  apply List.map_congr_left
  intro i hi
  exact trace.address_position i

def turnInt : Turn → Int
  | .right => 1
  | .left => -1

/-- Exact signed phase visits belonging to one drift orbit. -/
def orbitSignedToggles (trace : ExactPeriodTrace n orbitCount)
    (o : Fin orbitCount) : List (Int × Turn) :=
  ((List.finRange trace.period).filter fun i => (trace.address i).orbit == o).map
    fun i => ((trace.address i).level, turnAt (run i.val trace.initial))

def orbitToggleSum (trace : ExactPeriodTrace n orbitCount)
    (o : Fin orbitCount) : Int :=
  (orbitSignedToggles trace o).map (fun entry => turnInt entry.2) |>.sum

/-! ## Exact finite aggregation of phase toggles by drift level -/

/-- Add an integer coefficient at one in-bounds list index. -/
def addIntAt : Nat → Int → List Int → List Int
  | _, _, [] => []
  | 0, a, x :: xs => (x + a) :: xs
  | i + 1, a, x :: xs => x :: addIntAt i a xs

@[simp] theorem length_addIntAt (i : Nat) (a : Int) (xs : List Int) :
    (addIntAt i a xs).length = xs.length := by
  induction i generalizing xs with
  | zero => cases xs <;> simp [addIntAt]
  | succ i ih =>
      cases xs with
      | nil => rfl
      | cons x xs => simp [addIntAt, ih]

theorem sum_addIntAt_of_lt (i : Nat) (a : Int) (xs : List Int)
    (h : i < xs.length) :
    (addIntAt i a xs).sum = xs.sum + a := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => simp at h
      | cons x xs => simp [addIntAt]; omega
  | succ i ih =>
      cases xs with
      | nil => simp at h
      | cons x xs =>
          simp only [List.length_cons, Nat.succ_lt_succ_iff] at h
          simp only [addIntAt, List.sum_cons]
          rw [ih xs h]
          omega

/-- Zero-based list index of an orbit level relative to a chosen finite window. -/
def toggleIndex (origin level : Int) : Nat := (level - origin).toNat

/-- Every signed phase toggle lies in the chosen half-open integer window. -/
def EntriesCovered (origin : Int) (width : Nat) (entries : List (Int × Turn)) : Prop :=
  ∀ entry ∈ entries,
    origin ≤ entry.1 ∧ entry.1 < origin + (width : Int)

theorem toggleIndex_lt_of_covered (origin : Int) (width : Nat)
    (entries : List (Int × Turn)) (hcovered : EntriesCovered origin width entries)
    (entry : Int × Turn) (hmem : entry ∈ entries) :
    toggleIndex origin entry.1 < width := by
  have hbounds := hcovered entry hmem
  have hnonnegative : 0 ≤ entry.1 - origin := by omega
  unfold toggleIndex
  exact (Int.toNat_lt hnonnegative).2 (by omega)

/-- Aggregate an exact signed phase list into coefficients at consecutive levels. -/
def aggregateToggles (origin : Int) (width : Nat) (entries : List (Int × Turn)) :
    List Int :=
  entries.foldl
    (fun coeffs entry => addIntAt (toggleIndex origin entry.1) (turnInt entry.2) coeffs)
    (List.replicate width 0)

theorem foldl_addIntAt_sum (origin : Int) (width : Nat)
    (entries : List (Int × Turn)) (coeffs : List Int)
    (hlength : coeffs.length = width)
    (hcovered : EntriesCovered origin width entries) :
    (entries.foldl
      (fun values entry => addIntAt (toggleIndex origin entry.1) (turnInt entry.2) values)
      coeffs).sum =
      coeffs.sum + (entries.map (fun entry => turnInt entry.2)).sum := by
  induction entries generalizing coeffs with
  | nil => simp
  | cons entry entries ih =>
      have hhead : origin ≤ entry.1 ∧ entry.1 < origin + (width : Int) :=
        hcovered entry (by simp)
      have htail : EntriesCovered origin width entries := by
        intro e he
        exact hcovered e (by simp [he])
      have hindexWidth : toggleIndex origin entry.1 < width := by
        exact toggleIndex_lt_of_covered origin width (entry :: entries)
          hcovered entry (by simp)
      have hindex : toggleIndex origin entry.1 < coeffs.length := by
        simp [hlength, hindexWidth]
      have hsum := sum_addIntAt_of_lt (toggleIndex origin entry.1)
        (turnInt entry.2) coeffs hindex
      have hlength' :
          (addIntAt (toggleIndex origin entry.1) (turnInt entry.2) coeffs).length = width := by
        simp [hlength]
      rw [List.foldl_cons, ih
        (addIntAt (toggleIndex origin entry.1) (turnInt entry.2) coeffs)
        hlength' htail]
      simp only [List.map_cons, List.sum_cons]
      rw [hsum]
      omega

theorem aggregateToggles_sum (origin : Int) (width : Nat)
    (entries : List (Int × Turn)) (hcovered : EntriesCovered origin width entries) :
    (aggregateToggles origin width entries).sum =
      (entries.map (fun entry => turnInt entry.2)).sum := by
  unfold aggregateToggles
  rw [foldl_addIntAt_sum origin width entries (List.replicate width 0)
    (by simp) hcovered]
  simp

/-! ## Canonical finite endpoint/strand decomposition on one orbit -/

def addOneAt : Nat → List Int → List Int
  | _, [] => []
  | 0, x :: xs => (x + 1) :: xs
  | i + 1, x :: xs => x :: addOneAt i xs

def removeOneAt : Nat → List Int → List Int
  | _, [] => []
  | 0, x :: xs => (x - 1) :: xs
  | i + 1, x :: xs => x :: removeOneAt i xs

theorem addOneAt_removeOneAt (i : Nat) (xs : List Int) (h : i < xs.length) :
    addOneAt i (removeOneAt i xs) = xs := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => simp at h
      | cons x xs => simp [addOneAt, removeOneAt]
  | succ i ih =>
      cases xs with
      | nil => simp at h
      | cons x xs =>
          simp only [List.length_cons, Nat.succ_lt_succ_iff] at h
          simp [addOneAt, removeOneAt, ih xs h]

theorem sum_removeOneAt (i : Nat) (xs : List Int) (h : i < xs.length) :
    (removeOneAt i xs).sum = xs.sum - 1 := by
  induction i generalizing xs with
  | zero =>
      cases xs with
      | nil => simp at h
      | cons x xs =>
          simp only [removeOneAt, List.sum_cons]
          omega
  | succ i ih =>
      cases xs with
      | nil => simp at h
      | cons x xs =>
          simp only [List.length_cons, Nat.succ_lt_succ_iff] at h
          simp only [removeOneAt, List.sum_cons]
          rw [ih xs h]
          omega

/-- Recover widget coefficients from a balanced signed endpoint difference. -/
def scanWidget (previous : Int) : List Int → List Int
  | [] => []
  | b :: bs =>
      let current := previous - b
      current :: scanWidget current bs

/-- The coefficient list of `(T - 1)A`, starting with predecessor `previous`. -/
def differenceFromWidget (previous : Int) : List Int → List Int
  | [] => []
  | a :: as => (previous - a) :: differenceFromWidget a as

theorem difference_scanWidget (previous : Int) (balanced : List Int) :
    differenceFromWidget previous (scanWidget previous balanced) = balanced := by
  induction balanced generalizing previous with
  | nil => rfl
  | cons b bs ih =>
      simp only [scanWidget, differenceFromWidget]
      have hhead : previous - (previous - b) = b := by omega
      rw [hhead, ih]

theorem last_scanWidget (previous : Int) (balanced : List Int) :
    ChargeTelescoping.lastFrom previous (scanWidget previous balanced) =
      previous - balanced.sum := by
  induction balanced generalizing previous with
  | nil => simp [scanWidget, ChargeTelescoping.lastFrom]
  | cons b bs ih =>
      simp only [scanWidget, ChargeTelescoping.lastFrom, List.sum_cons]
      rw [ih]
      omega

structure OrbitEndpointData (n orbitCount : Nat) (o : Fin orbitCount) where
  residue : Fin n
  odd : Bool
  level0 : Int
  delta : List Int
  growth : Bool
  strandIndex : Nat
  strandIndex_valid : growth = true → strandIndex < delta.length
  strand_is_first_positive : ∀ hg : growth = true,
    delta[strandIndex]'(strandIndex_valid hg) = 1 ∧
      ∀ j, (hj : j < strandIndex) →
        delta[j]'(Nat.lt_trans hj (strandIndex_valid hg)) ≠ 1
  balanced_sum_zero :
    (if growth then removeOneAt strandIndex delta else delta).sum = 0
  binary_prefix : ∀ a ∈
    scanWidget 0 (if growth then removeOneAt strandIndex delta else delta),
    a = 0 ∨ a = 1

def OrbitEndpointData.balanced (data : OrbitEndpointData n orbitCount o) : List Int :=
  if data.growth then removeOneAt data.strandIndex data.delta else data.delta

def OrbitEndpointData.widgetCoeffs (data : OrbitEndpointData n orbitCount o) : List Int :=
  scanWidget 0 data.balanced

theorem OrbitEndpointData.widget_binary (data : OrbitEndpointData n orbitCount o) :
    ∀ a ∈ data.widgetCoeffs, a = 0 ∨ a = 1 := by
  exact data.binary_prefix

theorem OrbitEndpointData.widget_terminal_zero (data : OrbitEndpointData n orbitCount o) :
    ChargeTelescoping.lastFrom 0 data.widgetCoeffs = 0 := by
  unfold OrbitEndpointData.widgetCoeffs
  rw [last_scanWidget]
  simp only [Int.zero_sub]
  have hz : data.balanced.sum = 0 := by
    simpa [OrbitEndpointData.balanced] using data.balanced_sum_zero
  rw [hz]
  rfl

theorem OrbitEndpointData.delta_sum (data : OrbitEndpointData n orbitCount o) :
    data.delta.sum = if data.growth then 1 else 0 := by
  cases hg : data.growth with
  | false =>
      have hz : data.delta.sum = 0 := by
        simpa [OrbitEndpointData.balanced, hg] using data.balanced_sum_zero
      exact hz
  | true =>
      have hremove := sum_removeOneAt data.strandIndex data.delta
        (data.strandIndex_valid hg)
      have hz : (removeOneAt data.strandIndex data.delta).sum = 0 := by
        simpa [hg] using data.balanced_sum_zero
      have hsum : data.delta.sum = 1 := by
        rw [hremove] at hz
        omega
      exact hsum

/-- Exact coefficient form `D = S + (T - 1)A`. -/
theorem OrbitEndpointData.canonical_decomposition
    (data : OrbitEndpointData n orbitCount o) :
    data.delta =
      if data.growth then
        addOneAt data.strandIndex (differenceFromWidget 0 data.widgetCoeffs)
      else differenceFromWidget 0 data.widgetCoeffs := by
  have hdiff : differenceFromWidget 0 data.widgetCoeffs = data.balanced := by
    exact difference_scanWidget 0 data.balanced
  by_cases hg : data.growth = true
  · simp only [hg, if_true]
    rw [hdiff]
    simp only [OrbitEndpointData.balanced, hg, if_true]
    exact (addOneAt_removeOneAt data.strandIndex data.delta
      (data.strandIndex_valid hg)).symm
  · cases hgf : data.growth with
    | false => simp [hgf, hdiff, OrbitEndpointData.balanced]
    | true => exact False.elim (hg hgf)

/-! ## Canonical strand and widget sites -/

def collectOnesFrom (make : Nat → α) : List Int → List α
  | [] => []
  | a :: as =>
      let tail := collectOnesFrom (fun i => make (i + 1)) as
      if a = 1 then make 0 :: tail else tail

def endpointSite (data : OrbitEndpointData n orbitCount o) (i : Nat) :
    OrbitSite n orbitCount :=
  { residue := data.residue
    odd := data.odd
    orbit := o
    level := data.level0 + Int.ofNat i }

def canonicalStrandSites (data : OrbitEndpointData n orbitCount o) :
    List (OrbitSite n orbitCount) :=
  if data.growth then [endpointSite data data.strandIndex] else []

def canonicalWidgetSites (data : OrbitEndpointData n orbitCount o) :
    List (OrbitSite n orbitCount) :=
  collectOnesFrom (endpointSite data) data.widgetCoeffs

/-- Normalized orbit data tied to the exact signed phase list. -/
structure NormalizedTrace (n orbitCount : Nat) where
  trace : ExactPeriodTrace n orbitCount
  endpoint : ∀ o : Fin orbitCount, OrbitEndpointData n orbitCount o
  entries_covered : ∀ o : Fin orbitCount,
    EntriesCovered (endpoint o).level0 (endpoint o).delta.length
      (orbitSignedToggles trace o)
  delta_exact : ∀ o : Fin orbitCount,
    (endpoint o).delta =
      aggregateToggles (endpoint o).level0 (endpoint o).delta.length
        (orbitSignedToggles trace o)

theorem NormalizedTrace.delta_sum_matches_phases
    (normal : NormalizedTrace n orbitCount) (o : Fin orbitCount) :
    (normal.endpoint o).delta.sum = orbitToggleSum normal.trace o := by
  rw [normal.delta_exact o]
  simpa [orbitToggleSum] using aggregateToggles_sum
    (normal.endpoint o).level0 (normal.endpoint o).delta.length
    (orbitSignedToggles normal.trace o) (normal.entries_covered o)

def allStrandSites (normal : NormalizedTrace n orbitCount) :
    List (OrbitSite n orbitCount) :=
  (List.finRange orbitCount).flatMap fun o => canonicalStrandSites (normal.endpoint o)

def allWidgetSites (normal : NormalizedTrace n orbitCount) :
    List (OrbitSite n orbitCount) :=
  (List.finRange orbitCount).flatMap fun o => canonicalWidgetSites (normal.endpoint o)

def siteBase (site : OrbitSite n orbitCount) : ResidueCharge.Base n :=
  (site.residue, site.odd)

def canonicalBases (normal : NormalizedTrace n orbitCount) :
    List (ResidueCharge.Base n) := (allStrandSites normal).map siteBase

/-! ## Certificate fields that now follow mechanically -/

def residueWeight (r : Fin n) (site : OrbitSite n orbitCount) : ZMod4 :=
  if site.residue = r then ResidueCharge.paritySign site.odd else 0

theorem residueWeight_translate (r : Fin n) (site : OrbitSite n orbitCount) :
    residueWeight r (translateSite site) = residueWeight r site := by
  rfl

theorem additiveResidueWeight_eq_fiberCharge (r : Fin n)
    (sites : List (OrbitSite n orbitCount)) :
    ChargeTelescoping.additiveCharge (residueWeight r) sites =
      ResidueCharge.fiberCharge r (sites.map siteBase) := by
  induction sites with
  | nil => rfl
  | cons site sites ih =>
      by_cases h : site.residue = r
      · simp [ChargeTelescoping.additiveCharge, residueWeight, siteBase,
          ResidueCharge.fiberCharge, h, ih]
      · simp [ChargeTelescoping.additiveCharge, residueWeight, siteBase,
          ResidueCharge.fiberCharge, h, ih]

/-! ## Exact grouped phase charge and its strand reduction -/

def intMod4 (z : Int) : ZMod4 := Int.cast z

def signedToggleCharge (weight : ZMod4) : List (Int × Turn) → ZMod4
  | [] => 0
  | entry :: entries =>
      (match entry.2 with | .right => weight | .left => -weight) +
        signedToggleCharge weight entries

theorem signedToggleCharge_eq_balance (weight : ZMod4)
    (entries : List (Int × Turn)) :
  signedToggleCharge weight entries =
      intMod4 ((entries.map fun entry => turnInt entry.2).sum) * weight := by
  induction entries with
  | nil =>
      change (0 : ZMod4) = (0 : ZMod4) * weight
      exact (Fin.zero_mul weight).symm
  | cons entry entries ih =>
      cases entry with
      | mk level turn =>
          cases turn <;>
            simp [signedToggleCharge, turnInt, intMod4, ih, List.sum_cons] <;> grind

def orbitClassWeight (normal : NormalizedTrace n orbitCount) (r : Fin n)
    (o : Fin orbitCount) : ZMod4 :=
  residueWeight r (endpointSite (normal.endpoint o) 0)

def orbitPhaseCharge (normal : NormalizedTrace n orbitCount) (r : Fin n)
    (o : Fin orbitCount) : ZMod4 :=
  signedToggleCharge (orbitClassWeight normal r o)
    (orbitSignedToggles normal.trace o)

theorem orbitPhaseCharge_eq_strandCharge
    (normal : NormalizedTrace n orbitCount) (r : Fin n) (o : Fin orbitCount) :
    orbitPhaseCharge normal r o =
      ChargeTelescoping.additiveCharge (residueWeight r)
        (canonicalStrandSites (normal.endpoint o)) := by
  rw [orbitPhaseCharge, signedToggleCharge_eq_balance]
  have hsum := normal.delta_sum_matches_phases o
  have hgrowth := (normal.endpoint o).delta_sum
  change intMod4 (orbitToggleSum normal.trace o) * orbitClassWeight normal r o = _
  rw [← hsum, hgrowth]
  cases hg : (normal.endpoint o).growth <;>
    simp [hg, intMod4, orbitClassWeight, canonicalStrandSites,
      ChargeTelescoping.additiveCharge, endpointSite, residueWeight] <;> grind

def groupedPhaseCharge (normal : NormalizedTrace n orbitCount) (r : Fin n) : ZMod4 :=
  ((List.finRange orbitCount).map fun o => orbitPhaseCharge normal r o).sum

theorem additiveCharge_append (weight : α → ZMod4) (xs ys : List α) :
    ChargeTelescoping.additiveCharge weight (xs ++ ys) =
      ChargeTelescoping.additiveCharge weight xs +
        ChargeTelescoping.additiveCharge weight ys := by
  induction xs with
  | nil => simp [ChargeTelescoping.additiveCharge]
  | cons x xs ih =>
      simp [ChargeTelescoping.additiveCharge, ih, Lean.Grind.Fin.add_assoc]

theorem groupedPhaseCharge_eq_strandCharge
    (normal : NormalizedTrace n orbitCount) (r : Fin n) :
    groupedPhaseCharge normal r =
      ChargeTelescoping.additiveCharge (residueWeight r) (allStrandSites normal) := by
  unfold groupedPhaseCharge allStrandSites
  generalize List.finRange orbitCount = orbits
  induction orbits with
  | nil => rfl
  | cons o os ih =>
      simp only [List.map_cons, List.sum_cons, List.flatMap_cons]
      rw [orbitPhaseCharge_eq_strandCharge, additiveCharge_append, ih]

def deltaAlphaCycle (r : Fin n) : List ZMod4 :=
  (List.finRange n).map fun s => if r = s then 1 else 0

def residueAlpha (r : Fin n) (site : OrbitSite n orbitCount) : ZMod4 :=
  if r = site.residue then 1 else 0

theorem map_closeCycle (f : α → β) (values : List α) :
    (ChargeTelescoping.closeCycle values).map f =
      ChargeTelescoping.closeCycle (values.map f) := by
  cases values <;> simp [ChargeTelescoping.closeCycle]

theorem residueAlpha_cycle_values (r : Fin n)
    (start : OrbitSite n orbitCount) (rest : List (OrbitSite n orbitCount))
    (hresidues :
      (start :: rest).map (fun site => site.residue) =
        ChargeTelescoping.closeCycle (List.finRange n)) :
    (start :: rest).map (residueAlpha r) =
      ChargeTelescoping.closeCycle (deltaAlphaCycle r) := by
  calc
    (start :: rest).map (residueAlpha r) =
        ((start :: rest).map (fun site => site.residue)).map
          (fun s => if r = s then (1 : ZMod4) else 0) := by
            simp [List.map_map, residueAlpha]
    _ = (ChargeTelescoping.closeCycle (List.finRange n)).map
          (fun s => if r = s then (1 : ZMod4) else 0) := by rw [hresidues]
    _ = ChargeTelescoping.closeCycle
          ((List.finRange n).map fun s => if r = s then (1 : ZMod4) else 0) :=
            map_closeCycle _ _
    _ = ChargeTelescoping.closeCycle (deltaAlphaCycle r) := rfl

def zIndicator (r : Fin n) : List (Fin n) → ZMod4
  | [] => 0
  | s :: ss => (if r = s then 1 else 0) + zIndicator r ss

theorem zIndicator_zero_of_not_mem (r : Fin n) (residues : List (Fin n))
    (hnot : r ∉ residues) : zIndicator r residues = 0 := by
  induction residues with
  | nil => rfl
  | cons s ss ih =>
      have hne : r ≠ s := by
        intro h
        apply hnot
        simp [h]
      have htail : r ∉ ss := by
        intro h
        apply hnot
        simp [h]
      simp [zIndicator, hne, ih htail]

theorem zIndicator_one_of_nodup_mem (r : Fin n) (residues : List (Fin n))
    (hnd : residues.Nodup) (hmem : r ∈ residues) : zIndicator r residues = 1 := by
  induction residues with
  | nil => simp at hmem
  | cons s ss ih =>
      have hnd' : s ∉ ss ∧ ss.Nodup := by simpa using hnd
      by_cases h : r = s
      · subst s
        rw [show zIndicator r (r :: ss) = 1 + zIndicator r ss by
          simp [zIndicator]]
        rw [zIndicator_zero_of_not_mem r ss hnd'.1]
        grind
      · have htail : r ∈ ss := by
          have hm : r = s ∨ r ∈ ss := by simpa using hmem
          exact hm.resolve_left h
        simp [zIndicator, h, ih hnd'.2 htail]

theorem deltaAlphaCycle_sum (r : Fin n) : (deltaAlphaCycle r).sum = 1 := by
  have hz := zIndicator_one_of_nodup_mem r (List.finRange n)
    (ResidueCharge.finRange_nodup n) (List.mem_finRange r)
  have heq : ((List.finRange n).map fun s => if r = s then (1 : ZMod4) else 0).sum =
      zIndicator r (List.finRange n) := by
    generalize List.finRange n = residues
    induction residues with
    | nil => rfl
    | cons s ss ih => simp [zIndicator, ih]
  unfold deltaAlphaCycle
  rw [heq]
  exact hz

/--
Only potential/charge geometry remains here.  All combinatorial fields of the
old local certificate are supplied by `NormalizedTrace` and the definitions
above.
-/
structure RemainingPotentialGeometry
    (normal : NormalizedTrace n orbitCount) (r : Fin n) where
  potential : OrbitSite n orbitCount → ZMod4
  start : OrbitSite n orbitCount
  rest : List (OrbitSite n orbitCount)
  residue_cycle :
    (start :: rest).map (fun site => site.residue) =
      ChargeTelescoping.closeCycle (List.finRange n)
  local_potential : ChargeTelescoping.OnEdges
    (fun u v => ChargeTelescoping.checkerEdgeIncrement start.odd
      (residueAlpha r u) (residueAlpha r v) = potential v - potential u)
    (start :: rest)
  conserved_trace_charge :
    groupedPhaseCharge normal r +
      (potential (ChargeTelescoping.lastFrom start rest) - potential start) = 0

def toLocalResidueCertificate
    (normal : NormalizedTrace n orbitCount) (r : Fin n)
    (remaining : RemainingPotentialGeometry normal r) :
    ChargeTelescoping.LocalResidueCertificate n (OrbitSite n orbitCount)
      (canonicalBases normal) r :=
  { weight := residueWeight r
    translate := translateSite
    strands := allStrandSites normal
    widget := allWidgetSites normal
    potential := remaining.potential
    alphaAt := residueAlpha r
    start := remaining.start
    rest := remaining.rest
    alphaCycle := deltaAlphaCycle r
    odd := remaining.start.odd
    weight_periodic := residueWeight_translate r
    cycle_values := residueAlpha_cycle_values r remaining.start remaining.rest
      remaining.residue_cycle
    local_potential := remaining.local_potential
    conserved_decomposition := by
      have hphase := remaining.conserved_trace_charge
      rw [groupedPhaseCharge_eq_strandCharge] at hphase
      have hwidget := ChargeTelescoping.translatedWidgetDifference_eq_zero
        (residueWeight r) translateSite (allWidgetSites normal)
        (residueWeight_translate r)
      rw [hwidget]
      simpa using hphase
    strand_identification := additiveResidueWeight_eq_fiberCharge r (allStrandSites normal)
    delta_alpha_sum := deltaAlphaCycle_sum r }

theorem remainingGeometry_implies_residueIdentity
    (normal : NormalizedTrace n orbitCount) (r : Fin n)
    (remaining : RemainingPotentialGeometry normal r) :
    ResidueCharge.fiberCharge r (canonicalBases normal) + 2 = 0 := by
  exact ChargeTelescoping.localCertificate_implies_residueIdentity
    (toLocalResidueCertificate normal r remaining)

theorem remainingGeometry_implies_growthBound
    (normal : NormalizedTrace n orbitCount)
    (remaining : ∀ r : Fin n, RemainingPotentialGeometry normal r) :
    2 * n ≤ (canonicalBases normal).length := by
  apply ResidueCharge.cyclicCharge_implies_growth_bound
  intro r
  exact remainingGeometry_implies_residueIdentity normal r (remaining r)

end Langton.TraceGeometry
