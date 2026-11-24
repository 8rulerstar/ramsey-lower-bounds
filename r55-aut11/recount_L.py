#!/usr/bin/env python3
"""Recount the list L of stage1 (C, direct clique test) by a different method: take the K5 clauses of the 5-sets that use only
the fixed point and orbits 0, 1, set fixed point - orbits 0, 1 red, and enumerate all models over the 21 variables (S1, S2, T)
with blocking clauses. On 22 vertices joined in red to the fixed point, 'no red K4' and 'no independent 5-set' are exactly
these clauses. Compare the resulting set with L.txt."""
import sys, itertools, numpy as np
sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('stage2','stage2.py'); st=importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
from pysat.solvers import Glucose4
p=11; n,h,vid,pv=st.setup(p)
keep=[v for v in range(2*p)]+[4*p]
combos=np.array([c for c in itertools.combinations(keep,5)],dtype=np.int32)
cols=[pv[combos[:,a],combos[:,b]] for a in range(5) for b in range(a+1,5)]
U=np.unique(np.sort(np.stack(cols,axis=1),axis=1),axis=0)
s=Glucose4()
for row in U.tolist():
    s.add_clause([-v for v in row]); s.add_clause(row)
s.add_clause([vid[('f',0)]]); s.add_clause([vid[('f',1)]])
proj=[vid[('d',0,d)] for d in range(1,6)]+[vid[('d',1,d)] for d in range(1,6)]+[vid[('o',0,1,x)] for x in range(11)]
found=set()
while s.solve():
    m={abs(l):l>0 for l in s.get_model()}
    s1=sum(1<<(d-1) for d in range(1,6) if m[vid[('d',0,d)]]); s2=sum(1<<(d-1) for d in range(1,6) if m[vid[('d',1,d)]])
    t=sum(1<<x for x in range(11) if m[vid[('o',0,1,x)]])
    found.add((s1,s2,t)); s.add_clause([-v if m[v] else v for v in proj])
L={tuple(map(int,l.split()[:3])) for l in open('L.txt')}
print('count by SAT enumeration',len(found),'stage1 list',len(L),'same set',found==L)
