"""F = G (x) pattern12 as a graph file (own code). Vertex (j,c) -> 12*j+c, j vertex of G, c in Z_12.
(j,c) ~ (l,c'):  d = c-c' mod 12.  d=0: jl in E(G).  d in {4,6,8}: j=l.  d in {1,2,5,7,10,11}: jl in E(G).  d in {3,9}: no edge.
python3 glue12.py G.txt out.txt"""
import sys
tok=open(sys.argv[1]).read().split(); n=int(tok[0]); G=tok[1:1+n]
assert all(len(r)==n for r in G) and all(G[i][j]==G[j][i] for i in range(n) for j in range(n)) and all(G[i][i]=='0' for i in range(n))
P={4,6,8}; Q={1,2,5,7,10,11}
rows=[]
for j in range(n):
    for c in range(12):
        r=[]
        for l in range(n):
            for d in range(12):
                x=(c-d)%12
                if x==0 or x in Q: e=G[j][l]          # G[j][j] = 0
                elif x in P: e='1' if j==l else '0'
                else: e='0'
                r.append(e)
        rows.append("".join(r))
open(sys.argv[2],"w").write(f"{12*n}\n"+"\n".join(rows)+"\n")
print("built",12*n,"vertices from",sys.argv[1])
