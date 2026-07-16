"""Rigorous check of Remark 4.4 (no monotone affine combination of (E,V,k,beta)).

Tait graph of a black set B (paper eq. (4.1)):
    e_z = {(x,y-1),(x-1,y)}   if x+y even
        = {(x-1,y-1),(x,y)}   if x+y odd
E = |B| (z -> e_z is injective), V = #endpoints, k = #components, beta = E - V + k.

Since beta = E - V + k identically, every affine combination
    a*E + b*V + c*k + d*beta + e
equals (a+d)*E + (b-d)*V + (c+d)*k + e.  So the space of affine combinations of
(E,V,k,beta) IS the space of affine combinations of (E,V,k), and "nonconstant"
means the reduced vector (a+d, b-d, c+d) is nonzero.  The claim therefore reduces
to: no nonzero linear functional on (E,V,k) is monotone along the orbit.

Certificate: exhibit four observed one-step change vectors v1..v4 in Z^3 and
positive rationals lam_i summing to 1 with sum lam_i v_i = 0.  Then 0 lies in the
INTERIOR of conv{v1..v4}, hence for every nonzero c some observed step has
c.v > 0 and some has c.v < 0 -- so no nonzero c is monotone.  Exact arithmetic.
"""
from fractions import Fraction
from itertools import combinations

DX = {0: 0, 1: 1, 2: 0, 3: -1}   # 0=N,1=E,2=S,3=W
DY = {0: 1, 1: 0, 2: -1, 3: 0}


def tait_edge(z):
    x, y = z
    if (x + y) % 2 == 0:
        return ((x, y - 1), (x - 1, y))
    return ((x - 1, y - 1), (x, y))


def evk(black):
    """Return (E, V, k) of the Tait subgraph induced by the black cells."""
    edges = [tait_edge(z) for z in black]
    E = len(edges)
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    V = len(adj)
    seen, k = set(), 0
    for s in adj:
        if s in seen:
            continue
        k += 1
        stack = [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return E, V, k


def run(steps):
    black = set()
    x = y = 0
    d = 0
    vecs = set()
    prev = evk(black)
    for t in range(steps):
        if (x, y) in black:          # black: turn left, whiten
            d = (d + 3) % 4
            black.discard((x, y))
        else:                        # white: turn right, blacken
            d = (d + 1) % 4
            black.add((x, y))
        cur = evk(black)
        vecs.add(tuple(c - p for c, p in zip(cur, prev)))
        prev = cur
        x += DX[d]
        y += DY[d]
    return vecs


def rank3(vs):
    """Exact rank of a list of integer 3-vectors."""
    M = [[Fraction(c) for c in v] for v in vs]
    r = 0
    for c in range(3):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def symmetric_spanning_certificate(vecs):
    """The decisive test.

    If the observed change set S is centrally symmetric (v in S => -v in S) and
    spans R^3, then 0 lies in the interior of conv(S) and NO nonzero functional
    is monotone.  Proof: let c != 0.  Since span(S) = R^3 there is v in S with
    c.v != 0.  Replacing v by -v in S if needed, c.v > 0; then c.(-v) < 0 and
    -v is also an observed step.  So c strictly increases at one step and
    strictly decreases at another.  No LP or hull computation is required.
    """
    sym = all(tuple(-c for c in v) in vecs for v in vecs)
    rk = rank3(sorted(vecs))
    basis = []
    for v in sorted(vecs):
        if rank3(basis + [v]) > len(basis):
            basis.append(v)
    return sym, rk, basis


def zero_in_interior(vecs):
    """Find 4 vectors whose open convex hull contains 0. Exact rationals."""
    vl = sorted(vecs)
    for quad in combinations(vl, 4):
        # Solve sum lam_i v_i = 0, sum lam_i = 1 (4x4 exact linear system).
        A = [[Fraction(quad[j][i]) for j in range(4)] for i in range(3)]
        A.append([Fraction(1)] * 4)
        b = [Fraction(0), Fraction(0), Fraction(0), Fraction(1)]
        M = [row[:] + [b[i]] for i, row in enumerate(A)]
        n = 4
        piv_rows = []
        r = 0
        for c in range(n):
            p = next((i for i in range(r, n) if M[i][c] != 0), None)
            if p is None:
                continue
            M[r], M[p] = M[p], M[r]
            pv = M[r][c]
            M[r] = [v / pv for v in M[r]]
            for i in range(n):
                if i != r and M[i][c] != 0:
                    f = M[i][c]
                    M[i] = [a - f * bb for a, bb in zip(M[i], M[r])]
            piv_rows.append(c)
            r += 1
        if r != n:
            continue                      # singular: not affinely independent
        lam = [M[i][n] for i in range(n)]
        if all(l > 0 for l in lam):
            return quad, lam
    return None, None


if __name__ == "__main__":
    STEPS = 12000
    vecs = run(STEPS)
    print(f"distinct one-step change vectors (dE,dV,dk) over {STEPS} steps: {len(vecs)}")
    for v in sorted(vecs):
        print("   ", v)
    sym, rk, basis = symmetric_spanning_certificate(vecs)
    print()
    print("=== symmetry / spanning certificate ===")
    print(f"  centrally symmetric (v in S => -v in S): {sym}")
    print(f"  rank of span(S) over Q: {rk} (need 3)")
    print(f"  spanning subset: {basis}")
    if sym and rk == 3:
        print("  => 0 is in the INTERIOR of conv(S).")
        print("  => for every nonzero c, some observed step has c.v>0 and another c.v<0")
        print("  => no nonconstant affine combination of (E,V,k,beta) is monotone. QED")
    else:
        print("  => certificate FAILED; the claim must be softened.")

    quad, lam = zero_in_interior(vecs)
    print()
    print("=== (secondary) single-tetrahedron certificate ===")
    if quad:
        print("CERTIFICATE: 0 is in the INTERIOR of conv of these observed vectors")
        for v, l in zip(quad, lam):
            print(f"   lambda={str(l):>10}  v={v}")
        chk = [sum(l * Fraction(v[i]) for v, l in zip(quad, lam)) for i in range(3)]
        print(f"   sum lambda_i v_i = {tuple(chk)}   sum lambda_i = {sum(lam)}")
        print("   => every nonzero linear functional on (E,V,k) strictly increases")
        print("      at some step and strictly decreases at another: NOT monotone.")
        print("   => no nonconstant affine combination of (E,V,k,beta) is monotone. QED")
    else:
        print("  none (expected: a symmetric set has 0 on every tetrahedron boundary)")
