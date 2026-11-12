"""Machine check of every finite claim used in THEOREM_D12.md (independent of lp12.py / ilp12*.py).
Positions a in Z_12 are written as cells (x,y) = (a mod 4, a mod 3) of a 4 x 3 grid (columns x in Z_4, rows y in Z_3).
A. translation of the difference classes into the grid.
B. labels (P-independent sets) and the list of separated pairs (types A..F of the note).
C. the colour sets C(L) of section 3.2: |C(L)| >= |L| and C(L), C(M) disjoint for separated L, M.
D. clique side: P-cliques, and the largest size of a clique made of r fibres (r = 1..6) by brute force."""
import itertools
N=12
cell=lambda a:(a%4,a%3)
pos={cell(a):a for a in range(N)}
def typ(a,b):
    d=(a-b)%N
    return {0:"same",4:"P",6:"P",8:"P",3:"none",9:"none"}.get(d,"Q")
# A
for a in range(N):
    for b in range(N):
        (x,y),(u,v)=cell(a),cell(b); t=typ(a,b)
        if a==b: g="same"
        elif x==u: g="P"                       # same column
        elif y==v and (x-u)%4==2: g="P"        # same row, opposite columns
        elif y==v: g="none"                    # same row, neighbouring columns
        else: g="Q"                            # both coordinates differ
        assert g==t,(a,b)
print("A ok: P = same column, or same row and opposite columns; none = same row and neighbouring columns; Q = both coordinates differ")
# B
labels=[L for k in range(1,N+1) for L in itertools.combinations(range(N),k)
        if all(typ(a,b)!="P" for a,b in itertools.combinations(L,2))]
assert max(map(len,labels))==4 and len(labels)==168
sep=lambda L,M: all(typ(a,b) in ("P","none") for a in L for b in M)      # disjoint and no Q pair
seps=[(L,M) for L in labels for M in labels if L<M and sep(L,M)]
def classify(L,M):
    if len(L)>len(M): L,M=M,L
    f={cell(a)[0]:cell(a)[1] for a in L}; g={cell(a)[0]:cell(a)[1] for a in M}
    if len(f)==1 and len(g)==1:
        (x,c),=f.items(); (u,b),=g.items()
        return "A" if (x==u)!=(b==c) else None
    if len(f)==1:
        (x,c),=f.items()
        if len(g)==2:
            if x not in g and set(g.values())=={c} and (list(g)[0]-list(g)[1])%4 in (1,3): return "B"
            if x in g and g[x]!=c and all(g[u]==c for u in g if u!=x): return "C"
        if len(g)==3:
            oth=[u for u in g if u!=x]
            if x in g and g[x]!=c and all(g[u]==c for u in oth) and (oth[0]-oth[1])%4 in (1,3): return "D"
        return None
    if len(f)==2 and len(g)==2:
        if set(f)==set(g):
            x1,x2=list(f)
            return "F" if f[x1]==g[x2] and f[x2]==g[x1] and f[x1]!=f[x2] else None
        if not set(f)&set(g) and len(set(f.values())|set(g.values()))==1: return "E"
    return None
from collections import Counter
cnt=Counter()
for L,M in seps:
    t=classify(L,M); assert t is not None,(L,M); cnt[t]+=1
# and conversely every pair of labels of one of the six shapes is separated
for L in labels:
    for M in labels:
        if L<M and classify(L,M) is not None: assert sep(L,M)
print("B ok: 168 labels, separated pairs",len(seps),"by type",dict(sorted(cnt.items())))
# C
kap=lambda a: a//3
for a in range(N):
    x,y=cell(a); assert kap(a)==(y-x)%4
def C(L):
    k={kap(a) for a in L}
    if len(L)==1: return k
    if len(L)==4: return {0,1,2,3}
    f={cell(a)[0]:cell(a)[1] for a in L}
    if len(L)==3:
        # excluded colour: kappa of the cell (x,c) when f(x)=b != c and f = c on the two other (neighbouring) columns
        ex=set()
        for x in f:
            oth=[u for u in f if u!=x]
            if f[oth[0]]==f[oth[1]]!=f[x] and (oth[0]-oth[1])%4 in (1,3): ex.add(kap(pos[(x,f[oth[0]])]))
        assert len(ex)<=1
        return {0,1,2,3}-ex
    x1,x2=sorted(f)
    if len(k)==2: return k
    # |kappa(L)| = 1: add colours outside kappa of the swapped pair {(x1,f(x2)), (x2,f(x1))}
    sw={kap(pos[(x1,f[x2])]),kap(pos[(x2,f[x1])])}
    if len(sw)==2: return {0,1,2,3}-sw
    (k0,),=[tuple(k)]
    return {k0,(k0+1)%4}
for L in labels: assert len(C(L))>=len(L),L
for L,M in seps: assert not C(L)&C(M),(L,M)
print("C ok: |C(L)| >= |L| for all 168 labels, C(L) and C(M) disjoint for all",len(seps),"separated pairs")
fam=[[L for L in labels if i in C(L)] for i in range(4)]
print("   family sizes",[len(f) for f in fam])
open("families.txt","w").write("\n".join(f"F_{i}: "+" ".join("{"+",".join(map(str,L))+"}" for L in fam[i]) for i in range(4))+"\n")
# D
Pcl=[K for k in range(1,N+1) for K in itertools.combinations(range(N),k)
     if all(typ(a,b)=="P" for a,b in itertools.combinations(K,2))]
print("D: P-cliques by size",Counter(map(len,Pcl)))
comp=lambda K,L: all(typ(a,b) in ("same","Q") for a in K for b in L)   # fibres of two adjacent indices
best={}
cand=Pcl
def rec2(ch,cand,size):
    r=len(ch); best[r]=max(best.get(r,0),size)
    if r==6: return
    for i,K in enumerate(cand):
        nc=[L for j,L in enumerate(cand) if j>=i and comp(K,L) and (j!=i or len(K)==1)]
        rec2(ch+[K],nc,size+len(K))
rec2([],cand,0)
print("   largest clique with r fibres, r=1..6:",[best[r] for r in range(1,7)])
assert [best[r] for r in range(1,7)]==[3,4,4,5,6,7]
# with >= 3 fibres: at most one fibre is not a single position
for K in Pcl:
    for L in Pcl:
        if len(K)>=2 and len(L)>=2 and K<L and comp(K,L):
            assert not any(comp(K,M) and comp(L,M) for M in Pcl), (K,L)
        if len(K)==3: assert not comp(K,L) or K==L
print("D ok: r fibres give at most r+1 for r>=3, 4 for r=2, 3 for r=1; two non-single fibres admit no third fibre")
