"""Heptagon gluing (theorem D). Copies are indexed by Z_7. Three positions (sides) carry the full graphs G_1,G_2,G_3,
the other four carry a copy W_c of M. Vertices of M inside G_i: x_i(j).
Adjacency of u in copy c and v in copy c':
  c == c'              : the edges of G_i (side) or of M (W copy)
  c' = c +- 1 (mod 7)  : only same index, (j,c) ~ (j,c')
  otherwise            : twin rule. both indexed j,l: adjacent iff jl in E(M); u private in G_c, v indexed l: iff u ~ x_c(l); both private: no.
build(Gs, maps, sides) -> (n, adjacency as list of sets, info)
Gs: list of 3 adjacency matrices (list of lists of 0/1); maps: 3 lists, maps[i][j] = x_i(j); sides: 3 distinct positions.
CLI: python3 heptaglue.py G1.txt G2.txt G3.txt maps.txt out.txt [s1 s2 s3 positions]  (default sides 0 1 6)"""
import sys
def read_graph(fn):
    tok=open(fn).read().split(); n=int(tok[0]); return [[int(c) for c in r] for r in tok[1:1+n]]
def build(Gs,maps,sides=(0,1,6)):
    m=len(maps[0]); assert all(len(x)==m and len(set(x))==m for x in maps) and len(set(sides))==3
    # M from G_1, and the copies must be induced in all three
    M=[[Gs[0][maps[0][j]][maps[0][l]] for l in range(m)] for j in range(m)]
    induced=all(Gs[i][maps[i][j]][maps[i][l]]==M[j][l] for i in range(3) for j in range(m) for l in range(m))
    off={}; cur=0; pos_of={}
    for i,c in enumerate(sides): off[c]=cur; cur+=len(Gs[i]); pos_of[c]=i
    wpos=[c for c in range(7) if c not in sides]
    for c in wpos: off[c]=cur; cur+=m
    n=cur
    # vertex descriptors: (copy c, index j or None, local id)
    V=[]
    for i,c in enumerate(sides):
        inv={v:j for j,v in enumerate(maps[i])}
        for v in range(len(Gs[i])): V.append((c,inv.get(v),v))
    for c in wpos:
        for j in range(m): V.append((c,j,j))
    adj=[[0]*n for _ in range(n)]
    for a in range(n):
        ca,ja,va=V[a]
        for b in range(a):
            cb,jb,vb=V[b]
            d=(ca-cb)%7
            if d==0:
                e=Gs[pos_of[ca]][va][vb] if ca in pos_of else M[ja][jb]
            elif d in (1,6):
                e=1 if (ja is not None and ja==jb) else 0
            else:
                if ja is not None and jb is not None: e=M[ja][jb]
                elif ja is None and jb is None: e=0
                elif ja is None: e=Gs[pos_of[ca]][va][maps[pos_of[ca]][jb]]
                else: e=Gs[pos_of[cb]][vb][maps[pos_of[cb]][ja]]
            adj[a][b]=adj[b][a]=e
    return n,adj,dict(induced=induced,V=V,m=m)
if __name__=="__main__":
    Gs=[read_graph(f) for f in sys.argv[1:4]]
    maps=[[int(x) for x in l.split()] for l in open(sys.argv[4]) if l.strip()]
    sides=tuple(int(x) for x in sys.argv[6:9]) if len(sys.argv)>=9 else (0,1,6)
    n,adj,info=build(Gs,maps,sides)
    assert info["induced"], "the copies of M are not induced / not equal"
    open(sys.argv[5],"w").write(f"{n}\n"+"\n".join("".join(map(str,r)) for r in adj)+"\n")
    print("built",n,"vertices; m =",info["m"],"sides",sides)
