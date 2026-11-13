"""Step 1. Root neighbourhoods K = N_A(w) (10 vertices, a (3,5)-graph) of a window local graph A.
Input: data/mckay/r35_10.g6 (all 313 (3,5,10)-graphs, McKay). Filter: Haemers interlacing for the quotient matrix of the
partition {w}, each vertex of K (singletons), rest (11 vertices). For a 10-regular A the quotient matrix is determined by K.
Output: indices of the passing classes; compared with data/quotient_pass.txt (expected 147) and data/K/K_<i>.g6."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from common import *
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
L = [l for l in open(os.path.join(D, 'mckay', 'r35_10.g6')) if l.strip()]
keep = []
for i, l in enumerate(L):
    K = g6dec(l); e = K.sum() // 2; dK = K.sum(1); B = np.zeros((12, 12))
    B[0, 1:11] = 1
    for a in range(10):
        B[1 + a, 0] = 1; B[1 + a, 1:11] = K[a]; B[1 + a, 11] = 9 - dK[a]; B[11, 1 + a] = (9 - dK[a]) / 11
    B[11, 11] = 10 - (90 - 2 * e) / 11
    w = np.sort(np.linalg.eigvals(B).real)
    if w[0] >= S - EPS and w[-2] <= R + EPS: keep.append(i)
ref = [int(x) for x in open(os.path.join(D, 'quotient_pass.txt')).read().split()]
same_files = all(open(os.path.join(D, 'K', f'K_{i}.g6')).read().strip() == L[i].strip() for i in keep)
print(f'(3,5,10) classes {len(L)}, pass {len(keep)}, equal to data/quotient_pass.txt: {keep == ref}, data/K files match: {same_files}')
