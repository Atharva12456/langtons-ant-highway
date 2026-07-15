import Langton.CollisionParity
import Langton.ResidueCharge

namespace Langton.DirectedPoseDiscrepancy

abbrev ZMod4 := Fin 4

/-!
## Generic additive-charge conservation on the exact ant kernel

The local-potential equations are precisely the conclusion supplied by the
complete additive-charge criterion.  Keeping them as a named structure makes
the formalization boundary explicit rather than assuming endpoint congruences.
-/

/-- Sum an arbitrary mod-four weight over a duplicate-free finite black list. -/
def weightedBlack (weight : Pos -> ZMod4) : List Pos -> ZMod4
  | [] => 0
  | p :: ps => weight p + weightedBlack weight ps

theorem weightedBlack_eraseAll_of_nodup_mem (weight : Pos -> ZMod4)
    (p : Pos) (xs : List Pos) (hnd : xs.Nodup) (hm : p ∈ xs) :
    weightedBlack weight (eraseAll p xs) = weightedBlack weight xs - weight p := by
  induction xs with
  | nil => simp at hm
  | cons a as ih =>
      have ha : a ∉ as := (List.nodup_cons.mp hnd).1
      have htail : as.Nodup := (List.nodup_cons.mp hnd).2
      by_cases hap : a = p
      · subst a
        have hpnot : p ∉ as := ha
        rw [show eraseAll p (p :: as) = eraseAll p as by simp [eraseAll]]
        rw [CollisionParity.eraseAll_eq_self_of_not_mem p as hpnot]
        simp only [weightedBlack]
        grind
      · have hpa : p ≠ a := Ne.symm hap
        have hmemtail : p ∈ as := by simpa [hpa] using hm
        simp only [eraseAll, hap, if_false, weightedBlack]
        rw [ih htail hmemtail]
        grind

/-- The exact right/left potential equations for an additive cell weight. -/
structure LocalPotential (weight : Pos -> ZMod4)
    (potential : Dir -> Pos -> ZMod4) : Prop where
  right : ∀ p q,
    potential (turnRight q) (advance p (turnRight q)) - potential q p = -weight p
  left : ∀ p q,
    potential (turnLeft q) (advance p (turnLeft q)) - potential q p = weight p

def additiveStateCharge (weight : Pos -> ZMod4)
    (potential : Dir -> Pos -> ZMod4) (s : State) : ZMod4 :=
  weightedBlack weight s.black + potential s.dir s.pos

/-- One-step conservation from the exact local potential equations. -/
theorem additiveStateCharge_step (weight : Pos -> ZMod4)
    (potential : Dir -> Pos -> ZMod4)
    (hlocal : LocalPotential weight potential) (s : State)
    (hnd : s.black.Nodup) :
    additiveStateCharge weight potential (step s) =
      additiveStateCharge weight potential s := by
  by_cases hm : s.pos ∈ s.black
  · have hw := weightedBlack_eraseAll_of_nodup_mem weight s.pos s.black hnd hm
    have hp := hlocal.left s.pos s.dir
    simp only [additiveStateCharge, step, toggledBlack, turnAt, hm, if_pos,
      applyTurn]
    rw [hw]
    grind
  · have hp := hlocal.right s.pos s.dir
    simp only [additiveStateCharge, step, toggledBlack, turnAt, hm, if_false,
      weightedBlack, applyTurn]
    grind

/-- Finite-run conservation; no recurrence or translation hypothesis. -/
theorem additiveStateCharge_run (weight : Pos -> ZMod4)
    (potential : Dir -> Pos -> ZMod4)
    (hlocal : LocalPotential weight potential) (n : Nat) (s : State)
    (hnd : s.black.Nodup) :
    additiveStateCharge weight potential (run n s) =
      additiveStateCharge weight potential s := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih =>
      calc
        additiveStateCharge weight potential (run (n + 1) s) =
            additiveStateCharge weight potential (run n (step s)) := rfl
        _ = additiveStateCharge weight potential (step s) :=
          ih (step s) (CollisionParity.step_black_nodup s hnd)
        _ = additiveStateCharge weight potential s :=
          additiveStateCharge_step weight potential hlocal s hnd

