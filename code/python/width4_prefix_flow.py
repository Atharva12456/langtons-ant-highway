"""Exploratory integer-flow relaxation using ordering-sensitive P3 prefix charge.

This is not a trace search.  It forgets chronological connectivity and keeps only
flow conservation on the four-state width-four macro graph, extremal-residue
uniqueness, the all-period bound P<=7m, positive growth, and the theorem that every
forward spatial prefix of a translation class has turn charge zero or one.

UNSAT would therefore prove a genuine obstruction at this relaxed level.  SAT only
produces a countermodel to that proof strategy, not a Langton highway.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

from z3 import Implies, Int, Or, Solver, Sum, sat

from search_width4 import LN, LS, UN, US, TRANSITIONS


NAMES = {
    (LN, LS): "a", (LN, UN): "b", (LN, LN): "x",
    (LS, LN): "c", (LS, LS): "d", (LS, UN): "e",
    (UN, US): "f", (UN, UN): "q", (UN, LS): "h",
    (US, UN): "i", (US, LS): "j", (US, US): "y",
}


def solve_relaxation(m: int, above_five: bool = False):
    bound = 7 * m
    coords = range(-bound, bound + 1)
    solver = Solver()
    variables = {}

    for state, transitions in TRANSITIONS.items():
        for nxt, delta, pair, even_line, even_offset in transitions:
            name = NAMES[(state, nxt)]
            for ell in coords:
                v = Int(f"{name}_{ell:+d}")
                variables[state, nxt, ell] = v
                solver.add(v >= 0)
                if not -bound <= ell + delta <= bound:
                    solver.add(v == 0)

    def var(state, nxt, ell):
        if ell not in coords:
            return 0
        return variables[state, nxt, ell]

    # One integral flow from (LN,0) to (LN,m); disconnected circulations are
    # intentionally not excluded in this relaxation.
    for state in (LN, LS, UN, US):
        for ell in coords:
            outgoing = []
            incoming = []
            for nxt, delta, pair, even_line, even_offset in TRANSITIONS[state]:
                outgoing.append(var(state, nxt, ell))
            for previous, transitions in TRANSITIONS.items():
                for nxt, delta, pair, even_line, even_offset in transitions:
                    if nxt == state:
                        incoming.append(var(previous, state, ell - delta))
            rhs = (1 if state == LN and ell == 0 else 0)
            rhs -= (1 if state == LN and ell == m else 0)
            solver.add(Sum(outgoing) - Sum(incoming) == rhs)

    # A directed multigraph with the degree equations has an Euler trail when its
    # nonzero support is weakly connected.  Certify that connectivity by assigning
    # every used vertex except the start a strictly descending parent edge.
    ranks = {}
    vertex_used = {}
    vertex_count = 4 * len(list(coords))
    for state in (LN, LS, UN, US):
        for ell in coords:
            incident = []
            neighbors = []
            for nxt, delta, pair, even_line, even_offset in TRANSITIONS[state]:
                edge = var(state, nxt, ell)
                incident.append(edge)
                neighbors.append((nxt, ell + delta, edge))
            for previous, transitions in TRANSITIONS.items():
                for nxt, delta, pair, even_line, even_offset in transitions:
                    if nxt == state:
                        edge = var(previous, state, ell - delta)
                        incident.append(edge)
                        neighbors.append((previous, ell - delta, edge))
            used = Sum(incident) > 0
            rank = Int(f"rank_{state}_{ell:+d}")
            vertex_used[state, ell] = used
            ranks[state, ell] = rank
            solver.add(rank >= 0, rank <= vertex_count)
            if state == LN and ell == 0:
                solver.add(rank == 0)
            else:
                parents = [
                    (edge > 0) & (ranks.get((other, other_ell),
                        Int(f"rank_{other}_{other_ell:+d}")) < rank)
                    for other, other_ell, edge in neighbors
                    if -bound <= other_ell <= bound
                ]
                solver.add(Implies(used, Or(parents)))

    all_vars = list(variables.values())
    macro_period = Sum(all_vars)
    solver.add(macro_period > 0, macro_period <= 7 * m)
    if above_five:
        solver.add(macro_period >= 5 * m + 7)

    by_name = defaultdict(dict)
    for (state, nxt, ell), value in variables.items():
        by_name[NAMES[(state, nxt)]][ell] = value

    def nv(name, ell):
        return by_name[name].get(ell, 0)

    # Extremal cells are R singletons; no residue class can be used twice.
    bottom_total = []
    top_total = []
    for r in range(m):
        bottom = Sum([nv("x", ell) + nv("c", ell)
                      for ell in coords if (ell - 1) % m == r])
        top = Sum([nv("f", ell) + nv("y", ell)
                   for ell in coords if (ell + 1) % m == r])
        solver.add(bottom >= 0, bottom <= 1, top >= 0, top <= 1)
        bottom_total.append(bottom)
        top_total.append(top)
    solver.add(Sum(bottom_total) >= 1, Sum(top_total) >= 1)

    # Charge at each physical cell.  Centre-line terms are shifted from the
    # starting odd-cell coordinate exactly as in the macro transition table.
    charge = {line: {} for line in (0, 1, 2, 3, 4)}
    cell_coords = range(-bound - 1, bound + 2)
    for ell in cell_coords:
        charge[0][ell] = nv("x", ell + 1) + nv("c", ell + 1)
        charge[1][ell] = (nv("a", ell) + nv("b", ell) + nv("c", ell)
                          - nv("x", ell) - nv("d", ell) - nv("e", ell))
        charge[2][ell] = (nv("a", ell - 1) - nv("b", ell - 1)
                          + nv("d", ell - 1) - nv("e", ell - 1)
                          + nv("q", ell + 1) - nv("h", ell + 1)
                          + nv("i", ell + 1) - nv("j", ell + 1))
        charge[3][ell] = (nv("f", ell) + nv("i", ell)
                          - nv("q", ell) - nv("h", ell)
                          - nv("j", ell) - nv("y", ell))
        charge[4][ell] = nv("f", ell - 1) + nv("y", ell - 1)

    # Ordering-sensitive theorem: in each line/residue, every suffix (forward
    # spatial prefix) has charge 0 or 1.
    for line in range(5):
        for r in range(m):
            residue_cells = [ell for ell in cell_coords if ell % m == r]
            residue_cells.sort(reverse=True)
            prefix = []
            for ell in residue_cells:
                prefix.append(charge[line][ell])
                total = Sum(prefix)
                solver.add(total >= 0, total <= 1)

    growth = Sum([charge[line][ell]
                  for line in range(5) for ell in cell_coords])
    solver.add(growth >= 4)

    result = solver.check()
    print(f"m={m} above_five={above_five} result={result}")
    if result == sat:
        model = solver.model()
        used = []
        for (state, nxt, ell), value in variables.items():
            count = model.eval(value).as_long()
            if count:
                used.append((NAMES[(state, nxt)], ell, count))
        print(f"  P={model.eval(macro_period)} growth={model.eval(growth)}")
        print("  flow=" + " ".join(f"{name}@{ell}:{count}"
                                    for name, ell, count in sorted(used,
                                        key=lambda item: (item[1], item[0]))))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-drift", type=int, default=1)
    parser.add_argument("--max-drift", type=int, default=6)
    parser.add_argument("--above-five", action="store_true",
                        help="require P >= 5m+7")
    args = parser.parse_args()
    for m in range(args.min_drift, args.max_drift + 1):
        solve_relaxation(m, args.above_five)


if __name__ == "__main__":
    main()
