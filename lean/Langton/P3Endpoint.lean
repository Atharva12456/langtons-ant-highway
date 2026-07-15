import Langton.TraceGeometry

namespace Langton.TraceGeometry

/-! ## Stabilized P3 words -/

def oppositeTurn : Turn → Turn
  | .right => .left
  | .left => .right

@[simp] theorem oppositeTurn_oppositeTurn (turn : Turn) :
    oppositeTurn (oppositeTurn turn) = turn := by
  cases turn <;> rfl

@[simp] theorem turnInt_oppositeTurn (turn : Turn) :
    turnInt (oppositeTurn turn) = -turnInt turn := by
  cases turn <;> rfl

/-- The unique strictly alternating word on the supplied level sequence. -/
def alternatingEntriesFrom : Turn → List Int → List (Int × Turn)
  | _, [] => []
  | expected, level :: levels =>
      (level, expected) :: alternatingEntriesFrom (oppositeTurn expected) levels

def entryBalance (entries : List (Int × Turn)) : Int :=
  (entries.map fun entry => turnInt entry.2).sum

/-- Sign of the final letter; on the empty word this is the sign before it. -/
def terminalSign : Turn → List Int → Int
  | expected, [] => -turnInt expected
  | expected, _ :: levels => terminalSign (oppositeTurn expected) levels

theorem map_fst_alternatingEntriesFrom (expected : Turn) (levels : List Int) :
    (alternatingEntriesFrom expected levels).map Prod.fst = levels := by
  induction levels generalizing expected with
  | nil => rfl
  | cons level levels ih =>
      simp [alternatingEntriesFrom, ih]

theorem alternatingBalance_zero_or_terminal (expected : Turn) :
    ∀ levels : List Int,
      entryBalance (alternatingEntriesFrom expected levels) = 0 ∨
        entryBalance (alternatingEntriesFrom expected levels) = terminalSign expected levels
  | [] => Or.inl rfl
  | [level] => Or.inr (by cases expected <;> rfl)
  | level₁ :: level₂ :: levels => by
      have ih := alternatingBalance_zero_or_terminal expected levels
      rcases ih with hzero | hterminal
      · left
        cases expected <;>
          simp [alternatingEntriesFrom, entryBalance, oppositeTurn, turnInt] at hzero ⊢ <;>
          omega
      · right
        cases expected <;>
          simp [alternatingEntriesFrom, entryBalance, terminalSign,
            oppositeTurn, turnInt] at hterminal ⊢ <;>
          omega

theorem alternatingRight_classification : ∀ levels : List Int,
    levels = [] ∨
      (entryBalance (alternatingEntriesFrom .right levels) = 0 ∧
        terminalSign .right levels = -1) ∨
      (entryBalance (alternatingEntriesFrom .right levels) = 1 ∧
        terminalSign .right levels = 1)
  | [] => Or.inl rfl
  | [level] => Or.inr (Or.inr (by
      simp [alternatingEntriesFrom, entryBalance, terminalSign, oppositeTurn, turnInt]))
  | level₁ :: level₂ :: levels => by
      rcases alternatingRight_classification levels with hnil | heven | hodd
      · subst levels
        exact Or.inr (Or.inl (by
          simp [alternatingEntriesFrom, entryBalance, terminalSign,
            oppositeTurn, turnInt]))
      · apply Or.inr
        apply Or.inl
        constructor
        · have hbalance := heven.1
          unfold entryBalance at hbalance ⊢
          simp only [alternatingEntriesFrom, List.map_cons, List.sum_cons,
            turnInt, oppositeTurn] at hbalance ⊢
          omega
        · simpa [terminalSign, oppositeTurn] using heven.2
      · apply Or.inr
        apply Or.inr
        constructor
        · have hbalance := hodd.1
          unfold entryBalance at hbalance ⊢
          simp only [alternatingEntriesFrom, List.map_cons, List.sum_cons,
            turnInt, oppositeTurn] at hbalance ⊢
          omega
        · simpa [terminalSign, oppositeTurn] using hodd.2

theorem alternatingSuffix_balance (expected : Turn) (levels : List Int)
    (suffix : List (Int × Turn))
    (hsuffix : suffix <:+ alternatingEntriesFrom expected levels) :
    entryBalance suffix = 0 ∨ entryBalance suffix = terminalSign expected levels := by
  rcases hsuffix with ⟨pre, hpre⟩
  induction pre generalizing expected levels with
  | nil =>
      simp only [List.nil_append] at hpre
      subst suffix
      exact alternatingBalance_zero_or_terminal expected levels
  | cons entry pre ih =>
      cases levels with
      | nil => simp [alternatingEntriesFrom] at hpre
      | cons level levels =>
          simp only [List.cons_append, alternatingEntriesFrom] at hpre
          have htail : pre ++ suffix = alternatingEntriesFrom (oppositeTurn expected) levels := by
            exact (List.cons.inj hpre).2
          have hresult := ih (oppositeTurn expected) levels htail
          simpa [terminalSign] using hresult

