#!/usr/bin/env python3
"""Independent adversarial checks of the mod-four residue theorem.

This deliberately reimplements the periodic trace criterion and does not call
``finite_seed_for_periodic_trace`` or ``periodic_trace_structure``.
"""

from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "outputs"))
import langton_research as lr  # noqa: E402  (used only to obtain known word)


DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def simulate(trace: tuple[int, ...]) -> tuple[list[tuple[int, int]], int, tuple[int, int]]:
    x = y = direction = 0
    positions: list[tuple[int, int]] = []
    for turn in trace:
        positions.append((x, y))
        direction = (direction + (1 if turn == 0 else -1)) & 3
        dx, dy = DIRS[direction]
        x += dx
        y += dy
    return positions, direction, (x, y)


def representative_level(
    point: tuple[int, int], drift: tuple[int, int]
) -> tuple[tuple[int, int], int]:
    x, y = point
    a, b = drift
    if a:
        reduced = x % abs(a)
        level = (x - reduced) // a
    else:
        reduced = y % abs(b)
        level = (y - reduced) // b
    return (x - level * a, y - level * b), level


def independent_p3(trace: tuple[int, ...]):
    positions, direction, drift = simulate(trace)
    if direction != 0 or drift == (0, 0):
        return None
    groups: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
    for phase, (point, turn) in enumerate(zip(positions, trace)):
        representative, level = representative_level(point, drift)
        groups.setdefault(representative, []).append((level, phase, turn))
    odd_representatives: list[tuple[int, int]] = []
    for representative, entries in groups.items():
        stable = sorted(entries, key=lambda entry: (-entry[0], entry[1]))
        turns = [entry[2] for entry in stable]
        if turns[0] != 0 or any(x == y for x, y in zip(turns, turns[1:])):
            return None
        if len(turns) & 1:
            odd_representatives.append(representative)
    return drift, odd_representatives


def residue_holds(drift: tuple[int, int], bases: list[tuple[int, int]]) -> bool:
    a, b = drift
    for axis, component in ((0, a), (1, b)):
        if component:
            modulus = abs(component)
            for residue in range(modulus):
                signed = sum(
                    1 if (x + y) % 2 == 0 else -1
                    for x, y in bases
                    if (x, y)[axis] % modulus == residue
                )
                if signed % 4 != 2:
                    return False
        else:
            coordinates = {point[axis] for point in bases}
            for coordinate in coordinates:
                signed = sum(
                    1 if (x + y) % 2 == 0 else -1
                    for x, y in bases
                    if (x, y)[axis] == coordinate
                )
                if signed % 4 != 0:
                    return False
    return True


def direct_toggle_residue_holds(trace: tuple[int, ...]) -> bool:
    """Check the charge identity directly on D, without P3 or strand bases."""

    positions, direction, drift = simulate(trace)
    if direction != 0 or drift == (0, 0):
        return False
    a, b = drift
    for axis, component in ((0, a), (1, b)):
        if component:
            modulus = abs(component)
            for residue in range(modulus):
                signed_toggle = sum(
                    (1 if turn == 0 else -1)
                    * (1 if (x + y) % 2 == 0 else -1)
                    for (x, y), turn in zip(positions, trace)
                    if (x, y)[axis] % modulus == residue
                )
                if signed_toggle % 4 != 2:
                    return False
        else:
            coordinates = {point[axis] for point in positions}
            for coordinate in coordinates:
                signed_toggle = sum(
                    (1 if turn == 0 else -1)
                    * (1 if (x + y) % 2 == 0 else -1)
                    for (x, y), turn in zip(positions, trace)
                    if (x, y)[axis] == coordinate
                )
                if signed_toggle % 4 != 0:
                    return False
    return True


def dihedral(point: tuple[int, int], code: int) -> tuple[int, int]:
    x, y = point
    if code & 4:
        x = -x
    for _ in range(code & 3):
        x, y = y, -x
    return x, y


def exhaustive_short(max_period: int) -> dict[str, object]:
    structural = 0
    valid = 0
    per_period = []
    for period in range(1, max_period + 1):
        period_structural = 0
        period_valid = 0
        for trace in itertools.product((0, 1), repeat=period):
            positions, direction, drift = simulate(trace)
            del positions
            if direction != 0 or drift == (0, 0):
                continue
            period_structural += 1
            assert direct_toggle_residue_holds(trace)
            result = independent_p3(trace)
            if result is not None:
                period_valid += 1
                assert residue_holds(*result)
        structural += period_structural
        valid += period_valid
        per_period.append(
            {
                "period": period,
                "heading_reset_nonzero_drift": period_structural,
                "p3_valid": period_valid,
            }
        )
    return {
        "max_period": max_period,
        "structural_candidates": structural,
        "p3_valid": valid,
        "per_period": per_period,
    }


def known_family_audit() -> dict[str, int]:
    _, standard_list, _ = lr.find_blank_highway_start()
    standard = tuple(standard_list)
    checked = 0
    dihedral_checks = 0
    for power in range(1, 9):
        word = standard * power
        # All distinct phases of the primitive 104-word occur among these.
        for shift in range(len(standard)):
            trace = word[shift:] + word[:shift]
            result = independent_p3(trace)
            assert result is not None
            assert direct_toggle_residue_holds(trace)
            drift, bases = result
            assert len(bases) == 12 * power
            assert residue_holds(drift, bases)
            checked += 1
            for code in range(8):
                transformed_drift = dihedral(drift, code)
                transformed_bases = [dihedral(point, code) for point in bases]
                assert residue_holds(transformed_drift, transformed_bases)
                dihedral_checks += 1

    # Random larger powers/phases stress long level orderings.
    rng = random.Random(20260714)
    for _ in range(1000):
        power = rng.randrange(1, 33)
        word = standard * power
        shift = rng.randrange(len(word))
        trace = word[shift:] + word[:shift]
        result = independent_p3(trace)
        assert result is not None
        assert direct_toggle_residue_holds(trace)
        assert residue_holds(*result)
        checked += 1
    return {"p3_words_checked": checked, "dihedral_checks": dihedral_checks}


def main() -> None:
    result = {
        "schema": "residue-theorem-adversarial-audit-v1",
        "exhaustive": exhaustive_short(18),
        "known_family": known_family_audit(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
