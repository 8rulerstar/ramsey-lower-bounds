"""Compare indep engine output (out/*.txt) with results/window_solutions.tsv per (job,idx); exact det M."""
import glob, math, sys, networkx as nx
import os; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
def g6(t):
    n = ord(t[0]) - 63; bits = []
    for ch in t[1:]: v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    A = [[0]*n for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: A[i][j] = A[j][i] = 1
            k += 1
    return A
jobs = {}
for f in ('jobs.txt', 'jobs_e15.txt'):
    for l in open(f'{R}/data/{f}'):
        if l.strip(): p = l.split(); jobs[p[0]] = p
def tsv_graph(job, idx, cones):
    p = jobs[job]; K = g6(open(f'{R}/data/K/K_{p[1]}.g6').readline())
    B = g6(blines(f'{R}/data/{p[2]}')[int(p[3]) + idx].strip())
    A = [[0]*22 for _ in range(22)]
    for i in range(10):
        A[0][1+i] = A[1+i][0] = 1
        for j in range(10): A[1+i][1+j] = K[i][j]
    for h in range(11):
        for j in range(11): A[11+h][11+j] = B[h][j]
        for i in range(10):
            if cones[h] >> i & 1: A[11+h][1+i] = A[1+i][11+h] = 1
    return A
import numpy as np
from functools import lru_cache
@lru_cache(None)
def blines(p): return open(p).readlines()
def inv(g):
    A = nx.to_numpy_array(g, dtype=np.int64, nodelist=range(22)); A2 = A @ A; A3 = A2 @ A
    tri = np.diag(A3); co = sorted(tuple(sorted(r)) for r in (A2 * A)) 
    return (tuple(sorted(tri)), tuple(co), tuple(np.round(np.linalg.eigvalsh(A.astype(float)), 6)))
def iso(x, y): return x[1] == y[1] and nx.vf2pp_is_isomorphic(x[0], y[0])
def G(A):
    g = nx.from_numpy_array(np.array(A)); return (g, inv(g))
def classes(As):
    reps = []
    for A in As:
        g = G(A)
        if not any(iso(g, r) for r in reps): reps.append(g)
    return reps
def bareiss(M):
    M = [r[:] for r in M]; n = len(M); prev = 1; sign = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k+1, n) if M[i][k]), None)
            if sw is None: return 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k+1, n):
            for j in range(k+1, n):
                M[i][j] = (M[i][j]*M[k][k] - M[i][k]*M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n-1][n-1]
orig = {}
for l in list(open(f'{R}/results/window_solutions.tsv'))[1:]:
    p = l.rstrip('\n').split('\t'); orig.setdefault((p[0], int(p[1])), []).append(tsv_graph(p[0], int(p[1]), list(map(int, p[2].split()))))
mine = {}; covered = set()
for f in glob.glob('out/*.txt'):
    if not glob.os.path.exists(f + '.done'): continue
    job, off, n = f[4:-4].rsplit('_', 2); off = int(off)
    for l in open(f):
        p = l.split()
        if p[0] == 'R': covered.add((job, off + int(p[1])))
        if p[0] == 'W': mine.setdefault((job, off + int(p[1])), []).append(g6(p[2]))
mism = []; allreps = []; npairs_win = 0
for key in sorted(covered):
    a = classes(orig.get(key, [])); b = classes(mine.get(key, []))
    ok = len(a) == len(b) and all(any(iso(x, y) for y in b) for x in a)
    if not ok: mism.append((key, len(a), len(b)))
    if b: npairs_win += 1
    for g in b:
        if not any(iso(g, r) for r in allreps): allreps.append(g)
missing_win = [k for k in orig if k not in covered]
print('pairs covered', len(covered), 'pairs with window (mine)', npairs_win, 'orig window pairs not yet covered', len(missing_win))
print('mismatches', len(mism), mism[:20])
sq = 0; dets = []
for g, _ in allreps:
    A = nx.to_numpy_array(g, nodelist=range(22), dtype=int).tolist(); n = 22
    A2 = [[sum(A[i][k]*A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    M = [[11*(i == j) + 10 - A[i][j] - A2[i][j] for j in range(n)] for i in range(n)]
    d = bareiss(M); dets.append(d)
    if d >= 0 and math.isqrt(d)**2 == d: sq += 1
print('distinct window graphs (iso)', len(allreps), 'square dets', sq, 'zero dets', dets.count(0), 'neg', sum(d < 0 for d in dets))
open('dets.txt', 'w').write('\n'.join(map(str, dets)) + '\n')
