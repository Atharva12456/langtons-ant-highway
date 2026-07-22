"""Verification of the extremal-line theorem for periodic highways.

CLAIM (diagonal drift).  Let w be a finite-support-realisable periodic trace of
length N with drift d = (a,b) satisfying |a| = |b| = m > 0.  Put t(x,y) = x+y if
ab < 0, and t(x,y) = x-y if ab > 0, so that t(d) = 0 and every unit step changes
t by exactly +-1.  Let T = max_i t(p_i) and T' = min_i t(p_i).  Then:

  (E1) every cell on the line t = T is visited exactly ONCE per period, and
       likewise on t = T';
  (E2) all arrivals on those two lines are HORIZONTAL (E or W);
  (E3) every turn on those two lines is R;
  (E4) T - T' is even.

PROOF SKETCH.  d preserves t, so the transverse range is period-independent.
A step changes t by +-1, so the ant reaches t=T from t=T-1: the arrival heading
increases t.  All cells on a fixed t-line share one checkerboard parity, so by
the HV partition their arrivals are all vertical or all horizontal.
  * vertical case: the only vertical heading increasing t is the one whose turn-R
    image also increases t, so R would leave the strip; hence every turn on the
    line is L, contradicting P3(ii) (the stabilised word starts with R).
  * horizontal case: the turn that would keep increasing t is excluded, so every
    turn on the line is R; by P3(i) the stabilised word alternates, so a cell
    visited twice would read RR.  Hence each cell is visited once.
Both extremal lines are therefore of the same (horizontal) parity class, so
T = T' mod 2.

This file verifies the claim and, more importantly, its CONTRAPOSITIVE content:
every word whose extremal line carries a repeated cell must fail P3.
"""
from __future__ import annotations

import itertools
from math import gcd

from explore_chronology import STD, classes_of, walk

NAME = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
HORIZ = {1, 3}


def tfun(d):
    """Transverse functional with t(d)=0 and |t(step)|=1, for diagonal drift."""
    a, b = d
    if abs(a) != abs(b) or a == 0:
        return None
    if a * b < 0:
        return lambda p: p[0] + p[1]
    return lambda p: p[0] - p[1]


def p3_valid(word):
    N = len(word)
    pts, arr, hfin, d = walk(word)
    if hfin != 0 or d == (0, 0):
        return False, d, pts, arr
    for idx in classes_of(pts, d):
        a0, b0 = d
        base = idx[0]
        lv = {}
        for i in idx:
            dx = pts[i][0] - pts[base][0]
            dy = pts[i][1] - pts[base][1]
            lv[i] = dx // a0 if a0 else dy // b0
        order = sorted(idx, key=lambda i: (i - N * lv[i]))
        turns = [word[i] for i in order]
        if turns[0] != 'R':
            return False, d, pts, arr
        if any(u == v for u, v in zip(turns, turns[1:])):
            return False, d, pts, arr
    return True, d, pts, arr


def extremal_report(word, label=""):
    ok, d, pts, arr = p3_valid(word)
    t = tfun(d)
    if t is None:
        print(f"{label}: drift {d} not diagonal - theorem does not apply")
        return
    ts = [t(p) for p in pts]
    T, Tp = max(ts), min(ts)
    print(f"=== {label} ===")
    print(f"  N={len(word)} drift={d} P3={ok}  t-range [{Tp},{T}]  "
          f"width={T-Tp} (even? {(T-Tp) % 2 == 0})")
    for lvl, nm in ((T, 'MAX'), (Tp, 'MIN')):
        ph = [i for i, v in enumerate(ts) if v == lvl]
        cells = {}
        for i in ph:
            cells.setdefault(pts[i], []).append(i)
        arrs = {NAME[arr[i]] for i in ph}
        turns = {word[i] for i in ph}
        pars = {(pts[i][0] + pts[i][1]) % 2 for i in ph}
        mult = sorted(len(v) for v in cells.values())
        print(f"  t={lvl:<4}({nm}) phases={len(ph)} cells={len(cells)} "
              f"per-cell visits={mult} arrivals={sorted(arrs)} turns={sorted(turns)} "
              f"parities={sorted(pars)}")
        print(f"        E1 all-once={all(m == 1 for m in mult)}  "
              f"E2 horizontal={all(arr[i] in HORIZ for i in ph)}  "
              f"E3 all-R={turns <= {'R'}}")


def dihedral(word):
    """The 8 dihedral images of a turn word: rotations fix it, reflections swap R/L."""
    swap = word.translate(str.maketrans('RL', 'LR'))
    return {'identity': word, 'reflected': swap}


def exhaustive_contrapositive(maxlen):
    """Every word whose extremal line repeats a cell must FAIL P3."""
    print(f"\n=== exhaustive contrapositive check, lengths <= {maxlen} ===")
    tested = viol = p3ok = diag = 0
    for L in range(4, maxlen + 1):
        for bits in itertools.product('RL', repeat=L):
            w = ''.join(bits)
            pts, arr, hfin, d = walk(w)
            if hfin != 0 or d == (0, 0):
                continue
            t = tfun(d)
            if t is None:
                continue
            diag += 1
            ts = [t(p) for p in pts]
            for lvl in (max(ts), min(ts)):
                ph = [i for i, v in enumerate(ts) if v == lvl]
                cells = {}
                for i in ph:
                    cells.setdefault(pts[i], []).append(i)
                if any(len(v) > 1 for v in cells.values()):
                    tested += 1
                    ok, *_ = p3_valid(w)
                    if ok:
                        viol += 1
                        print(f"   *** COUNTEREXAMPLE {w} drift={d} ***")
                    break
            else:
                ok, *_ = p3_valid(w)
                if ok:
                    p3ok += 1
    print(f"  diagonal-drift heading-reset words: {diag:,}")
    print(f"  words with a repeated extremal cell: {tested:,}")
    print(f"  ... of those, P3-VALID (must be 0):  {viol}")
    print(f"  P3-valid words with all-once extremal lines: {p3ok}")
    return viol == 0


if __name__ == "__main__":
    extremal_report(STD, "standard period-104 highway")
    extremal_report(STD * 2, "standard squared (period 208)")
    for nm, w in dihedral(STD).items():
        if nm != 'identity':
            extremal_report(w, f"standard {nm}")
    import sys
    ml = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    good = exhaustive_contrapositive(ml)
    print(f"\nRESULT: contrapositive holds = {good}")
