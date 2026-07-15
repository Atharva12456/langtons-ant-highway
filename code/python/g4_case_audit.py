#!/usr/bin/env python3
"""Exact checks for the six g=4 chronological countermodels in the notes."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "outputs"))
import langton_research as lr  # noqa: E402


WORDS = {
    (0, 2): "LRRLRRRR",
    (2, 0): "RLRRLRRR",
    (1, -1): "LLLRLRRRRLRRRR",
    (1, 1): "LLRRRRLLRLRRRR",
    (2, -2): "LLLRLRRRRLLLLRLRRRRLRRRR",
    (2, 2): "LLLRRRRLRLRLRLLRRRRLLRRR",
}


def signed_residue_equations(
    drift: tuple[int, int], bases: list[tuple[int, int]]
) -> bool:
    for axis, component in ((0, drift[0]), (1, drift[1])):
        if component:
            for residue in range(abs(component)):
                signed = sum(
                    1 if (x + y) % 2 == 0 else -1
                    for x, y in bases
                    if (x, y)[axis] % abs(component) == residue
                )
                if signed % 4 != 2:
                    return False
        else:
            for coordinate in {point[axis] for point in bases}:
                signed = sum(
                    1 if (x + y) % 2 == 0 else -1
                    for x, y in bases
                    if (x, y)[axis] == coordinate
                )
                if signed % 4 != 0:
                    return False
    return True


def audit(target: tuple[int, int], text: str) -> dict[str, object]:
    trace = [0 if symbol == "R" else 1 for symbol in text]
    x = y = direction = 0
    positions: list[tuple[int, int]] = []
    physical_words: dict[tuple[int, int], list[int]] = defaultdict(list)
    for turn in trace:
        positions.append((x, y))
        physical_words[x, y].append(turn)
        direction = (direction + (1 if turn == 0 else -1)) & 3
        dx, dy = lr.DIRS[direction]
        x += dx
        y += dy
    assert direction == 0 and (x, y) == target
    assert sum(1 if turn == 0 else -1 for turn in trace) == 4
    assert all(
        all(left != right for left, right in zip(word, word[1:]))
        for word in physical_words.values()
    )

    groups: dict[tuple[int, int], list[tuple[int, int, int]]] = defaultdict(list)
    for phase, (point, turn) in enumerate(zip(positions, trace)):
        representative, level = lr.quotient_representative_level(point, target)
        groups[representative].append((level, phase, turn))
    excess = {
        representative: sum(1 if turn == 0 else -1 for _, _, turn in entries)
        for representative, entries in groups.items()
    }
    assert all(value in (0, 1) for value in excess.values())
    odd = sorted(representative for representative, value in excess.items() if value)
    assert len(odd) == 4
    assert signed_residue_equations(target, odd)

    score, drift, classes = lr.periodic_trace_violation_score(trace)
    assert drift == target and score > 0
    return {
        "drift": target,
        "period": len(trace),
        "word": text,
        "physical_cell_alternation": True,
        "class_excesses_are_zero_or_one": True,
        "signed_residue_equations": True,
        "odd_class_representatives": odd,
        "p3_violation_score": score,
        "translation_classes": classes,
    }


if __name__ == "__main__":
    print(json.dumps([audit(drift, word) for drift, word in WORDS.items()], indent=2))
