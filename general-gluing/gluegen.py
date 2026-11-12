"""Builder for the generalised D family (theorem DG). spec.json:
  {"pattern": 7 | 12, "M": m, "parts": [{"graph": "file", "map": "mapsfile:line" , "S": [positions]}, ...], "colouring": key in colourings.json}
Gamma = amalgam of the part graphs over M (vertex j < m of M is map[j] in each part; private vertices of different parts are not adjacent).
M-vertices sit on all positions, the private vertices of a part on its set S.
Vertex order of F: Gamma-vertices j = 0..m-1 (M), then the private vertices of part 0 (in the order of its graph), part 1, ...;
for each j its positions in increasing order. layout(spec) returns (Gamma adjacency rows as int bitmasks, pos list, part-of list).
python3 gluegen.py spec.json out.txt"""
import sys, json, os
from dgen import pat7, pat12
def read_graph(fn):
    tok=open(fn).read().split(); n=int(tok[0]); return [[int(c) for c in r] for r in tok[1:1+n]]
def read_map(s,base):
    fn,line=s.split(":"); return [int(x) for x in [l for l in open(os.path.join(base,fn)) if l.strip()][int(line)].split()]
def layout(specfile):
    base=os.path.dirname(os.path.abspath(specfile)); spec=json.load(open(specfile))
    N,typ=(pat7() if spec["pattern"]==7 else pat12()); m=spec["M"]
    Gs=[read_graph(os.path.join(base,p["graph"])) for p in spec["parts"]]
    maps=[read_map(p["map"],base) for p in spec["parts"]]
    assert all(len(mp)==m and len(set(mp))==m for mp in maps)
    M=[[Gs[0][maps[0][a]][maps[0][b]] for b in range(m)] for a in range(m)]
    for G,mp in zip(Gs,maps):       # M induced and equal in every part
        assert all(G[mp[a]][mp[b]]==M[a][b] for a in range(m) for b in range(m)), "M is not the same induced subgraph in all parts"
    gid=[]; pos=[list(range(N))]*m; part=[-1]*m      # gid[i][v] = Gamma index of vertex v of part i
    cur=m
    for i,(G,mp) in enumerate(zip(Gs,maps)):
        d={v:j for j,v in enumerate(mp)}
        for v in range(len(G)):
            if v not in d: d[v]=cur; cur+=1; pos.append(sorted(spec["parts"][i]["S"])); part.append(i)
        gid.append(d)
    n=cur; A=[[0]*n for _ in range(n)]
    for i,G in enumerate(Gs):
        d=gid[i]
        for a in range(len(G)):
            for b in range(len(G)):
                if G[a][b]: A[d[a]][d[b]]=1
    return spec,N,typ,A,pos,part,Gs,gid
if __name__=="__main__":
    spec,N,typ,A,pos,part,Gs,gid=layout(sys.argv[1])
    V=[(j,c) for j in range(len(A)) for c in pos[j]]
    T=[[typ(a,b) for b in range(N)] for a in range(N)]
    rows=[]
    for (j,c) in V:
        Aj=A[j]; Tc=T[c]; r=[]
        for (l,d) in V:
            t=Tc[d]
            if t=="same" or t=="Q": r.append('1' if Aj[l] else '0')
            elif t=="P": r.append('1' if j==l else '0')
            else: r.append('0')
        rows.append("".join(r))
    open(sys.argv[2],"w").write(f"{len(V)}\n"+"\n".join(rows)+"\n")
    print("built",len(V),"vertices; Gamma has",len(A),"vertices; parts",[(p["graph"],p["S"]) for p in spec["parts"]])
