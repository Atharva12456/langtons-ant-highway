import Langton

namespace Langton.ResidueCharge

/-!
# Cyclic mod-four residue charge

This module isolates the finite algebra in the new residue-charge argument.
`Fin n` is the cyclic horizontal residue set and `Fin 4` is `Z/4Z`.
A strand base records its horizontal residue and the parity of `x+y`.

The geometric derivation of the charge identity from a Langton trace is not
assumed silently: the final density theorem takes that identity as a named
hypothesis.
-/

abbrev ZMod4 := Fin 4
abbrev Base (n : Nat) := Fin n × Bool

/-- `false` is checkerboard sign `+1`; `true` is sign `-1`. -/
def signed (odd : Bool) (z : ZMod4) : ZMod4 :=
  if odd then -z else z

def paritySign (odd : Bool) : ZMod4 :=
  signed odd 1

/-- The weight `(-1)^(x+y) * alpha(x mod n)`. -/
def checkerWeight (alpha : Fin n → ZMod4) (residue : Fin n) (odd : Bool) : ZMod4 :=
  signed odd (alpha residue)

theorem checkerWeight_eq_paritySign_mul (alpha : Fin n → ZMod4)
    (residue : Fin n) (odd : Bool) :
    checkerWeight alpha residue odd = paritySign odd * alpha residue := by
  cases odd <;> simp [checkerWeight, paritySign, signed] <;> grind

/--
Four-corner admissibility: the mixed difference of every checker-signed cyclic
weight is zero, for completely arbitrary `alpha`.
-/
theorem fourCornerAdmissible (alpha : Fin n → ZMod4)
    (r s : Fin n) (odd : Bool) :
    checkerWeight alpha r odd + checkerWeight alpha s (!odd) +
      checkerWeight alpha r (!odd) + checkerWeight alpha s odd = 0 := by
  cases odd <;> simp [checkerWeight, signed] <;> grind

/-- Number of bases in one cyclic horizontal residue. -/
def fiberCard (r : Fin n) : List (Base n) → Nat
  | [] => 0
  | b :: bs => (if b.1 = r then 1 else 0) + fiberCard r bs

/-- Signed checkerboard sum `E_r` in `Z/4Z` for one residue fiber. -/
def fiberCharge (r : Fin n) : List (Base n) → ZMod4
  | [] => 0
  | b :: bs =>
      if b.1 = r then paritySign b.2 + fiberCharge r bs
      else fiberCharge r bs

theorem paritySign_is_odd (odd : Bool) : (paritySign odd).val % 2 = 1 := by
  cases odd <;> rfl

theorem fin4_add_mod_two (u v : ZMod4) :
    (u + v).val % 2 = (u.val + v.val) % 2 := by
  simp only [Fin.val_add]
  omega

/-- Reducing `E_r` modulo two forgets signs and counts the fiber. -/
theorem fiberCharge_mod_two_eq_card (r : Fin n) (bases : List (Base n)) :
    (fiberCharge r bases).val % 2 = fiberCard r bases % 2 := by
  induction bases with
  | nil => rfl
  | cons b bs ih =>
      by_cases h : b.1 = r
      · simp only [fiberCharge, fiberCard, h, if_pos]
        rw [fin4_add_mod_two]
        have hs := paritySign_is_odd b.2
        omega
      · simp [fiberCharge, fiberCard, h, ih]

