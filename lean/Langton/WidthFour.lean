import Langton

namespace Langton.WidthFour

/-!
# Arithmetic certificates for the width-four macro reduction

These lemmas check the finite arithmetic at the end of the width-four argument.
They deliberately expose the geometric inputs as hypotheses: the paper must still
derive the transition-count identities and inequalities from the exact P3 criterion
and extremal-line rigidity.
-/

/-- The signed mod-four equation on five binary transverse levels has exactly
the six masks listed in the paper. -/
theorem sixMask_of_signedCharge
    (o0 o1 o2 o3 o4 : Nat)
    (h0 : o0 <= 1) (h1 : o1 <= 1) (h2 : o2 <= 1)
    (h3 : o3 <= 1) (h4 : o4 <= 1)
    (hcharge : (o0 + 3 * o1 + o2 + 3 * o3 + o4) % 4 = 2) :
    (o0 = 1 /\ o1 = 0 /\ o2 = 1 /\ o3 = 0 /\ o4 = 0) \/
    (o0 = 0 /\ o1 = 1 /\ o2 = 0 /\ o3 = 1 /\ o4 = 0) \/
    (o0 = 1 /\ o1 = 0 /\ o2 = 0 /\ o3 = 0 /\ o4 = 1) \/
    (o0 = 0 /\ o1 = 0 /\ o2 = 1 /\ o3 = 0 /\ o4 = 1) \/
    (o0 = 1 /\ o1 = 1 /\ o2 = 1 /\ o3 = 0 /\ o4 = 1) \/
    (o0 = 1 /\ o1 = 0 /\ o2 = 1 /\ o3 = 1 /\ o4 = 1) := by
  have c0 : o0 = 0 \/ o0 = 1 := by omega
  have c1 : o1 = 0 \/ o1 = 1 := by omega
  have c2 : o2 = 0 \/ o2 = 1 := by omega
  have c3 : o3 = 0 \/ o3 = 1 := by omega
  have c4 : o4 = 0 \/ o4 = 1 := by omega
  rcases c0 with rfl | rfl <;>
    rcases c1 with rfl | rfl <;>
    rcases c2 with rfl | rfl <;>
    rcases c3 with rfl | rfl <;>
    rcases c4 with rfl | rfl <;>
    simp at hcharge ⊢

/-- An even fiber occupying at most `W+1` levels occupies at most `W` levels
when the transverse width `W` is even. -/
theorem evenFiber_le_evenWidth
    (fiberCard width : Nat)
    (hfiber : fiberCard % 2 = 0)
    (hwidth : width % 2 = 0)
    (hlevels : fiberCard <= width + 1) :
    fiberCard <= width := by
  omega

theorem sum_le_length_mul_of_each_le
    (values : List Nat) (bound : Nat)
    (hEach : ∀ value ∈ values, value <= bound) :
    values.sum <= values.length * bound := by
  induction values with
  | nil => simp
  | cons value values ih =>
      have hvalue : value <= bound := hEach value (by simp)
      have htail : ∀ later ∈ values, later <= bound := by
        intro later hlater
        exact hEach later (by simp [hlater])
      have hsum := ih htail
      simp only [List.sum_cons, List.length_cons, Nat.succ_mul]
      omega

/-- Arithmetic endpoint of the diagonal width-growth upper bound: `m` residue
fibers, each of size at most `W`, contain at most `m*W` odd classes. -/
theorem growth_le_drift_mul_width
    (fibers : List Nat) (m width growth : Nat)
    (hlength : fibers.length = m)
    (hEach : ∀ fiber ∈ fibers, fiber <= width)
    (hgrowth : growth = fibers.sum) :
    growth <= m * width := by
  rw [hgrowth, ← hlength]
  exact sum_le_length_mul_of_each_le fibers width hEach

/--
If `c` and `f` are the two boundary-entering flow counts, and `lowerL` and
`upperL` are the left-turn counts on the two odd lines, then extremal uniqueness,
nonnegative P3 class excess, and the signed displacement identity imply the
sharpened macro-period bound `P + 8*x <= 7*m`.
-/
theorem macroPeriod_le_seven_mul_drift
    (m x c f y lowerL upperL P : Nat)
    (hbottom : x + c <= m)
    (htop : f + y <= m)
    (hlower : lowerL <= 2 * c)
    (hdisplacement : m + upperL + 2 * x = lowerL + 2 * y)
    (hperiod : P = 2 * c + 2 * f + lowerL + upperL) :
    P + 8 * x <= 7 * m := by
  omega

/-- A walk of `P` unit `+1` and `-1` macro moves ending at displacement `m` has
the same parity as `m`. -/
theorem macroPeriod_mod_two_eq_drift
    (m P plus minus : Nat)
    (hperiod : P = plus + minus)
    (hdisplacement : plus = m + minus) :
    P % 2 = m % 2 := by
  omega

/-- Combining the width-four macro bound with strand density gives `N <= 7*g`. -/
theorem antPeriod_le_seven_mul_growth
    (macroPeriod antPeriod m growth : Nat)
    (hmacro : macroPeriod <= 7 * m)
    (hperiod : antPeriod = 2 * macroPeriod)
    (hdensity : 2 * m <= growth) :
    antPeriod <= 7 * growth := by
  omega

