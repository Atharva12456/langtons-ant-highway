import Langton.WidthFour

namespace Langton.WidthFourCrossing

/-!
# Acyclicity certificate for the width-four blank-column graph

The Python local simulator supplies the twelve edges below.  This file deliberately
checks only the finite graph consequence: every edge lowers an explicit rank, so no
four-edge path exists.  Exhaustiveness of the local simulator is not formalised here.
-/

abbrev Signature := List Nat
abbrev Edge := Prod Signature Signature

def blankEdges : List Edge :=
  [([2,0,2], [4]),
   ([4,2,2,0,2,2,2], [2]),
   ([4,2,2,0,2,2,2], [2,0,2]),
   ([4,2,2,0,2,2,2], [2,0,2,2,2]),
   ([4,2,2,0,2,2,2], [2,0,2,2,2,2,4]),
   ([2,0,4,2,2,2,2], [2]),
   ([2,0,4,2,2,2,2], [2,0,2]),
   ([2,0,4,2,2,2,2], [2,0,2,2,2]),
   ([2,0,4,2,2,2,2], [2,0,2,2,2,2,4]),
   ([2,0,2,2,4,2,2,2,2], [4,2,2]),
   ([2,0,2,2,4,2,2,2,2], [4,2,2,0,2]),
   ([2,0,2,2,4,2,2,2,2], [4,2,2,0,2,2,2])]

def BlankEdge (a b : Signature) : Prop := (a, b) ∈ blankEdges

theorem blankEdge_cases (a b : Signature) :
    BlankEdge a b ↔
      (a = [2,0,2] /\ b = [4]) \/
      (a = [4,2,2,0,2,2,2] /\ b = [2]) \/
      (a = [4,2,2,0,2,2,2] /\ b = [2,0,2]) \/
      (a = [4,2,2,0,2,2,2] /\ b = [2,0,2,2,2]) \/
      (a = [4,2,2,0,2,2,2] /\ b = [2,0,2,2,2,2,4]) \/
      (a = [2,0,4,2,2,2,2] /\ b = [2]) \/
      (a = [2,0,4,2,2,2,2] /\ b = [2,0,2]) \/
      (a = [2,0,4,2,2,2,2] /\ b = [2,0,2,2,2]) \/
      (a = [2,0,4,2,2,2,2] /\ b = [2,0,2,2,2,2,4]) \/
      (a = [2,0,2,2,4,2,2,2,2] /\ b = [4,2,2]) \/
      (a = [2,0,2,2,4,2,2,2,2] /\ b = [4,2,2,0,2]) \/
      (a = [2,0,2,2,4,2,2,2,2] /\ b = [4,2,2,0,2,2,2]) := by
  simp [BlankEdge, blankEdges]

def rank (signature : Signature) : Nat :=
  if signature = [2,0,2,2,4,2,2,2,2] then 3
  else if signature = [4,2,2,0,2,2,2] then 2
  else if signature = [2,0,4,2,2,2,2] then 2
  else if signature = [2,0,2] then 1
  else 0

theorem blankEdge_rank_decreases
    (a b : Signature) (hEdge : BlankEdge a b) :
    rank b < rank a := by
  rw [blankEdge_cases] at hEdge
  rcases hEdge with h | h | h | h | h | h | h | h | h | h | h | h <;>
    cases h with
    | intro ha hb =>
      subst a
      subst b
      decide

theorem rank_le_three (signature : Signature) : rank signature <= 3 := by
  unfold rank
  split
  · omega
  · split
    · omega
    · split
      · omega
      · split <;> omega

/-- The certified graph has longest directed path at most three. -/
theorem no_four_blankEdge_chain
    (a b c d e : Signature)
    (hab : BlankEdge a b) (hbc : BlankEdge b c)
    (hcd : BlankEdge c d) (hde : BlankEdge d e) : False := by
  have h1 : rank b < rank a := blankEdge_rank_decreases a b hab
  have h2 : rank c < rank b := blankEdge_rank_decreases b c hbc
  have h3 : rank d < rank c := blankEdge_rank_decreases c d hcd
  have h4 : rank e < rank d := blankEdge_rank_decreases d e hde
  have ha := rank_le_three a
  omega

end Langton.WidthFourCrossing
