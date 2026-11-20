"""(a), (c), (d-1): the window solutions, their isomorphism classes, standard orbit counts, exact window and determinant.
Inputs (read only):
  r55-srg45/results/window_solutions.tsv   799 window solutions of the main engine (first cone up to Aut(K))
  recheck/indep/out/*.txt (extract ../second_engine/raw_out.tar.gz into recheck/indep/)          second engine (no symmetry reduction): ALL labelled window solutions
                                            ("W idx g6", vertex 0 = root w, 1..10 = K, 11..21 = B) of 40,453 pairs
Computes, with exact integer arithmetic (exact.py) for every solution: 10-regularity, exact window (M(A) PSD), det M(A).
Canonical forms, |Aut| and vertex orbits by igraph (bliss). Orbits of Aut(K) x Aut(B) on the labelled solutions of one pair
= isomorphism classes of rooted graphs (A, w) with the root coloured, counted per pair.
Outputs: out/window52.tsv, out/window52.g6, out/classes_summary.txt, out/orbits_per_pair.tsv.
Usage: python s2_classes.py   (needs python-igraph and numpy; see README.md)"""
import os, sys, glob, collections, igraph as ig, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exact import g6dec, g6enc, Mmat, psd_exact, window_exact, factor, fmt_factor
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); IND = os.path.join(HERE, 'indep')
D = os.path.join(PUB, 'data')
jobs = {}
for f in ('jobs.txt', 'jobs_e15.txt'):
    for l in open(os.path.join(D, f)):
        if l.strip(): p = l.split(); jobs[p[0]] = p
Bc = {}
def bline(bf, i):
    if bf not in Bc: Bc[bf] = [x.strip() for x in open(os.path.join(D, bf)) if x.strip()]
    return Bc[bf][i]
def build(job, idx, cones):
    _, k, bf, st, _ = jobs[job]; K = g6dec(open(os.path.join(D, 'K', f'K_{k}.g6')).read()); B = g6dec(bline(bf, int(st) + idx))
    A = [[0] * 22 for _ in range(22)]
    for i in range(10):
        A[0][1 + i] = A[1 + i][0] = 1
        for j in range(10): A[1 + i][1 + j] = K[i][j]
    for h in range(11):
        for j in range(11): A[11 + h][11 + j] = B[h][j]
        for i in range(10):
            if cones[h] >> i & 1: A[11 + h][1 + i] = A[1 + i][11 + h] = 1
    return A
def G(A): return ig.Graph.Adjacency(A, mode='max')
def canon(A, color=None):
    # 2026-11-18 윈도우 수정: 손으로 만든 역순열 대신 igraph permute_vertices 로 정준 그래프를 만든다(재표지 100개 대조: 옛 판 100류, 새 판 1류).
    # 색이 있으면 정준 위치의 색 열을 키에 붙인다(뿌리 위치가 다른 두 뿌리 그래프를 합치지 않게).
    g = G(A); p = g.canonical_permutation(color=color); h = g.permute_vertices(p)
    key = g6enc([list(r) for r in h.get_adjacency()])
    if color is not None:
        col = [0] * len(A)
        for k, x in enumerate(p): col[x] = color[k]
        key += ':' + ''.join(map(str, col))
    return key
ROOTC = [0] + [1] * 10 + [2] * 11
out = lambda name: open(os.path.join(HERE, 'out', name), 'w')
# main engine: 799
main = []
for l in list(open(os.path.join(PUB, 'results', 'window_solutions.tsv')))[1:]:
    p = l.rstrip('\n').split('\t'); main.append((p[0], int(p[1]), build(p[0], int(p[1]), list(map(int, p[2].split()))), int(p[8]), p[9]))
# second engine: all labelled window solutions, per pair
lab = collections.defaultdict(list); covered = set()
for f in glob.glob(os.path.join(IND, 'out', '*.txt')):
    if not os.path.exists(f + '.done'): continue
    job, off, n = os.path.basename(f)[:-4].rsplit('_', 2); off = int(off)
    for l in open(f):
        p = l.split()
        if p and p[0] == 'R': covered.add((job, off + int(p[1])))
        if p and p[0] == 'W': lab[(job, off + int(p[1]))].append(g6dec(p[2]))
winpairs = sorted(set((j, i) for j, i, *_ in main))
S = open(os.path.join(HERE, 'out', 'classes_summary.txt'), 'w')
def P(*a): print(*a); print(*a, file=S); S.flush()
P(f'main engine window solutions {len(main)} in {len(winpairs)} pairs; second engine pairs covered {len(covered)}, '
  f'window pairs covered {sum(1 for k in winpairs if k in covered)}, pairs with labelled windows {len(lab)}, labelled windows {sum(map(len, lab.values()))}')
P(f'second-engine window pairs outside the 454: {sorted(set(lab) - set(winpairs))[:5]}')
# classes
cls = {}; order = []
def cid(A):
    c = canon(A)
    if c not in cls: cls[c] = len(order); order.append(c)
    return cls[c]
