# Encoder: fixed matrix F (1 red, 0 blue, -1 unknown) -> CNF forbidding mono K5.
import itertools, sys, random, json, networkx as nx
def k5s(n, adj):
    # all 5-cliques of graph given by adjacency bitmask list
    out=[]
    def rec(cl, cand):
        if len(cl)==5: out.append(tuple(cl)); return
        while cand:
            b=cand & -cand; i=b.bit_length()-1; cand^=b
            rec(cl+[i], cand & adj[i])
    for i in range(n): rec([i], adj[i] & ~((1<<(i+1))-1))
    return out
def encode(F):
    n=len(F); var={}
    for i in range(n):
        for j in range(i+1,n):
            if F[i][j]<0: var[(i,j)]=len(var)+1
    cls=[]
    for col in (1,0):
        adj=[0]*n
        for i in range(n):
            for j in range(n):
                if i!=j and F[i][j] in (col,-1): adj[i]|=1<<j
        for q in k5s(n,adj):
            lits=[(-var[p] if col==1 else var[p]) for p in itertools.combinations(q,2) if p in var]
            assert lits, ('fixed mono K5', col, q)
            cls.append(lits)
    return var, cls
def write(F, path):
    var,cls=encode(F)
    with open(path,'w') as f:
        f.write('p cnf %d %d\n'%(len(var),len(cls)))
        for c in cls: f.write(' '.join(map(str,c))+' 0\n')
    return var,cls
def decode(F, var, model):
    n=len(F); G=[[F[i][j] for j in range(n)] for i in range(n)]
    pos=set(l for l in model if l>0)
    for (i,j),x in var.items(): G[i][j]=G[j][i]=1 if x in pos else 0
    return G
def mono_k5(G):
    n=len(G)
    for col in (1,0):
        adj=[sum(1<<j for j in range(n) if j!=i and G[i][j]==col) for i in range(n)]
        if k5s(n,adj): return True
    return False