/-- Equal directed pose cancels the complete ant potential at the endpoints. -/
theorem weightedBlack_eq_of_directedPose_return (weight : Pos -> ZMod4)
    (potential : Dir -> Pos -> ZMod4)
    (hlocal : LocalPotential weight potential) (n : Nat) (s : State)
    (hnd : s.black.Nodup)
    (hpos : (run n s).pos = s.pos) (hdir : (run n s).dir = s.dir) :
    weightedBlack weight (run n s).black = weightedBlack weight s.black := by
  have hc := additiveStateCharge_run weight potential hlocal n s hnd
  unfold additiveStateCharge at hc
  rw [hpos, hdir] at hc
  grind

/-! ## Checker-signed exact-fiber weights -/

def checkerWeight (alpha : α -> ZMod4) (fiber : α) (odd : Bool) : ZMod4 :=
  ResidueCharge.signed odd (alpha fiber)

/--
The mixed four-corner sum vanishes for an arbitrary fiber function.  In
particular `alpha` may be the indicator of one exact integer row or column.
-/
theorem checkerWeight_fourCorner (alpha : α -> ZMod4) (a b : α) (odd : Bool) :
    checkerWeight alpha a odd + checkerWeight alpha b (!odd) +
      checkerWeight alpha a (!odd) + checkerWeight alpha b odd = 0 := by
  cases odd <;> simp [checkerWeight, ResidueCharge.signed] <;> grind

def exactIndicator (target value : Int) : ZMod4 :=
  if value = target then 1 else 0

theorem exactFiberChecker_fourCorner (target x : Int) (odd : Bool) :
    checkerWeight (exactIndicator target) x odd +
      checkerWeight (exactIndicator target) (x + 1) (!odd) +
      checkerWeight (exactIndicator target) x (!odd) +
      checkerWeight (exactIndicator target) (x + 1) odd = 0 := by
  exact checkerWeight_fourCorner (exactIndicator target) x (x + 1) odd

/-! ## Explicit exact-column potential -/

/-- Checkerboard unit `(-1)^n` in `Z/4Z`. -/
def checkerInt (n : Int) : ZMod4 :=
  if n % 2 = 0 then 1 else -1

def checkerPos (p : Pos) : ZMod4 := checkerInt (p.x + p.y)

theorem checkerInt_add_one (n : Int) : checkerInt (n + 1) = -checkerInt n := by
  by_cases h : n % 2 = 0
  · have hnext : (n + 1) % 2 = 1 := by omega
    simp [checkerInt, h, hnext]
  · have hn : n % 2 = 1 := by omega
    have hnext : (n + 1) % 2 = 0 := by omega
    simp [checkerInt, hn, hnext] <;> grind

theorem checkerInt_sub_one (n : Int) : checkerInt (n - 1) = -checkerInt n := by
  by_cases h : n % 2 = 0
  · have hprev : (n - 1) % 2 = 1 := by omega
    simp [checkerInt, h, hprev]
  · have hn : n % 2 = 1 := by omega
    have hprev : (n - 1) % 2 = 0 := by omega
    simp [checkerInt, hn, hprev] <;> grind

theorem checkerPos_advance (p : Pos) (q : Dir) :
    checkerPos (advance p q) = -checkerPos p := by
  cases q with
  | north =>
      change checkerInt (p.x + (p.y + 1)) = -checkerInt (p.x + p.y)
      rw [show p.x + (p.y + 1) = (p.x + p.y) + 1 by omega,
        checkerInt_add_one]
  | east =>
      change checkerInt ((p.x + 1) + p.y) = -checkerInt (p.x + p.y)
      rw [show (p.x + 1) + p.y = (p.x + p.y) + 1 by omega,
        checkerInt_add_one]
  | south =>
      change checkerInt (p.x + (p.y - 1)) = -checkerInt (p.x + p.y)
      rw [show p.x + (p.y - 1) = (p.x + p.y) - 1 by omega,
        checkerInt_sub_one]
  | west =>
      change checkerInt ((p.x - 1) + p.y) = -checkerInt (p.x + p.y)
      rw [show (p.x - 1) + p.y = (p.x + p.y) - 1 by omega,
        checkerInt_sub_one]

