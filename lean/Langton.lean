import Std
import Init.Omega

namespace Langton

/-! # Exact finite-support Langton ant kernel

This file deliberately uses only Lean's `Std` library.  A state consists of a
finite set of black lattice cells, an ant position, and one of four headings.
The transition convention is the usual one: on white, turn right and make the
cell black; on black, turn left and make the cell white; then move forward.
-/

/-- A point of the integer square lattice. -/
structure Pos where
  x : Int
  y : Int
deriving DecidableEq, Repr

/-- The four headings, in clockwise order. -/
inductive Dir where
  | north | east | south | west
deriving DecidableEq, Repr

/-- The two possible turn instructions. -/
inductive Turn where
  | right | left
deriving DecidableEq, Repr

def turnRight : Dir → Dir
  | .north => .east
  | .east  => .south
  | .south => .west
  | .west  => .north

def turnLeft : Dir → Dir
  | .north => .west
  | .west  => .south
  | .south => .east
  | .east  => .north

def applyTurn : Turn → Dir → Dir
  | .right => turnRight
  | .left  => turnLeft

def advance : Pos → Dir → Pos
  | p, .north => { p with y := p.y + 1 }
  | p, .east  => { p with x := p.x + 1 }
  | p, .south => { p with y := p.y - 1 }
  | p, .west  => { p with x := p.x - 1 }

/--
A Langton state with genuinely finite black support.  The list is interpreted
extensionally: duplicates, if supplied, do not change the represented set.
The transition removes every occurrence when whitening a cell, so the set
semantics is exact for every list representation.
-/
structure State where
  black : List Pos
  pos   : Pos
  dir   : Dir
deriving DecidableEq, Repr

/-- Remove every occurrence of a point from a finite support list. -/
def eraseAll (p : Pos) : List Pos → List Pos
  | []      => []
  | q :: qs => if q = p then eraseAll p qs else q :: eraseAll p qs

theorem mem_eraseAll_iff (p q : Pos) (xs : List Pos) :
    q ∈ eraseAll p xs ↔ q ∈ xs ∧ q ≠ p := by
  induction xs with
  | nil => simp [eraseAll]
  | cons a as ih =>
      by_cases hap : a = p
      · subst a
        rw [show eraseAll p (p :: as) = eraseAll p as by simp [eraseAll]]
        rw [ih]
        constructor
        · intro h
          exact ⟨by simp [h.1], h.2⟩
        · intro h
          have hm : q = p ∨ q ∈ as := by simpa using h.1
          exact ⟨hm.resolve_left h.2, h.2⟩
      · by_cases hqa : q = a
        · subst q
          simp [eraseAll, hap]
        · simp [eraseAll, hap, hqa, ih]

def turnAt (s : State) : Turn :=
  if s.pos ∈ s.black then .left else .right

def toggledBlack (s : State) : List Pos :=
  if s.pos ∈ s.black then eraseAll s.pos s.black else s.pos :: s.black

/-- One exact transition of the original two-colour Langton ant. -/
def step (s : State) : State :=
  let d := applyTurn (turnAt s) s.dir
  { black := toggledBlack s
    pos   := advance s.pos d
    dir   := d }

theorem step_dir (s : State) :
    (step s).dir = applyTurn (turnAt s) s.dir := by
  rfl

/-- The departed cell is toggled, with no assumptions on the rest of the grid. -/
theorem departed_cell_toggled (s : State) :
    (s.pos ∈ (step s).black) ↔ (s.pos ∉ s.black) := by
  by_cases h : s.pos ∈ s.black
  · simp [step, toggledBlack, h, mem_eraseAll_iff]
  · simp [step, toggledBlack, h]

/-- Every cell other than the departed cell keeps exactly the same colour. -/
theorem other_cell_unchanged (s : State) (q : Pos) (hne : q ≠ s.pos) :
    (q ∈ (step s).black) ↔ (q ∈ s.black) := by
  by_cases h : s.pos ∈ s.black
  · simp [step, toggledBlack, h, mem_eraseAll_iff, hne]
  · simp [step, toggledBlack, h, hne]

theorem turnAt_of_black (s : State) (h : s.pos ∈ s.black) : turnAt s = .left := by
  simp [turnAt, h]

theorem turnAt_of_white (s : State) (h : s.pos ∉ s.black) : turnAt s = .right := by
  simp [turnAt, h]

/-! ## Exact heading residue of a finite run

`Fin 4` is used as the cyclic group of quarter-turns.  Right contributes `1`
and left contributes `3 = -1 (mod 4)`.  Consequently a restored heading forces
the signed R-minus-L turn count to vanish modulo four.  This is the precise
finite-state statement used in the growth divisibility part of P16.
-/

def dirCode : Dir → Fin 4
  | .north => 0
  | .east  => 1
  | .south => 2
  | .west  => 3

def turnQuarter : Turn → Fin 4
  | .right => 1
  | .left  => 3

def followTurns : List Turn → Dir → Dir
  | [], d      => d
  | t :: ts, d => followTurns ts (applyTurn t d)

def turnResidue : List Turn → Fin 4
  | []      => 0
  | t :: ts => turnQuarter t + turnResidue ts

theorem dirCode_applyTurn (t : Turn) (d : Dir) :
    dirCode (applyTurn t d) = dirCode d + turnQuarter t := by
  cases t <;> cases d <;> rfl

