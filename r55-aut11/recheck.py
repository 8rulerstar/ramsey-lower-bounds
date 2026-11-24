#!/usr/bin/env python3
"""Re-solve the 630 gluing cases with other solver families (Glucose4, MiniSat22), using the functions of stage2.py with only the
solver changed. Also write the full CNF (all K5 clauses, no assumptions, no symmetry breaking) to full_p11.cnf; the 46 unit
assumptions of each case are given by assum() below (drat11.py appends them as unit clauses)."""
import sys, time, numpy as np
sys.argv = ['x']  # do not run the main() of stage2
import importlib.util
spec = importlib.util.spec_from_file_location('stage2', 'stage2.py'); st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
from pysat.solvers import Solver
p = 11; n, h, vid, pv = st.setup(p)
U = st.k5_varsets(n, pv)
L = [tuple(map(int, l.split()[:3])) for l in open('L.txt')]
def unpack(g):
    s1, s2, t = g
    return (frozenset(d for d in range(1, 6) if s1 >> (d - 1) & 1), frozenset(d for d in range(1, 6) if s2 >> (d - 1) & 1), frozenset(s for s in range(11) if t >> s & 1))
Ls = {unpack(g) for g in L}
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
        seen.update(images(g, mults, swap)); R.append(g)
    return R
R1 = reps(range(1, 11), True); R2 = reps([1], True)
lit = lambda k, red: vid[k] if red else -vid[k]
def assum(g1, g2):
    a = [lit(('f', 0), True), lit(('f', 1), True), lit(('f', 2), False), lit(('f', 3), False)]
    S1, S2, T = g1
    a += [lit(('d', 0, d), d in S1) for d in range(1, 6)] + [lit(('d', 1, d), d in S2) for d in range(1, 6)]
    a += [lit(('o', 0, 1, x), x in T) for x in range(11)]
    B1, B2, BT = g2
    a += [lit(('d', 2, d), d not in B1) for d in range(1, 6)] + [lit(('d', 3, d), d not in B2) for d in range(1, 6)]
    a += [lit(('o', 2, 3, x), x not in BT) for x in range(11)]
    return a
clauses = []
for row in U.tolist():
    clauses.append([-v for v in row]); clauses.append(row)
with open('full_p11.cnf', 'w') as f:
    f.write(f'p cnf {len(vid)} {len(clauses)}\n'); f.writelines(' '.join(map(str, c)) + ' 0\n' for c in clauses)
print('wrote full_p11.cnf vars', len(vid), 'clauses', len(clauses), flush=True)
for name in ('glucose4', 'minisat22'):
    s = Solver(name=name, bootstrap_with=clauses); t0 = time.time(); un = sat = 0
    for g1 in R1:
        for g2 in R2:
            if s.solve(assumptions=assum(g1, g2)): sat += 1
            else: un += 1
    print(f'{name}: instances {un+sat} UNSAT {un} SAT {sat} ({time.time()-t0:.1f}s)', flush=True)
    s.delete()
# orbit count check: the orbit sizes of the group action must sum to |L|
tot1 = sum(len(set(images(g, range(1, 11), True))) for g in R1); tot2 = sum(len(set(images(g, [1], True))) for g in R2)
print('orbit size sums:', tot1, tot2, '(both must be 1430)')