/-- The step profile `0,1,2` across the target exact column. -/
def columnStep (target x : Int) : ZMod4 :=
  if x < target then 0 else if x = target then 1 else 2

/-- `G(x+1)-G(x)=alpha(x)+alpha(x+1)` for an exact-column indicator. -/
theorem columnStep_add_one (target x : Int) :
    columnStep target (x + 1) =
      columnStep target x + exactIndicator target x + exactIndicator target (x + 1) := by
  by_cases hlt : x < target
  · by_cases heq : x + 1 = target
    · have hxne : x ≠ target := by omega
      simp [columnStep, exactIndicator, hlt, heq, hxne]
    · have hnextLt : x + 1 < target := by omega
      have hxne : x ≠ target := by omega
      simp [columnStep, exactIndicator, hlt, heq, hnextLt, hxne]
  · by_cases heq : x = target
    · subst x
      have hnextNotLt : ¬target + 1 < target := by omega
      have hnextNe : target + 1 ≠ target := by omega
      simp [columnStep, exactIndicator, hnextNotLt, hnextNe]
    · have hnextNotLt : ¬x + 1 < target := by omega
      have hnextNe : x + 1 ≠ target := by omega
      simp [columnStep, exactIndicator, hlt, heq, hnextNotLt, hnextNe]

theorem columnStep_eq_previous (target x : Int) :
    columnStep target x =
      columnStep target (x - 1) + exactIndicator target (x - 1) +
        exactIndicator target x := by
  have h := columnStep_add_one target (x - 1)
  simpa [show x - 1 + 1 = x by omega] using h

def exactColumnWeight (target : Int) (p : Pos) : ZMod4 :=
  checkerPos p * exactIndicator target p.x

/--
An explicit potential for the exact-column checker weight.  With
`c=(-1)^(x+y)`, `a=1[x=target]`, and `G=columnStep target x`, the four rows are
`c*(-G)`, `c*(G-a)`, `c*(-G+2a)`, and `c*(G+a)`.
-/
def exactColumnPotential (target : Int) : Dir -> Pos -> ZMod4
  | .north, p => checkerPos p * (-columnStep target p.x)
  | .east, p => checkerPos p *
      (columnStep target p.x - exactIndicator target p.x)
  | .south, p => checkerPos p *
      (-columnStep target p.x + 2 * exactIndicator target p.x)
  | .west, p => checkerPos p *
      (columnStep target p.x + exactIndicator target p.x)

/-- The displayed exact-column potential satisfies all eight R/L equations. -/
theorem exactColumn_localPotential (target : Int) :
    LocalPotential (exactColumnWeight target) (exactColumnPotential target) := by
  constructor
  · intro p q
    cases q with
    | north =>
        change
          checkerPos (advance p .east) *
                (columnStep target (p.x + 1) - exactIndicator target (p.x + 1)) -
              checkerPos p * (-columnStep target p.x) =
            -(checkerPos p * exactIndicator target p.x)
        rw [checkerPos_advance p .east, columnStep_add_one]
        grind
    | east =>
        change
          checkerPos (advance p .south) *
                (-columnStep target p.x + 2 * exactIndicator target p.x) -
              checkerPos p *
                (columnStep target p.x - exactIndicator target p.x) =
            -(checkerPos p * exactIndicator target p.x)
        rw [checkerPos_advance p .south]
        grind
    | south =>
        have hg := columnStep_eq_previous target p.x
        change
          checkerPos (advance p .west) *
                (columnStep target (p.x - 1) + exactIndicator target (p.x - 1)) -
              checkerPos p *
                (-columnStep target p.x + 2 * exactIndicator target p.x) =
            -(checkerPos p * exactIndicator target p.x)
        rw [checkerPos_advance p .west]
        grind
    | west =>
        change
          checkerPos (advance p .north) * (-columnStep target p.x) -
              checkerPos p *
                (columnStep target p.x + exactIndicator target p.x) =
            -(checkerPos p * exactIndicator target p.x)
        rw [checkerPos_advance p .north]
        grind
  · intro p q
    cases q with
    | north =>
        have hg := columnStep_eq_previous target p.x
        change
          checkerPos (advance p .west) *
                (columnStep target (p.x - 1) + exactIndicator target (p.x - 1)) -
              checkerPos p * (-columnStep target p.x) =
            checkerPos p * exactIndicator target p.x
        rw [checkerPos_advance p .west]
        grind
    | east =>
        change
          checkerPos (advance p .north) * (-columnStep target p.x) -
              checkerPos p *
                (columnStep target p.x - exactIndicator target p.x) =
            checkerPos p * exactIndicator target p.x
        rw [checkerPos_advance p .north]
        grind
    | south =>
        have hg := columnStep_add_one target p.x
        change
          checkerPos (advance p .east) *
                (columnStep target (p.x + 1) - exactIndicator target (p.x + 1)) -
              checkerPos p *
                (-columnStep target p.x + 2 * exactIndicator target p.x) =
            checkerPos p * exactIndicator target p.x
        rw [checkerPos_advance p .east, columnStep_add_one]
        grind
    | west =>
        change
          checkerPos (advance p .south) *
                (-columnStep target p.x + 2 * exactIndicator target p.x) -
              checkerPos p *
                (columnStep target p.x + exactIndicator target p.x) =
            checkerPos p * exactIndicator target p.x
        rw [checkerPos_advance p .south]
        grind

