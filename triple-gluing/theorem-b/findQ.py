# Independent search for Q on T = complete multipartite graph with (Q2) and d <= 1 (at most one Q-pair per 4-set).
# usage: findQ.py r seed  -> writes Q{r}_seed{seed}.txt (seed 1 reproduces Q{r}_mine.txt)
import sys, random, itertools
from core import q2_violation, gadget_params
r = int(sys.argv[1]); rng = random.Random(int(sys.argv[2]))
parts = {4: [[0], [1, 2], [3]], 5: [[0, 3], [1, 4], [2]], 6: [[0, 3], [1, 4], [2, 5]], 7: [[0, 3, 6], [1, 4], [2, 5]], 8: [[0, 3, 6], [1, 4, 7], [2, 5]]}[r]
lab = {v: i for i, P in enumerate(parts) for v in P}
T = [e for e in itertools.combinations(range(r), 2) if lab[e[0]] != lab[e[1]]]
Ts = set(T)
# per 4-set, the perfect matchings fully inside T
opts = {}
for S in itertools.combinations(range(r), 4):
    a, b, c, d = S
    ms = [m for m in [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))] if m[0] in Ts and m[1] in Ts]
    if ms: opts[S] = ms
choice = {S: None for S in opts}
def Qset(): return {frozenset(m) for m in choice.values() if m}
it = 0
while True:
    it += 1
    v = q2_violation(T, Qset())
    if v is None: break
    # shrink to minimal violating set
    v = list(v)
    for e in list(v):
        w = [f for f in v if f != e]
        Qs = Qset()
        if not any(frozenset(p) in Qs for p in itertools.combinations(w, 2)) and not __import__('core').is_pseudoforest(w): v = w
    cands = [(S, m) for S, ms in opts.items() for m in ms if m[0] in v and m[1] in v]
    S, m = rng.choice(cands); choice[S] = m
    if it % 50 == 0 and rng.random() < .3:   # noise
        S = rng.choice(list(opts)); choice[S] = None
Q = sorted(tuple(sorted(m)) for m in Qset())
d, kappa = gadget_params(r, T, Qset())
print("r", r, "|E(T)|", len(T), "iters", it, "|Q|", len(Q), "d", d, "kappa", kappa)
open(f"Q{r}_seed{sys.argv[2]}.txt", "w").write(repr(Q))
