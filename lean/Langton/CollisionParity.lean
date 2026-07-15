import Langton

namespace Langton.CollisionParity

/-!
# Endpoint parity carried through an arbitrary collision chain

Every departed cell is naturally an edge between its column and its row.
Over `F_2`, the boundary of the cells toggled along any finite Langton run is
supported only at the two endpoint ant states.  The endpoint associated to a
vertical heading is the current column; the endpoint associated to a
horizontal heading is the current row.

This file formalizes the kinematic and telescoping kernel.  Interpreting the
visit parity as the symmetric difference of the initial and final black sets
uses only the already proved fact that exactly the departed cell is toggled at
each step.
-/

abbrev F2 := Fin 2

@[simp] theorem f2_add_self (a : F2) : a + a = 0 := by
  apply Fin.ext
  simp only [Fin.val_add, Fin.val_zero]
  omega

/-- Vertices of the row-column incidence graph of lattice cells. -/
inductive CoordVertex where
  | column : Int -> CoordVertex
  | row : Int -> CoordVertex
deriving DecidableEq, Repr

/-- The unique coordinate vertex selected by a directed ant state. -/
def endpointIndicator (s : State) : CoordVertex -> F2
  | .column x =>
      match s.dir with
      | .north | .south => if x = s.pos.x then 1 else 0
      | .east | .west => 0
  | .row y =>
      match s.dir with
      | .east | .west => if y = s.pos.y then 1 else 0
      | .north | .south => 0

/-- A cell is the incidence edge joining its column to its row. -/
def cellBoundary (p : Pos) : CoordVertex -> F2
  | .column x => if x = p.x then 1 else 0
  | .row y => if y = p.y then 1 else 0

/-- Row/column parity profile of a duplicate-free finite black list. -/
def blackBoundary : List Pos -> CoordVertex -> F2
  | [], _ => 0
  | p :: ps, v => cellBoundary p v + blackBoundary ps v

theorem eraseAll_eq_self_of_not_mem (p : Pos) (xs : List Pos)
    (h : p ∉ xs) : eraseAll p xs = xs := by
  induction xs with
  | nil => rfl
  | cons a as ih =>
      have hap : a ≠ p := by
        intro heq
        apply h
        simp [heq]
      have htail : p ∉ as := by
        intro hm
        exact h (by simp [hm])
      simp [eraseAll, hap, ih htail]

theorem eraseAll_nodup (p : Pos) (xs : List Pos) (h : xs.Nodup) :
    (eraseAll p xs).Nodup := by
  induction xs with
  | nil => simp [eraseAll]
  | cons a as ih =>
      have ha : a ∉ as := (List.nodup_cons.mp h).1
      have htail : as.Nodup := (List.nodup_cons.mp h).2
      by_cases hap : a = p
      · subst a
        simpa [eraseAll] using ih htail
      · simp only [eraseAll, hap, if_false]
        apply List.nodup_cons.mpr
        constructor
        · intro hm
          have hold : a ∈ as := (mem_eraseAll_iff p a as).mp hm |>.1
          exact ha hold
        · exact ih htail

/-- Removing the unique occurrence of `p` flips every incidence parity of it. -/
theorem blackBoundary_eraseAll_of_nodup_mem (p : Pos) (xs : List Pos)
    (v : CoordVertex) (hnd : xs.Nodup) (hm : p ∈ xs) :
    blackBoundary (eraseAll p xs) v =
      blackBoundary xs v + cellBoundary p v := by
  induction xs with
  | nil => simp at hm
  | cons a as ih =>
      have ha : a ∉ as := (List.nodup_cons.mp hnd).1
      have htail : as.Nodup := (List.nodup_cons.mp hnd).2
      by_cases hap : a = p
      · subst a
        have hpnot : p ∉ as := ha
        rw [show eraseAll p (p :: as) = eraseAll p as by simp [eraseAll]]
        rw [eraseAll_eq_self_of_not_mem p as hpnot]
        simp only [blackBoundary]
        grind
      · have hmemtail : p ∈ as := by
          have hpa : p ≠ a := Ne.symm hap
          simpa [hpa] using hm
        simp only [eraseAll, hap, if_false, blackBoundary]
        rw [ih htail hmemtail]
        grind

