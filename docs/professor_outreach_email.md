# Outreach: who to write to, and what to say

**Nothing here has been sent.** Every address below was found published on an
institutional or personal page and is marked with a confidence level. Read the
"Before you send anything" section first — the arXiv endorsement rules changed in
December 2025 and again in January 2026, and that changes the order you should
approach people in.

Each letter is written to be short. Unsolicited mail to a mathematician competes with
a full inbox; the ones that get answered ask **one** specific question that only that
person can answer, and make it easy to say "no, but try X".

---

## Before you send anything

0. **Publish the width-four release FIRST — this is the hard blocker.** The live link
   in every draft, `https://atharva12456.github.io/langtons-ant-highway/paper.pdf`,
   still serves the *pre-width-four* paper until you commit and push the current
   working tree. If a recipient clicks it before you push, they get a paper that does
   not contain the results your letter describes — the worst possible first
   impression. Commit, push `main`, wait for GitHub Pages to rebuild, and confirm the
   live PDF is 24 pages with the width-four theorem, before sending anything.
1. **Check your author details.** The paper lists Atharva Jillhewar as an independent
   researcher with the Gmail address `Atharvajil124@gmail.com`. Add an ORCID only if
   you have one and want it shown. Rebuild the PDFs, resync `docs/`, and rerun
   `python results/update_artifact_hashes.py` after any change.
2. **Mint a version DOI.** The concept DOI `10.5281/zenodo.21381637` always resolves
   to the newest version, which means it does *not* pin the bytes someone reviews.
   Cite the exact version DOI in the letter.
3. **Send them one at a time**, a few days apart. arXiv explicitly asks that you not
   mass-email potential endorsers.
4. **Never** describe the AI-assisted audits as peer review, never say the conjecture
   is solved, and never call the residue-free Java variant an independent
   implementation. All three are things a referee will check.
5. **Attach nothing** unless their page says unsolicited attachments are welcome —
   link instead.

### On arXiv endorsement (this is the binding constraint)

arXiv tightened endorsement for Mathematics on 10 December 2025 and extended it to all
archives on 21 January 2026. Verified against arXiv's own help page and policy
announcement, the rule is now:

> automatic endorsement requires "an institutional email address from an
> academic/research institution **and** previous authorship on an existing paper which
> has been accepted to the arXiv"

**A GMU institutional address is necessary but not sufficient.** Both conditions must
hold, and the second one — a prior arXiv-accepted paper — does not. So a **personal
endorsement is still required**. Do not assume the `.edu` address alone will get the
submission through; it will not.

Note also what an *endorser* must be: someone who has authored enough papers **within
the specific endorsement domain** (math.CO or math.DS) and is registered as an author
of them on arXiv. A professor who works in, say, PDEs or statistics cannot endorse for
math.CO no matter how senior. Check the person's actual arXiv category history before
asking.

### About the GMU address (summer-programme account) — two cautions

The GMU account here comes from the ASSIP summer programme, not from matriculated
enrolment in the Mathematical Sciences department. That has two consequences worth
getting right.

**Do not put George Mason on the paper as an affiliation.** An affiliation line says
the work was done under that institution's auspices. This work was done independently
— not through ASSIP, not under a GMU mentor, not reviewed by anyone there. Claiming
GMU implies institutional backing the paper does not have, and it is exactly the sort
of thing a referee or a professor checks. The paper therefore reads *Independent
researcher*, which is accurate. Being selected for ASSIP is a genuine credential, and
you can mention it in the body of a letter — "I am at GMU this summer on the ASSIP
programme" — where it is a true statement about you rather than a claim about the
paper.

**Do not use the programme address as the contact of record.** It will very likely be
deactivated when the summer ends. Anything you put in the paper, or register with
arXiv, has to outlive that: readers write to a corresponding address for years, and
arXiv ties your account to the address you sign up with — losing it is a genuine
nuisance to undo. So:

- put a **permanent personal address** in `\email{}` and in every signature block;
- if you like, *send* from the GMU address while it is live, since a `.edu` sender does
  get opened more often than free webmail — but sign with the permanent one, and say
  which is which;
