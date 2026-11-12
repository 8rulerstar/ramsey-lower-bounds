# Verifies every finite fact used in the proof in README.md (pure Python, no dependencies).
import itertools
P="001112121221211221111"
def t(c,d):
    if c>d: c,d=d,c
    return P[d*(d-1)//2+c]
V=range(7)
C7=[0,5,2,3,4,1,6]                      # cyclic order p0..p6
cyc={frozenset((C7[i],C7[(i+1)%7])) for i in V}
assert cyc=={frozenset(p) for p in itertools.combinations(V,2) if t(*p)=='2'}
assert {frozenset(p) for p in itertools.combinations(V,2) if t(*p)=='0'}=={frozenset((0,1)),frozenset((0,2))}
R={c:{d for d in V if d!=c and t(c,d)!='1'} for c in V}   # R = '2' or '0'
print("R neighbourhoods:",R)
phi={0:1,4:1,1:2,2:2,3:3,5:3,6:3}
assert all(phi[c]!=phi[d] for c in V for d in R[c])        # proper 3-colouring of R
ind=lambda S: all(frozenset(p) not in cyc for p in itertools.combinations(S,2))
for S in itertools.combinations(V,2):
    if ind(S):
        cn=R[S[0]]&R[S[1]]; print("pair",S,"common R-neighbours",cn); assert len(cn)<=1
trip=[S for S in itertools.combinations(V,3) if ind(S)]; assert len(trip)==7
for S in trip: assert not (R[S[0]]&R[S[1]]&R[S[2]])
assert not any(ind(S) for S in itertools.combinations(V,4))
# clique side: pairs of fibre edges with no R-edge between them, and no third copy
ok=[(e,f) for e,f in itertools.combinations(sorted(map(sorted,cyc)),2)
    if not set(e)&set(f) and all(d not in R[c] for c in e for d in f)]
print("compatible pairs of fibre edges:",ok)
for e,f in ok:
    assert not [d for d in V if d not in e+f and all(d not in R[c] for c in e+f)]
assert ([0,5],[3,4]) in ok and 3 not in R[0]|R[5]
print("all table checks passed")
