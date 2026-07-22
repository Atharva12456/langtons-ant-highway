"""Transverse skeleton of a periodic highway.

For drift d, write d = m * e with e primitive and m = gcd(|a|,|b|) >= 1.
Translation classes are orbits of Z*d, NOT of Z*e.  So a class is indexed by
  * a transverse coordinate  t  (an integer linear functional killing e), and
  * a longitudinal residue   r  in Z/m'  along e,
where the longitudinal step of d is m' units of e.

For the standard highway d = (2,-2) = 2*(1,-1): t = x+y is invariant along e,
and u = x-y advances by 4 per period, so the class label is (t, u mod 4).

The point of interest: the ODD classes are exactly the permanent wake strands.
Their (t, r) distribution is the "residue skeleton" that Theorem 7.1 constrains.
"""
from __future__ import annotations

from math import gcd

from explore_chronology import STD, analyse, walk


def skeleton(word, label=""):
    N = len(word)
    pts, arr, hfin, d = walk(word)
    a, b = d
    m = gcd(abs(a), abs(b))
    e = (a // m, b // m)          # primitive drift direction
    # transverse functional killing e: t(x,y) = b'*x - a'*y  with e=(a',b')
    ap, bp = e
    tf = lambda p: bp * p[0] - ap * p[1]
    # longitudinal functional: any lf with lf(e) = 1 (Bezout)
    # find s,u with s*ap + u*bp = 1
    def bezout(p, q):
        old_r, r = p, q
        old_s, s = 1, 0
        old_t, t = 0, 1
        while r:
            k = old_r // r
            old_r, r = r, old_r - k * r
            old_s, s = s, old_s - k * s
            old_t, t = t, old_t - k * t
        return old_r, old_s, old_t
    _, s, u = bezout(ap, bp)
    lf = lambda p: s * p[0] + u * p[1]      # lf(e) = 1
    # d advances lf by m, so class label = (t, lf mod m)
    lab = lambda p: (tf(p), lf(p) % m if m > 1 else 0)

    from collections import defaultdict
    cnt = defaultdict(int)
    for p in pts:
        cnt[lab(p)] += 1

    odd = {k: v for k, v in cnt.items() if v % 2 == 1}
    even = {k: v for k, v in cnt.items() if v % 2 == 0}
    ts = sorted({k[0] for k in cnt})
    print(f"=== skeleton: {label} ===")
    print(f"  N={N} drift={d} primitive e={e} m={m}  #classes={len(cnt)} "
          f"#odd={len(odd)}  growth={word.count('R')-word.count('L')}")
    print(f"  transverse range t in [{min(ts)},{max(ts)}]  ({len(ts)} distinct t)")
    print(f"  {'t':>5} | {'classes (r:size)':<34} | odd count")
    for t in ts:
        row = sorted((k[1], v) for k, v in cnt.items() if k[0] == t)
        nodd = sum(1 for _, v in row if v % 2 == 1)
        cells = " ".join(f"{r}:{v}" for r, v in row)
        print(f"  {t:>5} | {cells:<34} | {nodd}")
    # per-transverse-line odd counts
    per = {t: sum(1 for k, v in cnt.items() if k[0] == t and v % 2 == 1) for t in ts}
    print(f"  odd-per-t multiset: {sorted(per.values())}")
    print(f"  total odd = {sum(per.values())} (should equal growth)")
    return cnt, per


if __name__ == "__main__":
    skeleton(STD, "standard period-104 highway")
