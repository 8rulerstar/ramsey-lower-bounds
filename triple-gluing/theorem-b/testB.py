# Random exact tests of theorem B for a gadget. usage: testB.py NAME seconds seed
import sys, time, random, itertools, ast, resource
from core import *
name = sys.argv[1]; secs = float(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
def tripart(parts):
    lab = {v: i for i, P in enumerate(parts) for v in P}
    r = sum(map(len, parts))
    return r, [(a, b) for a, b in itertools.combinations(range(r), 2) if lab[a] != lab[b]]
if name == "B4":  # args: B4 secs seed [big] [noQ]
    r = 4; T = [e for e in itertools.combinations(range(4), 2) if e != (1, 2)]; Q = [((0, 1), (2, 3))]
elif name in ("B5", "B6", "B7", "B8"):
    r = int(name[1]); src = ast.literal_eval(open(sys.argv[4]).read())  # args: Br secs seed Qfile [big] [noQ]
    T = None; Q = src["Q"] if isinstance(src, dict) else src
    parts = {5: [[0, 3], [1, 4], [2]], 6: [[0, 3], [1, 4], [2, 5]], 7: [[0, 3, 6], [1, 4], [2, 5]], 8: [[0, 3, 6], [1, 4, 7], [2, 5]]}[r]
    r, T = tripart(parts)
BIG = 'big' in sys.argv
if 'noQ' in sys.argv: Q = []
Qset = {frozenset((tuple(sorted(e)), tuple(sorted(f)))) for e, f in Q}
viol = q2_violation(T, Qset); d, kappa = gadget_params(r, T, Qset)
print(name, "r", r, "|E(T)|", len(T), "|Q|", len(Qset), "Q2", viol is None, "d", d, "kappa", kappa, flush=True)
t0 = time.time(); n = cv = av = tight = wkm2 = 0; maxN = 0
while time.time() - t0 < secs:
    if BIG:   # force omega(M) = kappa - 1 so that (H2) is the binding hypothesis (omega(M) = k-2)
        while True:
            m = rng.randint(kappa - 1, kappa); M = rand_M(rng, m, rng.choice([.8, 1, 1]))
            if omega(adj_from(*M)) == kappa - 1: break
    else:
        m = rng.randint(1, 3 if r <= 5 else 2)
        M = rand_M(rng, m, rng.choice([0, .5, 1, 1]))
    Gs, xs = [], []
    for a in range(r):
        g, x = rand_graph_with_M(rng, M, rng.randint(0, 1 if BIG else (3 if r <= 5 else 2)), rng.choice([.3, .5, .7]))
        Gs.append(g); xs.append(x)
    oM = omega(adj_from(*M)); oG = [omega(adj_from(*g)) for g in Gs]; aG = [alpha(adj_from(*g)) for g in Gs]
    km1 = max(max(oG), kappa, oM + 1, oM + min(oM, d))   # smallest k-1 allowed by H1-H3
    N, F = build_F(Gs, xs, M, T, Qset)
    assert N == sum(g[0] for g in Gs) + len(T) * m
    oF = omega(F); aF = alpha(F)
    n += 1; maxN = max(maxN, N); cv += oF > km1; av += aF > sum(aG); tight += oF == km1; wkm2 += oM == km1 - 1
print(name, "tested", n, "clique viol", cv, "alpha viol", av, "omega(F)=k-1", tight, "omega(M)=k-2", wkm2, "maxN", maxN,
      "maxRSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 2**20)