- register any arXiv account with the permanent address.

**The one thing genuinely worth using it for:** ASSIP places you with a GMU faculty
mentor. That person already knows you and sees you regularly, which makes them the
warmest contact available by a wide margin. Even if their field is nothing like
discrete dynamics, "who at Mason would be the right person to ask about discrete
dynamical systems?" is a thirty-second question that gets you a name plus an implicit
introduction — worth more than any cold email on this list.

- **math.CO endorser:** James Propp — active in math.CO, co-author of the 1995 ant
  paper, and has a long public record of engaging with people outside academia.
- **math.DS endorser:** Serge Troubetzkoy — active math.DS submitter and author of the
  foundational unboundedness theorem.
- Note that Gajardo, Lutfalla and Rao post mainly to **cs.DM**. They are the best
  *scientific* readers but may not be eligible endorsers for math.CO or math.DS. If
  cs.DM is an acceptable primary category, Lutfalla becomes the obvious first ask.

### Order of operations

1. **Lutfalla** — most active on exactly this problem, publishes counterexamples to the
   generalised highway conjecture, and by some distance the most likely to reply.
2. **Propp** — endorsement-eligible in math.CO, gives the rotor-router structural
   reading, and has a long public record of engaging people outside academia. If you
   send only two letters, these are the two.
3. **Moreira or Gajardo** — the decidability-versus-undecidability question, which is
   the first objection any referee will raise. Worth having an answer before
   submission rather than after.

Send one at a time, a few days apart. In parallel, and at essentially no cost, ask your
ASSIP mentor the thirty-second question in the GMU note below — it is the one local
lever available and it costs you nothing to pull.

---

---

# GMU note — one cheap parallel move

You are at GMU for the summer on ASSIP, not as a Mathematical Sciences student, so the
local route is thinner than it would otherwise be: you cannot lean on being "their"
student in the department, and a cold email to a Mason professor you have never met is
just another cold email. But two moves cost almost nothing.

**Ask your ASSIP mentor** who at Mason works on discrete dynamical systems or
combinatorics. Thirty seconds, and it converts a cold email into a referred one.

**If you do get a name, the letter is a different genre** from the international ones
below — do not send a Mason professor the same letter you would send Gajardo:

- **Ask for twenty minutes, not a review.** "Would you be willing to look at a
  manuscript" is a large ask that is easy to decline by not replying. "Could I come to
  your office hours for twenty minutes to ask about one theorem" is small, concrete,
  and hard to refuse.
- **Lead with the fact that you are their student.** It is the entire reason this
  letter outranks a cold email.
- **Keep it under 200 words.** They can ask for detail.
- **Attach nothing.** Bring a printout to the meeting instead.
- Go to **office hours** if they hold them. An email is a fallback, not the preferred
  channel, when you are on the same campus.

## GMU template

**Subject:** ASSIP student at Mason — 20 minutes on a discrete-dynamics result?

> Dear Professor [Surname],
>
> I am at George Mason this summer on the ASSIP programme. Separately from that, and on
> my own, I have been working on a problem in discrete dynamical systems — the highway
> conjecture for Langton's ant. I have written it up, and I have reached the point where
> I need someone who knows the area to tell me whether it is worth anything.
>
> The specific result I would most like to ask you about: for a periodic "highway"
> trajectory, I can show that the two extreme lines transverse to the direction of
> travel consist of cells the ant enters exactly once and never returns to, and from
> that I get an exclusion result that holds for every period rather than up to a
> computational bound. The proof is short — about a page — and uses only a parity
> argument plus the order in which a cell is visited.
>
> Could I come to your office hours for twenty minutes and walk you through that one
> argument? I am not asking you to referee the whole thing. If it is outside your area,
> I would be grateful for a pointer to whoever at Mason is closest to it.
>
> [Your name] · [GMU email] · [degree programme and year]

## Also worth doing at GMU