# exact checks on the 799
bad = collections.Counter(); main_cls = collections.Counter(); detmis = 0
for job, idx, A, det_tsv, fac_tsv in main:
    ok, pd, d = window_exact(A)
    if not ok: bad['main not exact window'] += 1
    if not pd: bad['main det M = 0'] += 1
    if d != det_tsv: detmis += 1
    main_cls[cid(A)] += 1
P(f'799 main solutions: exact window (M PSD) {len(main) - bad["main not exact window"]}, positive definite {len(main) - bad["main det M = 0"]}, '
  f'det equal to window_solutions.tsv {len(main) - detmis}; classes {len(main_cls)}')
# labelled solutions: exact window, classes, rooted orbits per pair
orbit_rows = []; lab_cls = collections.Counter(); rooted_cls = collections.Counter(); nlab = nwin_exact = 0
for key in winpairs:
    L = lab.get(key, []); roots = set()
    for A in L:
        nlab += 1; ok, pd, d = window_exact(A); nwin_exact += ok
        if not ok: bad['labelled not exact window'] += 1
        c = cid(A); lab_cls[c] += 1; r = canon(A, ROOTC)
        if r not in roots: roots.add(r); rooted_cls[c] += 1
    n_main = sum(1 for j, i, *_ in main if (j, i) == key)
    orbit_rows.append((key[0], key[1], jobs[key[0]][1], len(L), len(roots), n_main))
P(f'labelled solutions of the 454 pairs {nlab}, exact window {nwin_exact}; classes {len(lab_cls)}; '
  f'classes equal to main classes {set(lab_cls) == set(main_cls)}')
tot_orb = sum(r[4] for r in orbit_rows)
P(f'Aut(K) x Aut(B) orbits (rooted iso classes per pair), summed over the 454 pairs: {tot_orb}')
P(f'main engine (first cone up to Aut(K)): {len(main)}; second engine (labelled): {nlab}')
P(f'pairs where #orbits <= #main <= #labelled fails: {sum(1 for r in orbit_rows if not (r[4] <= r[5] <= r[3]))}')
with out('orbits_per_pair.tsv') as f:
    f.write('job\tidx\tK\tlabelled\torbits_AutK_x_AutB\tmain_engine\n')
    for r in orbit_rows: f.write('\t'.join(map(str, r)) + '\n')
# per class: Aut, vertex orbits, roots with e(N(w)) in {15,16,18,19}, det, factorisation
rows = []; tot_root_orbits = 0; tot_pairs_gr = 0
for c, s6 in enumerate(order):
    A = g6dec(s6); g = G(A); aut = g.count_automorphisms()
    gens = g.automorphism_group(); par = list(range(22))
    def fd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for gen in gens:
        for i, j in enumerate(gen): par[fd(i)] = fd(j)
    orbs = collections.defaultdict(list)
    for v in range(22): orbs[fd(v)].append(v)
    eN = [sum(A[a][b] for a in range(22) for b in range(a + 1, 22) if A[v][a] and A[v][b]) for v in range(22)]
    adm = [o for o in orbs.values() if eN[o[0]] in (15, 16, 18, 19)]
    tot_root_orbits += len(adm)
    ok, pd, d = window_exact(A); f = factor(d)
    w = np.linalg.eigvalsh(np.array(A, float))
    prof = ','.join(f'{e}:{eN.count(e)}' for e in sorted(set(eN)))
    rows.append((c + 1, s6, aut, len(orbs), len(adm), prof, f'{w[0]:.9f}', f'{w[-2]:.9f}', ok, pd, d, fmt_factor(f),
                 int(round(d ** 0.5)) ** 2 == d if d >= 0 else False, main_cls[c], lab_cls[c], rooted_cls[c]))
P(f'sum over classes of Aut(A)-orbits of roots w with e(N(w)) in {{15,16,18,19}}: {tot_root_orbits} '
  f'(should equal the Aut(K) x Aut(B) orbit total {tot_orb}: {tot_root_orbits == tot_orb})')
P(f'classes with exact window {sum(r[8] for r in rows)}, positive definite {sum(r[9] for r in rows)}, square det {sum(r[12] for r in rows)}')
P(f'det values distinct {len(set(r[10] for r in rows))}; |Aut| distribution {sorted(collections.Counter(r[2] for r in rows).items())}')
dets_indep = [int(x) for x in open(os.path.join(PUB, 'second_engine', 'dets.txt')).read().split()]
P(f'multiset of the 52 dets equal to indep/dets.txt: {sorted(dets_indep) == sorted(r[10] for r in rows)}')
with out('window52.tsv') as f:
    f.write('class\tgraph6_canonical\taut\tvertex_orbits\troot_orbits_e15_16_18_19\te(N(w))_profile\tlambda_min\tlambda_2\t'
            'exact_window\tM_pos_def\tdet_M\tfactorisation\tsquare\tmain_engine_count\tlabelled_count\trooted_orbits\n')
    for r in rows: f.write('\t'.join(map(str, r)) + '\n')
with out('window52.g6') as f:
    for r in rows: f.write(r[1] + '\n')
P('bad counters', dict(bad))
