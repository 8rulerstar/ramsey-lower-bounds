"""Step 7. Closure check on the window solutions (a positive control of the search on instances that have solutions).
Every window graph A found must be found again from every vertex w whose neighbourhood K = N_A(w) has 15, 16, 18 or 19
edges, i.e. as a window solution of a job with that root class K. The script rebuilds all window solutions, groups them by
a graph invariant (not a canonical form), lists for each graph the root classes of its vertices, and compares with the
root classes under which the graph appears in results/window_solutions.tsv.
Usage: python pipeline/07_reroot_check.py   (reads data/ and results/window_solutions.tsv)"""
import os, sys, collections, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from common import *
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
jobs = {}
for jf in ('jobs.txt', 'jobs_e15.txt'):
    for l in open(os.path.join(D, jf)):
        if l.strip(): p = l.split(); jobs[p[0]] = p
Bcache = {}
def Bline(bf, i):
    if bf not in Bcache: Bcache[bf] = [x.strip() for x in open(os.path.join(D, bf)) if x.strip()]
    return Bcache[bf][i]
def build(jid, idx, cones):
    _, k, bf, st, cnt = jobs[jid]
    K = g6dec(open(os.path.join(D, 'K', f'K_{k}.g6')).read()); B = g6dec(Bline(bf, int(st) + idx))
    A = np.zeros((22, 22), dtype=np.int64); A[0, 1:11] = A[1:11, 0] = 1; A[1:11, 1:11] = K; A[11:, 11:] = B
    for h in range(11):
        for i in range(10):
            if cones[h] >> i & 1: A[11 + h, 1 + i] = A[1 + i, 11 + h] = 1
    return A, int(k)
def inv(A):
    n = len(A); d = A.sum(1); A2 = A @ A; A3 = A2 @ A; A4 = A3 @ A
    cp = tuple(np.round(np.poly(A.astype(float))).astype(np.int64).tolist())
    loc = tuple(sorted((int(d[i]), int(A3[i, i]), int(A4[i, i]), tuple(sorted(int(d[j]) for j in range(n) if A[i, j])),
                        tuple(sorted(int(A2[i, j]) for j in range(n) if j != i and A[i, j])),
                        tuple(sorted(int(A2[i, j]) for j in range(n) if j != i and not A[i, j]))) for i in range(n)))
    return (cp, loc)
L = [l for l in open(os.path.join(D, 'mckay', 'r35_10.g6')) if l.strip()]
Kinv = {}
for i, l in enumerate(L): Kinv.setdefault(inv(g6dec(l)), []).append(i)
assert all(len(v) == 1 for v in Kinv.values()), 'invariant does not separate the (3,5,10) classes'
passk = set(int(x) for x in open(os.path.join(D, 'quotient_pass.txt')).read().split())
rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, '..', 'results', 'window_solutions.tsv'))][1:]
obs = collections.defaultdict(set); pred = {}; unknown = notpass = 0
for r in rows:
    A, k = build(r[0], int(r[1]), list(map(int, r[2].split()))); I = inv(A) + (r[8],)
    obs[I].add(k)
    if I in pred: continue
    P = set()
    for w in range(22):
        nb = np.nonzero(A[w])[0]; Kw = A[np.ix_(nb, nb)]; e = int(Kw.sum() // 2); c = Kinv.get(inv(Kw))
        if c is None: unknown += 1; continue
        if c[0] not in passk: notpass += 1
        if e in (15, 16, 18, 19): P.add(c[0])
    pred[I] = P
miss = sum(1 for I, P in pred.items() for c in P if c not in obs[I]); extra = sum(1 for I in pred for k in obs[I] if k not in pred[I])
print(f'window solutions {len(rows)}, distinct graphs by invariant {len(pred)}')
print(f'root neighbourhoods outside the (3,5,10) list {unknown}, outside the 147 classes {notpass}')
print(f'(graph, root class) pairs expected {sum(len(P) for P in pred.values())}, missing from the results {miss}, unexpected {extra}')
sys.exit(1 if (unknown or notpass or miss or extra) else 0)
