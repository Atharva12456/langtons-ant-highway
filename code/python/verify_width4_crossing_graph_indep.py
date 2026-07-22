"""Independent literal verifier for the width-four blank-column edge table.

This file intentionally imports no project search or crossing-graph code.  It uses
compass-letter headings, a set of black transverse rows, and a separately written
depth-first generator.
"""
from __future__ import annotations


RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
LEFT = {value: key for key, value in RIGHT.items()}


def leave_column(black_rows: frozenset[int], row: int, heading: str):
    black = set(black_rows)
    while True:
        was_black = row in black
        if was_black:
            black.remove(row)
            heading = LEFT[heading]
        else:
            black.add(row)
            heading = RIGHT[heading]
        if heading == "E":
            return frozenset(black), "R", row + 1
        if heading == "W":
            return frozenset(black), "L", row - 1
        row += 1 if heading == "N" else -1
        assert 0 <= row <= 4


def enumerate_edges():
    edges = set()
    active_cycles = []

    def dfs(black, row, heading, used, left, right, active):
        state = (black, row, heading, used)
        if state in active:
            active_cycles.append(state)
            return
        active = active | {state}
        black2, side, landing = leave_column(black, row, heading)
        left_top, left_bottom, right_top, right_bottom = used
        if side == "R":
            if landing == 4 and right_top:
                return
            right2 = right + (landing,)
            used2 = (left_top, left_bottom,
                     right_top or landing == 4, right_bottom)
            edges.add((left, right2))
            for entry in (0, 2):
                if entry == 0 and right_bottom:
                    continue
                dfs(black2, entry, "W",
                    (used2[0], used2[1], used2[2], right_bottom or entry == 0),
                    left, right2 + (entry,), active)
        else:
            if landing == 0 and left_bottom:
                return
            left2 = left + (landing,)
            used2 = (left_top, left_bottom or landing == 0,
                     right_top, right_bottom)
            for entry in (2, 4):
                if entry == 4 and left_top:
                    continue
                dfs(black2, entry, "E",
                    (left_top or entry == 4, used2[1], right_top, right_bottom),
                    left2 + (entry,), right, active)

    for first in (2, 4):
        dfs(frozenset(), first, "E", (first == 4, False, False, False),
            (first,), (), frozenset())
    assert not active_cycles
    return edges


EXPECTED = {((2,0,2), (4,))}
EXPECTED |= {
    (source, target)
    for source in ((4,2,2,0,2,2,2), (2,0,4,2,2,2,2))
    for target in ((2,), (2,0,2), (2,0,2,2,2), (2,0,2,2,2,2,4))
}
EXPECTED |= {
    ((2,0,2,2,4,2,2,2,2), target)
    for target in ((4,2,2), (4,2,2,0,2), (4,2,2,0,2,2,2))
}


def main():
    actual = enumerate_edges()
    assert actual == EXPECTED, (actual - EXPECTED, EXPECTED - actual)
    print(f"independent_exact_edges={len(actual)} agrees=true")

    # Convention audit on the genuine standard highway.  Simulate its documented
    # finite seed, extract complete crossing sequences at two far-ahead cuts, and
    # replay the intervening initially white column using the same boundary-index
    # interpretation as the width-four verifier.
    seed = {(-2,-2), (-2,-1), (-1,0), (0,1), (1,-2), (1,1),
            (2,-2), (2,0), (3,-1), (3,0), (4,0)}
    black = set(seed)
    x = y = 0
    heading = "N"
    crossings = {}
    for _ in range(104 * 120):
        point = (x, y)
        was_black = point in black
        if was_black:
            black.remove(point)
            heading = LEFT[heading]
        else:
            black.add(point)
            heading = RIGHT[heading]
        if heading == "E":
            cut = x
            x += 1
            crossings.setdefault(cut, []).append(("R", x + y))
        elif heading == "W":
            cut = x - 1
            x -= 1
            crossings.setdefault(cut, []).append(("L", x + y))
        elif heading == "N":
            y += 1
        else:
            y -= 1

    assert (x, y, heading) == (240, -240, "N"), (x, y, heading)

    left_events = crossings[100]
    right_events = crossings[101]
    assert [direction for direction, _row in left_events] == [
        "R" if i % 2 == 0 else "L" for i in range(len(left_events))]
    assert [direction for direction, _row in right_events] == [
        "R" if i % 2 == 0 else "L" for i in range(len(right_events))]
    left_rows = tuple(row for _direction, row in left_events)
    right_rows = tuple(row for _direction, row in right_events)

    column_black = frozenset()
    li, ri = 1, 0
    row, local_heading = left_rows[0], "E"
    while True:
        column_black, side, landing = leave_column_unbounded(
            column_black, row, local_heading)
        if side == "R":
            assert right_rows[ri] == landing
            ri += 1
            if ri == len(right_rows):
                assert li == len(left_rows)
                break
            row, local_heading = right_rows[ri], "W"
            ri += 1
        else:
            assert left_rows[li] == landing
            li += 1
            row, local_heading = left_rows[li], "E"
            li += 1
    print(f"standard_highway_boundary_replay=true left_len={len(left_rows)} "
          f"right_len={len(right_rows)}")


def leave_column_unbounded(black_rows: frozenset[int], row: int, heading: str):
    black = set(black_rows)
    while True:
        was_black = row in black
        if was_black:
            black.remove(row)
            heading = LEFT[heading]
        else:
            black.add(row)
            heading = RIGHT[heading]
        if heading == "E":
            return frozenset(black), "R", row + 1
        if heading == "W":
            return frozenset(black), "L", row - 1
        row += 1 if heading == "N" else -1


if __name__ == "__main__":
    main()
