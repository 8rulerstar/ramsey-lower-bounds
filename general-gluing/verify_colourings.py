"""Re-check every colouring stored in colourings.json from the definition (independent of the ILP that found it):
all labels present, |C(L)| >= |L|, separated labels disjoint, and every label inside a design set S uses only the allowed colours."""
import json
from dgen import pat7, pat12, labels_of, sep
CJ=json.load(open("colourings.json")); n=0
for key,e in CJ.items():
    N,typ=(pat7() if e["N"]==7 else pat12()); t=e["t"]
    C={tuple(int(x) for x in k.split(",")):set(v) for k,v in e["col"].items()}
    labs=labels_of(N,typ); assert set(labs)==set(C),key
    assert all(len(C[L])>=len(L) and C[L]<=set(range(t)) for L in labs),key
    for L in labs:
        for M in labs:
            if L<M and sep(typ,L,M): assert not C[L]&C[M],key
    for S,cols in e["design"]:
        for L in labs:
            if set(L)<=set(S): assert C[L]<=set(cols),(key,L)
    n+=1
from collections import Counter
print("colourings checked:",n,dict(Counter(k.split("|")[0] for k in CJ)))