/-- Duplicate-free support is preserved by a Langton toggle. -/
theorem toggledBlack_nodup (s : State) (hnd : s.black.Nodup) :
    (toggledBlack s).Nodup := by
  by_cases hm : s.pos ∈ s.black
  · simpa [toggledBlack, hm] using eraseAll_nodup s.pos s.black hnd
  · simp [toggledBlack, hm, hnd]

/-- The black row-column profile flips precisely at the departed cell. -/
theorem blackBoundary_step (s : State) (v : CoordVertex)
    (hnd : s.black.Nodup) :
    blackBoundary (step s).black v =
      blackBoundary s.black v + cellBoundary s.pos v := by
  by_cases hm : s.pos ∈ s.black
  · simpa [step, toggledBlack, hm] using
      blackBoundary_eraseAll_of_nodup_mem s.pos s.black v hnd hm
  · simp only [step, toggledBlack, hm, if_false, blackBoundary]
    grind

theorem step_black_nodup (s : State) (hnd : s.black.Nodup) :
    (step s).black.Nodup := by
  exact toggledBlack_nodup s hnd

/--
One exact Langton step moves the endpoint token across the incidence edge
corresponding to the departed (and toggled) cell.  This is independent of the
cell color: either turn changes vertical heading to horizontal or conversely,
and the move preserves the coordinate selected by the new heading.
-/
theorem cellBoundary_eq_endpoint_add_step (s : State) (v : CoordVertex) :
    cellBoundary s.pos v = endpointIndicator s v + endpointIndicator (step s) v := by
  rcases s with ⟨black, pos, dir⟩
  by_cases h : pos ∈ black
  <;> cases dir
  <;> cases v
  <;> simp [cellBoundary, endpointIndicator, step, turnAt, h, applyTurn,
    turnLeft, turnRight, advance]

/-- The two Laurent parity charges, evaluated at one coordinate vertex. -/
def stateCharge (s : State) (v : CoordVertex) : F2 :=
  blackBoundary s.black v + endpointIndicator s v

/-- Exact one-step conservation of the row/column parity charge. -/
theorem stateCharge_step (s : State) (v : CoordVertex)
    (hnd : s.black.Nodup) : stateCharge (step s) v = stateCharge s v := by
  unfold stateCharge
  rw [blackBoundary_step s v hnd]
  have hk := cellBoundary_eq_endpoint_add_step s v
  grind

theorem run_black_nodup (n : Nat) (s : State) (hnd : s.black.Nodup) :
    (run n s).black.Nodup := by
  induction n generalizing s with
  | zero => exact hnd
  | succ n ih =>
      exact ih (step s) (step_black_nodup s hnd)

/-- Exact finite-run conservation, with no periodicity assumption. -/
theorem stateCharge_run (n : Nat) (s : State) (v : CoordVertex)
    (hnd : s.black.Nodup) : stateCharge (run n s) v = stateCharge s v := by
  induction n generalizing s with
  | zero => rfl
  | succ n ih =>
      calc
        stateCharge (run (n + 1) s) v = stateCharge (run n (step s)) v := rfl
        _ = stateCharge (step s) v := ih (step s) (step_black_nodup s hnd)
        _ = stateCharge s v := stateCharge_step s v hnd

/--
The parity profile of the black symmetric difference has boundary equal to
the two endpoint tokens.  Addition is symmetric difference in `F_2`.
-/
theorem blackDifferenceBoundary_eq_endpoints (n : Nat) (s : State)
    (v : CoordVertex) (hnd : s.black.Nodup) :
    blackBoundary s.black v + blackBoundary (run n s).black v =
      endpointIndicator s v + endpointIndicator (run n s) v := by
  have hc := stateCharge_run n s v hnd
  unfold stateCharge at hc
  grind

