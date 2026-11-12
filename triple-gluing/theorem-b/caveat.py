# Referee caveat: M = K_q (q = k-2), r = 4, plain 2.3.h only, common part = any K_{q+1}-free induced subgraph (not just copies).
# (a) size of the best common part for the 2+2 split; (b) exact check of the resulting graphs on random instances.
import sys, itertools, random, time
from core import *
def glue_h(G1, G2, U1, U2, Uedges):
    """2.3.h: G=(n,edges); U1[i], U2[i] = images of common-part vertex i. Returns (graph, list of new w vertices)."""
    n1, e1 = G1; n2, e2 = G2; c = len(U1); N = n1 + n2 + c
    A1 = adj_from(n1, e1); A2 = adj_from(n2, e2)
    E = list(e1) + [(n1 + u, n1 + v) for u, v in e2]
    for i in range(c):
        w = n1 + n2 + i; E.append((U1[i], n1 + U2[i]))
        E += [(w, y) for y in range(n1) if A1[U1[i]] >> y & 1]
        E += [(w, n1 + y) for y in range(n2) if A2[U2[i]] >> y & 1]
    E += [(n1 + n2 + i, n1 + n2 + j) for i, j in Uedges]
    return (N, E), [n1 + n2 + i for i in range(c)]
def best_free_subset(adj, verts, q):
    """largest subset of verts whose induced subgraph is K_{q+1}-free (exhaustive by size, descending)."""
    for sz in range(len(verts), 0, -1):
        for S in itertools.combinations(verts, sz):
            if maxclique(adj, sum(1 << v for v in S)) <= q: return list(S)
for q in range(1, 6):
    # abstract S12 on 3 copies of K_q: x1, x2, w  (only the copy part matters for the common part)
    n = 3 * q; V = lambda c, j: c * q + j; E = []
    for c in range(3): E += [(V(c, j), V(c, l)) for j, l in itertools.combinations(range(q), 2)]
    E += [(V(0, j), V(1, j)) for j in range(q)]
    E += [(V(2, j), V(c, l)) for c in (0, 1) for j in range(q) for l in range(q) if j != l]
    S = best_free_subset(adj_from(n, E), list(range(n)), q)
    print(f"q={q}: best K_(q+1)-free induced part of the 3-copy structure = {len(S)} = 3q-{3*q-len(S)}; total extra 2q+{len(S)} = 5m-{5*q-2*q-len(S)} (m=q)", flush=True)
# (b) exact check, k = q+2
rng = random.Random(1); t0 = time.time(); cnt = viol_c = viol_a = 0
while time.time() - t0 < (float(sys.argv[1]) if len(sys.argv) > 1 else 60):
    q = rng.choice([1, 2, 3]); k = q + 2
    M = (q, list(itertools.combinations(range(q), 2)))
    Gs = []
    while len(Gs) < 4:
        g, x = rand_graph_with_M(rng, M, rng.randint(0, 3), rng.choice([.3, .5, .7]))
        if omega(adj_from(*g)) <= k - 1: Gs.append((g, x))
    al = [alpha(adj_from(*g)) for g, _ in Gs]
    H12, w12 = glue_h(Gs[0][0], Gs[1][0], Gs[0][1], Gs[1][1], M[1])
    H34, w34 = glue_h(Gs[2][0], Gs[3][0], Gs[2][1], Gs[3][1], M[1])
    n1 = Gs[0][0][0]; n3 = Gs[2][0][0]
    copies12 = [Gs[0][1], [n1 + y for y in Gs[1][1]], w12]; copies34 = [Gs[2][1], [n3 + y for y in Gs[3][1]], w34]
    A12 = adj_from(*H12); A34 = adj_from(*H34)
    order = [(c, j) for c in range(3) for j in range(q)]
    cv = [copies12[c][j] for c, j in order]
    Ssub = best_free_subset(A12, cv, q)
    pos = [cv.index(v) for v in Ssub]
    U1 = [copies12[order[p][0]][order[p][1]] for p in pos]; U2 = [copies34[order[p][0]][order[p][1]] for p in pos]
    # the map must be an induced isomorphism: check it
    assert all((A12[U1[i]] >> U1[j] & 1) == (A34[U2[i]] >> U2[j] & 1) for i, j in itertools.combinations(range(len(U1)), 2))
    Ued = [(i, j) for i, j in itertools.combinations(range(len(U1)), 2) if A12[U1[i]] >> U1[j] & 1]
    F, _ = glue_h(H12, H34, U1, U2, Ued)
    ext = F[0] - sum(g[0] for g, _ in Gs); assert ext == 5 * q - 2 or q == 1
    AF = adj_from(*F); cnt += 1
    viol_c += omega(AF) > k - 1; viol_a += alpha(AF) > sum(al)
print(f"exact check 2.3.h twice + 2.3.h on {{3q-2}}-vertex common part: {cnt} instances, extra = 5m-2 (q>=2), clique viol {viol_c}, alpha viol {viol_a}")
