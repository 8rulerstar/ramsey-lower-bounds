"""Certificate for the independent side of theorem D12 on a concrete graph file F (read from file, not rebuilt).
Vertex (j,c) of F is 12*j+c (glue12.py). Elements: fibre states (j,L), L a non-empty set of positions with
{(j,c): c in L} independent in F. Checks
  1. no fibre has an independent 5-set, and every state L gets a colour set C(L) (rule of THEOREM_D12.md 3.2) with |C(L)| >= |L|;
  2. for all states (j,L), (l,M) of different fibres with no F-edge between them (so they can lie in one independent set):
     if C(L) and C(M) share a colour then j and l are non-adjacent in G.
Then for an independent set I of F the sets T_i = {j : i in C(I_j)} are independent in G and |I| <= |T_0|+..+|T_3| <= 4 alpha(G).
python3 certifyD12.py G.txt F.txt"""
import sys, itertools
def read_graph(fn):
    tok=open(fn).read().split(); n=int(tok[0]); return n,tok[1:1+n]
n,G=read_graph(sys.argv[1]); N,F=read_graph(sys.argv[2]); assert N==12*n
cell=lambda a:(a%4,a%3); pos={cell(a):a for a in range(12)}; kap=lambda a:a//3
def C(L):
    k={kap(a) for a in L}
    if len(L)==1: return k
    if len(L)>=4: return {0,1,2,3}
    f={cell(a)[0]:cell(a)[1] for a in L}
    if len(f)<len(L): return k            # two positions in one column: not a label of the pattern, keep kappa only
    if len(L)==3:
        ex=set()
        for x in f:
            o=[u for u in f if u!=x]
            if f[o[0]]==f[o[1]]!=f[x] and (o[0]-o[1])%4 in (1,3): ex.add(kap(pos[(x,f[o[0]])]))
        return {0,1,2,3}-ex
    x1,x2=sorted(f)
    if len(k)==2: return k
    sw={kap(pos[(x1,f[x2])]),kap(pos[(x2,f[x1])])}
    if len(sw)==2: return {0,1,2,3}-sw
    k0=next(iter(k)); return {k0,(k0+1)%4}
cmask={}
def cm(L):
    if L not in cmask: cmask[L]=sum(1<<i for i in C([c for c in range(12) if L>>c&1]))
    return cmask[L]
bad_mult=0; states=[]
for j in range(n):
    inner=[sum(1<<d for d in range(12) if F[12*j+c][12*j+d]=='1') for c in range(12)]
    st=[L for L in range(1,4096) if all(not (L>>c&1) or not (inner[c]&L) for c in range(12))]
    assert all(bin(L).count("1")<=4 for L in st), f"independent 5-set inside fibre {j}"
    for L in st:
        if bin(cm(L)).count("1")<bin(L).count("1"): bad_mult+=1
    states.append(st)
pairs=0; viol=0; nel=sum(map(len,states))
for j in range(n):
    for l in range(j):
        cross=[sum(1<<d for d in range(12) if F[12*j+c][12*l+d]=='1') for c in range(12)]
        adjG=G[j][l]=='1'
        if not any(cross):
            pairs+=len(states[j])*len(states[l])
            if adjG:                                   # every pair of states is admissible: any shared colour is a violation
                viol+=sum(1 for L in states[j] for M in states[l] if cm(L)&cm(M))
            continue
        un={}
        for L in states[j]:
            u=0
            for c in range(12):
                if L>>c&1: u|=cross[c]
            un[L]=u
        for L in states[j]:
            u=un[L]; cl=cm(L)
            for M in states[l]:
                if u&M: continue
                pairs+=1
                if adjG and cl&cm(M): viol+=1
print(f"fibres {n}, elements {nel}, admissible pairs {pairs}, violations {viol}, multiplicity failures {bad_mult}")
sys.exit(1 if viol or bad_mult else 0)