/-- Unconditional exact-kernel conservation for one checker-signed column. -/
theorem exactColumnWeight_directedPose_return (target : Int) (n : Nat) (s : State)
    (hnd : s.black.Nodup)
    (hpos : (run n s).pos = s.pos) (hdir : (run n s).dir = s.dir) :
    weightedBlack (exactColumnWeight target) (run n s).black =
      weightedBlack (exactColumnWeight target) s.black := by
  exact weightedBlack_eq_of_directedPose_return
    (exactColumnWeight target) (exactColumnPotential target)
    (exactColumn_localPotential target) n s hnd hpos hdir

/-! ## Explicit exact-row potential (the quarter-turned column construction) -/

def exactRowWeight (target : Int) (p : Pos) : ZMod4 :=
  checkerPos p * exactIndicator target p.y

def exactRowPotential (target : Int) : Dir -> Pos -> ZMod4
  | .north, p => checkerPos p *
      (columnStep target p.y - exactIndicator target p.y)
  | .east, p => checkerPos p *
      (-columnStep target p.y + 2 * exactIndicator target p.y)
  | .south, p => checkerPos p *
      (columnStep target p.y + exactIndicator target p.y)
  | .west, p => checkerPos p * (-columnStep target p.y)

theorem exactRow_localPotential (target : Int) :
    LocalPotential (exactRowWeight target) (exactRowPotential target) := by
  constructor
  · intro p q
    cases q with
    | north =>
        change
          checkerPos (advance p .east) *
                (-columnStep target p.y + 2 * exactIndicator target p.y) -
              checkerPos p *
                (columnStep target p.y - exactIndicator target p.y) =
            -(checkerPos p * exactIndicator target p.y)
        rw [checkerPos_advance p .east]
        grind
    | east =>
        have hg := columnStep_eq_previous target p.y
        change
          checkerPos (advance p .south) *
                (columnStep target (p.y - 1) + exactIndicator target (p.y - 1)) -
              checkerPos p *
                (-columnStep target p.y + 2 * exactIndicator target p.y) =
            -(checkerPos p * exactIndicator target p.y)
        rw [checkerPos_advance p .south]
        grind
    | south =>
        change
          checkerPos (advance p .west) * (-columnStep target p.y) -
              checkerPos p *
                (columnStep target p.y + exactIndicator target p.y) =
            -(checkerPos p * exactIndicator target p.y)
        rw [checkerPos_advance p .west]
        grind
    | west =>
        change
          checkerPos (advance p .north) *
                (columnStep target (p.y + 1) - exactIndicator target (p.y + 1)) -
              checkerPos p * (-columnStep target p.y) =
            -(checkerPos p * exactIndicator target p.y)
        rw [checkerPos_advance p .north, columnStep_add_one]
        grind
  · intro p q
    cases q with
    | north =>
        change
          checkerPos (advance p .west) * (-columnStep target p.y) -
              checkerPos p *
                (columnStep target p.y - exactIndicator target p.y) =
            checkerPos p * exactIndicator target p.y
        rw [checkerPos_advance p .west]
        grind
    | east =>
        change
          checkerPos (advance p .north) *
                (columnStep target (p.y + 1) - exactIndicator target (p.y + 1)) -
              checkerPos p *
                (-columnStep target p.y + 2 * exactIndicator target p.y) =
            checkerPos p * exactIndicator target p.y
        rw [checkerPos_advance p .north, columnStep_add_one]
        grind
    | south =>
        change
          checkerPos (advance p .east) *
                (-columnStep target p.y + 2 * exactIndicator target p.y) -
              checkerPos p *
                (columnStep target p.y + exactIndicator target p.y) =
            checkerPos p * exactIndicator target p.y
        rw [checkerPos_advance p .east]
        grind
    | west =>
        have hg := columnStep_eq_previous target p.y
        change
          checkerPos (advance p .south) *
                (columnStep target (p.y - 1) + exactIndicator target (p.y - 1)) -
              checkerPos p * (-columnStep target p.y) =
            checkerPos p * exactIndicator target p.y
        rw [checkerPos_advance p .south]
        grind

