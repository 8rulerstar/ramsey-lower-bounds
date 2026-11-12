"""Certificate for the independent-set side of theorem D on a concrete graph F (read from file, not rebuilt).
Checks, for every pair of 'elements' that can lie together in an independent set of F, that the assignment used
in the proof sends them to distinct non-adjacent vertices of the same G_i. Then alpha(F) <= alpha(G_1)+alpha(G_2).
Elements: private vertices of the sides, and fibre states (j, L): L a non-empty set of positions with {(j,c): c in L} independent in F.
python3 certifyD1.py G1 G2 maps F  (two-side version, positions 0,1 sides, 2,3 copies of M)"""
import sys, itertools
def read_graph(fn):
    tok=open(fn).read().split(); n=int(tok[0]); return [[int(c) for c in r] for r in tok[1:1+n]]
Gs=[read_graph(f) for f in sys.argv[1:3]]
maps=[[int(x) for x in l.split()] for l in open(sys.argv[3]) if l.strip()]
F=read_graph(sys.argv[4]); n=len(F)
sides=(0,1)
m=len(maps[0])
# vertex numbering convention of heptaglue.py
off={}; cur=0
for i,c in enumerate(sides): off[c]=cur; cur+=len(Gs[i])
for c in range(4):
    if c not in sides: off[c]=cur; cur+=m
assert cur==n
side_of={c:i for i,c in enumerate(sides)}
def vid(c,j): return off[c]+(maps[side_of[c]][j] if c in side_of else j)
col=(0,1,0,1)   # classes {0,2},{1,3}; matching pairs of positions are {0,1},{2,3}
def fam(L,i):
    return True if len(L)==2 else col[L[0]]==i
Fmask=[sum(1<<b for b in range(n) if F[a][b]) for a in range(n)]
elems=[]   # (vertex mask, neighbour mask, images: dict side->vertex of G_side, key)
for i,c in enumerate(sides):
    img=set(maps[i])
    for v in range(len(Gs[i])):
        if v not in img: a=off[c]+v; elems.append((1<<a,Fmask[a],{i:v},("p",i,v)))
bad_mult=0
for j in range(m):
    for k in (1,2):
        for L in itertools.combinations(range(4),k):
            vs=[vid(c,j) for c in L]
            if any(F[a][b] for a in vs for b in vs): continue
            fi=[i for i in range(2) if fam(L,i)]
            if len(fi)<len(L): bad_mult+=1
            vm=sum(1<<a for a in vs); nm=0
            for a in vs: nm|=Fmask[a]
            elems.append((vm,nm,{i:maps[i][j] for i in fi},("f",j,L)))
    # labels of size >=4 must not be independent
    for L in itertools.combinations(range(4),3):
        vs=[vid(c,j) for c in L]
        assert any(F[a][b] for a in vs for b in vs), "independent 4-set inside a fibre"
pairs=0; viol=0
for a in range(len(elems)):
    vma,nma,ia,ka=elems[a]
    for b in range(a):
        vmb,nmb,ib,kb=elems[b]
        if ka[0]=="f" and kb[0]=="f" and ka[1]==kb[1]: continue    # same fibre: one state per fibre
        if nma&vmb: continue
        pairs+=1
        for i in ia:
            if i in ib and (ia[i]==ib[i] or Gs[i][ia[i]][ib[i]]): viol+=1
print(f"elements {len(elems)}, admissible pairs {pairs}, violations {viol}, multiplicity failures {bad_mult}")
sys.exit(1 if viol or bad_mult else 0)
