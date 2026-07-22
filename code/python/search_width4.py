"""Exploratory exact search for diagonal periodic traces of transverse width four.

This is research code, not a proof certificate.  It enumerates the two-step
collapse obtained by observing the ant whenever it is on one of the odd transverse
lines.  In the normalised frame ``t=x+y`` the five lines are 0,...,4.  Lines 0 and
4 are extremal and therefore turn R once; lines 1 and 3 are the two odd-line
tracks, while line 2 is the revisitable centre line.

Each macro transition below records

    (next state, longitudinal displacement, two turns, even line, even offset).

The four odd-line states are LN, LS, UN, US: lower/upper track followed by the
arrival heading.  A closed macro path based at LN has heading reset automatically.
Returning to LN also forces a bottom-boundary visit in the final transition; an
explicit top-boundary visit is required to make the width exactly four.

At every node we enforce ordinary same-cell alternation.  At every leaf we invoke
the full translation-class P3 criterion from ``verify_extremal.p3_valid``.  Thus a
reported hit would be a genuine finite-support periodic highway word, while a
zero-hit result is only a bounded computational observation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import time

from explore_chronology import classes_of, levels, walk
from verify_extremal import p3_valid, tfun


LN, LS, UN, US = range(4)
STATE_NAME = ("LN", "LS", "UN", "US")
ODD_LINE = (1, 1, 3, 3)

# next state, delta longitudinal coordinate, two turns, even line, even offset
TRANSITIONS = {
    LN: ((LS, +1, "RR", 2, +1),
         (UN, +1, "RL", 2, +1),
         (LN, -1, "LR", 0, -1)),
    LS: ((LN, -1, "RR", 0, -1),
         (LS, +1, "LR", 2, +1),
         (UN, +1, "LL", 2, +1)),
    UN: ((US, +1, "RR", 4, +1),
         (UN, -1, "LR", 2, -1),
         (LS, -1, "LL", 2, -1)),
    US: ((UN, -1, "RR", 2, -1),
         (LS, -1, "RL", 2, -1),
         (US, +1, "LR", 4, +1)),
}


def _put(last_turn, cell, turn):
    """Install one turn subject to physical-cell alternation; return old value."""
    old = last_turn.get(cell)
    if old is not None and old == turn:
        return None, False
    last_turn[cell] = turn
    return old, True


def _undo(last_turn, cell, old):
    if old is None:
        del last_turn[cell]
    else:
        last_turn[cell] = old


def fast_p3_data(word, pts, drift):
    """Build width-four P3 classes directly as ``(t, x mod m)``.

    Here ``drift=(m,-m)`` with ``m>0``.  Writing ``r=x mod m`` gives the
    longitudinal level ``a=(x-r)/m`` up to a harmless classwise constant, so the
    chronological key is ``i-N*a``.
    """
    n = len(word)
    m = drift[0]
    if m <= 0 or drift[1] != -m:
        raise ValueError(drift)
    groups = {}
    for i, (x, y) in enumerate(pts):
        r = x % m
        a = (x - r) // m
        groups.setdefault((x + y, r), []).append((i - n * a, word[i]))
    return groups


def fast_p3_valid(word, pts, drift):
    groups = fast_p3_data(word, pts, drift)
    for entries in groups.values():
        seq = [turn for _, turn in sorted(entries)]
        if seq[0] != "R" or any(a == b for a, b in zip(seq, seq[1:])):
            return False, groups
    return True, groups


def p3_failure_signature(word, pts, drift, groups=None):
    """Return the set of local obstruction types, labelled by transverse line."""
    if groups is None:
        groups = fast_p3_data(word, pts, drift)
    low = min(x + y for x, y in pts)
    failures = set()
    for (t, _), entries in groups.items():
        seq = [turn for _, turn in sorted(entries)]
        line = t - low
        if seq[0] != "R":
            failures.add((line, "starts_L"))
        if any(a == b for a, b in zip(seq, seq[1:])):
            failures.add((line, "nonalternating"))
    return tuple(sorted(failures))


def search_macro_period(macros, node_cap=0, keep_hits=20, diagnostics=False,
                        required_drift=0):
    """Enumerate all based width-four macro cycles of the requested length."""
    nodes = 0
    structural_leaves = 0
    p3_checks = 0
    odd_identity_pass = 0
    starts_r_pass = 0
    starts_r_odd_pass = 0
    extremal_singleton_pass = 0
    starts_r_extremal_pass = 0
    starts_r_examples = []
    extremal_examples = []
    hits = []
    failure_counts = Counter()
    odd_identity_failure_counts = Counter()
    failure_examples = {}
    best_defect = None
    best_defect_word = None
    best_odd_defect = None
    best_odd_defect_word = None
    turns = []
    last_turn = {}
    start = time.perf_counter()
    capped = False

    def dfs(depth, state, ell, balance, used_top):
        nonlocal nodes, structural_leaves, p3_checks, odd_identity_pass
        nonlocal starts_r_pass, starts_r_odd_pass, extremal_singleton_pass
        nonlocal starts_r_extremal_pass, best_defect, best_defect_word
        nonlocal best_odd_defect, best_odd_defect_word, capped
        if capped:
            return
        nodes += 1
        if node_cap and nodes > node_cap:
            capped = True
            return
        remaining = macros - depth
        if required_drift and (ell + remaining < required_drift
                               or ell - remaining > required_drift):
            return
        if ell + remaining <= 0:  # even all +1 moves cannot give positive drift
            return
        if balance + 2 * remaining <= 0:  # RR is the largest macro growth
            return
        if depth == macros:
            if (state != LN or ell <= 0 or balance <= 0 or not used_top
                    or (required_drift and ell != required_drift)):
                return
            structural_leaves += 1
            word = "".join(turns)
            pts, _, hfin, drift = walk(word)
            t = tfun(drift)
            if hfin != 0 or drift != (ell, -ell) or t is None:
                raise AssertionError((state, ell, hfin, drift, word))
            ts = [t(p) for p in pts]
            if max(ts) - min(ts) != 4:
                raise AssertionError((min(ts), max(ts), word))
            groups = fast_p3_data(word, pts, drift)
            ordered = [[turn for _, turn in sorted(entries)]
                       for entries in groups.values()]
            low_t = min(t for t, _ in groups)
            high_t = max(t for t, _ in groups)
            extreme_ok = all(len(entries) == 1 for (t, _), entries in groups.items()
                             if t == low_t or t == high_t)
            if extreme_ok:
                extremal_singleton_pass += 1
                if len(extremal_examples) < keep_hits:
                    extremal_examples.append((word, balance, drift))
            start_l_count = sum(seq[0] == "L" for seq in ordered)
            nonalt_count = sum(any(a == b for a, b in zip(seq, seq[1:]))
                               for seq in ordered)
            defect = (start_l_count + nonalt_count, start_l_count, nonalt_count)
            if best_defect is None or defect < best_defect:
                best_defect = defect
                best_defect_word = word
            if start_l_count == 0:
                starts_r_pass += 1
                if extreme_ok:
                    starts_r_extremal_pass += 1
                if len(starts_r_examples) < keep_hits:
                    starts_r_examples.append((word, nonalt_count, balance, drift))
            odd_ok = balance == sum(len(entries) & 1 for entries in groups.values())
            if odd_ok:
                odd_identity_pass += 1
                if start_l_count == 0:
                    starts_r_odd_pass += 1
                if best_odd_defect is None or defect < best_odd_defect:
                    best_odd_defect = defect
                    best_odd_defect_word = word
                p3_checks += 1
                ok, groups = fast_p3_valid(word, pts, drift)
            else:
                ok = False
            if ok and len(hits) < keep_hits:
                hits.append(word)
            elif diagnostics:
                sig = p3_failure_signature(word, pts, drift, groups)
                failure_counts[sig] += 1
                if odd_ok:
                    odd_identity_failure_counts[sig] += 1
                failure_examples.setdefault(sig, word)
            return

        odd_cell = (ODD_LINE[state], ell)
        for nxt, delta, pair, even_line, even_offset in TRANSITIONS[state]:
            old1, ok1 = _put(last_turn, odd_cell, pair[0])
            if not ok1:
                continue
            even_cell = (even_line, ell + even_offset)
            old2, ok2 = _put(last_turn, even_cell, pair[1])
            if ok2:
                turns.append(pair)
                dfs(depth + 1, nxt, ell + delta,
                    balance + pair.count("R") - pair.count("L"),
                    used_top or even_line == 4)
                turns.pop()
                _undo(last_turn, even_cell, old2)
            _undo(last_turn, odd_cell, old1)

    dfs(0, LN, 0, 0, False)
    return {
        "macros": macros,
        "period": 2 * macros,
        "nodes": nodes,
        "structural_leaves": structural_leaves,
        "p3_checks": p3_checks,
        "odd_identity_pass": odd_identity_pass,
        "starts_r_pass": starts_r_pass,
        "starts_r_odd_pass": starts_r_odd_pass,
        "extremal_singleton_pass": extremal_singleton_pass,
        "starts_r_extremal_pass": starts_r_extremal_pass,
        "starts_r_examples": starts_r_examples,
        "extremal_examples": extremal_examples,
        "hits": hits,
        "failure_counts": failure_counts,
        "odd_identity_failure_counts": odd_identity_failure_counts,
        "failure_examples": failure_examples,
        "best_defect": best_defect,
        "best_defect_word": best_defect_word,
        "best_odd_defect": best_odd_defect,
        "best_odd_defect_word": best_odd_defect_word,
        "capped": capped,
        "seconds": time.perf_counter() - start,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-macros", type=int, default=2)
    ap.add_argument("--max-macros", type=int, default=30)
    ap.add_argument("--node-cap", type=int, default=0)
    ap.add_argument("--diagnostics", action="store_true")
    ap.add_argument("--drift", type=int, default=0,
                    help="require normalized drift (m,-m)")
    args = ap.parse_args()
    for p in range(args.min_macros, args.max_macros + 1):
        r = search_macro_period(p, args.node_cap, diagnostics=args.diagnostics,
                                required_drift=args.drift)
        print("P={macros:2d} N={period:3d} nodes={nodes:12,d} "
              "leaves={structural_leaves:10,d} p3={p3_checks:10,d} "
              "odd-id={odd_identity_pass:8,d} starts-R={starts_r_pass:6,d} "
              "ext={extremal_singleton_pass:8,d} "
              "R+ext={starts_r_extremal_pass:5,d} both={starts_r_odd_pass:5,d} "
              "hits={nh:2d} "
              "capped={capped} sec={seconds:8.3f}".format(
                  nh=len(r["hits"]), **r), flush=True)
        print(f"  best-defect(total,start-L,nonalt)={r['best_defect']} "
              f"word={r['best_defect_word']}")
        print(f"  best odd-id defect={r['best_odd_defect']} "
              f"word={r['best_odd_defect_word']}")
        for word, nonalt, growth, drift in r["starts_r_examples"]:
            print(f"  STARTS-R survivor nonalt={nonalt} growth={growth} "
                  f"drift={drift} word={word}")
        if args.diagnostics:
            for word, growth, drift in r["extremal_examples"]:
                print(f"  EXTREMAL growth={growth} drift={drift} word={word}")
        for word in r["hits"]:
            print(f"  HIT {word}")
        if args.diagnostics:
            for sig, count in r["failure_counts"].most_common(12):
                print(f"  FAIL {count:8,d} {sig} example={r['failure_examples'][sig]}")
            print("  failures among odd-class-identity survivors:")
            for sig, count in r["odd_identity_failure_counts"].most_common(12):
                print(f"    ODD-ID FAIL {count:8,d} {sig} "
                      f"example={r['failure_examples'][sig]}")


if __name__ == "__main__":
    main()