/--
An explicit stabilized P3 orbit word.  Equal-level entries are understood to
be in phase order; that tie-break is irrelevant to the aggregate proof below.
The turns themselves are generated as `R,L,R,L,...`, so alternation and the
initial `R` are data-free consequences rather than certificate fields.
-/
structure StabilizedP3Word where
  levels : List Int
  nonempty : levels ≠ []
  levels_nonincreasing : levels.Pairwise (fun high low => low ≤ high)
  origin : Int
  width : Nat
  levels_covered : ∀ level ∈ levels,
    origin ≤ level ∧ level < origin + (width : Int)

def StabilizedP3Word.entries (word : StabilizedP3Word) : List (Int × Turn) :=
  alternatingEntriesFrom .right word.levels

def StabilizedP3Word.balance (word : StabilizedP3Word) : Int :=
  entryBalance word.entries

def StabilizedP3Word.growth (word : StabilizedP3Word) : Bool :=
  if word.balance = 1 then true else false

def StabilizedP3Word.delta (word : StabilizedP3Word) : List Int :=
  aggregateToggles word.origin word.width word.entries

theorem StabilizedP3Word.entries_levels (word : StabilizedP3Word) :
    word.entries.map Prod.fst = word.levels := by
  exact map_fst_alternatingEntriesFrom .right word.levels

theorem StabilizedP3Word.entries_covered (word : StabilizedP3Word) :
    EntriesCovered word.origin word.width word.entries := by
  intro entry hentry
  apply word.levels_covered entry.1
  have hmapped : entry.1 ∈ word.entries.map Prod.fst :=
    List.mem_map_of_mem hentry
  simpa [word.entries_levels] using hmapped

theorem alternatingEntries_pairwise_levels (expected : Turn) (levels : List Int)
    (hsorted : levels.Pairwise (fun high low => low ≤ high)) :
    (alternatingEntriesFrom expected levels).Pairwise
      (fun high low => low.1 ≤ high.1) := by
  induction levels generalizing expected with
  | nil => simp [alternatingEntriesFrom]
  | cons level levels ih =>
      simp only [List.pairwise_cons] at hsorted
      simp only [alternatingEntriesFrom, List.pairwise_cons]
      constructor
      · intro entry hentry
        apply hsorted.1 entry.1
        have hmapped : entry.1 ∈
            (alternatingEntriesFrom (oppositeTurn expected) levels).map Prod.fst :=
          List.mem_map_of_mem hentry
        simpa [map_fst_alternatingEntriesFrom] using hmapped
      · exact ih (oppositeTurn expected) hsorted.2

theorem StabilizedP3Word.entries_nonincreasing (word : StabilizedP3Word) :
    word.entries.Pairwise (fun high low => low.1 ≤ high.1) := by
  exact alternatingEntries_pairwise_levels .right word.levels word.levels_nonincreasing

/-! ## Low-level prefixes are alternating suffixes -/

theorem toggleIndex_mono (origin low high : Int)
    (hlow : origin ≤ low) (hle : low ≤ high) :
    toggleIndex origin low ≤ toggleIndex origin high := by
  unfold toggleIndex
  rw [← Int.ofNat_le]
  rw [Int.toNat_of_nonneg (by omega), Int.toNat_of_nonneg (by omega)]
  omega

theorem lowIndexFilter_isSuffix (origin : Int) (cut : Nat)
    (entries : List (Int × Turn))
    (hsorted : entries.Pairwise (fun high low => low.1 ≤ high.1))
    (hlower : ∀ entry ∈ entries, origin ≤ entry.1) :
    (entries.filter fun entry => decide (toggleIndex origin entry.1 < cut)) <:+ entries := by
  induction entries with
  | nil => exact ⟨[], rfl⟩
  | cons entry entries ih =>
      simp only [List.pairwise_cons] at hsorted
      by_cases hhead : toggleIndex origin entry.1 < cut
      · have hall : ∀ later ∈ entries,
            decide (toggleIndex origin later.1 < cut) = true := by
          intro later hlater
          have hlowerLater := hlower later (by simp [hlater])
          have hlowerHead := hlower entry (by simp)
          have hindex := toggleIndex_mono origin later.1 entry.1 hlowerLater
            (hsorted.1 later hlater)
          simp only [decide_eq_true_eq]
          omega
        have hfilterTail :
            entries.filter (fun later => decide (toggleIndex origin later.1 < cut)) = entries := by
          exact List.filter_eq_self.2 (by
            intro later hlater
            exact hall later hlater)
        exact ⟨[], by simp [hhead, hfilterTail]⟩
      · have hlowerTail : ∀ later ∈ entries, origin ≤ later.1 := by
          intro later hlater
          exact hlower later (by simp [hlater])
        rcases ih hsorted.2 hlowerTail with ⟨pre, hpre⟩
        refine ⟨entry :: pre, ?_⟩
        simp [hhead, hpre]

