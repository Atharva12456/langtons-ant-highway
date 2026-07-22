"""Check the Section-8 token claim: eta(s)+eta(t)=C_x+R_y (not 0), and >=4 cells."""
U={0:(0,1),1:(1,0),2:(0,-1),3:(-1,0)}
def eta(p,q):        # token of state (pos,heading)
    return ('C',p[0]) if q in (0,2) else ('R',p[1])

# run blank orbit, record (pos,dir,turn) and the black set snapshot indices
black=set(); p=(0,0); q=0
events=[]   # (t, pos, dir_before, turn, black_after_snapshot_id)
snaps=[]    # black set copies (sparse: store frozenset) -- only when needed
STEPS=3000
history=[]
for t in range(STEPS):
    pre=(p,q)
    if p in black:
        q2=(q-1)%4; turn='L'; black.discard(p)
    else:
        q2=(q+1)%4; turn='R'; black.add(p)
    # state IMMEDIATELY AFTER this visit's turn+move:
    dx,dy=U[q2]; np=(p[0]+dx,p[1]+dy)
    history.append(dict(t=t, cell=p, q_before=q, turn=turn,
                        state_after=(np,q2), black_after=frozenset(black)))
    p=np; q=q2

# find first R-to-L lifetime: cell z visited with R at time t1, next visit L at t2
from collections import defaultdict
visits=defaultdict(list)
for h in history: visits[h['cell']].append(h)
found=None
for z,vs in visits.items():
    for i in range(len(vs)-1):
        if vs[i]['turn']=='R' and vs[i+1]['turn']=='L':
            found=(z,vs[i],vs[i+1]); break
    if found: break
z,hR,hL=found
x,y=z
# s = state immediately AFTER the R visit; t = state immediately BEFORE the L visit
s_state=hR['state_after']
# state immediately before L visit: ant at z with its arrival heading = q_before of hL
t_state=(z, hL['q_before'])
es=eta(*s_state); et=eta(*t_state)
print("paired cell z =",z)
print("eta(s) =",es,"   eta(t) =",et)
print("eta(s)==eta(t)? ", es==et, "  (reviewer says NO)")
print("eta(s)+eta(t) as set:", sorted({es,et}), " expected {C_x, R_y} =", sorted({('C',x),('R',y)}))

# B_s triangle B_t : black sets at s (after R) and just before L
Bs=hR['black_after']
# black just before L visit = black_after of the step just before hL, i.e. black state entering hL
# reconstruct: black set right before processing hL = black_after of previous history entry
idxL=history.index(hL)
Bt=history[idxL-1]['black_after']   # black entering the L step (== state before L visit)
G=set(Bs)^set(Bt)
print("z in G (should be False, z black at both):", z in G, " |G| =",len(G))
# incidence-graph boundary of G over F2
deg=defaultdict(int)
for (cx,cy) in G:
    deg[('C',cx)]^=1; deg[('R',cy)]^=1
bd=sorted(k for k,v in deg.items() if v)
print("boundary(G) =", bd, " expected [C_x,R_y] =", sorted([('C',x),('R',y)]))
lifetime_support = set(G)
lifetime_support.add(z)
print(">=4 distinct cells in G union {z}:", len(lifetime_support) >= 4,
      " |G union {z}| =", len(lifetime_support))
assert len(lifetime_support) >= 4
