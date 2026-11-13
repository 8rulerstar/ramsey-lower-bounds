"""Step 2. Non-neighbourhoods B = A - N[w] (11 vertices, a (4,4)-graph) of the root w.
Input: r44_11.g6.gz (all 546,356 (4,4,11)-graphs, McKay; pass its path as argument).
Necessary conditions, each from the window of A (every induced subgraph S of A has lambda_min >= s, lambda_2 <= r,
and 11I + 10J - A_S - A_S^2 >= 0 because it equals the principal submatrix of N N^T plus C C^T):
 (a) B and {w} u B (w isolated) satisfy those three conditions; (b) e(B) = 10 + e(K), so e(B) in 25..30; max degree <= 10;
 (c) pair quotient filter: quotient matrix of the partition {w}, K (one part), each vertex of B (singletons), which is
     determined by e(K) and B alone, has lambda_min >= s and lambda_2 <= r.
Output: compared with data/B/Bq_e<e>.g6."""
import os, sys, gzip, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from common import *
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
def three(A):
    w = np.linalg.eigvalsh(A.astype(float)); P = 11 * np.eye(len(A)) + 10 - A - A @ A
    return w[0] >= S - EPS and w[-2] <= R + EPS and np.linalg.eigvalsh(P.astype(float))[0] >= -EPS
def qpass(B):
    n = len(B); eK = B.sum() // 2 - 10; c = 10 - B.sum(1); sz = np.array([1, 10] + [1] * n, float)
    E = np.zeros((n + 2, n + 2)); E[0, 1] = E[1, 0] = 10; E[1, 1] = 2 * eK; E[1, 2:] = c; E[2:, 1] = c; E[2:, 2:] = B
    w = np.linalg.eigvalsh(E / np.sqrt(np.outer(sz, sz))); return w[0] >= S - EPS and w[-2] <= R + EPS
got = {e: set() for e in range(25, 31)}; tot = 0
for l in gzip.open(sys.argv[1], 'rt'):
    if not l.strip(): continue
    tot += 1; B = g6dec(l); e = B.sum() // 2
    if not 25 <= e <= 30 or B.sum(1).max() > 10: continue
    B0 = np.zeros((12, 12), dtype=np.int64); B0[1:, 1:] = B
    if three(B) and three(B0) and qpass(B): got[e].add(l.strip())
print('(4,4,11) graphs read', tot)
for e in range(25, 31):
    ref = set(x.strip() for x in open(os.path.join(D, 'B', f'Bq_e{e}.g6')) if x.strip())
    print(f'e(B)={e}: built {len(got[e])}, data/B {len(ref)}, equal {got[e] == ref}')
