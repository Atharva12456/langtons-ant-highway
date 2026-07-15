#!/usr/bin/env python3
"""Exact regression checks for the mod-four residue-charge theorem.

This is an audit, not the proof.  The proof is written in
``translator_classification_notes.md``.  Arithmetic here is entirely over
integers modulo four.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "outputs"))

import langton_research as lr  # noqa: E402


DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def potential(alpha: list[int]):
    """Return w and one explicit family of ant potentials modulo four."""

    period = len(alpha)

    def a(x: int) -> int:
        return alpha[x % period]

    def chi(x: int, y: int) -> int:
        return 1 if (x + y) % 2 == 0 else -1

    def w(x: int, y: int) -> int:
        return chi(x, y) * a(x) % 4

    # F_N is vertically 2-periodic.  Its two parity-sector values satisfy
    # F_N(x+1,y+/-1)-F_N(x,y)=-chi(x,y)(a(x)+a(x+1)).
    h: dict[tuple[int, int], int] = {}
    for parity in (0, 1):
        h[parity, 0] = 0
        sector_sign = 1 if parity == 0 else -1
        for x in range(0, 64):
            h[parity, x + 1] = (
                h[parity, x] - sector_sign * (a(x) + a(x + 1))
            ) % 4
        for x in range(-1, -65, -1):
            h[parity, x] = (
                h[parity, x + 1] + sector_sign * (a(x) + a(x + 1))
            ) % 4

    def f_north(x: int, y: int) -> int:
        return h[(x + y) & 1, x]

    def f(direction: int, x: int, y: int) -> int:
        if direction == 0:
            return f_north(x, y)
        if direction == 1:
            return (f_north(x - 1, y) - w(x - 1, y)) % 4
        if direction == 2:
            return (f_north(x, y) - 2 * w(x, y)) % 4
        return (f_north(x + 1, y) + w(x + 1, y)) % 4

    return w, f


def check_local_equations() -> None:
    rng = random.Random(20260714)
    for period in range(1, 9):
        for _ in range(40):
            alpha = [rng.randrange(4) for _ in range(period)]
            w, f = potential(alpha)
            for x in range(-20, 21):
                for y in range(-4, 5):
                    for direction in range(4):
                        for turn in (1, -1):  # R=+1, L=-1
                            next_direction = (direction + turn) & 3
                            dx, dy = DIRS[next_direction]
                            delta = (
                                f(next_direction, x + dx, y + dy)
                                - f(direction, x, y)
                            ) % 4
                            assert delta == (-turn * w(x, y)) % 4

            monodromy = 2 * sum(alpha) % 4
            for horizontal_drift in (period, -period):
                for vertical_drift in range(-7, 8):
                    if (horizontal_drift + vertical_drift) & 1:
                        continue
                    for direction in range(4):
                        for x in range(-12, 13):
                            for y in range(-3, 4):
                                assert (
                                    f(
                                        direction,
                                        x + horizontal_drift,
                                        y + vertical_drift,
                                    )
                                    - f(direction, x, y)
                                ) % 4 == monodromy

            # When the x drift is zero, every even vertical translation has
            # zero monodromy; this is the exact-column version RC-x0.
            for vertical_drift in range(-8, 9, 2):
                for direction in range(4):
                    for x in range(-12, 13):
                        for y in range(-3, 4):
                            assert (
                                f(direction, x, y + vertical_drift)
                                - f(direction, x, y)
                            ) % 4 == 0


def check_standard_powers() -> None:
    _, standard, _ = lr.find_blank_highway_start()
    for power in range(1, 7):
        structure = lr.periodic_trace_structure(list(standard) * power)
        assert structure["finite_seed_valid"]
        drift_x, drift_y = structure["drift"]
        bases = [tuple(point) for point in structure["canonical_strand_bases"]]
        for axis, modulus in ((0, abs(drift_x)), (1, abs(drift_y))):
            for residue in range(modulus):
                signed_count = sum(
                    1 if (x + y) % 2 == 0 else -1
                    for x, y in bases
                    if (x, y)[axis] % modulus == residue
                )
                assert signed_count % 4 == 2


if __name__ == "__main__":
    check_local_equations()
    check_standard_powers()
    print("all mod-four residue-charge audit checks passed")
