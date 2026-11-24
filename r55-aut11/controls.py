#!/usr/bin/env python3
"""Controls for drat11.py (2026-11-24).
(1) positive: the unit clauses of cases (0,0)..(0,7) added only to the clauses of 5-sets that use the fixed point and one side
    (orbits 0,1 or orbits 2,3) must give SAT (same as control 1 of stage2.py), solved with command-line cadical.
    Checks that the unit-clause encoding fixes a case that exists on each side.
(2) negative: the real proof of case (0,0) cut at 80% of its lines (dropping the final empty clause) must not be VERIFIED by drat-trim.
(3) reference: the original proof of (0,0) on the CNF with one unit clause flipped. VERIFIED is expected if the proof does not use
    that unit clause (the assumption cores use 17 to 34 of the 46 units).
(4) negative: the original proof on the satisfiable one-side CNF of (1) must not be VERIFIED.
"""
import os, sys, subprocess, tempfile, importlib.util
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drat11 as D

cs, nvars = D.cases()
spec = importlib.util.spec_from_file_location('stage2', os.path.join(D.K, 'stage2.py'))
st = importlib.util.module_from_spec(spec); argv = sys.argv; sys.argv = ['x']; spec.loader.exec_module(st); sys.argv = argv
n, h, vid, pv = st.setup(11)
side = np.array([0] * 22 + [1] * 22 + [2])
def one_side(c):
    sd = side[c]; return ~((sd == 0).any(axis=1) & (sd == 1).any(axis=1))
U2 = st.k5_varsets(n, pv, one_side)
cl2 = []
for row in U2.tolist():
    cl2.append([-v for v in row]); cl2.append(row)
tmp = tempfile.mkdtemp(prefix='drat11ctl_', dir=os.environ.get('TMPDIR'))

def write(path, clauses, units):
    with open(path, 'w') as f:
        f.write(f'p cnf {nvars} {len(clauses) + len(units)}\n')
        f.writelines(' '.join(map(str, c)) + ' 0\n' for c in clauses)
        f.writelines(f'{u} 0\n' for u in units)

sat = 0
for i1, i2, u in cs[:8]:
    p = os.path.join(tmp, 'one.cnf'); write(p, cl2, u)
    r = subprocess.run(['timeout', '120', 'cadical', '-q', '-n', p], capture_output=True, text=True)
    sat += r.returncode == 10
print(f'(1) positive (one-side clauses + case units): SAT {sat}/8', flush=True)

full = open(D.CNF).read().split('\n', 1)[1]
body = [list(map(int, l.split()[:-1])) for l in full.splitlines() if l.strip()]
i1, i2, u = cs[0]
c0 = os.path.join(tmp, 'c0.cnf'); p0 = os.path.join(tmp, 'c0.drat'); write(c0, body, u)
r = subprocess.run(['cadical', '-q', '--no-binary', c0, p0], capture_output=True, text=True)
d = subprocess.run([D.DRAT, c0, p0], capture_output=True, text=True)
print('baseline: cadical rc', r.returncode, 'drat-trim VERIFIED', 's VERIFIED' in d.stdout, flush=True)
lines = open(p0).read().splitlines()
cut = os.path.join(tmp, 'cut.drat'); open(cut, 'w').write('\n'.join(lines[:int(len(lines) * 0.8)]) + '\n')
d = subprocess.run([D.DRAT, c0, cut], capture_output=True, text=True)
print('(2) negative (truncated proof): VERIFIED' if 's VERIFIED' in d.stdout else '(2) negative (truncated proof): rejected', flush=True)
u2 = list(u); u2[-1] = -u2[-1]
c1 = os.path.join(tmp, 'c1.cnf'); write(c1, body, u2)
d = subprocess.run([D.DRAT, c1, p0], capture_output=True, text=True)
print('(3) reference (CNF with one unit flipped + original proof): VERIFIED' if 's VERIFIED' in d.stdout else '(3) reference (CNF with one unit flipped + original proof): rejected',
      '(VERIFIED is expected if the proof does not use that unit; assumption cores use 17 to 34 of the 46 units)', flush=True)
c2 = os.path.join(tmp, 'c2.cnf'); write(c2, cl2, u)
d = subprocess.run([D.DRAT, c2, p0], capture_output=True, text=True)
print('(4) negative (satisfiable one-side CNF + original proof): VERIFIED' if 's VERIFIED' in d.stdout else '(4) negative (satisfiable one-side CNF + original proof): rejected', flush=True)
for x in os.listdir(tmp): os.remove(os.path.join(tmp, x))
os.rmdir(tmp)