theorem fiberCharge_eq_zero_of_card_eq_zero (r : Fin n) (bases : List (Base n))
    (hzero : fiberCard r bases = 0) : fiberCharge r bases = 0 := by
  induction bases with
  | nil => rfl
  | cons b bs ih =>
      by_cases h : b.1 = r
      · simp [fiberCard, h] at hzero
      · have hzero' : fiberCard r bs = 0 := by
          simpa [fiberCard, h] using hzero
        simp [fiberCharge, h, ih hzero']

/-- The cyclic charge equation `E_r + 2 = 0` is exactly `E_r = 2`. -/
theorem chargeIdentity_implies_two (e : ZMod4) (h : e + 2 = 0) : e = 2 := by
  have hv := congrArg Fin.val h
  simp only [Fin.val_add] at hv
  apply Fin.ext
  change e.val = 2
  omega

/-- A residue charge equal to two has positive, even fiber cardinality. -/
theorem chargeTwo_implies_positive_even (r : Fin n) (bases : List (Base n))
    (hcharge : fiberCharge r bases = 2) :
    0 < fiberCard r bases ∧ fiberCard r bases % 2 = 0 := by
  constructor
  · cases hcard : fiberCard r bases with
    | zero =>
        have hc0 := fiberCharge_eq_zero_of_card_eq_zero r bases hcard
        rw [hcharge] at hc0
        contradiction
    | succ k => exact Nat.zero_lt_succ k
  · have hp := fiberCharge_mod_two_eq_card r bases
    rw [hcharge] at hp
    simpa using hp.symm

/-- Direct form using the charge-conservation identity from the geometry. -/
theorem chargeIdentity_implies_positive_even (r : Fin n) (bases : List (Base n))
    (hidentity : fiberCharge r bases + 2 = 0) :
    0 < fiberCard r bases ∧ fiberCard r bases % 2 = 0 := by
  apply chargeTwo_implies_positive_even r bases
  exact chargeIdentity_implies_two (fiberCharge r bases) hidentity

/-- Hence every such fiber contains at least two bases. -/
theorem chargeTwo_implies_two_le_card (r : Fin n) (bases : List (Base n))
    (hcharge : fiberCharge r bases = 2) : 2 ≤ fiberCard r bases := by
  have h := chargeTwo_implies_positive_even r bases hcharge
  omega

/-! ## Exact partition of a finite base list by cyclic residues -/

def indicatorCount (target : Fin n) : List (Fin n) → Nat
  | [] => 0
  | r :: rs => (if target = r then 1 else 0) + indicatorCount target rs

def sumFiberCards (residues : List (Fin n)) (bases : List (Base n)) : Nat :=
  match residues with
  | [] => 0
  | r :: rs => fiberCard r bases + sumFiberCards rs bases

theorem indicatorCount_eq_zero_of_not_mem (target : Fin n) (residues : List (Fin n))
    (hnot : target ∉ residues) : indicatorCount target residues = 0 := by
  induction residues with
  | nil => rfl
  | cons r rs ih =>
      have hne : target ≠ r := by
        intro h
        apply hnot
        simp [h]
      have htail : target ∉ rs := by
        intro h
        apply hnot
        simp [h]
      simp [indicatorCount, hne, ih htail]

theorem indicatorCount_eq_one_of_nodup_mem (target : Fin n) (residues : List (Fin n))
    (hnd : residues.Nodup) (hmem : target ∈ residues) :
    indicatorCount target residues = 1 := by
  induction residues with
  | nil => simp at hmem
  | cons r rs ih =>
      have hnd' : r ∉ rs ∧ rs.Nodup := by simpa using hnd
      by_cases h : target = r
      · subst r
        simp [indicatorCount, indicatorCount_eq_zero_of_not_mem target rs hnd'.1]
      · have htail : target ∈ rs := by
          have hm : target = r ∨ target ∈ rs := by simpa using hmem
          exact hm.resolve_left h
        simp [indicatorCount, h, ih hnd'.2 htail]

theorem finRange_nodup (n : Nat) : (List.finRange n).Nodup := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [List.finRange_succ]
      simp only [List.nodup_cons]
      constructor
      · simp [Fin.succ_ne_zero]
      · rw [List.nodup_iff_pairwise_ne] at ih ⊢
        exact ih.map Fin.succ (by
          intro a b hab h
          apply hab
          exact Fin.succ_inj.mp h)

theorem indicatorCount_finRange (target : Fin n) :
    indicatorCount target (List.finRange n) = 1 :=
  indicatorCount_eq_one_of_nodup_mem target (List.finRange n)
    (finRange_nodup n) (List.mem_finRange target)

theorem sumFiberCards_cons (residues : List (Fin n))
    (b : Base n) (bases : List (Base n)) :
    sumFiberCards residues (b :: bases) =
      indicatorCount b.1 residues + sumFiberCards residues bases := by
  induction residues with
  | nil => rfl
  | cons r rs ih =>
      by_cases h : b.1 = r
      · simp [sumFiberCards, fiberCard, indicatorCount, h, ih,
          Nat.add_assoc, Nat.add_left_comm]
      · simp [sumFiberCards, fiberCard, indicatorCount, h, ih,
          Nat.add_left_comm]

/-- The residue fibers partition the base list exactly. -/
theorem sumFiberCards_finRange_eq_length (bases : List (Base n)) :
    sumFiberCards (List.finRange n) bases = bases.length := by
  induction bases with
  | nil =>
      induction List.finRange n with
      | nil => rfl
      | cons r rs ih => simp [sumFiberCards, fiberCard, ih]
  | cons b bs ih =>
      rw [sumFiberCards_cons, indicatorCount_finRange, ih]
      simp [Nat.add_comm]

theorem two_mul_length_le_sumFiberCards (residues : List (Fin n))
    (bases : List (Base n))
    (hEach : ∀ r ∈ residues, 2 ≤ fiberCard r bases) :
    2 * residues.length ≤ sumFiberCards residues bases := by
  induction residues with
  | nil => simp [sumFiberCards]
  | cons r rs ih =>
      have hr : 2 ≤ fiberCard r bases := hEach r (by simp)
      have hrs : ∀ s ∈ rs, 2 ≤ fiberCard s bases := by
        intro s hs
        exact hEach s (by simp [hs])
      have ht := ih hrs
      simp only [sumFiberCards, List.length_cons]
      omega

/--
Main finite consequence.  If every cyclic residue obeys the charge identity
`E_r + 2 = 0`, then every residue contains at least two bases and the total
strand count is at least `2*n`.
-/
theorem cyclicCharge_implies_growth_bound (bases : List (Base n))
    (hcharge : ∀ r : Fin n, fiberCharge r bases + 2 = 0) :
    2 * n ≤ bases.length := by
  have hEach : ∀ r ∈ List.finRange n, 2 ≤ fiberCard r bases := by
    intro r _
    apply chargeTwo_implies_two_le_card r bases
    exact chargeIdentity_implies_two (fiberCharge r bases) (hcharge r)
  have hsum := two_mul_length_le_sumFiberCards (List.finRange n) bases hEach
  rw [List.length_finRange, sumFiberCards_finRange_eq_length] at hsum
  exact hsum

/-- Same conclusion with an explicitly named total growth/strand count `g`. -/
theorem cyclicCharge_implies_explicit_growth_bound (bases : List (Base n)) (g : Nat)
    (hg : g = bases.length)
    (hcharge : ∀ r : Fin n, fiberCharge r bases + 2 = 0) :
    2 * n ≤ g := by
  rw [hg]
  exact cyclicCharge_implies_growth_bound bases hcharge

end Langton.ResidueCharge
