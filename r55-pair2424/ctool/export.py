# Export Aut data for ctool (same logic as ../count_exact.py). out: ctool/aut.txt
import networkx as nx, collections, time, sys
from networkx.algorithms.isomorphism import GraphMatcher
import os; D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
gs=[nx.from_graph6_bytes(l.strip()) for l in open(D+'d24_e127.g6','rb') if l.strip()]
def auts(g): return [m for m in GraphMatcher(g,g).isomorphisms_iter()]
t0=time.time(); pts=[]
for gi,g in enumerate(gs):
    A=auts(g); seen=set()
    for a in g:
        if a in seen: continue
        orb={m[a] for m in A}; seen|=orb
        N=sorted(g[a]); st=[tuple(m[x] for x in N) for m in A if m[a]==a]
        pts.append((gi,a,N,st))
classes=collections.defaultdict(list)
for idx,(gi,a,N,st) in enumerate(pts):
    K=gs[gi].subgraph(N); h=(len(N),K.number_of_edges(),nx.weisfeiler_lehman_graph_hash(K,iterations=4))
    for cl in classes[h]:
        gm=GraphMatcher(cl[0],K)
        if gm.is_isomorphic(): cl[1].append((idx,gm.mapping)); break
    else: classes[h].append([nx.Graph(K),[(idx,{x:x for x in N})]])
out=open(D+'ctool/aut.txt','w')
out.write('NG %d\n'%len(gs))
for g in gs:
    out.write(' '.join(str(sum(1<<y for y in g[x])) for x in range(24))+'\n')
ncl=sum(len(l) for l in classes.values()); out.write('NC %d\n'%ncl); mx=0
for h,lst in sorted(classes.items(),key=lambda kv:kv[0][0]):
    for Krep,mem in lst:
        c=h[0]; V=sorted(Krep); pos={x:i for i,x in enumerate(V)}
        G=[tuple(pos[m[x]] for x in V) for m in auts(Krep)]; gid={p:i for i,p in enumerate(G)}; mx=max(mx,len(G))
        out.write('K %d %d %d\n'%(c,len(G),len(mem)))
        for p in G: out.write(' '.join(map(str,p))+'\n')
        for idx,mp in mem:
            gi,a,N,st=pts[idx]; rinv={mp[x]:x for x in V}
            H=sorted({gid[tuple(pos[rinv[dict(zip(N,s))[mp[x]]]] for x in V)] for s in st})
            out.write('%d %d %s %d %s\n'%(gi,a,' '.join(str(mp[x]) for x in V),len(H),' '.join(map(str,H))))
out.close(); print('done',time.time()-t0,'classes',ncl,'max|AutK|',mx)
