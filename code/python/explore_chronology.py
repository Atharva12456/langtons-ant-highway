"""Chronological structure of periodic highway traces.

Static/incidence arguments are exhausted (journal 31.3): every residue equation,
drift/growth skeleton, and within-period alternation check is satisfied by explicit
non-realisable countermodels.  What kills those countermodels is CROSS-PERIOD order.
This module computes the chronological data exactly so patterns can be found and
then proved.

Notation follows the paper.  For a heading-resetting word w of length N with drift
d != 0:
  * phases i = 0..N-1 sit at path points p_i;
  * i ~ j iff p_i - p_j in Z*d;  classes are the translation classes;
  * within a class, p_i = b_I + a_i*d for integer levels a_i;
  * the physical cell b_I + n*d is visited by phase i at absolute time
        t = i + (n - a_i)*N,
    so the chronological order at EVERY cell of the class is by the key
        kappa_i = i - N*a_i,
    which is independent of n.  This is why the stabilised word is well defined.
"""
from __future__ import annotations

DX = {0: 0, 1: 1, 2: 0, 3: -1}   # 0=N 1=E 2=S 3=W
DY = {0: 1, 1: 0, 2: -1, 3: 0}
NAME = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}

STD = ("RRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRR"
       "LLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLL")


def walk(word):
    """Return (points, arrival_heading_at_each_phase, final_heading, drift).

    Convention: the ant is AT p_i when it reads w_i.  `arr[i]` is the heading it
    was travelling on when it arrived at p_i (i.e. the heading after the turn at
    the previous phase).  arr[0] is the initial heading.
    """
    x = y = 0
    d = 0
    pts, arr = [], []
    for ch in word:
        pts.append((x, y))
        arr.append(d)
        d = (d + 1) % 4 if ch == 'R' else (d + 3) % 4
        x += DX[d]
        y += DY[d]
    return pts, arr, d, (x, y)


def _is_multiple(delta, drift):
    ax, ay = drift
    dx, dy = delta
    if ax != 0:
        if dx % ax:
            return False
        k = dx // ax
        return k * ay == dy
    if dx:
        return False
    if dy % ay:
        return False
    return True


def classes_of(pts, drift):
    n = len(pts)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            di = (pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if _is_multiple(di, drift):
                ra, rb = find(i), find(j)
                if ra != rb:
                    parent[max(ra, rb)] = min(ra, rb)
    g = {}
    for i in range(n):
        g.setdefault(find(i), []).append(i)
    return list(g.values())


def levels(idx, pts, drift):
    ax, ay = drift
    base = idx[0]
    lv = {}
    for i in idx:
        dx = pts[i][0] - pts[base][0]
        dy = pts[i][1] - pts[base][1]
        lv[i] = dx // ax if ax else dy // ay
    m = min(lv.values())
    return {i: lv[i] - m for i in idx}


def analyse(word, label=""):
    N = len(word)
    pts, arr, hfinal, drift = walk(word)
    g = word.count('R') - word.count('L')
    out = {
        'label': label, 'N': N, 'growth': g, 'drift': drift,
        'heading_reset': hfinal == 0,
    }
    cls = classes_of(pts, drift)
    recs = []
    for idx in cls:
        a = levels(idx, pts, drift)
        # chronological key: kappa = i - N*a_i  (smaller = earlier)
        order = sorted(idx, key=lambda i: (i - N * a[i]))
        turns = [word[i] for i in order]
        alt = all(u != v for u, v in zip(turns, turns[1:]))
        recs.append({
            'phases': order,
            'levels': [a[i] for i in order],
            'kappa': [i - N * a[i] for i in order],
            'turns': ''.join(turns),
            'size': len(idx),
            'odd': len(idx) % 2 == 1,
            'alternates': alt,
            'starts_R': turns[0] == 'R',
            'arrivals': ''.join(NAME[arr[i]] for i in order),
            'cellparity': (pts[idx[0]][0] + pts[idx[0]][1]) % 2,
        })
    out['classes'] = recs
    out['num_classes'] = len(recs)
    out['num_odd'] = sum(1 for r in recs if r['odd'])
    out['p3_valid'] = all(r['alternates'] and r['starts_R'] for r in recs)
    out['sizes'] = sorted(r['size'] for r in recs)
    return out


def report(a, show_classes=False):
    print(f"=== {a['label']} ===")
    print(f"  N={a['N']}  growth={a['growth']}  drift={a['drift']}  "
          f"heading_reset={a['heading_reset']}")
    print(f"  classes={a['num_classes']}  odd classes={a['num_odd']}  "
          f"(growth == #odd? {a['growth'] == a['num_odd']})")
    print(f"  class sizes: {a['sizes']}")
    print(f"  P3 valid: {a['p3_valid']}")
    if show_classes:
        for r in a['classes']:
            flag = '' if (r['alternates'] and r['starts_R']) else '   <-- FAILS'
            print(f"    size={r['size']} par={r['cellparity']} turns={r['turns']:<8}"
                  f" arrivals={r['arrivals']:<8} levels={r['levels']}{flag}")


if __name__ == "__main__":
    a = analyse(STD, "standard period-104 highway")
    report(a, show_classes=True)