theorem exactRowWeight_directedPose_return (target : Int) (n : Nat) (s : State)
    (hnd : s.black.Nodup)
    (hpos : (run n s).pos = s.pos) (hdir : (run n s).dir = s.dir) :
    weightedBlack (exactRowWeight target) (run n s).black =
      weightedBlack (exactRowWeight target) s.black := by
  exact weightedBlack_eq_of_directedPose_return
    (exactRowWeight target) (exactRowPotential target)
    (exactRow_localPotential target) n s hnd hpos hdir


/-! ## Four-corner endpoint-sign algebra -/

/-- XOR on sign bits: `false` denotes `+1`, `true` denotes `-1`. -/
def xorSign : Bool -> Bool -> Bool
  | false, b => b
  | true, b => !b

/-- Sign of `endpoint sign * checkerboard sign`. -/
def signedCheckerTerm (endpointNegative checkerOdd : Bool) : ZMod4 :=
  ResidueCharge.paritySign (xorSign endpointNegative checkerOdd)

/-- Two signed units sum to zero modulo four exactly when their signs differ. -/
theorem twoSignedCheckerTerms_zero_iff (aOdd bOdd : Bool) :
    ResidueCharge.paritySign aOdd + ResidueCharge.paritySign bOdd = 0 ↔
      bOdd = !aOdd := by
  cases aOdd <;> cases bOdd <;>
    simp [ResidueCharge.paritySign, ResidueCharge.signed] <;> grind

/--
Machine-checked form of formula (5.4).  `baseOdd` is the checker parity of the
actual southwest corner; it is deliberately arbitrary, so translating the
rectangle does not silently assume an even southwest corner.
-/
theorem rectangleEndpointSigns
    (baseOdd rOdd sOdd : Bool)
    (southwest southeast northwest northeast : Bool)
    (southRow :
      signedCheckerTerm southwest baseOdd +
        signedCheckerTerm southeast (xorSign baseOdd rOdd) = 0)
    (westColumn :
      signedCheckerTerm southwest baseOdd +
        signedCheckerTerm northwest (xorSign baseOdd sOdd) = 0)
    (northRow :
      signedCheckerTerm northwest (xorSign baseOdd sOdd) +
        signedCheckerTerm northeast (xorSign baseOdd (xorSign rOdd sOdd)) = 0)
    (eastColumn :
      signedCheckerTerm southeast (xorSign baseOdd rOdd) +
        signedCheckerTerm northeast (xorSign baseOdd (xorSign rOdd sOdd)) = 0) :
    southeast = xorSign southwest (!rOdd) ∧
      northwest = xorSign southwest (!sOdd) ∧
      northeast = xorSign southwest (xorSign rOdd sOdd) := by
  cases baseOdd <;> cases rOdd <;> cases sOdd <;>
    cases southwest <;> cases southeast <;> cases northwest <;> cases northeast <;>
    simp [signedCheckerTerm, xorSign, ResidueCharge.paritySign,
      ResidueCharge.signed] at * <;> grind

end Langton.DirectedPoseDiscrepancy
