"""Find reachable local entry-state cycles in wider even transverse strips."""
from __future__ import annotations

import argparse


RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
LEFT = {value: key for key, value in RIGHT.items()}


def leave(black, row, heading, width):
    black = set(black)
    while True:
        old = row in black
        if old:
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
        assert 0 <= row <= width


def first_cycle(width):
    right_entries = tuple(range(2, width + 1, 2))
    left_entries = tuple(range(0, width, 2))
    visited = set()

    def dfs(black, row, heading, flags, active, trace):
        state = (black, row, heading, flags)
        visited.add(state)
        if state in active:
            start = trace.index(state)
            return trace[start:] + [state]
        active = active | {state}
        black2, side, landing = leave(black, row, heading, width)
        lp, lm, rp, rm = flags
        if side == "R":
            if landing == width and rp:
                return None
            rp2 = rp or landing == width
            for entry in left_entries:
                if entry == 0 and rm:
                    continue
                found = dfs(black2, entry, "W", (lp, lm, rp2, rm or entry == 0),
                            active, trace + [state])
                if found:
                    return found
        else:
            if landing == 0 and lm:
                return None
            lm2 = lm or landing == 0
            for entry in right_entries:
                if entry == width and lp:
                    continue
                found = dfs(black2, entry, "E", (lp or entry == width, lm2, rp, rm),
                            active, trace + [state])
                if found:
                    return found
        return None

    for first in right_entries:
        found = dfs(frozenset(), first, "E", (first == width, False, False, False),
                    set(), [])
        if found:
            return found, visited
    return None, visited


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("widths", nargs="*", type=int, default=[4, 6, 8])
    args = parser.parse_args()
    for width in args.widths:
        cycle, visited = first_cycle(width)
        print(f"width={width} visited_states={len(visited)} cycle={cycle is not None} "
              f"cycle_length={0 if cycle is None else len(cycle)-1}")
        if cycle:
            for state in cycle:
                print(state)


if __name__ == "__main__":
    main()
