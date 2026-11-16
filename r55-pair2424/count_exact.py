# exact count of (24,24) gluing configurations. out: cnt/
import networkx as nx, sys, json, time, collections
from networkx.algorithms.isomorphism import GraphMatcher
import os; D=os.path.dirname(os.path.abspath(__file__))+'/'
gs=[nx.from_graph6_bytes(l.strip()) for l in open(D+'d24_e127.g6','rb') if l.strip()]
def auts(g):
    return [m for m in GraphMatcher(g,g).isomorphisms_iter()]
t0=time.time()
# 1. pointed orbits
pts=[]  # (gi,a,stab list of dicts restricted to N(a))
autsz=[]
for gi,g in enumerate(gs):
    A=auts(g); autsz.append(len(A)); seen=set()
    for a in g:
        if a in seen: continue
        orb={m[a] for m in A}; seen|=orb
        N=sorted(g[a]); st=[tuple(m[x] for x in N) for m in A if m[a]==a]
        pts.append((gi,a,N,st))
    if gi%500==0: print(gi,len(pts),time.time()-t0,flush=True)
print('aut sizes',collections.Counter(autsz),flush=True)
# 2. K classes
classes=collections.defaultdict(list)  # wl -> list of [Krep, members]
for idx,(gi,a,N,st) in enumerate(pts):
    K=gs[gi].subgraph(N); h=(len(N),K.number_of_edges(),nx.weisfeiler_lehman_graph_hash(K,iterations=4))
    for cl in classes[h]:
        gm=GraphMatcher(cl[0],K)
        if gm.is_isomorphic(): cl[1].append((idx,gm.mapping)); break  # mapping rep->K
    else: classes[h].append([nx.Graph(K),[(idx,{x:x for x in N})]])
res=collections.defaultdict(lambda:[0,0,0,0,0])  # c: nK, npts, ordered pairs, ordered configs, unordered configs
for h,lst in classes.items():
    for Krep,mem in lst:
        c=h[0]; V=sorted(Krep); pos={x:i for i,x in enumerate(V)}
        G=[tuple(pos[m[x]] for x in V) for m in auts(Krep)]; Gs=set(G)
        inv=lambda p: tuple(sorted(range(len(p)),key=lambda i:p[i]))
        comp=lambda p,q: tuple(p[q[i]] for i in range(len(p)))  # p after q
        Hs=[]
        for idx,mp in mem:
            gi,a,N,st=pts[idx]; rinv={mp[x]:x for x in V}  # K-vertex -> rep vertex
            H=set()
            for s in st:
                sm=dict(zip(N,s)); H.add(tuple(pos[rinv[sm[mp[x]]]] for x in V))
            assert H<=Gs; Hs.append(H)
        n=len(mem); r=res[c]; r[0]+=1; r[1]+=n; r[2]+=n*n
        # double cosets H1\G/H2 via orbit counting (Burnside-free direct)
        cache={}
        def dc(H1,H2):
            k=(frozenset(H1),frozenset(H2))
            if k in cache: return cache[k]
            left=set(G); cnt=0; selfinv=0
            while left:
                g=next(iter(left)); D_={comp(comp(h1,g),h2) for h1 in H1 for h2 in H2}; left-=D_; cnt+=1
                if H1==H2 and inv(g) in D_: selfinv+=1
            cache[k]=(cnt,selfinv); return cache[k]
        grp=collections.Counter(frozenset(H) for H in Hs); keys=list(grp)
        tot=0; diag_si=0
        for H1 in keys:
            for H2 in keys:
                d,si=dc(H1,H2); tot+=d*grp[H1]*grp[H2]
            diag_si+=dc(H1,H1)[1]*grp[H1]
        r[3]+=tot; r[4]+=(tot+diag_si)//2
print('time',time.time()-t0)
out={c:dict(nK=v[0],pointed=v[1],ordered_pairs=v[2],ordered_configs=v[3],unordered_configs=v[4]) for c,v in sorted(res.items())}
T=sum(v[4] for v in res.values())
print(json.dumps(out,indent=1)); print('TOTAL unordered',T,'x0.06s h',T*0.06/3600,'x0.15s h',T*0.15/3600)
json.dump(out,open(D+'cnt/count_exact.json','w'),indent=1)