- **Ask the Director of Undergraduate Studies (or Graduate Studies) in Mathematical
  Sciences** who is closest to discrete dynamics or combinatorics. That is precisely
  their job, it is a one-line email, and it gets you a name with an implicit
  introduction.
- **Go to the department colloquium.** Speakers and attendees are the people you want,
  and talking to someone after a talk is far more effective than any email.
- **Check whether GMU's undergraduate research programme (URSP) or an honours-thesis
  route applies to you.** Either gives you a formal reason for a faculty member to
  supervise the work, which solves the endorsement problem as a side effect.
- **The endorsement check:** before asking anyone at GMU to endorse you, look them up
  on arXiv and confirm they actually post in math.CO or math.DS. Being a mathematician
  is not enough; arXiv requires papers in the specific endorsement domain.

## Standard closing block

Use this at the foot of every letter:

> The manuscript, LaTeX source, Lean project and hash-audited search records are here:
>
> - Paper (PDF): `https://atharva12456.github.io/langtons-ant-highway/paper.pdf`
> - Code, data and records: `https://github.com/Atharva12456/langtons-ant-highway`
> - Version DOI: **[fill in the exact version DOI, not the concept DOI]**
>
> I know an unsolicited manuscript is a lot to ask for. Even a pointer to the right
> reader or the right piece of literature would help.
>
> With thanks,
> Atharva Jillhewar
> Independent researcher
> [professional email] · [ORCID, if you have one]

---

# 1. Victor H. Lutfalla — *send this one first*