/--
Primitive drift has one visit to each extreme.  Once growth/class parity and
macro-period parity force the two odd-line left-turn totals to be `1` and `2` in
some order, the macro period is exactly seven.
-/
theorem primitive_macroPeriod_eq_seven
    (c f lowerL upperL P : Nat)
    (hc : c = 1)
    (hf : f = 1)
    (hoddLines :
      (lowerL = 1 /\ upperL = 2) \/ (lowerL = 2 /\ upperL = 1))
    (hperiod : P = 2 * c + 2 * f + lowerL + upperL) :
    P = 7 := by
  rcases hoddLines with h | h <;> omega

/-- Arithmetic kernel behind the spatial-block form of P3.  `baseHigh` and
`baseLow` are consecutive (or more widely separated) multiples of the ant period
attached to two physical cells in one translation class.  Every phase key from the
higher cell precedes every phase key from the lower cell. -/
theorem higherCellBlock_precedes
    (period phaseHigh phaseLow baseHigh baseLow : Int)
    (hphaseHighN : phaseHigh < period)
    (hphaseLow0 : 0 <= phaseLow)
    (hbase : baseLow + period <= baseHigh) :
    phaseHigh - baseHigh < phaseLow - baseLow := by
  omega

/-- If a length-at-most-`7m` unit walk has positive odd crossing count on all `m`
cut residues modulo its drift, then at least one quarter have count at most
seven. `largeCuts` contribute at least nine crossings and all other cuts at least
one, giving the hypothesis `9*m <= total + 8*lowCuts`. -/
theorem many_low_crossing_cuts
    (m total lowCuts : Nat)
    (htotal : total <= 7 * m)
    (hcount : 9 * m <= total + 8 * lowCuts) :
    m <= 4 * lowCuts := by
  omega

/-- Finite cardinality of the splice-sufficient control signatures of odd length
at most seven. Direction is forced by the alternating position, leaving two
geometrically possible even destination lines at every crossing. -/
theorem shortControlSignature_count :
    2 + 2^3 + 2^5 + 2^7 = 170 := by
  decide

/-- Arithmetic endpoint of the candidate crossing-signature pumping argument.
The geometric splice lemma is not formalised here. -/
theorem drift_le_candidate_signature_cutoff
    (m lowCuts : Nat)
    (hdensity : m <= 4 * lowCuts)
    (hdistinct : lowCuts <= 287934) :
    m <= 1151736 := by
  omega

/-- Sharper arithmetic endpoint obtained by projecting a decorated macro crossing
to the ordinary one-tape control state. At a crossing the direction is fixed by
its position in the alternating sequence. A rightward crossing lands on line `2`
or `4`, and a leftward crossing on line `0` or `2`, leaving two choices. Thus there
are at most `2 + 2^3 + 2^5 + 2^7 = 170` short control signatures. The simultaneous geometric
splice remains an explicit paper hypothesis, not a theorem formalised here. -/
theorem drift_le_candidate_control_signature_cutoff
    (m lowCuts : Nat)
    (hdensity : m <= 4 * lowCuts)
    (hdistinct : lowCuts <= 170) :
    m <= 680 := by
  omega

/-- Weighted refinement of the candidate control-signature cutoff.  Distinct
signatures of lengths `1,3,5,7` have capacities `2,8,32,128`; all remaining
signatures have length at least nine.  Combining those capacities with average
length at most seven gives `m <= 224`.  The geometric splice remains an explicit
hypothesis outside this arithmetic lemma. -/
theorem drift_le_candidate_weighted_control_cutoff
    (m period n1 n3 n5 n7 nLong : Nat)
    (hsplit : m = n1 + n3 + n5 + n7 + nLong)
    (h1 : n1 <= 2) (h3 : n3 <= 8) (h5 : n5 <= 32) (h7 : n7 <= 128)
    (hlength : n1 + 3*n3 + 5*n5 + 7*n7 + 9*nLong <= period)
    (hperiod : period <= 7*m) :
    m <= 224 := by
  omega

/-- The extremal-singleton refinement of the signature capacities.  In a signature
of length `2*n+1`, the exceptional rightward top label and exceptional leftward
bottom label can each occur at most once, giving `(n+2)*(n+1)` possibilities.
These are the four short-length values used in the weighted cutoff. -/
theorem shortExtremalControlSignature_counts :
    (2, 6, 12, 20) = ((0+2)*(0+1), (1+2)*(1+1),
                      (2+2)*(2+1), (3+2)*(3+1)) := by
  decide

/-- Strongest current arithmetic endpoint of the candidate pumping theorem.
Extremal singleton rigidity lowers the capacities at lengths `1,3,5,7` to
`2,6,12,20`; all remaining signatures have length at least nine.  With average
length at most seven this gives `m <= 70`.  The one-tape splice itself remains a
geometric paper lemma. -/
theorem drift_le_candidate_extremal_control_cutoff
    (m period n1 n3 n5 n7 nLong : Nat)
    (hsplit : m = n1 + n3 + n5 + n7 + nLong)
    (h1 : n1 <= 2) (h3 : n3 <= 6) (h5 : n5 <= 12) (h7 : n7 <= 20)
    (hlength : n1 + 3*n3 + 5*n5 + 7*n7 + 9*nLong <= period)
    (hperiod : period <= 7*m) :
    m <= 70 := by
  omega

end Langton.WidthFour