theorem dirCode_followTurns (ts : List Turn) (d : Dir) :
    dirCode (followTurns ts d) = dirCode d + turnResidue ts := by
  induction ts generalizing d with
  | nil => exact (Lean.Grind.Fin.add_zero (dirCode d)).symm
  | cons t ts ih =>
      rw [show followTurns (t :: ts) d = followTurns ts (applyTurn t d) by rfl]
      rw [ih, dirCode_applyTurn]
      exact Lean.Grind.Fin.add_assoc (dirCode d) (turnQuarter t) (turnResidue ts)

/-- Any instruction word that restores its heading has signed turn residue 0. -/
theorem headingReset_turnResidue_zero (ts : List Turn) (d : Dir)
    (h : followTurns ts d = d) : turnResidue ts = 0 := by
  have hc := congrArg dirCode h
  rw [dirCode_followTurns] at hc
  have hv := congrArg Fin.val hc
  simp only [Fin.val_add] at hv
  apply Fin.ext
  change (turnResidue ts).val = 0
  omega

/-- Iterate the exact ant transition `n` times. -/
def run : Nat → State → State
  | 0, s     => s
  | n + 1, s => run n (step s)

/-- The chronological turn word read during an exact finite run. -/
def turnsOf : Nat → State → List Turn
  | 0, _     => []
  | n + 1, s => turnAt s :: turnsOf n (step s)

theorem run_dir_eq_followTurns (n : Nat) (s : State) :
    (run n s).dir = followTurns (turnsOf n s) s.dir := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih =>
      change (run n (step s)).dir =
        followTurns (turnsOf n (step s)) (applyTurn (turnAt s) s.dir)
      rw [ih]
      rfl

/--
Machine-checked P4 kernel: if an actual finite ant run restores its heading,
then its R-minus-L turn balance is `0 (mod 4)`.
-/
theorem headingReset_trace_modFour (n : Nat) (s : State)
    (h : (run n s).dir = s.dir) : turnResidue (turnsOf n s) = 0 := by
  apply headingReset_turnResidue_zero (turnsOf n s) s.dir
  rw [← run_dir_eq_followTurns]
  exact h

/-! ## A finite parity certificate for the P15 seam argument

In the paper proof, vertical edge multiplicities are even, and `G` denotes
their halves.  The parity in row `y` is the XOR of the two adjacent half-flow
parities.  Because the exterior half-flows are zero, XORing all row parities
telescopes to zero.  The following theorem proves exactly that finite algebraic
core, independently of any geometric encoding.
-/

def bxor : Bool → Bool → Bool
  | false, b => b
  | true, false => true
  | true, true  => false

def xorAll : List Bool → Bool
  | []      => false
  | b :: bs => bxor b (xorAll bs)

/-- Adjacent incidence parities along a finite vertical column. -/
def incidences : List Bool → List Bool
  | []               => []
  | [_]              => []
  | a :: b :: rest   => bxor a b :: incidences (b :: rest)

def lastFrom (a : Bool) : List Bool → Bool
  | []      => a
  | b :: bs => lastFrom b bs

theorem bxor_self (a : Bool) : bxor a a = false := by
  cases a <;> rfl

theorem bxor_cancel_middle (a b c : Bool) :
    bxor (bxor a b) (bxor b c) = bxor a c := by
  cases a <;> cases b <;> cases c <;> rfl

/-- XOR of adjacent incidences is exactly the XOR of the two endpoints. -/
theorem xorAll_incidences (a : Bool) (rest : List Bool) :
    xorAll (incidences (a :: rest)) = bxor a (lastFrom a rest) := by
  induction rest generalizing a with
  | nil => simp [incidences, xorAll, lastFrom, bxor_self]
  | cons b bs ih =>
      simp only [incidences, xorAll, lastFrom]
      rw [ih]
      exact bxor_cancel_middle a b (lastFrom b bs)

theorem lastFrom_append_singleton (a z : Bool) (xs : List Bool) :
    lastFrom a (xs ++ [z]) = z := by
  induction xs generalizing a with
  | nil => rfl
  | cons b bs ih =>
      simp only [List.cons_append, lastFrom]
      exact ih b

/--
The finite-support boundary cancellation used in equation (21.5): when both
exterior vertical half-edge parities vanish, the XOR of all row parities is
zero.  This is the mod-two statement that the seam crossing count is even.
-/
theorem evenWindingParityCore (interior : List Bool) :
    xorAll (incidences (false :: (interior ++ [false]))) = false := by
  rw [xorAll_incidences]
  rw [lastFrom_append_singleton]
  rfl

/-- No finite half-flow profile with zero exterior values can have odd seam parity. -/
theorem noOddWindingFromFiniteHalfFlow (interior : List Bool)
    (hOdd : xorAll (incidences (false :: (interior ++ [false]))) = true) : False := by
  rw [evenWindingParityCore] at hOdd
  contradiction

/-! ## A small executable transition certificate -/

def blankOrigin : State :=
  { black := []
    pos := { x := 0, y := 0 }
    dir := .north }

/-- The first four exact steps on a blank grid form the familiar unit square. -/
theorem blankOrigin_four_steps :
    run 4 blankOrigin =
      { black :=
          [{ x := 0, y := -1 }, { x := 1, y := -1 },
           { x := 1, y := 0 }, { x := 0, y := 0 }]
        pos := { x := 0, y := 0 }
        dir := .north } := by
  rfl

end Langton