/-- Sum the row-column boundaries of a finite list of departed cells. -/
def visitBoundary : List Pos -> CoordVertex -> F2
  | [], _ => 0
  | p :: ps, v => cellBoundary p v + visitBoundary ps v

/-- Chronological departed positions of an exact finite run. -/
def departedPositions : Nat -> State -> List Pos
  | 0, _ => []
  | n + 1, s => s.pos :: departedPositions n (step s)

/--
The complete toggled-cell boundary of an exact run is the sum of its two
endpoint tokens.  Every intermediate token occurs twice and cancels in `F_2`.
-/
theorem departedBoundary_eq_endpoints (n : Nat) (s : State) (v : CoordVertex) :
    visitBoundary (departedPositions n s) v =
      endpointIndicator s v + endpointIndicator (run n s) v := by
  induction n generalizing s with
  | zero =>
      simp [departedPositions, visitBoundary, run]
  | succ n ih =>
      simp only [departedPositions, visitBoundary]
      rw [cellBoundary_eq_endpoint_add_step, ih]
      change endpointIndicator s v + endpointIndicator (step s) v +
          (endpointIndicator (step s) v + endpointIndicator (run n (step s)) v) =
        endpointIndicator s v + endpointIndicator (run n (step s)) v
      grind

/-! ## Collision-checkpoint telescoping -/

/-- Endpoint defect assigned to an interval between two checkpoints. -/
def intervalDefect (s t : State) (v : CoordVertex) : F2 :=
  endpointIndicator s v + endpointIndicator t v

/-- XOR-sum of interval defects along consecutive checkpoints. -/
def chainDefect : List State -> CoordVertex -> F2
  | [], _ => 0
  | [_], _ => 0
  | s :: t :: rest, v => intervalDefect s t v + chainDefect (t :: rest) v

/-- Final element of a nonempty list, written without a partial operation. -/
def lastFrom (a : α) : List α -> α
  | [] => a
  | b :: bs => lastFrom b bs

theorem lastFrom_append_singleton (a z : α) (xs : List α) :
    lastFrom a (xs ++ [z]) = z := by
  induction xs generalizing a with
  | nil => rfl
  | cons b bs ih =>
      simp only [List.cons_append, lastFrom]
      exact ih b

/-- Total endpoint defect of a nonempty checkpoint chain. -/
def endpointDefectFrom (s : State) : List State -> CoordVertex -> F2
  | [], v => intervalDefect s s v
  | t :: rest, v => intervalDefect s (lastFrom t rest) v

/--
All internal ant-state corrections cancel across an arbitrary chain of
collision intervals.  Only the first and final directed states remain.
-/
theorem chainDefect_eq_endpointDefect (s : State) (rest : List State)
    (v : CoordVertex) :
    chainDefect (s :: rest) v = endpointDefectFrom s rest v := by
  induction rest generalizing s with
  | nil =>
      simp [chainDefect, endpointDefectFrom, intervalDefect]
  | cons t ts ih =>
      cases ts with
      | nil =>
          simp [chainDefect, endpointDefectFrom, intervalDefect,
            lastFrom]
      | cons u us =>
          change intervalDefect s t v + chainDefect (t :: u :: us) v =
            intervalDefect s (lastFrom u us) v
          rw [ih t]
          simp only [endpointDefectFrom, intervalDefect]
          grind

/-- A chain returning to the same directed ant state has zero boundary. -/
theorem chainDefect_closed (s : State) (middle : List State)
    (v : CoordVertex) :
    chainDefect (s :: (middle ++ [s])) v = 0 := by
  rw [chainDefect_eq_endpointDefect]
  cases middle with
  | nil => simp [endpointDefectFrom, intervalDefect, lastFrom]
  | cons t ts =>
      simp only [List.cons_append, endpointDefectFrom]
      rw [lastFrom_append_singleton]
      simp [intervalDefect]

end Langton.CollisionParity
