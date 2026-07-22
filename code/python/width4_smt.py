"""Independent SMT search for a width-four periodic Langton highway.

The model uses the four-state two-turn macro table from ``search_width4.py`` but
does *not* use its chronological checker.  For fixed drift ``m`` and macro period
``P``, Z3 constructs the state/longitudinal path symbolically.  It then ranks every
phase inside its exact translation class by

    key = phase - 2*P*floor(longitudinal_coordinate / m)

and requires rank 0,2,4,... to turn R and rank 1,3,5,... to turn L.  This is exactly
the stabilized start-R and strict-alternation condition.  A SAT model is replayed
through the independent Python walk/checker before it is reported.

This is research code.  UNSAT is an independent bounded check, not an all-period
proof and not a proof certificate unless a separately checkable Z3 proof is saved.
"""
from __future__ import annotations

import argparse
import time

import z3

from explore_chronology import walk
from search_width4 import fast_p3_valid


LN, LS, UN, US = range(4)
ODD_LINE = (1, 1, 3, 3)

# source, destination, delta ell, pair, even line, even offset
TRANSITIONS = (
    (LN, LS, +1, "RR", 2, +1),
    (LN, UN, +1, "RL", 2, +1),
    (LN, LN, -1, "LR", 0, -1),
    (LS, LN, -1, "RR", 0, -1),
    (LS, LS, +1, "LR", 2, +1),
    (LS, UN, +1, "LL", 2, +1),
    (UN, US, +1, "RR", 4, +1),
    (UN, UN, -1, "LR", 2, -1),
    (UN, LS, -1, "LL", 2, -1),
    (US, UN, -1, "RR", 2, -1),
    (US, LS, -1, "RL", 2, -1),
    (US, US, +1, "LR", 4, +1),
)


def choice_value(choice, column):
    """Select one integer/string-derived transition column with nested Ifs."""
    values = [tr[column] for tr in TRANSITIONS]
    out = z3.IntVal(values[-1])
    for index in range(len(values) - 2, -1, -1):
        out = z3.If(choice == index, values[index], out)
    return out


def solve(m: int, macros: int, timeout_ms: int = 0):
    if m <= 0 or macros <= 0:
        raise ValueError((m, macros))
    n = 2 * macros
    solver = z3.Solver()
    if timeout_ms:
        solver.set(timeout=timeout_ms)

    state = [z3.Int(f"state_{i}") for i in range(macros + 1)]
    ell = [z3.Int(f"ell_{i}") for i in range(macros + 1)]
    choice = [z3.Int(f"choice_{i}") for i in range(macros)]
    solver.add(state[0] == LN, ell[0] == 0)
    solver.add(state[macros] == LN, ell[macros] == m)

    phase_line = []
    phase_ell = []
    phase_r = []
    for i in range(macros):
        solver.add(choice[i] >= 0, choice[i] < len(TRANSITIONS))
        source = choice_value(choice[i], 0)
        destination = choice_value(choice[i], 1)
        delta = choice_value(choice[i], 2)
        even_line = choice_value(choice[i], 4)
        even_offset = choice_value(choice[i], 5)
        solver.add(state[i] == source)
        solver.add(state[i + 1] == destination)
        solver.add(ell[i + 1] == ell[i] + delta)

        odd_line = z3.If(state[i] <= LS, 1, 3)
        odd_r = z3.Or(*[
            z3.And(choice[i] == k, z3.BoolVal(tr[3][0] == "R"))
            for k, tr in enumerate(TRANSITIONS)
        ])
        even_r = z3.Or(*[
            z3.And(choice[i] == k, z3.BoolVal(tr[3][1] == "R"))
            for k, tr in enumerate(TRANSITIONS)
        ])
        phase_line.extend((odd_line, even_line))
        phase_ell.extend((ell[i], ell[i] + even_offset))
        phase_r.extend((odd_r, even_r))

    solver.add(z3.Or(*[line == 4 for line in phase_line]))
    growth = z3.Sum([z3.If(is_r, 1, -1) for is_r in phase_r])
    solver.add(growth > 0, growth % 4 == 0)

    quotient = [(x - x % m) / m for x in phase_ell]
    key = [z3.IntVal(i) - n * quotient[i] for i in range(n)]

    for i in range(n):
        preceding = []
        for j in range(n):
            if i == j:
                continue
            same_class = z3.And(
                phase_line[i] == phase_line[j],
                (phase_ell[i] - phase_ell[j]) % m == 0,
            )
            preceding.append(z3.If(z3.And(same_class, key[j] < key[i]), 1, 0))
        rank = z3.Sum(preceding) if preceding else z3.IntVal(0)
        solver.add(phase_r[i] == (rank % 2 == 0))

    # Redundant aggregate consequences of the rank equations.  Stating them
    # explicitly gives the arithmetic solver useful propagation before it has
    # resolved the full chronological order.
    odd_classes = []
    for line in range(5):
        line_excess = []
        for residue in range(m):
            members = [z3.And(phase_line[i] == line,
                              phase_ell[i] % m == residue)
                       for i in range(n)]
            count = z3.Sum([z3.If(member, 1, 0) for member in members])
            excess = z3.Sum([
                z3.If(member, z3.If(phase_r[i], 1, -1), 0)
                for i, member in enumerate(members)
            ])
            solver.add(excess == count % 2)
            odd_classes.append(z3.If(count % 2 == 1, 1, 0))
            line_excess.append(excess)
        solver.add(z3.Sum(line_excess) >= 0, z3.Sum(line_excess) <= m)
    solver.add(growth == z3.Sum(odd_classes))

    # The two extremal lines have only R turns geometrically, so exact P3 forces
    # each residue class there to occur at most once.  State it explicitly as a
    # redundant strengthening which helps the solver.
    for line in (0, 4):
        for residue in range(m):
            members = [z3.If(z3.And(phase_line[i] == line,
                                   phase_ell[i] % m == residue), 1, 0)
                       for i in range(n)]
            solver.add(z3.Sum(members) <= 1)

    start = time.perf_counter()
    status = solver.check()
    seconds = time.perf_counter() - start
    result = {
        "m": m,
        "macros": macros,
        "period": n,
        "status": str(status),
        "seconds": seconds,
        "reason_unknown": solver.reason_unknown() if status == z3.unknown else "",
    }
    if status == z3.sat:
        model = solver.model()
        chosen = [model.eval(c).as_long() for c in choice]
        word = "".join(TRANSITIONS[k][3] for k in chosen)
        points, _, heading, drift = walk(word)
        valid, _ = fast_p3_valid(word, points, drift)
        if heading != 0 or drift != (m, -m) or not valid:
            raise AssertionError((heading, drift, valid, word))
        result["word"] = word
        result["growth"] = word.count("R") - word.count("L")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    parser.add_argument("min_macros", type=int)
    parser.add_argument("max_macros", type=int, nargs="?")
    parser.add_argument("--timeout-ms", type=int, default=0)
    args = parser.parse_args()
    maximum = args.max_macros if args.max_macros is not None else args.min_macros
    for macros in range(args.min_macros, maximum + 1):
        if (macros - args.m) % 2:
            continue
        print(solve(args.m, macros, args.timeout_ms), flush=True)


if __name__ == "__main__":
    main()
