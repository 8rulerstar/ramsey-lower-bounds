"""Step 5. Every window solution ("S idx 1 cones...") is rebuilt as a 22-vertex graph A and tested:
10-regular, K4-free, no independent 5-set, eigenvalues in the window (lambda_min >= s, lambda_2 <= r), and
det M(A), M(A) = 11I + 10J - A - A^2, computed exactly (sympy, integer). A local graph of an SRG(45,22,10,11)
(and, more generally, of a locally exact vertex) needs det M(A) = (det N)^2 to be a perfect square.
Vertices of A: 0 = root w, 1..10 = K (data/K/K_k.g6), 11..21 = B (line st+idx of the B list); B vertex h is adjacent to
K vertex i iff bit i of cone h is set.
Usage: python pipeline/05_check_windows.py RESULTS_DIR [jobs-file ...] > results/window_solutions.tsv"""
import os, sys, glob, math, itertools, numpy as np, sympy
sys.path.insert(0, os.path.dirname(__file__)); from common import *
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
rdir = sys.argv[1]; jfs = [a for a in sys.argv[2:] if not a.startswith('--')] or [os.path.join(D, 'jobs.txt'), os.path.join(D, 'jobs_e15.txt')]
jobs = {}
for jf in jfs:
    for l in open(jf):
        if l.strip(): p = l.split(); jobs[p[0]] = p
Bcache = {}
def Bline(bf, i):
    if bf not in Bcache: Bcache[bf] = [x.strip() for x in open(os.path.join(D, bf)) if x.strip()]
    return Bcache[bf][i]
print('job\tidx\tcones\tdeg_ok\tK4\tI5\tlmin\tl2\tdetM\tfactorization\tsquare')
n_all = n_sq = n_zero = n_invalid = 0; seen = set(); mismatch = []
for f in sorted(glob.glob(os.path.join(rdir, '*.txt'))):
    jid = os.path.basename(f)[:-4]
    if jid not in jobs: continue
    _, k, bf, st, cnt = jobs[jid]
    # ledger cross-check: window solutions printed for this job must equal the nwin total of its R lines
    rl = {}
    for l in open(f):
        q = l.split()
        if q and q[0] == 'R': rl[int(q[1])] = int(q[3])
    printed = len({l.strip() for l in open(f) if l.startswith('S ') and l.split()[2] == '1'})
    if printed != sum(rl.values()): mismatch.append((jid, printed, sum(rl.values())))
    for l in open(f):
        p = l.split()
        if not (len(p) > 3 and p[0] == 'S' and p[2] == '1'): continue
        if len(p) != 14: n_invalid += 1; continue   # truncated line: 11 cones expected
        key = (jid, l.strip())
        if key in seen: continue
        seen.add(key); idx = int(p[1]); cone = list(map(int, p[3:]))
        A0 = g6dec(open(os.path.join(D, 'K', f'K_{k}.g6')).read()); B = g6dec(Bline(bf, int(st) + idx))
        nA, nB = len(A0), len(B); n = 1 + nA + nB; A = np.zeros((n, n), dtype=np.int64)
        A[0, 1:1 + nA] = A[1:1 + nA, 0] = 1; A[1:1 + nA, 1:1 + nA] = A0; A[1 + nA:, 1 + nA:] = B
        for h in range(nB):
            for i in range(nA):
                if cone[h] >> i & 1: A[1 + nA + h, 1 + i] = A[1 + i, 1 + nA + h] = 1
        deg_ok = bool((A.sum(1) == 10).all()); ev = np.sort(np.linalg.eigvalsh(A.astype(float)))
        k4 = any(all(A[a, b] for a, b in itertools.combinations(Q, 2)) for Q in itertools.combinations(range(n), 4))
        i5 = any(not any(A[a, b] for a, b in itertools.combinations(Q, 2)) for Q in itertools.combinations(range(n), 5))
        M = 11 * np.eye(n, dtype=np.int64) + 10 - A - A @ A; d = int(sympy.Matrix(M.tolist()).det())
        sq = d >= 0 and math.isqrt(d) ** 2 == d; n_all += 1; n_sq += sq; n_zero += (d == 0)
        # the rebuilt graph must itself be a window graph; otherwise the raw line is corrupt
        n_invalid += not (deg_ok and not k4 and not i5 and ev[0] >= S - 1e-6 and ev[-2] <= R + 1e-6)
        print(f'{jid}\t{idx}\t{" ".join(p[3:])}\t{deg_ok}\t{k4}\t{i5}\t{ev[0]:.9f}\t{ev[-2]:.9f}\t{d}\t{sympy.factorint(abs(d))}\t{sq}', flush=True)
print(f'# window solutions {n_all}, perfect-square determinants {n_sq}, zero determinants {n_zero}, invalid rows {n_invalid}, jobs with printed/ledger mismatch {len(mismatch)} {mismatch[:5]}', file=sys.stderr)
sys.exit(1 if (n_sq or n_zero or n_invalid or mismatch) else 0)
