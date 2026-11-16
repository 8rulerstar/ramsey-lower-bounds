# Replay incr.py instance generation (seed 7, N=500, c=11) without SAT; dump fixed matrices. out: ctool/incr500.txt
import networkx as nx, random, collections, sys
from networkx.algorithms.isomorphism import GraphMatcher
import os; D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
random.seed(7); N=500; c=11; m=23-c; n=45
X=[nx.from_graph6_bytes(l.strip().encode()) for l in open(D+'d24_e127.g6')]
pts=[(gi,a) for gi,g in enumerate(X) for a in g if g.degree(a)==c]
kh={p:nx.weisfeiler_lehman_graph_hash(X[p[0]].subgraph(X[p[0]][p[1]]),iterations=4) for p in pts}
byk=collections.defaultdict(list)
for p in pts: byk[kh[p]].append(p)
def build(gi,a,hj,b,iso):
    Gu,Gv=X[gi],X[hj]; C=list(Gu[a]); A=[x for x in Gu if x!=a and x not in Gu[a]]; B=[y for y in Gv if y!=b and y not in iso.values()]
    mu={a:1}; mu.update({x:2+i for i,x in enumerate(C)}); mu.update({x:2+c+i for i,x in enumerate(A)})
    mv={b:0}; mv.update({iso[x]:2+i for i,x in enumerate(C)}); mv.update({y:2+c+m+i for i,y in enumerate(B)})
    F=[[-1]*n for _ in range(n)]
    for i in range(n): F[i][i]=0
    for w,G,mm in ((0,Gu,mu),(1,Gv,mv)):
        for x in range(n):
            if x!=w: F[w][x]=F[x][w]=0
        for x in G:
            F[w][mm[x]]=F[mm[x]][w]=1
            for y in G:
                if x!=y: F[mm[x]][mm[y]]=1 if G.has_edge(x,y) else 0
    return F
def randiso(K,Kb):
    nodes=list(Kb); random.shuffle(nodes); Kp=nx.relabel_nodes(Kb,{x:i for i,x in enumerate(nodes)})
    gm=GraphMatcher(K,Kp)
    return {x:nodes[y] for x,y in gm.mapping.items()} if gm.is_isomorphic() else None
out=open(D+'ctool/incr500.txt','w'); k=0
while k<N:
    gi,a=random.choice(pts); hj,b=random.choice(byk[kh[(gi,a)]])
    iso=randiso(X[gi].subgraph(X[gi][a]),X[hj].subgraph(X[hj][b]))
    if iso is None: continue
    F=build(gi,a,hj,b,iso)
    out.write(''.join('.' if v<0 else str(v) for r in F for v in r)+'\n'); k+=1
print('done',k)
