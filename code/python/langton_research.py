#!/usr/bin/env python3
"""Exact and heuristic experiments for the finite-support Langton-ant highway conjecture.

Conventions
-----------
* White cells are absent from ``black`` and cause a right turn.
* Black cells are present in ``black`` and cause a left turn.
* A step turns, flips the current cell, and then moves.

The important distinction in this file is between:
* a *heuristic* detector (three repeated 104-step traces), used for search; and
* a finite *gateway certificate*.  The latter proves indefinite highway motion
  when its finite template matches and its semi-infinite leading corridor is
  known to be white.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import deque
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence


Point = tuple[int, int]
DIRS: tuple[Point, ...] = ((0, 1), (1, 0), (0, -1), (-1, 0))
PERIOD = 104


def add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def sub(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def mul(k: int, a: Point) -> Point:
    return k * a[0], k * a[1]


def rotate_point(p: Point, quarter_turns: int) -> Point:
    x, y = p
    for _ in range(quarter_turns % 4):
        x, y = y, -x
    return x, y


def tait_edge(cell: Point) -> tuple[Point, Point]:
    """Map an ant cell to its edge in the checkerboard Tait lattice.

    Tait vertices label the all-white clockwise plaquette cycles by the
    lower-left corners of plaquettes whose coordinate sum is odd.  A black
    ant cell switches the two white boundary pairings and is therefore an
    occupied edge between the two diagonally opposite such plaquettes.
    """
    x, y = cell
    if (x + y) & 1:
        return (x - 1, y - 1), (x, y)
    return (x, y - 1), (x - 1, y)


def tait_graph_stats(black: Iterable[Point]) -> dict[str, int]:
    """Return exact finite-graph topology for a black-cell configuration.

    If E is the black-edge count, V the number of incident Tait vertices,
    and k the number of nonempty components, then beta=E-V+k is the cycle
    rank.  The regular-neighborhood boundary has k+beta components.  Relative
    to the V separate all-white plaquette cycles its loop-count change is
    E-2V+2k, and E + loop_change = 2*beta.
    """
    edges = [tait_edge(p) for p in black]
    parent: dict[Point, Point] = {}

    def find(v: Point) -> Point:
        parent.setdefault(v, v)
        root = v
        while parent[root] != root:
            root = parent[root]
        while parent[v] != v:
            parent[v], v = root, parent[v]
        return root

    def union(a: Point, b: Point) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in edges:
        union(a, b)
    vertices = set(parent)
    components = len({find(v) for v in vertices})
    edge_count = len(edges)
    vertex_count = len(vertices)
    beta = edge_count - vertex_count + components
    boundary_loops = components + beta
    loop_change = edge_count - 2 * vertex_count + 2 * components
    assert edge_count + loop_change == 2 * beta
    return {
        "edges": edge_count,
        "vertices": vertex_count,
        "components": components,
        "cycle_rank": beta,
        "boundary_loops": boundary_loops,
        "loop_change_from_white": loop_change,
    }


def parity_charge_profiles(
    black: Iterable[Point], pos: Point, direction: int
) -> tuple[frozenset[int], frozenset[int]]:
    """Return the conserved column and row charges over F_2.

    A Laurent polynomial over F_2 is represented by the set of exponents
    having coefficient one.  The two exact invariants are

        sum_{(x,y) in B} X^x + [q vertical] X^{p_x},
        sum_{(x,y) in B} Y^y + [q horizontal] Y^{p_y}.

    Repeated exponents cancel, so only column/row parities are stored.
    """
    columns: set[int] = set()
    rows: set[int] = set()
    for x, y in black:
        columns.symmetric_difference_update((x,))
        rows.symmetric_difference_update((y,))
    if direction % 2 == 0:
        columns.symmetric_difference_update((pos[0],))
    else:
        rows.symmetric_difference_update((pos[1],))
    return frozenset(columns), frozenset(rows)


def centered_black_moment(black: Iterable[Point], pos: Point) -> Point:
    """Return J=sum_{z in B}(z-pos), the black first moment about the ant."""
    sx = sy = count = 0
    for x, y in black:
        sx += x
        sy += y
        count += 1
    return sx - count * pos[0], sy - count * pos[1]


def mod4_moment_charge(
    black: Iterable[Point], pos: Point, direction: int
) -> int:
    """Return an exact conserved charge modulo four.

    The black contribution is sum(x+y).  The ant potentials for headings
    N,E,S,W are respectively 2x+3y+3, x+2y+2, y+3, and 3x+2.
    """
    x, y = pos
    potentials = (2 * x + 3 * y + 3, x + 2 * y + 2, y + 3, 3 * x + 2)
    return (sum(px + py for px, py in black) + potentials[direction & 3]) & 3


def mod4_rotated_moment_charge(
    black: Iterable[Point], pos: Point, direction: int
) -> int:
    """Return the conserved x-y analogue of ``mod4_moment_charge``."""
    x, y = pos
    potentials = (2 * x + 3 * y + 3, x + 2, y + 3, 3 * x + 2 * y + 2)
    return (sum(px - py for px, py in black) + potentials[direction & 3]) & 3


def mod4_quadratic_charge(
    black: Iterable[Point], pos: Point, direction: int
) -> int:
    """Return the independent quadratic additive charge modulo four.

    The black-cell weight is Q(x,y)=x^2+2xy.  Potentials for N,E,S,W are
    2xy+3x, 3x^2+x, 2x^2+2xy+3x, and x^2+x, respectively.
    """
    x, y = pos
    potentials = (
        2 * x * y + 3 * x,
        3 * x * x + x,
        2 * x * x + 2 * x * y + 3 * x,
        x * x + x,
    )
    black_sum = sum(px * px + 2 * px * py for px, py in black)
    return (black_sum + potentials[direction & 3]) & 3


def predicted_path_from_black_count(
    turns: Sequence[int],
    initial_black_count: int,
    initial_pos: Point = (0, 0),
    initial_direction: int = 0,
) -> tuple[list[int], list[Point], list[int]]:
    """Reconstruct the exact path from only the black-count walk.

    Turns use this file's encoding: 0 is R and 1 is L.  The return values
    include both endpoints, so their lengths are len(turns)+1.
    """
    if initial_black_count < 0:
        raise ValueError("black count must be nonnegative")
    offset = (initial_direction - initial_black_count) & 3
    count = initial_black_count
    pos = initial_pos
    counts = [count]
    positions = [pos]
    directions = [initial_direction]
    for turn in turns:
        if turn not in (0, 1):
            raise ValueError("turns must use 0=R and 1=L")
        count += 1 if turn == 0 else -1
        if count < 0:
            raise ValueError("the proposed black-count walk became negative")
        direction = (offset + count) & 3
        pos = add(pos, DIRS[direction])
        counts.append(count)
        positions.append(pos)
        directions.append(direction)
    return counts, positions, directions


def closed_count_edge_multiplicities(counts: Sequence[int]) -> dict[int, int]:
    """Return upcrossing counts m_k for a closed nonnegative count walk."""
    if not counts or counts[0] != counts[-1] or min(counts) < 0:
        raise ValueError("counts must be a closed nonnegative walk")
    up: dict[int, int] = {}
    down: dict[int, int] = {}
    for a, b in zip(counts, counts[1:]):
        if b == a + 1:
            up[a] = up.get(a, 0) + 1
        elif b == a - 1:
            down[b] = down.get(b, 0) + 1
        else:
            raise ValueError("successive black counts must differ by one")
    if up != down:
        raise AssertionError("a closed walk must cross each edge equally both ways")
    if up:
        support = sorted(up)
        if support != list(range(support[0], support[-1] + 1)):
            raise AssertionError("the support of a one-dimensional walk is contiguous")
    return up


def clean_translator_moment_sum(
    counts: Sequence[int], heading_offset: int = 0
) -> Point:
    """Evaluate the necessary centered-moment sum for a clean translator.

    A clean translation recurrence must make this vector zero.  This is only
    a necessary condition; it does not check the alternating-visit rule.
    """
    sx = sy = 0
    for count in counts[1:]:
        dx, dy = DIRS[(heading_offset + count) & 3]
        sx += count * dx
        sy += count * dy
    return sx, sy


DirectedState = tuple[Point, int]


def frozen_successor(black: set[Point], state: DirectedState) -> DirectedState:
    """One successor in the frozen routing permutation rho_B."""
    pos, direction = state
    direction = (direction - 1) & 3 if pos in black else (direction + 1) & 3
    return add(pos, DIRS[direction]), direction


def frozen_cycle(black: set[Point], start: DirectedState) -> tuple[DirectedState, ...]:
    """Trace one finite cycle of rho_B, rooted at ``start``."""
    cycle: list[DirectedState] = []
    state = start
    while True:
        cycle.append(state)
        state = frozen_successor(black, state)
        if state == start:
            return tuple(cycle)
        if len(cycle) > 4 + 8 * len(black):
            # A finite black perturbation is a finite collection of successor
            # swaps of 4-cycles.  This generous guard catches coding errors.
            raise AssertionError("frozen cycle exceeded the finite-surgery bound")


def is_pristine_cycle(cycle: Sequence[DirectedState]) -> bool:
    """Whether ``cycle`` is exactly an untouched all-white four-cycle."""
    if len(cycle) != 4:
        return False
    states = set(cycle)
    empty: set[Point] = set()
    return all(frozen_successor(empty, state) in states for state in states)


def loop_surgery_diagnostics(
    black: Iterable[Point], steps: int, checkpoints: Iterable[int] = ()
) -> dict[str, object]:
    """Brute-force exact active-loop and reabsorption-age diagnostics.

    This deliberately retraces the relevant frozen cycles at every step.  It
    is intended as an auditable diagnostic, not as the fastest long-run data
    structure.  Timestamps are attached to non-pristine inactive daughters
    at the toggle event that sheds them.
    """
    ant = Ant(set(black))
    inactive_birth: dict[frozenset[DirectedState], tuple[int, bool]] = {}
    checkpoint_set = set(checkpoints)
    snapshots: list[dict[str, int]] = []
    max_active = 0
    max_nonpristine_delay = 0
    max_any_partner_age = 0
    ancestral_intakes: list[int] = []
    splits = merges = 0

    def snapshot(t: int) -> None:
        snapshots.append(
            {
                "steps": t,
                "max_active_loop": max_active,
                "max_nonpristine_reabsorption_delay": max_nonpristine_delay,
                "max_tracked_partner_age": max_any_partner_age,
            }
        )

    for t in range(steps):
        a = (ant.pos, ant.direction)
        opposite = (ant.pos, (ant.direction + 2) & 3)
        active = frozen_cycle(ant.black, a)
        partner = frozen_cycle(ant.black, opposite)
        max_active = max(max_active, len(active))
        same_cycle = frozenset(active) == frozenset(partner)
        old_partner_key = frozenset(partner)
        actual_next = frozen_successor(ant.black, a)

        if same_cycle:
            splits += 1
        else:
            merges += 1
            birth_record = inactive_birth.pop(old_partner_key, None)
            if birth_record is not None:
                birth, was_nonpristine = birth_record
                delay = t - birth
                if was_nonpristine:
                    max_nonpristine_delay = max(max_nonpristine_delay, delay)
                max_any_partner_age = max(max_any_partner_age, delay)
            elif not is_pristine_cycle(partner):
                ancestral_intakes.append(t)

        ant.step()
        assert (ant.pos, ant.direction) == actual_next

        if same_cycle:
            # After the successor swap, the OLD active state lies on the
            # inactive daughter; actual_next lies on the new active daughter.
            shed = frozen_cycle(ant.black, a)
            new_active = frozen_cycle(ant.black, actual_next)
            assert frozenset(shed).isdisjoint(new_active)
            assert len(shed) + len(new_active) == len(active)
            nonpristine = not is_pristine_cycle(shed)
            inactive_birth[frozenset(shed)] = (t, nonpristine)
        else:
            new_active = frozen_cycle(ant.black, actual_next)
            assert len(new_active) == len(active) + len(partner)
        max_active = max(max_active, len(new_active))

        if t + 1 in checkpoint_set:
            snapshot(t + 1)

    if steps not in checkpoint_set:
        snapshot(steps)
    return {
        "steps": steps,
        "max_active_loop": max_active,
        "max_nonpristine_reabsorption_delay": max_nonpristine_delay,
        "max_tracked_partner_age": max_any_partner_age,
        "splits": splits,
        "merges": merges,
        "ancestral_nonpristine_intakes": ancestral_intakes,
        "currently_tracked_inactive_loops": len(inactive_birth),
        "currently_tracked_nonpristine_loops": sum(
            nonpristine for _, nonpristine in inactive_birth.values()
        ),
        "checkpoints": snapshots,
    }


def invariant_audit(samples: int, sample_steps: int, seed: int) -> dict[str, object]:
    """Run deterministic regression checks for the new exact invariants."""
    rng = random.Random(seed)
    for _ in range(samples):
        black = {
            (x, y)
            for x in range(-3, 4)
            for y in range(-3, 4)
            if rng.randrange(4) == 0
        }
        ant = Ant(black)
        initial_count = len(black)
        initial_direction = ant.direction
        parity_charge = parity_charge_profiles(ant.black, ant.pos, ant.direction)
        mod4_charge = mod4_moment_charge(ant.black, ant.pos, ant.direction)
        mod4_rotated_charge = mod4_rotated_moment_charge(
            ant.black, ant.pos, ant.direction
        )
        mod4_quadratic = mod4_quadratic_charge(
            ant.black, ant.pos, ant.direction
        )
        turns: list[int] = []
        for _ in range(sample_steps):
            turns.append(ant.step())
            assert (
                parity_charge_profiles(ant.black, ant.pos, ant.direction)
                == parity_charge
            )
            assert (
                mod4_moment_charge(ant.black, ant.pos, ant.direction)
                == mod4_charge
            )
            assert (
                mod4_rotated_moment_charge(ant.black, ant.pos, ant.direction)
                == mod4_rotated_charge
            )
            assert (
                mod4_quadratic_charge(ant.black, ant.pos, ant.direction)
                == mod4_quadratic
            )
            assert (ant.direction - len(ant.black)) & 3 == (
                initial_direction - initial_count
            ) & 3
        counts, positions, directions = predicted_path_from_black_count(
            turns, initial_count, initial_direction=initial_direction
        )
        assert counts[-1] == len(ant.black)
        assert positions[-1] == ant.pos
        assert directions[-1] == ant.direction

    abstract_word = "RRRRRLLLRLLRLLRL"
    abstract_turns = tuple(0 if symbol == "R" else 1 for symbol in abstract_word)
    counts, positions, _ = predicted_path_from_black_count(abstract_turns, 0)
    abstract_moment = clean_translator_moment_sum(counts)
    repeated_origin_phases = [i for i, point in enumerate(positions[:-1]) if point == (0, 0)]

    witness_specs: list[tuple[str, set[Point], Point, int]] = [
        ("+v1", set(), (-1, -1), 0),
        ("-v1", {(-1, -1)}, (-1, -1), 0),
        ("+v2", {(-1, -1)}, (-1, 0), 1),
        ("-v2", {(-1, 0), (-1, -1)}, (-1, -1), 0),
        ("+v3", {(-1, 0), (0, -1), (-1, -1)}, (0, 0), 0),
        ("-v3", {(-1, 0), (0, -1), (-1, -1), (0, 0)}, (-1, -1), 0),
        ("+v4", {(-1, 1), (-1, -1)}, (-1, 0), 1),
        ("-v4", {(-1, 0), (-1, 1), (-1, -1)}, (-1, 0), 1),
    ]
    witnesses: list[dict[str, object]] = []
    keys = ("edges", "vertices", "components", "cycle_rank")
    for name, black, pos, direction in witness_specs:
        ant = Ant(set(black), pos, direction)
        before = tait_graph_stats(ant.black)
        turn = ant.step()
        after = tait_graph_stats(ant.black)
        witnesses.append(
            {
                "name": name,
                "initial_black": sorted(black),
                "initial_position": pos,
                "initial_direction": direction,
                "turn": "L" if turn else "R",
                "delta_E_V_k_beta": [after[key] - before[key] for key in keys],
            }
        )

    return {
        "random_seed": seed,
        "random_states": samples,
        "steps_per_state": sample_steps,
        "checked": [
            "heading_minus_black_count_mod_4",
            "black_count_path_reconstruction",
            "column_and_row_F2_charges",
            "mod4_moment_charge",
            "mod4_rotated_moment_charge",
            "mod4_quadratic_charge",
        ],
        "all_random_checks_passed": True,
        "moment_sharpness_example": {
            "word": abstract_word,
            "counts": counts,
            "moment_sum": abstract_moment,
            "drift": positions[-1],
            "origin_visit_phases": repeated_origin_phases,
            "why_not_color_realizable": (
                "phases 0 and 4 both request R at the origin, violating alternation"
            ),
        },
        "affine_Tait_delta_witnesses": witnesses,
    }


@dataclass
class Ant:
    black: set[Point]
    pos: Point = (0, 0)
    direction: int = 0
    step_count: int = 0

    def clone(self) -> "Ant":
        return Ant(set(self.black), self.pos, self.direction, self.step_count)

    def step(self) -> int:
        """Execute one step and return 1 for L (black), 0 for R (white)."""
        p = self.pos
        if p in self.black:
            turn = 1
            self.direction = (self.direction - 1) & 3
            self.black.remove(p)
        else:
            turn = 0
            self.direction = (self.direction + 1) & 3
            self.black.add(p)
        self.pos = add(p, DIRS[self.direction])
        self.step_count += 1
        return turn


@dataclass(frozen=True)
class GatewayCertificate:
    """One phase of a translational highway, expressed relative to the ant.

    ``visited`` is Q, the set of cells read/flipped during one period.
    ``template_black`` gives the colors on Q at the start of the period.
    ``leading`` is (Q + drift) \\ Q.  Its forward translates must be white.
    """

    period: int
    drift: Point
    direction: int
    trace: tuple[int, ...]
    visited: frozenset[Point]
    template_black: frozenset[Point]
    leading: frozenset[Point]

    def rotated(self, quarter_turns: int) -> "GatewayCertificate":
        q = quarter_turns % 4
        return GatewayCertificate(
            self.period,
            rotate_point(self.drift, q),
            (self.direction + q) & 3,
            self.trace,
            frozenset(rotate_point(p, q) for p in self.visited),
            frozenset(rotate_point(p, q) for p in self.template_black),
            frozenset(rotate_point(p, q) for p in self.leading),
        )

    def verify_algebraically(self) -> None:
        """Verify the finite induction step defining this certificate."""
        # Start with the template on Q and white everywhere else.
        ant = Ant(set(self.template_black), (0, 0), self.direction)
        touched: set[Point] = set()
        trace: list[int] = []
        for _ in range(self.period):
            touched.add(ant.pos)
            trace.append(ant.step())
        assert tuple(trace) == self.trace
        assert frozenset(touched) == self.visited
        assert ant.pos == self.drift
        assert ant.direction == self.direction

        # At the new ant position, Q+drift must carry the translated template.
        for q in self.visited:
            absolute = add(q, self.drift)
            actual = absolute in ant.black
            expected = q in self.template_black
            assert actual == expected, (q, absolute, actual, expected)

        # A leading cell cannot secretly be an older-period footprint.
        # Because Q is finite, only finitely many negative translates can meet it.
        max_span = max(
            (abs(x) + abs(y) for x, y in self.visited), default=0
        )
        max_k = max_span + 4
        for a in self.leading:
            for k in range(1, max_k + 1):
                # The older footprints are Q-drift, Q-2*drift, ... .  Thus
                # a belongs to an older footprint iff a+k*drift belongs to Q.
                assert add(a, mul(k, self.drift)) not in self.visited, (a, k)

    def matches(self, ant: Ant) -> bool:
        """Return True only when this certificate proves an infinite highway."""
        if ant.direction != self.direction:
            return False
        origin = ant.pos
        for q in self.visited:
            if (add(origin, q) in ant.black) != (q in self.template_black):
                return False

        # The complete semi-infinite leading corridor must currently be white.
        # At every finite time the black support is finite, so it is enough to
        # intersect this finite set with the semilinear corridor exactly.
        bad = ant.black
        dx, dy = self.drift
        for b in bad:
            rel_b = sub(b, origin)
            for a in self.leading:
                rx, ry = sub(rel_b, a)
                if dx == 0:
                    if rx == 0 and dy and ry % dy == 0 and ry // dy >= 0:
                        return False
                elif dy == 0:
                    if ry == 0 and rx % dx == 0 and rx // dx >= 0:
                        return False
                elif rx % dx == 0 and ry % dy == 0:
                    kx, ky = rx // dx, ry // dy
                    if kx == ky and kx >= 0:
                        return False
        return True


def build_gateway_certificates(blank_start: int | None = None) -> list[GatewayCertificate]:
    """Build and verify one gateway phase in all four rotations.

    Not every temporal phase has an all-white leading set: halfway through a
    period, some memory cells from the preceding prefix are needed.  Checking
    this one phase is sufficient because an established highway returns to it
    every 104 steps.
    """
    if blank_start is None:
        blank_start, _, _ = find_blank_highway_start()
    result: list[GatewayCertificate] = []
    cert = derive_gateway_certificate(blank_start)
    for q in range(4):
        rotated = cert.rotated(q)
        rotated.verify_algebraically()
        result.append(rotated)
    return result


def simulate_trace(initial_black: Iterable[Point], steps: int) -> tuple[Ant, list[int], list[Point]]:
    ant = Ant(set(initial_black))
    trace: list[int] = []
    positions: list[Point] = [ant.pos]
    for _ in range(steps):
        trace.append(ant.step())
        positions.append(ant.pos)
    return ant, trace, positions


def find_blank_highway_start(
    total_steps: int = 20_000, repeats: int = 20
) -> tuple[int, tuple[int, ...], Point]:
    _, trace, positions = simulate_trace((), total_steps)
    needed = PERIOD * repeats
    for start in range(total_steps - needed + 1):
        word = trace[start : start + PERIOD]
        if all(
            trace[start + k * PERIOD : start + (k + 1) * PERIOD] == word
            for k in range(1, repeats)
        ):
            drift = sub(positions[start + PERIOD], positions[start])
            if drift != (0, 0) and all(
                sub(
                    positions[start + (k + 1) * PERIOD],
                    positions[start + k * PERIOD],
                )
                == drift
                for k in range(repeats)
            ):
                return start, tuple(word), drift
    raise RuntimeError("No stable period-104 trace found")


def state_at_blank_time(step: int) -> Ant:
    ant = Ant(set())
    for _ in range(step):
        ant.step()
    return ant


def derive_gateway_certificate(start: int) -> GatewayCertificate:
    ant = state_at_blank_time(start)
    origin = ant.pos
    direction = ant.direction
    template_source = set(ant.black)
    touched_absolute: set[Point] = set()
    trace: list[int] = []
    for _ in range(PERIOD):
        touched_absolute.add(ant.pos)
        trace.append(ant.step())
    drift = sub(ant.pos, origin)
    if ant.direction != direction:
        raise AssertionError("direction does not recur")
    visited = frozenset(sub(p, origin) for p in touched_absolute)
    template_black = frozenset(
        q for q in visited if add(origin, q) in template_source
    )
    shifted_q = frozenset(add(q, drift) for q in visited)
    leading = frozenset(p for p in shifted_q if p not in visited)
    cert = GatewayCertificate(
        PERIOD,
        drift,
        direction,
        tuple(trace),
        visited,
        template_black,
        leading,
    )
    cert.verify_algebraically()
    return cert


def heuristic_highway_time(
    initial_black: set[Point], max_steps: int, repeats: int = 3
) -> tuple[int | None, Ant, int, int]:
    """Search fitness: repeated trace/displacement, not an infinite certificate."""
    ant = Ant(set(initial_black))
    turns: deque[int] = deque(maxlen=PERIOD * repeats)
    positions: deque[Point] = deque([ant.pos], maxlen=PERIOD * repeats + 1)
    min_x = max_x = min_y = max_y = 0
    for step in range(max_steps):
        turns.append(ant.step())
        positions.append(ant.pos)
        x, y = ant.pos
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)
        if len(turns) == PERIOD * repeats:
            seq = tuple(turns)
            word = seq[:PERIOD]
            if all(seq[k * PERIOD : (k + 1) * PERIOD] == word for k in range(1, repeats)):
                ps = list(positions)
                drifts = [
                    sub(ps[(k + 1) * PERIOD], ps[k * PERIOD])
                    for k in range(repeats)
                ]
                if drifts[0] != (0, 0) and all(d == drifts[0] for d in drifts[1:]):
                    onset = step + 1 - PERIOD * repeats
                    area = (max_x - min_x + 1) * (max_y - min_y + 1)
                    return onset, ant, len(ant.black), area
    area = (max_x - min_x + 1) * (max_y - min_y + 1)
    return None, ant, len(ant.black), area


def exact_highway_certificate_time(
    initial_black: set[Point],
    max_steps: int,
    certificates: Sequence[GatewayCertificate],
    repeats: int = 3,
) -> tuple[int | None, int | None]:
    """Return a time and certificate index that prove infinite highway motion."""
    by_key: dict[tuple[int, tuple[int, ...]], list[tuple[int, GatewayCertificate]]] = {}
    for i, cert in enumerate(certificates):
        by_key.setdefault((cert.direction, cert.trace), []).append((i, cert))

    ant = Ant(set(initial_black))
    turns: deque[int] = deque(maxlen=PERIOD * repeats)
    positions: deque[Point] = deque([ant.pos], maxlen=PERIOD * repeats + 1)
    for step in range(max_steps):
        turns.append(ant.step())
        positions.append(ant.pos)
        if len(turns) != PERIOD * repeats:
            continue
        seq = tuple(turns)
        word = seq[:PERIOD]
        if not all(seq[k * PERIOD : (k + 1) * PERIOD] == word for k in range(1, repeats)):
            continue
        ps = list(positions)
        drifts = [
            sub(ps[(k + 1) * PERIOD], ps[k * PERIOD])
            for k in range(repeats)
        ]
        if drifts[0] == (0, 0) or not all(d == drifts[0] for d in drifts[1:]):
            continue

        # At the end of complete periods the future word is the same word.
        for cert_index, cert in by_key.get((ant.direction, word), ()):
            if cert.drift == drifts[0] and cert.matches(ant):
                return step + 1, cert_index
    return None, None


def points_from_bits(bits: int, side: int) -> set[Point]:
    offset = side // 2
    result: set[Point] = set()
    for i in range(side * side):
        if bits >> i & 1:
            result.add((i % side - offset, i // side - offset))
    return result


def bits_as_rows(bits: int, side: int) -> list[str]:
    return [
        "".join("#" if bits >> (y * side + x) & 1 else "." for x in range(side))
        for y in range(side - 1, -1, -1)
    ]


def exhaustive(
    side: int,
    max_steps: int,
    exact: bool = False,
    start_bits: int = 0,
    stop_bits: int | None = None,
) -> dict[str, object]:
    total = 1 << (side * side)
    if stop_bits is None:
        stop_bits = total
    if not 0 <= start_bits <= stop_bits <= total:
        raise ValueError("require 0 <= start <= stop <= 2^(side^2)")
    best_time = -1
    best_bits = 0
    unresolved: list[int] = []
    histogram: dict[int, int] = {}
    certificates = build_gateway_certificates() if exact else ()
    started = time.time()
    for bits in range(start_bits, stop_bits):
        points = points_from_bits(bits, side)
        if exact:
            detection, _ = exact_highway_certificate_time(points, max_steps, certificates)
        else:
            detection, _, _, _ = heuristic_highway_time(points, max_steps)
        if detection is None:
            unresolved.append(bits)
            score = max_steps
        else:
            score = detection
            bucket = detection // 1000
            histogram[bucket] = histogram.get(bucket, 0) + 1
        if score > best_time:
            best_time, best_bits = score, bits
    return {
        "side": side,
        "total": total,
        "range_start": start_bits,
        "range_stop": stop_bits,
        "range_count": stop_bits - start_bits,
        "max_steps": max_steps,
        "best_time_or_cap": best_time,
        "best_bits": best_bits,
        "best_rows": bits_as_rows(best_bits, side),
        "unresolved_count": len(unresolved),
        "unresolved_bits": unresolved[:100],
        "histogram_thousands": histogram,
        "seconds": time.time() - started,
        "detector": (
            "exact finite gateway plus all-white semi-infinite corridor certificate"
            if exact
            else "heuristic: 3 repeated period-104 traces and equal nonzero drift"
        ),
    }


def evolutionary_search(
    side: int,
    max_steps: int,
    population: int,
    generations: int,
    seed: int,
) -> dict[str, object]:
    rng = random.Random(seed)
    width = side * side
    mask = (1 << width) - 1
    cache: dict[int, tuple[int, int, int]] = {}

    def evaluate(bits: int) -> tuple[int, int, int]:
        if bits not in cache:
            onset, _, black_count, area = heuristic_highway_time(
                points_from_bits(bits, side), max_steps
            )
            cache[bits] = (
                max_steps if onset is None else onset,
                area,
                black_count,
            )
        return cache[bits]

    pop = [rng.getrandbits(width) for _ in range(population)]
    best_bits = pop[0]
    best_score = evaluate(best_bits)
    started = time.time()
    history: list[dict[str, int]] = []
    elite_count = max(2, population // 5)
    for generation in range(generations):
        ranked = sorted(pop, key=evaluate, reverse=True)
        if evaluate(ranked[0]) > best_score:
            best_bits, best_score = ranked[0], evaluate(ranked[0])
        history.append(
            {
                "generation": generation,
                "onset_or_cap": best_score[0],
                "area": best_score[1],
                "black_at_end": best_score[2],
            }
        )
        elites = ranked[:elite_count]
        next_pop = list(elites)
        while len(next_pop) < population:
            parent = rng.choice(elites)
            flips = 1 + int(rng.random() ** 3 * max(2, side))
            child = parent
            for _ in range(flips):
                child ^= 1 << rng.randrange(width)
            if rng.random() < 0.08:
                child ^= rng.getrandbits(width) & mask
            next_pop.append(child)
        pop = next_pop
    onset, _, black_count, area = heuristic_highway_time(
        points_from_bits(best_bits, side), max_steps
    )
    return {
        "side": side,
        "max_steps": max_steps,
        "population": population,
        "generations": generations,
        "seed": seed,
        "evaluated": len(cache),
        "best_onset": onset,
        "best_reached_cap": onset is None,
        "best_bits": best_bits,
        "best_rows": bits_as_rows(best_bits, side),
        "best_area": area,
        "best_black_at_end": black_count,
        "history": history,
        "seconds": time.time() - started,
        "detector": "heuristic: 3 repeated period-104 traces and equal nonzero drift",
    }


def certificate_to_json(cert: GatewayCertificate) -> dict[str, object]:
    return {
        "period": cert.period,
        "drift": cert.drift,
        "direction": cert.direction,
        "trace": "".join("L" if t else "R" for t in cert.trace),
        "visited": sorted(cert.visited),
        "template_black": sorted(cert.template_black),
        "leading": sorted(cert.leading),
    }


def certificate_from_trace(trace: Sequence[int]) -> GatewayCertificate | None:
    """Construct a finite-white-background gateway certificate from a trace.

    This is an exact counterexample search primitive: if it returns a
    certificate whose period is not 104, that finite template produces a
    different highway and disproves the usual unique-highway formulation.
    """
    pos = (0, 0)
    direction = 0
    visits: dict[Point, list[int]] = {}
    ordered_cells: list[Point] = []
    for turn in trace:
        ordered_cells.append(pos)
        history = visits.setdefault(pos, [])
        if history and history[-1] == turn:
            return None
        history.append(turn)
        direction = (direction - 1) & 3 if turn else (direction + 1) & 3
        pos = add(pos, DIRS[direction])
    if direction != 0 or pos == (0, 0):
        return None

    visited = frozenset(ordered_cells)
    template_black = frozenset(p for p, history in visits.items() if history[0] == 1)
    drift = pos
    shifted_q = frozenset(add(q, drift) for q in visited)
    leading = frozenset(p for p in shifted_q if p not in visited)
    cert = GatewayCertificate(
        len(trace),
        drift,
        0,
        tuple(trace),
        visited,
        template_black,
        leading,
    )
    try:
        cert.verify_algebraically()
    except AssertionError:
        return None
    return cert


def integer_multiple(vector: Point, step: Point) -> int | None:
    """Return k when vector == k*step, otherwise None."""
    x, y = vector
    dx, dy = step
    if dx == 0:
        if x != 0 or dy == 0 or y % dy:
            return None
        return y // dy
    if dy == 0:
        if y != 0 or x % dx:
            return None
        return x // dx
    if x % dx or y % dy:
        return None
    kx, ky = x // dx, y // dy
    return kx if kx == ky else None


def quotient_representative_level(point: Point, drift: Point) -> tuple[Point, int]:
    """Canonicalize ``point`` modulo the subgroup generated by ``drift``.

    Returns the unique pair ``(representative, level)`` selected by reducing
    the first nonzero drift coordinate into its least nonnegative residue,
    with ``point == representative + level*drift``.
    """
    x, y = point
    dx, dy = drift
    if dx:
        reduced_x = x % abs(dx)
        level = (x - reduced_x) // dx
    else:
        assert dy
        reduced_y = y % abs(dy)
        level = (y - reduced_y) // dy
    return sub(point, mul(level, drift)), level


def finite_seed_for_periodic_trace(
    trace: Sequence[int],
) -> tuple[set[Point], Point] | None:
    """Decide exactly whether ``trace**omega`` works from finite black support.

    Let p_i be the cell visited at phase i and d the displacement of a full
    period.  Occurrences p_i+k*d and p_j+l*d concern the same physical cell
    precisely when p_i-p_j=(l-k)d.  Grouping phases modulo translations by d
    therefore gives, for every physical cell, its complete chronological turn
    sequence.  Such a sequence is legal iff its turns alternate.  All but
    finitely many newly encountered cells are initially white, so the first
    turn in every stabilized group must be R.  The finitely many boundary
    groups whose first turn is L give the required finite black seed.
    """
    pos = (0, 0)
    direction = 0
    positions: list[Point] = []
    for turn in trace:
        positions.append(pos)
        direction = (direction - 1) & 3 if turn else (direction + 1) & 3
        pos = add(pos, DIRS[direction])
    drift = pos
    if direction != 0 or drift == (0, 0):
        return None

    # Each group is representative -> [(level, phase, turn), ...].
    groups: dict[Point, list[tuple[int, int, int]]] = {}
    for phase, (p, turn) in enumerate(zip(positions, trace)):
        representative, level = quotient_representative_level(p, drift)
        groups.setdefault(representative, []).append((level, phase, turn))

    initial_black: set[Point] = set()
    for representative, entries in groups.items():
        # At a sufficiently advanced physical level, occurrences are ordered
        # first by decreasing translation level and then by increasing phase.
        # Every boundary sequence is a suffix of this stabilized sequence:
        # moving the boundary merely removes whole high-level blocks.  Thus
        # alternation of this one sequence proves alternation at every level.
        stable = sorted(entries, key=lambda item: (-item[0], item[1]))
        turns = [turn for _, _, turn in stable]
        if turns[0] != 0:  # Stable fresh cells must start white/R.
            return None
        if any(a == b for a, b in zip(turns, turns[1:])):
            return None

        # Before stabilization, a cell's first turn is the first phase in the
        # greatest translation-level block that has reached it.  Only the
        # finite gaps between the observed levels can require initial black.
        first_turn_at_level: dict[int, int] = {}
        for level, phase, turn in sorted(entries, key=lambda item: item[1]):
            first_turn_at_level.setdefault(level, turn)
        levels = sorted(first_turn_at_level)
        max_level = levels[-1]
        for index, level in enumerate(levels[:-1]):
            next_level = levels[index + 1]
            if first_turn_at_level[level] == 1:
                for physical_level in range(level, next_level):
                    initial_black.add(
                        add(representative, mul(physical_level, drift))
                    )

    return initial_black, drift


def periodic_trace_structure(trace: Sequence[int]) -> dict[str, object]:
    """Return exact translation classes, growth strands, and toggle margins."""
    pos = (0, 0)
    direction = 0
    positions: list[Point] = []
    signed_toggle: dict[Point, int] = {}
    for turn in trace:
        positions.append(pos)
        signed_toggle[pos] = signed_toggle.get(pos, 0) + (1 if turn == 0 else -1)
        direction = (direction - 1) & 3 if turn else (direction + 1) & 3
        pos = add(pos, DIRS[direction])
    drift = pos
    growth = sum(1 if turn == 0 else -1 for turn in trace)
    nonzero_toggle = {point: value for point, value in signed_toggle.items() if value}

    result: dict[str, object] = {
        "period": len(trace),
        "heading_reset": direction == 0,
        "drift": drift,
        "growth_R_minus_L": growth,
        "signed_toggle_support_size": len(nonzero_toggle),
        "signed_toggle_pattern": [
            {"point": point, "change": value}
            for point, value in sorted(nonzero_toggle.items())
        ],
    }
    if drift == (0, 0):
        result.update(
            {
                "translation_classes": [],
                "class_count": 0,
                "growing_strands": 0,
                "finite_seed_valid": False,
            }
        )
        return result

    groups: dict[Point, list[tuple[int, int, int]]] = {}
    for phase, (point, turn) in enumerate(zip(positions, trace)):
        representative, level = quotient_representative_level(point, drift)
        groups.setdefault(representative, []).append((level, phase, turn))

    classes: list[dict[str, object]] = []
    for representative, entries in sorted(groups.items()):
        stable = sorted(entries, key=lambda item: (-item[0], item[1]))
        turns = tuple(turn for _, _, turn in stable)
        class_growth = sum(1 if turn == 0 else -1 for turn in turns)
        classes.append(
            {
                "representative": representative,
                "occurrences": len(entries),
                "levels_and_phases": [
                    {"level": level, "phase": phase, "turn": "L" if turn else "R"}
                    for level, phase, turn in stable
                ],
                "stable_word": "".join("L" if turn else "R" for turn in turns),
                "alternating": all(a != b for a, b in zip(turns, turns[1:])),
                "begins_R": bool(turns) and turns[0] == 0,
                "growth": class_growth,
            }
        )

    odd_columns: set[int] = set()
    odd_rows: set[int] = set()
    toggle_groups: dict[Point, list[tuple[int, Point, int]]] = {}
    for (x, y), value in nonzero_toggle.items():
        if value & 1:
            odd_columns.symmetric_difference_update((x,))
            odd_rows.symmetric_difference_update((y,))
        representative, level = quotient_representative_level((x, y), drift)
        toggle_groups.setdefault(representative, []).append((level, (x, y), value))

    toggle_orbits = [
        {
            "representative": representative,
            "sum": sum(value for _, _, value in entries),
            "entries": [
                {"level": level, "point": point, "change": value}
                for level, point, value in sorted(entries)
            ],
        }
        for representative, entries in sorted(toggle_groups.items())
    ]

    canonical_widget: set[Point] = set()
    strand_bases: set[Point] = set()
    canonical_valid = True
    for representative, entries in sorted(toggle_groups.items()):
        changes = {level: value for level, _, value in entries}
        low, high = min(changes), max(changes)
        total_change = sum(changes.values())
        if total_change not in (0, 1):
            canonical_valid = False
            break
        base_level: int | None = None
        if total_change == 1:
            base_level = min(level for level, value in changes.items() if value)
            if changes[base_level] != 1:
                canonical_valid = False
                break
            strand_bases.add(add(representative, mul(base_level, drift)))
        prefix = 0
        for level in range(low, high + 1):
            prefix += changes.get(level, 0)
            if total_change == 1:
                if prefix not in (0, 1):
                    canonical_valid = False
                    break
                assert base_level is not None
                widget_value = int(level >= base_level) - prefix
            else:
                if prefix not in (-1, 0):
                    canonical_valid = False
                    break
                widget_value = -prefix
            if widget_value == 1:
                canonical_widget.add(add(representative, mul(level, drift)))
            elif widget_value != 0:
                canonical_valid = False
                break
        if not canonical_valid:
            break

    if canonical_valid:
        reconstructed: dict[Point, int] = {}
        for point in strand_bases:
            reconstructed[point] = reconstructed.get(point, 0) + 1
        for point in canonical_widget:
            shifted = add(point, drift)
            reconstructed[shifted] = reconstructed.get(shifted, 0) + 1
            reconstructed[point] = reconstructed.get(point, 0) - 1
        reconstructed = {point: value for point, value in reconstructed.items() if value}
        canonical_valid = reconstructed == nonzero_toggle

    certificate = finite_seed_for_periodic_trace(trace)
    stationary_correction: list[dict[str, object]] | None = None
    if certificate is not None and canonical_valid:
        seed = certificate[0]
        correction: dict[Point, int] = {point: 1 for point in seed}
        for point in canonical_widget:
            correction[point] = correction.get(point, 0) - 1
        stationary_correction = [
            {"point": point, "coefficient": value}
            for point, value in sorted(correction.items())
            if value
        ]
    result.update(
        {
            "class_count": len(classes),
            "translation_classes": classes,
            "growing_strands": sum(item["growth"] for item in classes),
            "signed_toggle_orbit_count": len(toggle_orbits),
            "signed_toggle_orbits": toggle_orbits,
            "growing_toggle_orbits": sum(item["sum"] == 1 for item in toggle_orbits),
            "zero_sum_toggle_orbits": sum(item["sum"] == 0 for item in toggle_orbits),
            "canonical_decomposition_valid": canonical_valid,
            "canonical_strand_bases": sorted(strand_bases) if canonical_valid else None,
            "canonical_moving_widget": sorted(canonical_widget) if canonical_valid else None,
            "canonical_stationary_correction": stationary_correction,
            "odd_toggle_columns_mod2": sorted(odd_columns),
            "odd_toggle_rows_mod2": sorted(odd_rows),
            "finite_seed_valid": certificate is not None,
            "finite_black_seed": sorted(certificate[0]) if certificate else None,
        }
    )
    return result


def periodic_trace_violation_score(
    trace: Sequence[int],
) -> tuple[int, Point, int]:
    """Score a candidate period; zero is exactly a finite-seed highway.

    The score counts a wrong first turn and nonalternating adjacent turns in
    each stabilized translation class.  Candidates whose heading does not
    reset, or whose drift is zero, receive an additional structural penalty.
    The third return value is the number of translation classes.  This is a
    heuristic objective for searching; ``finite_seed_for_periodic_trace`` is
    still used to certify every zero-score result.
    """
    pos = (0, 0)
    direction = 0
    positions: list[Point] = []
    for turn in trace:
        positions.append(pos)
        direction = (direction - 1) & 3 if turn else (direction + 1) & 3
        pos = add(pos, DIRS[direction])
    drift = pos
    if drift == (0, 0):
        return len(trace) + (direction != 0), drift, 0

    groups: dict[Point, list[tuple[int, int, int]]] = {}
    for phase, (p, turn) in enumerate(zip(positions, trace)):
        representative, level = quotient_representative_level(p, drift)
        groups.setdefault(representative, []).append((level, phase, turn))

    score = len(trace) if direction != 0 else 0
    for entries in groups.values():
        stable = sorted(entries, key=lambda item: (-item[0], item[1]))
        turns = [turn for _, _, turn in stable]
        score += turns[0] != 0
        score += sum(a == b for a, b in zip(turns, turns[1:]))
    return score, drift, len(groups)


def search_highway_words(
    max_period: int,
    node_cap: int,
    prefix_text: str = "",
    exact_period: bool = False,
    target_growth: int | None = None,
    proved_clean_pruning: bool = False,
) -> dict[str, object]:
    """Depth-first exact search for finite-seed periodic words.

    ``exact_period`` restricts certificates to depth ``max_period``.
    ``target_growth`` restricts #R-#L and, in exact-period mode, permits an
    exact remaining-balance prune.  Neither option weakens the final
    finite-seed certificate check.

    ``proved_clean_pruning`` is an opt-in theorem-based optimization for the
    exact zero-growth case.  It uses the proved facts that the drift is an
    axis multiple of four, N >= 8*|d|, every translation class is even, and
    a cyclic phase may be chosen at a minimum of the black-count walk so
    that every relative prefix balance is nonnegative.
    """
    if proved_clean_pruning and not (exact_period and target_growth == 0):
        raise ValueError(
            "proved clean pruning requires --exact-period and --growth 0"
        )
    found: dict[tuple[int, Point, tuple[int, ...]], tuple[set[Point], Point, tuple[int, ...]]] = {}
    nodes = 0
    capped = False
    trace: list[int] = []
    last_at_cell: dict[Point, int] = {}
    clean_drifts: list[Point] = []
    odd_clean_classes: list[set[Point]] = []
    if proved_clean_pruning:
        for distance in range(4, max_period // 8 + 1, 4):
            clean_drifts.extend(
                ((distance, 0), (-distance, 0), (0, distance), (0, -distance))
            )
        odd_clean_classes = [set() for _ in clean_drifts]

    def toggle_clean_phase(point: Point) -> None:
        for drift, odd in zip(clean_drifts, odd_clean_classes):
            representative, _ = quotient_representative_level(point, drift)
            if representative in odd:
                odd.remove(representative)
            else:
                odd.add(representative)

    def dfs(pos: Point, direction: int, depth: int, growth: int) -> None:
        nonlocal nodes, capped
        if capped:
            return
        nodes += 1
        if nodes >= node_cap:
            capped = True
            return

        remaining = max_period - depth
        if proved_clean_pruning and growth < 0:
            return
        if exact_period and target_growth is not None:
            needed = target_growth - growth
            if abs(needed) > remaining or (remaining - needed) & 1:
                return

        if proved_clean_pruning:
            possible = False
            for drift, odd in zip(clean_drifts, odd_clean_classes):
                distance = abs(drift[0] - pos[0]) + abs(drift[1] - pos[1])
                if distance > remaining or (remaining - distance) & 1:
                    continue
                odd_count = len(odd)
                if odd_count > remaining or (remaining - odd_count) & 1:
                    continue
                possible = True
                break
            if not possible:
                return

        right_depth = not exact_period or depth == max_period
        right_growth = target_growth is None or growth == target_growth
        if depth > 0 and right_depth and right_growth and direction == 0 and pos != (0, 0):
            seed = finite_seed_for_periodic_trace(trace)
            if seed is not None:
                initial_black, drift = seed
                word = tuple(trace)
                key = (len(word), drift, word)
                found[key] = (initial_black, drift, word)
        if depth == max_period:
            return

        previous = last_at_cell.get(pos)
        choices = (1 - previous,) if previous is not None else (0, 1)
        for turn in choices:
            trace.append(turn)
            last_at_cell[pos] = turn
            if proved_clean_pruning:
                toggle_clean_phase(pos)
            next_direction = (direction - 1) & 3 if turn else (direction + 1) & 3
            next_growth = growth + (1 if turn == 0 else -1)
            dfs(
                add(pos, DIRS[next_direction]),
                next_direction,
                depth + 1,
                next_growth,
            )
            if proved_clean_pruning:
                toggle_clean_phase(pos)
            if previous is None:
                del last_at_cell[pos]
            else:
                last_at_cell[pos] = previous
            trace.pop()

    started = time.time()
    prefix_valid = True
    pos, direction, growth = (0, 0), 0, 0
    for symbol in prefix_text.upper():
        if symbol not in "RL":
            raise ValueError("prefix must contain only R and L")
        turn = 0 if symbol == "R" else 1
        previous = last_at_cell.get(pos)
        if previous is not None and turn != 1 - previous:
            prefix_valid = False
            break
        last_at_cell[pos] = turn
        trace.append(turn)
        if proved_clean_pruning:
            toggle_clean_phase(pos)
        growth += 1 if turn == 0 else -1
        if proved_clean_pruning and growth < 0:
            prefix_valid = False
            break
        direction = (direction - 1) & 3 if turn else (direction + 1) & 3
        pos = add(pos, DIRS[direction])
    if prefix_valid and len(trace) <= max_period:
        dfs(pos, direction, len(trace), growth)
    highways = sorted(found.values(), key=lambda item: (len(item[2]), item[1], item[2]))
    return {
        "max_period": max_period,
        "exact_period": exact_period,
        "target_growth": target_growth,
        "proved_clean_pruning": proved_clean_pruning,
        "proved_clean_candidate_drifts": clean_drifts,
        "prefix": prefix_text.upper(),
        "prefix_valid": prefix_valid,
        "node_cap": node_cap,
        "nodes": nodes,
        "search_complete": not capped,
        "highways_found": len(highways),
        "highways": [
            {
                "period": len(word),
                "drift": drift,
                "trace": "".join("L" if t else "R" for t in word),
                "finite_black_seed": sorted(initial_black),
            }
            for initial_black, drift, word in highways
        ],
        "seconds": time.time() - started,
    }


def search_standard_hamming_sphere(
    distance: int, shards: int = 1, shard: int = 0
) -> dict[str, object]:
    """Exactly search one sharded Hamming sphere around the standard word."""
    if distance < 1:
        raise ValueError("distance must be positive")
    if shards < 1 or not 0 <= shard < shards:
        raise ValueError("require shards >= 1 and 0 <= shard < shards")
    _, standard, _ = find_blank_highway_start()
    best_score = len(standard) + 1
    best_edits: list[tuple[int, ...]] = []
    highways: list[dict[str, object]] = []
    evaluated = 0
    started = time.time()
    total = math.comb(len(standard), distance)
    rank_start = total * shard // shards
    rank_stop = total * (shard + 1) // shards

    def unrank_lex(n: int, k: int, rank: int) -> list[int]:
        """Return the zero-based lexicographic ``rank``-th k-combination."""
        result: list[int] = []
        lower = 0
        for position in range(k):
            remaining = k - position - 1
            for value in range(lower, n - remaining):
                block = math.comb(n - value - 1, remaining)
                if rank < block:
                    result.append(value)
                    lower = value + 1
                    break
                rank -= block
            else:
                raise AssertionError("combination rank out of range")
        return result

    def advance(combo: list[int], n: int) -> bool:
        """Advance a lexicographic combination; return false after the last."""
        k = len(combo)
        for position in range(k - 1, -1, -1):
            if combo[position] < n - k + position:
                combo[position] += 1
                for later in range(position + 1, k):
                    combo[later] = combo[later - 1] + 1
                return True
        return False

    edits = unrank_lex(len(standard), distance, rank_start) if rank_start < rank_stop else []
    for rank in range(rank_start, rank_stop):
        candidate = list(standard)
        for index in edits:
            candidate[index] ^= 1
        score, drift, classes = periodic_trace_violation_score(candidate)
        evaluated += 1
        if score < best_score:
            best_score = score
            best_edits = [tuple(edits)]
        elif score == best_score and len(best_edits) < 50:
            best_edits.append(tuple(edits))
        if score == 0:
            certificate = finite_seed_for_periodic_trace(candidate)
            assert certificate is not None
            black, exact_drift = certificate
            highways.append(
                {
                    "edits": tuple(edits),
                    "drift": exact_drift,
                    "translation_classes": classes,
                    "trace": "".join("L" if turn else "R" for turn in candidate),
                    "finite_black_seed": sorted(black),
                }
            )
        if rank + 1 < rank_stop:
            assert advance(edits, len(standard))
    return {
        "distance": distance,
        "shards": shards,
        "shard": shard,
        "total_sphere_size": total,
        "rank_start": rank_start,
        "rank_stop": rank_stop,
        "evaluated": evaluated,
        "best_score": best_score,
        "best_edits": best_edits,
        "exact_highways_found": len(highways),
        "highways": highways,
        "seconds": time.time() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_blank = sub.add_parser("blank-certificate")
    p_blank.add_argument("--output", type=Path)

    p_ex = sub.add_parser("exhaustive")
    p_ex.add_argument("--side", type=int, default=3)
    p_ex.add_argument("--max-steps", type=int, default=100_000)
    p_ex.add_argument("--exact", action="store_true")
    p_ex.add_argument("--start", type=int, default=0)
    p_ex.add_argument("--stop", type=int)
    p_ex.add_argument("--output", type=Path)

    p_search = sub.add_parser("search")
    p_search.add_argument("--side", type=int, default=9)
    p_search.add_argument("--max-steps", type=int, default=300_000)
    p_search.add_argument("--population", type=int, default=40)
    p_search.add_argument("--generations", type=int, default=30)
    p_search.add_argument("--seed", type=int, default=1)
    p_search.add_argument("--output", type=Path)

    p_words = sub.add_parser("search-highway-words")
    p_words.add_argument("--max-period", type=int, default=24)
    p_words.add_argument("--node-cap", type=int, default=10_000_000)
    p_words.add_argument("--prefix", default="")
    p_words.add_argument("--exact-period", action="store_true")
    p_words.add_argument("--growth", type=int)
    p_words.add_argument("--proved-clean-pruning", action="store_true")
    p_words.add_argument("--output", type=Path)

    p_hamming = sub.add_parser("search-standard-hamming")
    p_hamming.add_argument("--distance", type=int, required=True)
    p_hamming.add_argument("--shards", type=int, default=1)
    p_hamming.add_argument("--shard", type=int, default=0)
    p_hamming.add_argument("--output", type=Path)

    p_loops = sub.add_parser("loop-diagnostics")
    p_loops.add_argument("--steps", type=int, required=True)
    p_loops.add_argument(
        "--initial", choices=("blank", "immediate-highway"), default="blank"
    )
    p_loops.add_argument("--checkpoints", type=int, nargs="*", default=[])
    p_loops.add_argument("--output", type=Path)

    p_audit = sub.add_parser("audit-invariants")
    p_audit.add_argument("--samples", type=int, default=100)
    p_audit.add_argument("--sample-steps", type=int, default=200)
    p_audit.add_argument("--seed", type=int, default=20260714)
    p_audit.add_argument("--output", type=Path)

    p_structure = sub.add_parser("analyze-periodic-trace")
    structure_source = p_structure.add_mutually_exclusive_group(required=True)
    structure_source.add_argument("--trace")
    structure_source.add_argument("--standard", action="store_true")
    p_structure.add_argument("--output", type=Path)

    args = parser.parse_args()
    if args.command == "blank-certificate":
        start, trace, drift = find_blank_highway_start()
        cert = derive_gateway_certificate(start)
        result = {
            "blank_highway_start": start,
            "detected_drift": drift,
            "certificate": certificate_to_json(cert),
            "rotations_verified": 4,
        }
        for q in range(4):
            cert.rotated(q).verify_algebraically()
    elif args.command == "exhaustive":
        result = exhaustive(
            args.side, args.max_steps, args.exact, args.start, args.stop
        )
    elif args.command == "search":
        result = evolutionary_search(
            args.side,
            args.max_steps,
            args.population,
            args.generations,
            args.seed,
        )
    elif args.command == "search-highway-words":
        result = search_highway_words(
            args.max_period,
            args.node_cap,
            args.prefix,
            args.exact_period,
            args.growth,
            args.proved_clean_pruning,
        )
    elif args.command == "search-standard-hamming":
        result = search_standard_hamming_sphere(
            args.distance, args.shards, args.shard
        )
    elif args.command == "loop-diagnostics":
        if args.initial == "blank":
            initial_black: set[Point] = set()
        else:
            _, standard, _ = find_blank_highway_start()
            seed = finite_seed_for_periodic_trace(standard)
            assert seed is not None
            initial_black, _ = seed
        result = {
            "initial": args.initial,
            **loop_surgery_diagnostics(
                initial_black, args.steps, args.checkpoints
            ),
        }
    elif args.command == "audit-invariants":
        result = invariant_audit(args.samples, args.sample_steps, args.seed)
    else:
        if args.standard:
            _, trace, _ = find_blank_highway_start()
        else:
            if any(symbol not in "RLrl" for symbol in args.trace):
                raise ValueError("--trace must contain only R and L")
            trace = tuple(0 if symbol.upper() == "R" else 1 for symbol in args.trace)
        result = periodic_trace_structure(trace)

    payload = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
