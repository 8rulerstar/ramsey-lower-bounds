import sys, os, random, igraph as ig
R = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, R)
from exact import g6dec, g6enc
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); D = os.path.join(PUB, 'data')
src = open(os.path.join(R, 's2_classes.py')).read()
ns = {'__file__': os.path.join(R, 's2_classes.py')}; exec(src.split('def G(A)')[0].split('import os, sys')[0], ns)  # docstring only
exec('import os, sys, glob, collections, igraph as ig, numpy as np\n' + src[src.index('HERE ='):src.index('ROOTC')].replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = "{R}"'), ns)
l = list(open(os.path.join(PUB, 'results', 'window_solutions.tsv')))[1]; p = l.rstrip('\n').split('\t')
A = ns['build'](p[0], int(p[1]), list(map(int, p[2].split())))
g = ns['G'](A); print('igraph', ig.__version__, 'edges', g.ecount(), 'expected', sum(map(sum, A)) // 2, 'multi', g.has_multiple())
def perm(A):
    n = len(A); q = list(range(n)); random.shuffle(q); return [[A[q[i]][q[j]] for j in range(n)] for i in range(n)]
random.seed(1)
print('canon (script) distinct over 100 relabels:', len({ns['canon'](perm(A)) for _ in range(100)}))
def canon2(A):
    g = ig.Graph.Adjacency(A, mode='max'); p = g.canonical_permutation(); return g6enc([[x for x in r] for r in g.permute_vertices(p).get_adjacency()])
print('canon2 (mode=max, permute_vertices) distinct:', len({canon2(perm(A)) for _ in range(100)}))