theorem sum_take_addIntAt_of_lt (i : Nat) (a : Int) (xs : List Int)
    (cut : Nat) (hi : i < xs.length) :
    ((addIntAt i a xs).take cut).sum =
      (xs.take cut).sum + if i < cut then a else 0 := by
  induction cut generalizing i xs with
  | zero => simp
  | succ cut ih =>
      cases xs with
      | nil => simp at hi
      | cons x xs =>
          cases i with
          | zero =>
              simp [addIntAt]
              omega
          | succ i =>
              simp only [List.length_cons, Nat.succ_lt_succ_iff] at hi
              simp only [addIntAt, List.take_succ_cons, List.sum_cons,
                Nat.succ_lt_succ_iff]
              rw [ih i xs hi]
              omega

theorem foldl_addIntAt_take_sum (origin : Int) (width : Nat)
    (entries : List (Int × Turn)) (coeffs : List Int) (cut : Nat)
    (hlength : coeffs.length = width)
    (hcovered : EntriesCovered origin width entries) :
    ((entries.foldl
      (fun values entry => addIntAt (toggleIndex origin entry.1) (turnInt entry.2) values)
      coeffs).take cut).sum =
      (coeffs.take cut).sum +
        ((entries.filter fun entry => decide (toggleIndex origin entry.1 < cut)).map
          (fun entry => turnInt entry.2)).sum := by
  induction entries generalizing coeffs with
  | nil => simp
  | cons entry entries ih =>
      have htail : EntriesCovered origin width entries := by
        intro later hlater
        exact hcovered later (by simp [hlater])
      have hindexWidth : toggleIndex origin entry.1 < width :=
        toggleIndex_lt_of_covered origin width (entry :: entries) hcovered entry (by simp)
      have hindex : toggleIndex origin entry.1 < coeffs.length := by
        simpa [hlength] using hindexWidth
      have hlength' :
          (addIntAt (toggleIndex origin entry.1) (turnInt entry.2) coeffs).length = width := by
        simp [hlength]
      rw [List.foldl_cons, ih
        (addIntAt (toggleIndex origin entry.1) (turnInt entry.2) coeffs)
        hlength' htail]
      rw [sum_take_addIntAt_of_lt (toggleIndex origin entry.1)
        (turnInt entry.2) coeffs cut hindex]
      by_cases hcut : toggleIndex origin entry.1 < cut
      · simp [hcut]
        omega
      · simp [hcut]

theorem aggregateToggles_take_sum (origin : Int) (width : Nat)
    (entries : List (Int × Turn)) (cut : Nat)
    (hcovered : EntriesCovered origin width entries) :
    ((aggregateToggles origin width entries).take cut).sum =
      ((entries.filter fun entry => decide (toggleIndex origin entry.1 < cut)).map
        (fun entry => turnInt entry.2)).sum := by
  unfold aggregateToggles
  rw [foldl_addIntAt_take_sum origin width entries (List.replicate width 0) cut
    (by simp) hcovered]
  simp

theorem StabilizedP3Word.filteredSuffix (word : StabilizedP3Word) (cut : Nat) :
    (word.entries.filter fun entry => decide (toggleIndex word.origin entry.1 < cut))
      <:+ word.entries := by
  apply lowIndexFilter_isSuffix word.origin cut word.entries word.entries_nonincreasing
  intro entry hentry
  exact (word.entries_covered entry hentry).1

theorem StabilizedP3Word.prefixSum_zero_or_terminal
    (word : StabilizedP3Word) (cut : Nat) :
    (word.delta.take cut).sum = 0 ∨
      (word.delta.take cut).sum = terminalSign .right word.levels := by
  rw [show (word.delta.take cut).sum =
      (((word.entries.filter fun entry =>
        decide (toggleIndex word.origin entry.1 < cut)).map
          (fun entry => turnInt entry.2)).sum) by
    exact aggregateToggles_take_sum word.origin word.width word.entries cut
      word.entries_covered]
  change entryBalance
      (word.entries.filter fun entry => decide (toggleIndex word.origin entry.1 < cut)) = 0 ∨ _
  exact alternatingSuffix_balance .right word.levels _ (word.filteredSuffix cut)

theorem StabilizedP3Word.balance_classification (word : StabilizedP3Word) :
    (word.balance = 0 ∧ terminalSign .right word.levels = -1) ∨
      (word.balance = 1 ∧ terminalSign .right word.levels = 1) := by
  rcases alternatingRight_classification word.levels with hnil | heven | hodd
  · exact False.elim (word.nonempty hnil)
  · exact Or.inl heven
  · exact Or.inr hodd

theorem StabilizedP3Word.delta_sum (word : StabilizedP3Word) :
    word.delta.sum = if word.growth then 1 else 0 := by
  have hsum : word.delta.sum = word.balance := by
    exact aggregateToggles_sum word.origin word.width word.entries word.entries_covered
  rcases word.balance_classification with heven | hodd
  · rw [hsum, heven.1]
    simp [StabilizedP3Word.growth, heven.1]
  · rw [hsum, hodd.1]
    simp [StabilizedP3Word.growth, hodd.1]

theorem StabilizedP3Word.terminalSign_eq_growth (word : StabilizedP3Word) :
    terminalSign .right word.levels = if word.growth then 1 else -1 := by
  rcases word.balance_classification with heven | hodd
  · rw [heven.2]
    simp [StabilizedP3Word.growth, heven.1]
  · rw [hodd.2]
    simp [StabilizedP3Word.growth, hodd.1]

theorem StabilizedP3Word.raw_prefix_bound (word : StabilizedP3Word) (cut : Nat) :
    (word.delta.take cut).sum = 0 ∨
      (word.delta.take cut).sum = if word.growth then 1 else -1 := by
  rw [← word.terminalSign_eq_growth]
  exact word.prefixSum_zero_or_terminal cut

/-! ## The derived odd strand and binary prefix scan -/

def firstOneIndex : List Int → Nat
  | [] => 0
  | x :: xs => if x = 1 then 0 else firstOneIndex xs + 1

structure FirstOneSpec (xs : List Int) (index : Nat) where
  valid : index < xs.length
  value : xs[index]'valid = 1
  earlier : ∀ j, (hj : j < index) → xs[j]'(Nat.lt_trans hj valid) ≠ 1
  prefixes_zero : ∀ cut, cut ≤ index → (xs.take cut).sum = 0

theorem firstOneIndex_spec : ∀ xs : List Int,
    (∀ cut, (xs.take cut).sum = 0 ∨ (xs.take cut).sum = 1) →
    xs.sum = 1 → FirstOneSpec xs (firstOneIndex xs)
  | [], _, hsum => by simp at hsum
  | x :: xs, hprefix, hsum => by
      have hhead := hprefix 1
      simp only [List.take_succ_cons, List.take_zero, List.sum_cons, List.sum_nil,
        Int.add_zero] at hhead
      rcases hhead with hx | hx
      · have htailPrefix : ∀ cut,
            (xs.take cut).sum = 0 ∨ (xs.take cut).sum = 1 := by
          intro cut
          have h := hprefix (Nat.succ cut)
          simp only [List.take_succ_cons, List.sum_cons] at h
          rw [hx] at h
          simpa using h
        have htailSum : xs.sum = 1 := by
          simpa [hx] using hsum
        have ih := firstOneIndex_spec xs htailPrefix htailSum
        have hindex : firstOneIndex (x :: xs) = firstOneIndex xs + 1 := by
          simp [firstOneIndex, hx]
        refine
          { valid := ?_
            value := ?_
            earlier := ?_
            prefixes_zero := ?_ }
        · rw [hindex]
          simpa using Nat.succ_lt_succ ih.valid
        · simpa [hindex] using ih.value
        · intro j hj
          cases j with
          | zero => simp [hx]
          | succ j =>
              have hj' : j < firstOneIndex xs := by
                rw [hindex] at hj
                omega
              simpa [hindex] using ih.earlier j hj'
        · intro cut hcut
          cases cut with
          | zero => rfl
          | succ cut =>
              have hcut' : cut ≤ firstOneIndex xs := by
                rw [hindex] at hcut
                omega
              have hzero := ih.prefixes_zero cut hcut'
              simp only [List.take_succ_cons, List.sum_cons]
              rw [hx, hzero]
              rfl
      · have hindex : firstOneIndex (x :: xs) = 0 := by
          simp [firstOneIndex, hx]
        refine
          { valid := ?_
            value := ?_
            earlier := ?_
            prefixes_zero := ?_ }
        · simp [hindex]
        · simp only [hindex]
          simp [hx]
        · intro j hj
          rw [hindex] at hj
          omega
        · intro cut hcut
          rw [hindex] at hcut
          have : cut = 0 := by omega
          subst cut
          rfl

theorem removeOneAt_eq_addIntAt_negOne (index : Nat) (xs : List Int) :
    removeOneAt index xs = addIntAt index (-1) xs := by
  induction index generalizing xs with
  | zero =>
      cases xs with
      | nil => rfl
      | cons x xs =>
          simp [removeOneAt, addIntAt]
          omega
  | succ index ih =>
      cases xs with
      | nil => rfl
      | cons x xs => simp [removeOneAt, addIntAt, ih]

theorem sum_take_removeOneAt (index : Nat) (xs : List Int) (cut : Nat)
    (hvalid : index < xs.length) :
    ((removeOneAt index xs).take cut).sum =
      (xs.take cut).sum - if index < cut then 1 else 0 := by
  rw [removeOneAt_eq_addIntAt_negOne]
  rw [sum_take_addIntAt_of_lt index (-1) xs cut hvalid]
  by_cases hcut : index < cut <;> simp [hcut] <;> omega

theorem removeOneAt_prefix_bound (xs : List Int) (index : Nat)
    (hvalid : index < xs.length)
    (hprefix : ∀ cut, (xs.take cut).sum = 0 ∨ (xs.take cut).sum = 1)
    (hbefore : ∀ cut, cut ≤ index → (xs.take cut).sum = 0) :
    ∀ cut, ((removeOneAt index xs).take cut).sum = 0 ∨
      ((removeOneAt index xs).take cut).sum = -1 := by
  intro cut
  rw [sum_take_removeOneAt index xs cut hvalid]
  by_cases hcut : index < cut
  · rcases hprefix cut with hzero | hone
    · right
      simp [hcut, hzero]
    · left
      simp [hcut, hone]
  · left
    have hle : cut ≤ index := by omega
    simp [hcut, hbefore cut hle]

theorem scanWidget_binary_of_prefix_bounds (previous : Int) :
    ∀ xs : List Int,
      (∀ cut, previous - (xs.take cut).sum = 0 ∨
        previous - (xs.take cut).sum = 1) →
      ∀ a ∈ scanWidget previous xs, a = 0 ∨ a = 1
  | [], _ => by simp [scanWidget]
  | x :: xs, hprefix => by
      intro a ha
      simp only [scanWidget, List.mem_cons] at ha
      rcases ha with hhead | htail
      · subst a
        have h := hprefix 1
        simpa using h
      · apply scanWidget_binary_of_prefix_bounds (previous - x) xs
          (fun cut => by
            have h := hprefix (Nat.succ cut)
            simp only [List.take_succ_cons, List.sum_cons] at h
            rcases h with hzero | hone
            · left; omega
            · right; omega) a htail

theorem StabilizedP3Word.firstOneSpec (word : StabilizedP3Word)
    (hgrowth : word.growth = true) :
    FirstOneSpec word.delta (firstOneIndex word.delta) := by
  apply firstOneIndex_spec word.delta
  · intro cut
    simpa [hgrowth] using word.raw_prefix_bound cut
  · simpa [hgrowth] using word.delta_sum

theorem StabilizedP3Word.even_prefix_bound (word : StabilizedP3Word)
    (hgrowth : word.growth = false) (cut : Nat) :
    (word.delta.take cut).sum = 0 ∨ (word.delta.take cut).sum = -1 := by
  simpa [hgrowth] using word.raw_prefix_bound cut

theorem StabilizedP3Word.odd_balanced_prefix_bound (word : StabilizedP3Word)
    (hgrowth : word.growth = true) (cut : Nat) :
    ((removeOneAt (firstOneIndex word.delta) word.delta).take cut).sum = 0 ∨
      ((removeOneAt (firstOneIndex word.delta) word.delta).take cut).sum = -1 := by
  have hspec := word.firstOneSpec hgrowth
  apply removeOneAt_prefix_bound word.delta (firstOneIndex word.delta)
    hspec.valid
  · intro k
    simpa [hgrowth] using word.raw_prefix_bound k
  · exact hspec.prefixes_zero

end Langton.TraceGeometry