- **Aix-Marseille Université, LIS (Laboratoire d'Informatique et Systèmes), team CaNa**
- `victor.lutfalla@lis-lab.fr` — published in anti-spam form on his page; also
  `victor.lutfalla@math.cnrs.fr`. **Confidence: high** (page current, lists 2025 work).
- Note: the "Ants on the highway" arXiv byline says I2M; he has since moved to LIS.

**Subject:** Extremal-line rigidity for classical ant highways — does it survive for generalised rules?

> Dear Dr Lutfalla,
>
> I have been working independently on the finite-support highway conjecture for the
> classical two-colour Langton's ant, and your recent papers are the reason I am
> writing.
>
> "Sideways on the highways" gives rules (LLRRRL, LLRLRLL) that admit both highway and
> non-highway emergent behaviour from finite configurations, which is exactly the kind
> of object I cannot test against. I have a preprint proving necessary conditions on
> *periodic* highways of the classical rule. One result is a transverse rigidity
> theorem: taking a linear functional t killing the drift, the two extremal level lines
> t = max and t = min share a single arrival axis, every turn on them is R, and each of
> their cells the trace reaches is entered exactly once and never revisited. The proof
> uses only the order in which a cell is visited — that the stabilised turn sequence at
> a cell alternates and begins with R — plus the checkerboard/HV partition. From it I
> get that no periodic highway has transverse width two. A separate computer-assisted
> crossing-sequence argument excludes width four at every period: two independent
> exact enumerators give the same 12-edge acyclic blank-column graph, and Lean checks
> its rank consequence. Both statements are scoped to diagonal periodic highways.
>
> My question is narrow: **does that argument have any chance for a longer rule
> string?** It leans on two things that are special to RL — that arrivals at a cell all
> share one axis, and that consecutive visits to a cell alternate turns. For a rule of
> length k the visit sequence at a cell is periodic with period k rather than
> alternating, so the "a second visit would read RR" step fails immediately. If your
> LLRLRLL highways have a well-defined transverse width, I would be very interested to
> know whether it is bounded below, and whether the extremal lines there are also
> single-visit.
>
> A second, much smaller question: I exclude all nonzero-drift periods up to 48 by
> exhaustive search. Could `GL_ant` reproduce that independently? A disagreement would
> be far more useful to me than agreement.

---

# 2. James Propp — *best math.CO endorsement prospect*

- **University of Massachusetts Lowell, Dept of Mathematics and Statistics**
- `James_Propp@uml.edu` — **Confidence: high** (page updated Oct 2025, Spring 2026
  teaching listed).
- Co-author of Gale–Propp–Sutherland–Troubetzkoy, "Further travels with my ant"
  (*Mathematical Intelligencer* 17(3), 1995), whose checkerboard partition my Section 2
  rests on; also the rotor-router / chip-firing literature.

**Subject:** Does the medial-graph encoding of Langton's ant make its non-abelianness visible?

> Dear Professor Propp,
>
> The checkerboard partition from "Further travels with my ant" is the foundation of a
> preprint I have written on the finite-support highway conjecture, and a question has
> come out of it that I think sits squarely in your territory.
>
> I re-encode the ant as an edge-toggling system on a medial (Tait) graph: cells become
> edges, the turn rule becomes a transition at a 4-valent vertex, and the black set
> becomes an edge subgraph, with a cycle-rank surgery identity E + ΔC = 2β. That is
> visibly the combinatorial language of the rotor-router and Eulerian-partition
> framework you surveyed in "Chip-Firing and Rotor-Routing on Directed Graphs".
>
> **My question: in that encoding, is the ant's failure of abelianness a legible
> obstruction?** The rotor-router's abelian property is transparent in the transition
> language; the ant is essentially a single-chip, non-abelian rotor-router, and I would
> like to know whether the medial picture localises exactly what breaks, or whether it
> just relocates the difficulty.
>
> There is a concrete reason to hope it does. A width-two strip forces a
> flipping-mirror walk on Z, and a width-four strip has an exact one-column
> crossing-sequence graph that turns out to be acyclic. At width six that local proof
> fails sharply: an interior two-state rotor oscillator appears and already respects
> same-cell alternation. Is there a rotor-router or abelian-network language that
> couples adjacent columns strongly enough to rule out that recurrence globally?
>
> I should say plainly that the paper does not prove the conjecture and does not claim
> to; it proves necessary conditions and an exhaustive exclusion of periods up to 48.
>
> If the work looks sound to you, I would also be grateful for advice on submitting to
> arXiv — as an independent researcher I now need a personal endorsement under the
> policy that took effect this January, and math.CO would be the natural category.

---

# 3. Anahí Gajardo

- **Universidad de Concepción, Depto de Ingeniería Matemática / CI²MA, Chile.**
  Her departmental listing gives her interests literally as "Discrete Dynamical
  Systems, Langton's ant".
- `anahi@ing-mat.udec.cl` — published in anti-spam form on her page.
  **Confidence: medium-high** — that page's publication list stops at 2018, so it may
  be stale even though she is demonstrably active (2025 journal paper). Fallback:
  the group address `discretemath@udec.cl`.

**Subject:** A decidable periodic-realisability criterion for the ant's trace subshift

> Dear Professor Gajardo,
>
> Your 2003 DMTCS paper associates a subshift to Langton's ant by symbolic projection
> and characterises forbidden factors. I have been working independently on the
> finite-support highway conjecture, and the main object in my preprint is, I think,
> a global condition on exactly that projection.
>
> The result is a decision procedure: for a finite turn word w that restores the
> heading and has nonzero drift, w^ω is the trace of the ant from *some* finite-support
> colouring if and only if, in each translation class of phases, the chronological turn
> sequence at a cell alternates and its stabilised form begins with R — and when that
> holds, an explicit finite black seed can be written down. It is a statement about
> global periodic realisability rather than local factor admissibility.
>
> **My question is whether this is the right formulation relative to your work.** Can
> the criterion be phrased as a condition on the language of the trace subshift, and if
> so, does it connect to your later undecidability results for trace subshifts of
> Turing machines? I would rather learn now that I have restated something known in
> unfamiliar notation than after submitting.
>
> A second question I would value your view on: "Ants on the highway" catalogues
> highways for generalised rules with a wide range of displacement vectors and speeds.
> For the classical rule I derive a lower bound g ≥ 2·max(|a|,|b|) tying net growth per
> period to the drift (a,b). Do any of the highways in your catalogue come close to
> saturating an analogous bound? If some do, my bound is close to sharp; if none do, it
> is probably weak and I would like to know that.

---

# 4. Serge Troubetzkoy — *best math.DS endorsement prospect*

- **Aix-Marseille Université, Institut de Mathématiques de Marseille (I2M, UMR 7373)**
- `serge.troubetzkoy@univ-amu.fr` — **Confidence: high** (listed literally on his I2M
  page and directory entry).

**Subject:** Is a signed mod-four wake residue a genuine strengthening of the 1992 parity argument?

> Dear Professor Troubetzkoy,
>
> Bunimovich–Troubetzkoy (1992) is the fixed point that everything I have done rests
> on, and I have a question about it that I cannot settle from the outside.
>
> Working independently on the finite-support highway conjecture, I have a preprint on
> necessary conditions for *periodic* highways. Two results are relevant to you. The
> first is an even-winding theorem: no finite-support pattern can drift to an exact
> translate of itself with the heading restored and zero net change in the number of
> black cells. That is a statement your 1992 theorem does not reach, since a
> zero-growth glider is unbounded; it implies every periodic highway must grow a wake,
> of size divisible by four. The second is a signed mod-four identity for the wake:
> checker-signed strand bases sum to 2 mod 4 in each residue class of a nonzero drift
> coordinate, which yields g ≥ 2·max(|a|,|b|).
>
> **The question: is that mod-four residue a real strengthening of the parity/counting
> argument in your 1992 paper, or is it logically downstream of it?** Both are
> bookkeeping on the boundary of the visited set, mine one level finer, and I cannot
> tell from the outside whether I have refined your argument or merely re-derived it in
> heavier notation. You are in the best position of anyone to say.
>
> I should be clear that none of this resolves the conjecture. The paper proves
> necessary conditions and an exhaustive exclusion of periods up to 48, and states the
> two remaining obligations explicitly.
>
> If it looks worth posting, I would also be grateful for advice about arXiv: the
> endorsement rules changed in December and I now need a personal endorsement to submit
> to math.DS.

---

# 5. Andrés Moreira — *asks the objection a referee will raise first*

- **Universidad Técnica Federico Santa María (UTFSM), Depto de Informática, Chile**
- `andres.moreira@usm.cl` — **Confidence: high** (literal, on his official department
  page).

**Subject:** Reconciling a decidable periodic criterion with the universality of Langton's ant

> Dear Professor Moreira,
>
> Gajardo–Moreira–Goles shows that a single ant trajectory can compute an arbitrary
> boolean circuit, giving P-hardness and undecidability for several asymptotic
> questions. I have a preprint that proves a **decidable** criterion, and I would like
> to check the boundary with you before I embarrass myself in front of a referee.
>
> The criterion decides, for a finite turn word restoring the heading with nonzero
> drift, whether its infinite repetition is realisable from *some* finite-support
> colouring, and constructs the seed when it is. My understanding of why this does not
> collide with your result is that decidability holds only for this restricted class —
> exactly periodic traces with nonzero drift, quantified existentially over seeds —
> whereas your undecidability bites on general asymptotic behaviour of a *given*
> configuration. The two quantify differently and over different objects.
>
> **Is that the right place to draw the line?** If the boundary is somewhere else, or
> if the restricted problem is already known to be decidable, I would very much rather
> hear it now. This is the first objection I expect a referee to raise, and I would
> like to answer it properly in the paper rather than defensively.
>
> The paper does not claim the conjecture; it proves necessary conditions on periodic
> highways plus an exhaustive exclusion of periods up to 48.

---

# 6. Michaël Rao — *the computational-methodology reader*

- **CNRS, LIP (Laboratoire de l'Informatique du Parallélisme), ENS de Lyon, team MC2**
- `michael.rao@ens-lyon.fr` — published in anti-spam form on his page.
  **Confidence: medium** — the address format is unambiguous but his publications page
  has not been updated since 2018 and the contact sub-page returned a server error.

**Subject:** Certificate design for an exhaustive periodic-highway exclusion

> Dear Dr Rao,
>
> "Ants on the highway" reports highway frequencies as low as one in 10⁷, which means
> the search behind it was serious. I have a search problem of the same shape and a
> methodological question for you.
>
> I have exhaustively excluded every finite-support periodic highway of nonzero drift
> with period at most 48 for the classical rule — about 4.2 × 10¹⁰ nodes at period 48,
> rank-sharded, with the exact realisability criterion applied at every
> positive-growth, nonzero-drift leaf. The per-rank shard records are published.
>
> **My question is about certificates rather than speed.** A zero-hit exhaustive search
> is only as good as the argument that the search space was complete, and I would value
> your judgement on two points: whether cyclic-phase normalisation plus rank sharding
> is the right way to make coverage auditable, and whether there is a practical way to
> emit a certificate an independent checker could verify *without* rerunning the
> search. At the moment I can only offer per-rank counters that reconcile with their
> aggregates, which proves internal consistency and not much else.
>
> One thing I would flag honestly: my three search variants share an enumeration
> framework and a criterion routine, so their agreement is a consistency check and not
> implementation independence. I have a separate Python verifier written from the
> theorem statement, but only brute-force-checkable up to length 18.

---

# 7. Jo Ellis-Monaghan — *the strongest reader for the medial-graph section*

- **University of Amsterdam, Korteweg-de Vries Institute for Mathematics; Director of
  KdVI since October 2024**
- `j.a.ellismonaghan@uva.nl` — **Confidence: high** (literal, on her UvA profile).
- No Langton's ant history — this is a *methods* contact. Keep the letter narrow, and
  bear in mind she directs an institute and has little spare time.

**Subject:** Is an edge-toggling dynamical system a transition system on the medial graph?

> Dear Professor Ellis-Monaghan,
>
> I am writing about a graph-theoretic question rather than a dynamical one, and your
> work on medial graphs, transition polynomials and k-valuations is the reason.
>
> In a preprint on Langton's ant I re-encode the automaton as an edge-toggling system:
> cells of Z² become edges of a medial (Tait) graph, the turn rule becomes a choice of
> transition at each 4-valent vertex, and the evolving black set becomes an edge
> subgraph, with a surgery identity E + ΔC = 2β relating edge count, component change
> and cycle rank.
>
> **My question: is this an instance of the general Tait/medial framework, or an ad hoc
> bijection that happens to work?** Concretely — can the ant's rule be presented as a
> transition system in your sense, so that the conjugacy follows from Tait/medial
> duality rather than being verified by hand? If it can, the structural part of my paper
> gets a much better framing than the one I gave it, and I would rather cite the general
> theory than reprove a special case of it badly.
>
> I am aware this is peripheral to your current work and that you are directing an
> institute; a one-line "yes, see X" or "no, because Y" would be worth a great deal to
> me.

---

# 8. Lorenzo Traldi

- **Lafayette College — Marshall R. Metzgar Professor *Emeritus*.** Address him as
  emeritus, not as serving faculty. He is genuinely still producing (four papers in
  2025).
- `traldil@lafayette.edu` — **Confidence: high** (literal, on his personal site and the
  department page; site carries a 2026 copyright).

**Subject:** Is a mod-four wake residue a specialisation of signed interlacement?

> Dear Professor Traldi,
>
> Your 2025 paper on circuit partitions and signed interlacement in 4-regular graphs
> describes, I believe, exactly the setting my problem lives in, and I would like to
> ask whether one of my invariants is really one of yours.
>
> In a preprint on Langton's ant, the visited region carries a 4-regular medial graph;
> the ant's turn rule selects a transition at each vertex, and one period of a periodic
> highway is a circuit in the resulting circuit partition. Separately I derive a signed
> mod-four residue identity on the highway's wake, which yields a lower bound
> g ≥ 2·max(|a|,|b|) tying growth to drift.
>
> **My question: is that mod-four residue a specialisation of a signed interlacement
> invariant?** If it is, the bound presumably has a cleaner derivation than mine, and
> possibly a stronger one — my proof is a hand computation with charges and I have
> explicit models showing it cannot be improved by incidence data alone.
>
> I should add one thing in the interest of not wasting your time: an earlier draft
> claimed a touch-graph rank computation built on your interlacement theory. I could not
> make it self-contained and I removed the claim rather than assert it. So this is a
> question about whether the connection is real, not a claim that I have already used
> it.

---

# 9. Wesley Pegden

- **Carnegie Mellon University, Dept of Mathematical Sciences**
- `wes@math.cmu.edu` — **Confidence: high** (literal, on the CMU faculty page).
- Prefer him over Lionel Levine for this content: Levine's rotor-router credentials are
  real, but his site now describes him as working on AI safety, and Pegden is still
  full-time on sandpiles.

**Subject:** What plays the role of an integer-superharmonic certificate for a non-abelian single-particle system?

> Dear Professor Pegden,
>
> Levine–Pegden–Smart is the example I keep returning to of an emergent pattern that
> looked inexplicable and was then actually proved rigid, via a classification of
> integer-superharmonic functions that certifies the limit shape. I am trying to do
> something of the same genre for Langton's ant and I am stuck in a way you may
> recognise.
>
> In a preprint on the finite-support highway conjecture I can prove local rigidity:
> for a periodic highway with diagonal drift, the two extremal level lines transverse to
> the drift consist of cells the ant enters exactly once and never revisits, every turn
> on them is R, and the transverse width is even. That excludes transverse width two.
> A computer-assisted 12-edge crossing-sequence graph also excludes width four at
> every period, so diagonal width is at least six. What I cannot do is control widths
> six and above, and so I still cannot turn local rigidity into a classification.
>
> **The question I would most like your view on: what plays the role of the
> integer-superharmonic certificate for a non-abelian, single-particle system?** The
> sandpile has an abelian property and a harmonic structure to exploit; the ant has
> neither, and every monotone quantity I have tried fails — I can show that no
> nonconstant affine combination of edge count, vertex count, component count and cycle
> rank is monotone along the orbit, because the eight possible one-step increments are
> centrally symmetric and span.
>
> If your answer is "there isn't one, and that's why the ant is hard", that is genuinely
> useful to me and I will stop looking for it.

---

## People considered and deprioritised, with reasons

| Person | Why not first |
|---|---|
| **Eric Goles** (UAI, Chile) — `eric.chacc@uai.cl`, confidence medium-high (from a Sept 2025 arXiv author block; his UAI profile renders it corrupted) | Same technical question as Moreira, but he is very senior, runs a doctoral programme, and now works on freezing automata networks. Write to Moreira instead. |
| **Leonid Bunimovich** (Georgia Tech) — `leonid.bunimovich@math.gatech.edu`, confidence high | Originated the Lorentz-lattice-gas framing, but the 1992 paper is 34 years old and he now works on billiards and statistical mechanics. Troubetzkoy is the better contact from the same paper. |
| **Scott Sutherland** (Stony Brook) — `scott@math.stonybrook.edu`, confidence high | Did the original computational exploration for the 1995 paper and still hosts the ant pages, but he is department chair and no longer researches this. Good for computational provenance only. |
| **Lionel Levine** (Cornell) — `levine@math.cornell.edu`, confidence high | Rotor-router credentials are real, but he has visibly pivoted to AI safety. Use only if Pegden does not reply. |
| **Benjamin Hellouin de Menibus** (LISN, Paris-Saclay) | Sits at the intersection of both groups (co-author on "Nontrivial Turmites are Turing-universal" and with Lutfalla). I did not verify his current affiliation or address — worth checking if you want a tenth. |

## What could not be verified

- No individual address is published on the UdeC group page; Gajardo's comes from her
  own page, whose publication list stops at 2018.
- Rao's contact sub-page returned a server error; his publications page is stale since
  2018.
- Goles's address is confirmed only from a September 2025 arXiv author block.
- Which of Gajardo / Lutfalla / Rao is the designated corresponding author for "Ants on
  the highway" could not be confirmed (publisher page behind a login).
