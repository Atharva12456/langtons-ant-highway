"""Verify the two sign/parity-sensitive round-4 fixes before editing."""
import random

# ============ (1) negative-a monodromy in Theorem 7.1 ============
# chi(x,y)=(-1)^{x+y}; weight w(x,y)=chi*alpha(x), alpha: Z/|a| -> Z/4.
def chi(x,y): return 1 if (x+y)%2==0 else -1

def monodromy_via_steps(a, b, alpha, z=(0,0)):
    """Sum the per-diagonal-step contribution -eps*chi(x,y)*(alpha[x mod|a|]+alpha[(x+eps) mod|a|]),
       moving |a| steps of (eps,sigma) from z, then even vertical part contributes 0. Return mod 4."""
    A=abs(a); eps=1 if a>0 else -1
    sig=(1 if b>0 else -1) if b!=0 else 1
    x,y=z; total=0
    for _ in range(A):
        term = -eps*chi(x,y)*(alpha[x%A]+alpha[(x+eps)%A])
        total += term
        x+=eps; y+=sig
    # vertical remainder (0, b - sig*A) is even; contributes 0 by 2-periodicity -> skip
    return total%4

def claimed(alpha):
    return (2*sum(alpha))%4

print("=== (1) monodromy == 2*sum(alpha) mod 4, for many drifts incl. a<0, b=0 ===")
bad=0
for a in [-6,-4,-2,-1,1,2,4,6]:
    A=abs(a)
    for b in [-4,-2,0,2,4]:
        if (a+b)%2!=0: continue          # heading-reset forces a+b even
        for _ in range(200):
            alpha=[random.randint(0,3) for _ in range(A)]
            if monodromy_via_steps(a,b,alpha)!=claimed(alpha): bad+=1
print("mismatches:",bad)

# ============ (5) diamond circulation ============
# increment formulas (as functions of w):
#   g1(x,y) = F_N(x+1,y+1)-F_N(x,y) = -w(x,y)+w(x+1,y)
#   g2(x,y) = F_N(x+1,y-1)-F_N(x,y) =  w(x,y-1)-w(x+1,y-1)
def diamond_circulation(w, x, y):
    g1=lambda X,Y: -w(X,Y)+w(X+1,Y)
    g2=lambda X,Y:  w(X,Y-1)-w(X+1,Y-1)
    # (x,y)->(x+1,y+1)->(x+2,y)->(x+1,y-1)->(x,y)
    return g1(x,y) + g2(x+1,y+1) - g1(x+1,y-1) - g2(x,y)
def FC(w,u,v):  # four-corner based at (u,v)
    return w(u,v)+w(u+1,v)+w(u,v+1)+w(u+1,v+1)

print("\n=== (5) circulation == -(FC(x,y-1)+FC(x+1,y-1)) mod 4, for random w:Z^2->Z/4 ===")
bad=0
for _ in range(2000):
    vals={}
    def w(X,Y):
        if (X,Y) not in vals: vals[(X,Y)]=random.randint(0,3)
        return vals[(X,Y)]
    x,y=random.randint(-3,3),random.randint(-3,3)
    lhs=diamond_circulation(w,x,y)%4
    rhs=(-(FC(w,x,y-1)+FC(w,x+1,y-1)))%4
    if lhs!=rhs: bad+=1
print("mismatches:",bad)
# also confirm: if four-corner==0 everywhere, circulation==0 mod4 (path independence)
bad2=0
for _ in range(500):
    # build w with all four-corner sums 0 mod4: w(x,y)=chi*alpha(x)
    A=random.choice([1,2,3,4]); alpha=[random.randint(0,3) for _ in range(A)]
    w=lambda X,Y: (chi(X,Y)*alpha[X%A])%4
    x,y=random.randint(-3,3),random.randint(-3,3)
    if diamond_circulation(w,x,y)%4!=0: bad2+=1
print("path-independence (circulation==0 for w=chi*alpha):",bad2,"mismatches")
