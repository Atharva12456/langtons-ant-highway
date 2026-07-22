"""Exact local crossing-sequence graph for a width-four all-white tail.

A vertex is the control crossing sequence at one longitudinal tape boundary.  The
direction is implicit: entries 0,2,... are rightward and entries 1,3,... leftward.
The stored value is the even transverse line immediately after the crossing.

For one initially white five-cell column, ``compatible(left, right)`` simulates every
read/write inside that column and consumes the two boundary sequences literally.
Together with the independent verifier, this supplies the exact local-classification
certificate used by the computer-assisted width-four exclusion theorem.
"""
from __future__ import annotations

import argparse
from itertools import product


E, S, W, N = 0, 1, 2, 3


def turn(heading: int, black: int) -> int:
    """White turns right; black turns left."""
    return (heading + (3 if black else 1)) % 4


def run_inside(bits: list[int], transverse: int, heading: int):
    """Run until the next horizontal exit, returning ``(side, line)``."""
    while True:
        if not 0 <= transverse <= 4:
            raise AssertionError((bits, transverse, heading))
        old = bits[transverse]
        bits[transverse] ^= 1
        heading = turn(heading, old)
        if heading == E:
            return "right", transverse + 1
        if heading == W:
            return "left", transverse - 1
        transverse += 1 if heading == N else -1


def compatible(left: tuple[int, ...], right: tuple[int, ...], initial_mask: int = 0):
    """Return final column mask iff the two exact crossing sequences are compatible."""
    if not left or not right or len(left) % 2 == 0 or len(right) % 2 == 0:
        return None
    bits = [(initial_mask >> line) & 1 for line in range(5)]
    li = 1
    ri = 0
    transverse = left[0]
    heading = E
    while True:
        side, out_line = run_inside(bits, transverse, heading)
        if side == "right":
            if ri >= len(right) or ri % 2 != 0 or right[ri] != out_line:
                return None
            ri += 1
            if ri == len(right):
                if li != len(left):
                    return None
                return sum(bit << line for line, bit in enumerate(bits))
            if ri % 2 != 1:
                raise AssertionError(ri)
            transverse = right[ri]
            heading = W
            ri += 1
        else:
            if li >= len(left) or li % 2 != 1 or left[li] != out_line:
                return None
            li += 1
            if li >= len(left) or li % 2 != 0:
                return None
            transverse = left[li]
            heading = E
            li += 1


def signatures(length: int):
    """Enumerate the extremal-singleton control signatures of a fixed odd length."""
    if length <= 0 or length % 2 == 0:
        raise ValueError(length)
    plus = (length + 1) // 2
    minus = (length - 1) // 2
    for plus_special in range(-1, plus):
        for minus_special in range(-1, minus):
            values = []
            for index in range(length):
                slot = index // 2
                if index % 2 == 0:
                    values.append(4 if slot == plus_special else 2)
                else:
                    values.append(0 if slot == minus_special else 2)
            yield tuple(values)


def short_graph(max_length: int):
    vertices = [signature for length in range(1, max_length + 1, 2)
                for signature in signatures(length)]
    edges = []
    for left, right in product(vertices, repeat=2):
        final_mask = compatible(left, right)
        if final_mask is not None:
            edges.append((left, right, final_mask))
    return vertices, edges


def all_compatible_edges():
    """Generate all exact blank-column edges, detecting any reachable local cycle.

    The four booleans record whether the exceptional `+4` / `-0` event has already
    occurred on the left and right boundary.  A repeated entry state would permit
    arbitrarily long compatible signatures, so it is reported explicitly.
    """
    terminals = set()
    cycles = []
    reachable = set()
    max_depth = 0

    def visit(bits_tuple, transverse, heading, flags, left, right, stack, depth):
        nonlocal max_depth
        state = (bits_tuple, transverse, heading, flags)
        reachable.add(state)
        max_depth = max(max_depth, depth)
        if state in stack:
            cycles.append((state, left, right))
            return
        stack = stack | {state}
        bits = list(bits_tuple)
        side, out_line = run_inside(bits, transverse, heading)
        bits_tuple = tuple(bits)
        lp, lm, rp, rm = flags
        if side == "right":
            if out_line == 4 and rp:
                return
            next_rp = rp or out_line == 4
            right_after_exit = right + (out_line,)
            terminals.add((left, right_after_exit,
                           sum(bit << line for line, bit in enumerate(bits))))
            # If the head returns, the next right-boundary event is a leftward
            # entry on line 2 or the one allowed exceptional line 0.
            for entry in (2, 0):
                if entry == 0 and rm:
                    continue
                visit(bits_tuple, entry, W,
                      (lp, lm, next_rp, rm or entry == 0),
                      left, right_after_exit + (entry,), stack, depth + 1)
        else:
            if out_line == 0 and lm:
                return
            next_lm = lm or out_line == 0
            left_after_exit = left + (out_line,)
            # A left exit must later be followed by a rightward re-entry.
            for entry in (2, 4):
                if entry == 4 and lp:
                    continue
                visit(bits_tuple, entry, E,
                      (lp or entry == 4, next_lm, rp, rm),
                      left_after_exit + (entry,), right, stack, depth + 1)

    blank = (0, 0, 0, 0, 0)
    for first in (2, 4):
        visit(blank, first, E, (first == 4, False, False, False),
              (first,), (), set(), 0)
    return terminals, cycles, reachable, max_depth


def graph_audit(edges):
    adjacency = {}
    for left, right, _mask in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set())
    colour = {}
    longest = {}

    def visit(vertex):
        if colour.get(vertex) == 1:
            raise AssertionError(("directed cycle", vertex))
        if colour.get(vertex) == 2:
            return longest[vertex]
        colour[vertex] = 1
        depth = 0
        for nxt in adjacency[vertex]:
            depth = max(depth, 1 + visit(nxt))
        colour[vertex] = 2
        longest[vertex] = depth
        return depth

    maximum = max((visit(vertex) for vertex in adjacency), default=0)
    return len(adjacency), maximum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=7)
    args = parser.parse_args()
    vertices, edges = short_graph(args.max_length)
    expected = sum((((length - 1) // 2) + 2) * (((length - 1) // 2) + 1)
                   for length in range(1, args.max_length + 1, 2))
    assert len(vertices) == expected
    print(f"vertices={len(vertices)} compatible_blank_edges={len(edges)}")
    generated, cycles, reachable, max_depth = all_compatible_edges()
    print(f"generated_exact_edges={len(generated)} reachable_entry_cycles={len(cycles)} "
          f"reachable_entry_states={len(reachable)} max_entry_depth={max_depth}")
    graph_vertices, longest_path = graph_audit(generated)
    print(f"exact_graph_vertices={graph_vertices} longest_directed_path={longest_path} acyclic=true")
    bounded_edges = {(left, right, mask) for left, right, mask in edges}
    generated_bounded = {edge for edge in generated
                         if len(edge[0]) <= args.max_length
                         and len(edge[1]) <= args.max_length}
    assert bounded_edges == generated_bounded, (bounded_edges ^ generated_bounded)
    for left, right, final_mask in edges[:40]:
        print(f"{left} -> {right} final_mask={final_mask:05b}")


if __name__ == "__main__":
    main()
