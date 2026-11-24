#!/usr/bin/env python3
"""stage2: n = 4p+1. Is there a 2-colouring of K_n with no monochromatic K5 on which Z_p acts with four orbits of size p and one fixed point?
Static encoding (independent of an earlier orbit-CEGAR tool in the author's working notes, not included here). Only K5 clauses, no other conditions.

Vertices (from 0): element a of orbit i = i*p + a (i=0..3), fixed point = 4p.
Variables (true = red): ('d',i,d) difference +-d inside orbit i, ('o',i,j,s) between orbits i<j with b-a = s, ('f',i) fixed point and orbit i.
Clauses: for every 5-set of vertices (5-sets with the same variable multiset only once) "not all red" and "not all blue".

Usage:
  stage2.py full p            solve the full CNF in one call. If SAT, save the matrix and recount K5s independently.
  stage2.py glue L.txt        p=11 only. Fix the red link G1 and the blue link G2 of the fixed point from L.txt (stage1 output, all
                              Z11-invariant (4,5,22)-graphs) and solve the remaining 44 bits. G1 runs over representatives under
                              (translation of orbit 1, the 10 multipliers, swap of orbits 0/1), G2 over representatives under
                              (translation of orbit 3, swap of orbits 2/3).
"""
import sys, itertools, time, numpy as np
from pysat.solvers import Cadical195

