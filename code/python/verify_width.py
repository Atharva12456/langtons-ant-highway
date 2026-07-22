"""Checks for the width-two exclusion (Theorem: no periodic highway has W = 2).

IMPORTANT CORRECTION.  An earlier version of this file simulated the strip as a
one-dimensional automaton in which every site's FIRST visit turns R:

    turn = 'R' if visits % 2 == 1 else 'L'          # WRONG

That is not implied by the realisability criterion.  Condition (ii) of the criterion
constrains only the STABILISED word of a translation class, i.e. the chronological
turn sequence at a cell all of whose phases have occurred.  Cells below their class's
maximum level may legitimately begin with L - indeed the paper's own seed
construction blackens exactly such cells.  So "unvisited" does not mean "white", and
a site's first turn is not forced to be R.

The theorem is nevertheless true, and the proof in the paper no longer uses that
assumption.  It runs on an EDGE budget instead:

  * an upward excursion out of site l uses the line-0 cell U_l, and a downward
    excursion out of site l uses the line-2 cell D_l;
  * distinct sites use distinct cells, and by the extremal-line theorem each such
    cell is entered at most once by the whole periodic trace;
  * hence the gap (l, l+1) is crossed at most once upward (from l) and at most once
    downward (from l+1);
  * drift +m forces the net crossing number of every gap above the start to be
    exactly +1, so each such gap is crossed exactly once upward and never downward;
  * therefore every site above the start is entered exactly once, arriving heading
    south and departing east, so its unique turn is L;
  * such a site's translation class is a singleton whose stabilised word is the
    single letter L, contradicting condition (ii).

This file checks the two facts the argument actually rests on, and additionally runs
an ADVERSARIAL search in which the colour of every previously unvisited site is
chosen by an adversary - which is exactly the freedom the old simulation wrongly
denied.  No adversary can survive, which is independent confirmation.
"""
from __future__ import annotations

import itertools

from explore_chronology import DX, DY, walk
from verify_extremal import p3_valid, tfun

NAME = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
R = lambda q: (q + 1) % 4
L = lambda q: (q + 3) % 4


def check_geometry():
    """The forced excursions and the arrival/departure headings used in the proof."""
    print("=== geometry underlying the proof ===")
    dt = {q: DX[q] + DY[q] for q in range(4)}
    print(f"  t=x+y increments: {{{', '.join(f'{NAME[q]}:{dt[q]:+d}' for q in range(4))}}}")
    ok = dt[1] == 1 and dt[0] == 1 and dt[3] == -1 and dt[2] == -1
    print(f"  east,north increase t and west,south decrease it: {ok}")

    # upward excursion: line-1 cell z -> east to line 0 -> forced R -> south -> z+e
    z = (0, 0)
    up = (z[0] + DX[1], z[1] + DY[1])
    land = (up[0] + DX[R(1)], up[1] + DY[R(1)])
    up_ok = (land[0] - z[0], land[1] - z[1]) == (1, -1) and R(1) == 2
    print(f"  upward excursion {z}->{up}->{land} = z+e, leaving line 0 heading "
          f"{NAME[R(1)]}: {up_ok}")

    # downward excursion: z -> west to line 2 -> forced R -> north -> z-e
    dn = (z[0] + DX[3], z[1] + DY[3])
    land2 = (dn[0] + DX[R(3)], dn[1] + DY[R(3)])
    dn_ok = (land2[0] - z[0], land2[1] - z[1]) == (-1, 1) and R(3) == 0
    print(f"  downward excursion {z}->{dn}->{land2} = z-e, leaving line 2 heading "
          f"{NAME[R(3)]}: {dn_ok}")

    # the turn read off in the last step of the proof
    turn_ok = L(2) == 1 and R(2) == 3
    print(f"  arrival heading south + departure east => turn L "
          f"(L(S)={NAME[L(2)]}, R(S)={NAME[R(2)]}): {turn_ok}")
    return ok and up_ok and dn_ok and turn_ok


def adversarial(budget=9):
    """Adversary picks the colour of each newly seen site; can the ant survive?

    Survival means: never crossing a gap twice in the same direction (the edge budget
    the extremal-line theorem imposes).  A width-two highway would have to survive
    forever, so any finite bound refutes it.  The adversary is unconstrained apart
    from using at most `budget` black seeds, which is the only finiteness the
    finite-support hypothesis supplies.
    """
    print(f"\n=== adversarial search over all finite seeds (budget {budget}) ===")
    best = {}
    for k in range(budget + 1):
        # state: pos, dir, dict site->visits, dict gap->(up,down), seeds used
        best_len = 0
        stack = [(0, +1, {}, {}, 0, 0)]
        while stack:
            pos, dirn, vis, gaps, used, steps = stack.pop()
            best_len = max(best_len, steps)
            opts = []
            if pos in vis:
                opts = [vis[pos]]          # colour already determined by history
            else:
                opts = [0, 1] if used < k else [0]   # adversary may seed black
            for col in opts:
                nvis = dict(vis)
                seed = 1 if (pos not in vis and col == 1) else 0
                # white -> R (reverse), black -> L (continue), then the cell flips
                nd = -dirn if col == 0 else dirn
                nvis[pos] = 1 - col
                gap = (pos, pos + 1) if nd > 0 else (pos - 1, pos)
                key = gap
                up, down = gaps.get(key, (0, 0))
                if nd > 0:
                    up += 1
                else:
                    down += 1
                if up > 1 or down > 1:
                    continue               # violates the edge budget: dead
                ngaps = dict(gaps)
                ngaps[key] = (up, down)
                if steps + 1 < 400:
                    stack.append((pos + nd, nd, nvis, ngaps, used + seed, steps + 1))
        best[k] = best_len
        print(f"  seeds<= {k}: longest surviving run = {best_len} steps")
    unbounded = any(v >= 399 for v in best.values())
    print(f"  any adversary survived to the step cap? {unbounded}  "
          f"(False = no width-two highway)")
    return not unbounded


def width_scan(maxlen):
    from collections import defaultdict
    tab = defaultdict(lambda: [0, 0])
    for Lw in range(4, maxlen + 1):
        for bits in itertools.product('RL', repeat=Lw):
            w = ''.join(bits)
            pts, arr, hfin, d = walk(w)
            if hfin != 0 or d == (0, 0):
                continue
            t = tfun(d)
            if t is None:
                continue
            ts = [t(p) for p in pts]
            ok, *_ = p3_valid(w)
            tab[max(ts) - min(ts)][0] += 1
            if ok:
                tab[max(ts) - min(ts)][1] += 1
    return tab


if __name__ == "__main__":
    import sys
    g = check_geometry()
    a = adversarial()
    ml = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    print(f"\n=== brute force: transverse width vs realisability (len <= {ml}) ===")
    tab = width_scan(ml)
    print(f"  {'width':>6} {'words':>10} {'realisable':>11}")
    for wd in sorted(tab):
        tot, ok = tab[wd]
        print(f"  {wd:>6} {tot:>10,} {ok:>11}")
    print(f"\nRESULT: geometry={g}  adversarial-refutation={a}")
