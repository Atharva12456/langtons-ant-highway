"""Correct criterion implementation via exact union-find; confirm 11-cell seed."""
U = {0:(0,1),1:(1,0),2:(0,-1),3:(-1,0)}
def sim_from_seed(black0,N,p0=(0,0),q0=0):
    black=set(black0);p=p0;q=q0;turns=[]
    for _ in range(N):
        if p in black: q=(q-1)%4;black.discard(p);turns.append('L')
        else: q=(q+1)%4;black.add(p);turns.append('R')
        dx,dy=U[q];p=(p[0]+dx,p[1]+dy)
    return ''.join(turns),p,q,len(black)-len(black0)
def path(w,p0=(0,0),q0=0):
    p=p0;q=q0;pos=[p]
    for c in w:
        q=(q-1)%4 if c=='L' else (q+1)%4
        dx,dy=U[q];p=(p[0]+dx,p[1]+dy);pos.append(p)
    return pos,q

def is_mult_of_d(dx,dy,a,b):
    """is (dx,dy) an integer multiple of (a,b)?  return k or None."""
    # need dx=k*a, dy=k*b for one integer k
    if a!=0:
        if dx % a != 0: return None
        k=dx//a
        return k if k*b==dy else None
    else: # a==0, b!=0
        if dx!=0: return None
        if dy % b != 0: return None
        return dy//b

def criterion_seed(w,q0=0):
    pos,qf=path(w,q0=q0);N=len(w)
    a,b=pos[N][0]-pos[0][0],pos[N][1]-pos[0][1]
    assert qf==q0 and (a,b)!=(0,0)
    # union-find over phases 0..N-1
    parent=list(range(N))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]];x=parent[x]
        return x
    for i in range(N):
        for j in range(i+1,N):
            dx=pos[i][0]-pos[j][0];dy=pos[i][1]-pos[j][1]
            if is_mult_of_d(dx,dy,a,b) is not None:
                parent[find(i)]=find(j)
    from collections import defaultdict
    cls=defaultdict(list)
    for i in range(N): cls[find(i)].append(i)
    seed=set(); all_ok=True; nbad=0
    for phases in cls.values():
        base=pos[phases[0]]
        lvl={}
        for i in phases:
            k=is_mult_of_d(pos[i][0]-base[0],pos[i][1]-base[1],a,b)
            assert k is not None; lvl[i]=k
        amin=min(lvl.values());amax=max(lvl.values())
        def S(n):
            items=sorted((n-lvl[i],i) for i in phases if lvl[i]<=n)
            return ''.join(w[i] for _,i in items)
        for n in range(amin,amax+1):
            s=S(n)
            if any(s[t]==s[t+1] for t in range(len(s)-1)): all_ok=False;nbad+=1
        if not S(amax).startswith('R'): all_ok=False;nbad+=1
        for n in range(amin,amax):
            if S(n).startswith('L'): seed.add((base[0]+n*a,base[1]+n*b))
    return seed,all_ok,(a,b),nbad

W="RRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLL"
seed,ok,d,nbad=criterion_seed(W)
print("criterion holds:",ok," nbad:",nbad," drift:",d," |seed|:",len(seed))
print("seed:",sorted(seed))
wv,pv,qv,gv=sim_from_seed(seed,104)
print("reproduces printed word:",wv==W," drift:",pv," reset:",qv==0)
# compare to reviewer 11-cell
rev=set([(-2,-2),(-2,-1),(-1,0),(0,1),(1,-2),(1,1),(2,-2),(2,0),(3,-1),(3,0),(4,0)])
print("matches reviewer 11-cell seed:",seed==rev)
print("|B_n| formula: n-th period boundary black count = ",len(seed),"+ 12n")

# ---- reviewer issue #2: RL word and realisability through length 18 ----
print("\n=== RL and realisability audit through length 18 ===")
def analyze(w):
    pos,qf=path(w);a,b=pos[-1][0]-pos[0][0],pos[-1][1]-pos[0][1]
    return qf==0,(a,b),w.count('R')-w.count('L')
r,dd,gg=analyze("RL")
print("RL: reset",r," drift",dd," g",gg)
# enumerate all words len<=18, count heading-reset nonzero-drift, and those passing criterion
from itertools import product
cnt_all=cnt_hr=cnt_hrnz=cnt_pass=0
for L in range(1,19):
    for tup in product('RL',repeat=L):
        w=''.join(tup); cnt_all+=1
        pos,qf=path(w)
        if qf!=0: continue
        cnt_hr+=1
        a,b=pos[-1][0]-pos[0][0],pos[-1][1]-pos[0][1]
        if (a,b)==(0,0): continue
        cnt_hrnz+=1
        try:
            s,okk,dd2,nb=criterion_seed(w)
            if okk: cnt_pass+=1
        except Exception:
            pass
print(f"all words len<=18: {cnt_all}")
print(f"heading-reset: {cnt_hr}")
print(f"heading-reset & nonzero-drift: {cnt_hrnz}")
print(f"...of those, PASSING criterion (realisable highways): {cnt_pass}")

# ---- reviewer round-2: corrected coset invariant (Bezout key) ----
def _egcd(a,b):
    if b==0: return (a,1,0)
    g,x,y=_egcd(b,a%b); return (g,y,x-(a//b)*y)
def coset_key(x,y,d):
    from math import gcd
    a,b=d; g=gcd(abs(a),abs(b)); ap,bp=a//g,b//g
    _,r,s=_egcd(ap,bp)  # r*ap+s*bp=1
    return (bp*x-ap*y, (r*x+s*y)%g)
if __name__=='__main__':
    # sanity: key is a complete Z^2/Zd invariant for d=(2,2)
    def mult(p,q,d):
        a,b=d;dx,dy=p[0]-q[0],p[1]-q[1]
        return (dx%a==0 and (dx//a)*b==dy) if a else (dx==0 and dy%b==0)
    d=(2,2);pts=[(x,y) for x in range(-4,5) for y in range(-4,5)];bad=0
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            if (coset_key(*pts[i],d)==coset_key(*pts[j],d))!=mult(pts[i],pts[j],d): bad+=1
    print('corrected coset key mismatches for d=(2,2):',bad)