def setup(p):
    h = p // 2; n = 4 * p + 1; vid = {}
    def V(k):
        if k not in vid: vid[k] = len(vid) + 1
        return vid[k]
    for i in range(4):
        for d in range(1, h + 1): V(('d', i, d))
    for i in range(4):
        for j in range(i + 1, 4):
            for s in range(p): V(('o', i, j, s))
    for i in range(4): V(('f', i))
    pv = np.zeros((n, n), dtype=np.int32)
    for x in range(n):
        for y in range(x + 1, n):
            if y == 4 * p: v = vid[('f', x // p)]
            else:
                i, a = divmod(x, p); j, b = divmod(y, p)
                if i == j:
                    d = (b - a) % p; d = min(d, p - d); v = vid[('d', i, d)]
                else: v = vid[('o', i, j, (b - a) % p)]
            pv[x, y] = pv[y, x] = v
    return n, h, vid, pv

def k5_varsets(n, pv, vertex_filter=None):
    """(Sorted) 10-variable rows of all 5-sets, duplicates removed. vertex_filter(combos)->bool array selects a subset."""
    combos = np.array(list(itertools.combinations(range(n), 5)), dtype=np.int32)
    if vertex_filter is not None: combos = combos[vertex_filter(combos)]
    cols = [pv[combos[:, a], combos[:, b]] for a in range(5) for b in range(a + 1, 5)]
    M = np.sort(np.stack(cols, axis=1), axis=1)
    return np.unique(M, axis=0)

def decode(model, n, pv):
    val = {abs(l): l > 0 for l in model}
    A = np.zeros((n, n), dtype=np.int8)
    for x in range(n):
        for y in range(x + 1, n):
            A[x, y] = A[y, x] = 1 if val[int(pv[x, y])] else 0
    return A

def count_k5(A):
    """Independent check: count monochromatic K5s directly from adjacency sets (red, blue)."""
    n = len(A); out = []
    for col in (1, 0):
        adj = [set(y for y in range(n) if y != x and A[x, y] == col) for x in range(n)]
        cnt = 0
        for a in range(n):
            for b in [y for y in adj[a] if y > a]:
                ab = adj[a] & adj[b]
                for c in [y for y in ab if y > b]:
                    abc = ab & adj[c]
                    for d in [y for y in abc if y > c]:
                        cnt += sum(1 for e in abc & adj[d] if e > d)
        out.append(cnt)
    return out

def main():
    mode = sys.argv[1]
    if mode == 'full':
        p = int(sys.argv[2]); n, h, vid, pv = setup(p)
        t0 = time.time(); U = k5_varsets(n, pv)
        print(f'p={p} n={n} vars={len(vid)} distinct 5-set var-rows={len(U)} ({time.time()-t0:.1f}s)', flush=True)
        s = Cadical195()
        for row in U.tolist():
            s.add_clause([-v for v in row]); s.add_clause(row)
        t0 = time.time(); r = s.solve()
        print('result', 'SAT' if r else 'UNSAT', f'{time.time()-t0:.1f}s', flush=True)
        if r:
            A = decode(s.get_model(), n, pv); k5 = count_k5(A)
            fn = f'full_p{p}_sol.mat'; open(fn, 'w').write('\n'.join(''.join(map(str, r_)) for r_ in A.tolist()) + '\n')
            print('independent K5 count (red, blue):', k5, '->', fn)
        return
    if mode == 'glue':
        p = 11; n, h, vid, pv = setup(p)
        L = [tuple(map(int, l.split()[:3])) for l in open(sys.argv[2])]
        def unpack(g):
            s1, s2, t = g
            return (frozenset(d for d in range(1, 6) if s1 >> (d - 1) & 1),
                    frozenset(d for d in range(1, 6) if s2 >> (d - 1) & 1),
                    frozenset(s for s in range(11) if t >> s & 1))
        Ls = {unpack(g) for g in L}; assert len(Ls) == len(L)
        nd = lambda d: min(d % 11, 11 - d % 11)
        def images(g, mults, swap):
            S1, S2, T = g; out = []
            for m in mults:
                A1 = frozenset(nd(m * d) for d in S1); A2 = frozenset(nd(m * d) for d in S2)
                for u in range(11):
                    TT = frozenset((m * s + u) % 11 for s in T); out.append((A1, A2, TT))
                    if swap: out.append((A2, A1, frozenset((-x) % 11 for x in TT)))
            return out
        key = lambda g: (sorted(g[0]), sorted(g[1]), sorted(g[2]))
        def reps(mults, swap):
            seen = set(); R = []
            for g in sorted(Ls, key=key):
                if g in seen: continue
                im = images(g, mults, swap); assert all(x in Ls for x in im), 'the list is not closed under the group action'
                seen.update(im); R.append(g)
            return R
        R1 = reps(range(1, 11), True); R2 = reps([1], True)
        print(f'|L|={len(Ls)}  G1 representatives {len(R1)} (translation x 10 multipliers x swap), G2 representatives {len(R2)} (translation x swap)', flush=True)
        t0 = time.time(); U = k5_varsets(n, pv)
        print(f'distinct 5-set var-rows={len(U)} ({time.time()-t0:.1f}s)', flush=True)
        s = Cadical195()
        for row in U.tolist():
            s.add_clause([-v for v in row]); s.add_clause(row)
        # for the control: a solver with only the clauses of 5-sets that use the fixed point and one side (orbits 0,1 or orbits 2,3)
        side = np.array([0] * (2 * p) + [1] * (2 * p) + [2])
        def one_side(c):
            sd = side[c]; hasX = (sd == 0).any(axis=1); hasY = (sd == 1).any(axis=1)
            return ~(hasX & hasY)
        U2 = k5_varsets(n, pv, one_side); s2 = Cadical195()
        for row in U2.tolist():
            s2.add_clause([-v for v in row]); s2.add_clause(row)
        lit = lambda k, red: vid[k] if red else -vid[k]
        def assum(g1, g2):
            a = [lit(('f', 0), True), lit(('f', 1), True), lit(('f', 2), False), lit(('f', 3), False)]
            S1, S2, T = g1
            a += [lit(('d', 0, d), d in S1) for d in range(1, 6)] + [lit(('d', 1, d), d in S2) for d in range(1, 6)]
            a += [lit(('o', 0, 1, x), x in T) for x in range(11)]
            B1, B2, BT = g2   # the blue graph is an element of L; red is its complement
            a += [lit(('d', 2, d), d not in B1) for d in range(1, 6)] + [lit(('d', 3, d), d not in B2) for d in range(1, 6)]
            a += [lit(('o', 2, 3, x), x not in BT) for x in range(11)]
            return a
        # control 1: with one-side clauses only, every (g1,g2) must be SAT (L agrees with the encoding); sample R1 x R2[:8] (72 pairs). 20 random G1 outside L must be UNSAT.
        okc = 0; tot = 0
        for g1 in R1:
            for g2 in R2[:8]:
                tot += 1; okc += bool(s2.solve(assumptions=assum(g1, g2)))
        import random; rnd = random.Random(1); bad = 0; tried = 0
        while tried < 20:
            g = (frozenset(rnd.sample(range(1, 6), rnd.choice([2, 3]))), frozenset(rnd.sample(range(1, 6), rnd.choice([2, 3]))),
                 frozenset(x for x in range(11) if rnd.random() < 0.5))
            if g in Ls: continue
            tried += 1; bad += (not s2.solve(assumptions=assum(g, R2[0])))
        print(f'control 1 (one-side clauses only): L pairs {okc}/{tot} SAT, G1 outside L {bad}/20 UNSAT', flush=True)
        # main computation
        t0 = time.time(); nsat = 0; nun = 0; tmax = 0.0; out = open('glue_results.tsv', 'w')
        out.write('g1_index\tg2_index\tresult\tseconds\n')
        for i1, g1 in enumerate(R1):
            for i2, g2 in enumerate(R2):
                t1 = time.time(); r = s.solve(assumptions=assum(g1, g2)); dt = time.time() - t1; tmax = max(tmax, dt)
                out.write(f'{i1}\t{i2}\t{"SAT" if r else "UNSAT"}\t{dt:.3f}\n')
                if r:
                    nsat += 1; A = decode(s.get_model(), n, pv); k5 = count_k5(A)
                    fn = f'glue_sol_{i1}_{i2}.mat'; open(fn, 'w').write('\n'.join(''.join(map(str, r_)) for r_ in A.tolist()) + '\n')
                    print('SAT', i1, i2, 'independent K5 count', k5, '->', fn, flush=True)
                else: nun += 1
            print(f'G1 {i1+1}/{len(R1)} done: UNSAT {nun} SAT {nsat} ({time.time()-t0:.0f}s, max {tmax:.2f}s)', flush=True)
        out.close()
        print(f'DONE instances={len(R1)*len(R2)} UNSAT={nun} SAT={nsat} total {time.time()-t0:.0f}s max single {tmax:.2f}s')
        return

if __name__ == '__main__':
    main()
