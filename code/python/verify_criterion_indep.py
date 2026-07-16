"""Independent re-implementation of the periodic-realisability criterion.

Purpose (external review, round 7, point 2): the two Java engines share one
enumeration framework, one data representation, and ONE exact-criterion checker.
A shared bug in that checker would affect both identically.  This module is a
deliberately independent verifier:

  * it is written from the STATEMENT of Theorem 3.1 in the paper, not from the
    Java source;
  * it builds translation classes by explicit pairwise membership tests plus
    union-find, NOT by the Java's arithmetic reduction + global sort;
  * it evaluates the LITERAL criterion -- every S_{I,n} for
    min_I a_i <= n <= max_I a_i -- rather than the single stabilised word that
    Remark 3.2 licenses.  This independently exercises Remark 3.2 itself, which
    is otherwise an unverified reduction sitting in the certification path.

`criterion_literal`  = literal Theorem 3.1.
`criterion_onesort`  = the Java engines' Remark 3.2 shortcut, re-coded here.
Agreement of the two over large word sets tests both the checker and Remark 3.2.
"""
from __future__ import annotations

DX = {0: 0, 1: 1, 2: 0, 3: -1}   # 0=N, 1=E, 2=S, 3=W
DY = {0: 1, 1: 0, 2: -1, 3: 0}


def path(word):
    """Induced path p_0..p_N, final heading, drift. R='R' turns right."""
    x = y = 0
    d = 0
    pts = []
    for ch in word:
        pts.append((x, y))
        d = (d + 1) % 4 if ch == 'R' else (d + 3) % 4
        x += DX[d]
        y += DY[d]
    return pts, d, (x, y)


def _multiple(delta, drift):
    """Is delta an integer multiple of drift?  Exact integer test."""
    ax, ay = drift
    dx, dy = delta
    if ax != 0:
        if dx % ax != 0:
            return False
        k = dx // ax
        return k * ay == dy
    if dx != 0:
        return False
    if dy % ay != 0:
        return False
    return True


def classes_unionfind(pts, drift):
    """Group phases by i~j iff p_i-p_j in Z*drift, via explicit pairwise tests."""
    n = len(pts)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for i in range(n):
        for j in range(i + 1, n):
            if _multiple((pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]), drift):
                union(i, j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def _levels(idx, pts, drift):
    """a_i with p_i = b_I + a_i*drift, b_I the class member of least level."""
    ax, ay = drift
    base = idx[0]
    lv = {}
    for i in idx:
        dx = pts[i][0] - pts[base][0]
        dy = pts[i][1] - pts[base][1]
        k = dx // ax if ax != 0 else dy // ay
        lv[i] = k
    m = min(lv.values())
    return {i: lv[i] - m for i in idx}     # shift so min level is 0


def criterion_literal(word):
    """LITERAL Theorem 3.1: check every S_{I,n}, min a_i <= n <= max a_i."""
    pts, heading, drift = path(word)
    if heading != 0 or drift == (0, 0):
        return False
    for idx in classes_unionfind(pts, drift):
        a = _levels(idx, pts, drift)
        amin, amax = min(a.values()), max(a.values())
        for n in range(amin, amax + 1):
            members = [i for i in idx if a[i] <= n]
            members.sort(key=lambda i: (n - a[i], i))
            s = [word[i] for i in members]
            for u, v in zip(s, s[1:]):          # (i) strict alternation
                if u == v:
                    return False
            if n == amax:                        # (ii) stabilised starts with R
                if not s or s[0] != 'R':
                    return False
    return True


def criterion_onesort(word):
    """The Java engines' Remark 3.2 shortcut, re-coded independently."""
    pts, heading, drift = path(word)
    if heading != 0 or drift == (0, 0):
        return False
    for idx in classes_unionfind(pts, drift):
        a = _levels(idx, pts, drift)
        order = sorted(idx, key=lambda i: (-a[i], i))
        s = [word[i] for i in order]
        if not s or s[0] != 'R':
            return False
        for u, v in zip(s, s[1:]):
            if u == v:
                return False
    return True
