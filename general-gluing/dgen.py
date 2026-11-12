"""Core of the generalised D family (theoryX/Dgen). Patterns, labels, colourings, support sets, builder.
A pattern is (N, typ) with typ(a,b) in {"same","P","Q","none"}.
A colouring is a map label -> set of colours (t colours) with |C(L)| >= |L| and C(L), C(M) disjoint for separated L, M.
col(S) = union of C(L) over labels L inside S (S a set of positions).
build(Gamma, pos): induced subgraph of Gamma (x) pattern on {(j,c): c in pos[j]}."""
import itertools
def pat12():
    def typ(a,b):
        d=(a-b)%12
        return {0:"same",4:"P",6:"P",8:"P",3:"none",9:"none"}.get(d,"Q")
    return 12,typ
def pat7():
    def typ(a,b):
        d=(a-b)%7
        return "same" if d==0 else ("P" if d in (1,6) else "Q")
    return 7,typ
def pat4():      # DS1 2.3.i / theorem D1: positions 0..3, P = {0,1},{2,3}; Q = the rest  (t = 2)
    def typ(a,b):
        if a==b: return "same"
        return "P" if a//2==b//2 else "Q"
    return 4,typ
def labels_of(N,typ):
    return [L for k in range(1,N+1) for L in itertools.combinations(range(N),k)
            if all(typ(a,b)!="P" for a,b in itertools.combinations(L,2))]
def sep(typ,L,M): return all(typ(a,b) in ("P","none") for a in L for b in M)
def check_colouring(N,typ,C,t):
    labs=labels_of(N,typ)
    for L in labs:
        assert C(L)<=set(range(t)) and len(C(L))>=len(L),L
    ns=0
    for L in labs:
        for M in labs:
            if L<M and sep(typ,L,M):
                ns+=1; assert not C(L)&C(M),(L,M)
    return len(labs),ns
# ---- colouring of the 12-pattern (THEOREM_D12.md 3.2, same rule as prove12.py)
cell=lambda a:(a%4,a%3); pos12={cell(a):a for a in range(12)}; kap=lambda a:a//3
def C12(L):
    k={kap(a) for a in L}
    if len(L)==1: return k
    if len(L)==4: return {0,1,2,3}
    f={cell(a)[0]:cell(a)[1] for a in L}
    if len(L)==3:
        ex=set()
        for x in f:
            o=[u for u in f if u!=x]
            if f[o[0]]==f[o[1]]!=f[x] and (o[0]-o[1])%4 in (1,3): ex.add(kap(pos12[(x,f[o[0]])]))
        return {0,1,2,3}-ex
    x1,x2=sorted(f)
    if len(k)==2: return k
    sw={kap(pos12[(x1,f[x2])]),kap(pos12[(x2,f[x1])])}
    if len(sw)==2: return {0,1,2,3}-sw
    k0=next(iter(k)); return {k0,(k0+1)%4}
# ---- colouring of the 7-pattern (theorem D): proper 3-colouring kc of C_7
def C7_factory(kc):
    assert all(kc[c]!=kc[(c+1)%7] for c in range(7))
    def C(L):
        L=tuple(sorted(L))
        if len(L)==3: return {0,1,2}
        if len(L)==1: return {kc[L[0]]}
        d=(L[1]-L[0])%7
        if d in (3,4): return {0,1,2}
        mid=(L[0]+1)%7 if d==2 else (L[1]+1)%7
        return {0,1,2}-{kc[mid]}
    return C
def C4(L):       # labels: singletons and Q pairs; colour = a//2 for singletons
    return {a//2 for a in L} if len(L)==1 else {0,1}
def col_table(N,typ,C):
    labs=labels_of(N,typ); lm=[(sum(1<<a for a in L),sum(1<<i for i in C(L))) for L in labs]
    tab=[0]*(1<<N)
    for S in range(1,1<<N):
        v=0
        for m,c in lm:
            if m&S==m: v|=c
        tab[S]=v
    return tab
def build(Gam,pos,typ):
    """Gam: adjacency matrix (lists of 0/1); pos[j]: iterable of positions. returns V (list of (j,c)), adjacency matrix."""
    V=[(j,c) for j in range(len(Gam)) for c in sorted(pos[j])]
    n=len(V); A=[[0]*n for _ in range(n)]
    for a in range(n):
        j,c=V[a]
        for b in range(a):
            l,d=V[b]; t=typ(c,d)
            if t=="same" or t=="Q": e=Gam[j][l]
            elif t=="P": e=1 if j==l else 0
            else: e=0
            A[a][b]=A[b][a]=e
    return V,A
