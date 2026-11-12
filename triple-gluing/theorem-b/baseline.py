# Baseline: iterate 2.3.h (pair) and theorem H (triple) where the common part is a union of M-copies.
# A structure = relation matrix between copies of M; rel in {0: none, 'I': x(j)~y(j), 'M': x(j)~y(l) iff jl in E(M)}; self = 'M'.
# Admissible common part U: omega(U(M)) <= k-2 for every M with omega(M) <= k-2, i.e. omega(U(K_q)) <= q, q = k-2.
# usage: baseline.py q RMAX FULLMAX [noH]
import sys, itertools, networkx as nx
from core import maxclique
q, RMAX, FULLMAX = map(int, sys.argv[1:4]); useH = 'noH' not in sys.argv
def concrete_omega(rel, copies):
    copies = list(copies); V = [(c, j) for c in copies for j in range(q)]; ix = {v: i for i, v in enumerate(V)}
    adj = [0] * len(V)
    for (c, j), (d, l) in itertools.combinations(V, 2):
        t = 'M' if c == d else rel[c][d]
        if (t == 'I' and j == l) or (t == 'M' and j != l):
            adj[ix[(c, j)]] |= 1 << ix[(d, l)]; adj[ix[(d, l)]] |= 1 << ix[(c, j)]
    return maxclique(adj, (1 << len(V)) - 1)
def adm_sets(rel):
    n = len(rel); out = []
    def ex(i, U):
        if i == n: out.append(U); return
        ex(i + 1, U)
        if concrete_omega(rel, U + [i]) <= q: ex(i + 1, U + [i])
    ex(0, []); return [tuple(u) for u in out if u]
def maps(R1, R2, adm1):
    """all rel-preserving injective partial maps from admissible domains of R1 into R2, as tuples of (u,v)."""
    out = []; n2 = len(R2)
    for D in adm1:
        def ex(i, mp, used):
            if i == len(D): out.append(tuple(mp)); return
            u = D[i]
            for v in range(n2):
                if v in used: continue
                if all(R1[u][a] == R2[v][b] for a, b in mp):
                    mp.append((u, v)); ex(i + 1, mp, used | {v}); mp.pop()
        ex(0, [], set())
    return out
def glue2(R1, R2, mp):
    n1, n2, c = len(R1), len(R2), len(mp); n = n1 + n2 + c
    R = [[0] * n for _ in range(n)]
    def s(a, b, t): R[a][b] = R[b][a] = t
    for a, b in itertools.combinations(range(n1), 2): s(a, b, R1[a][b])
    for a, b in itertools.combinations(range(n2), 2): s(n1 + a, n1 + b, R2[a][b])
    for i, (u, v) in enumerate(mp):
        w = n1 + n2 + i; s(u, n1 + v, 'I')
        for a in range(n1): s(w, a, 'M' if a == u else R1[u][a])          # w twin of x1(u) in G1
        for b in range(n2): s(w, n1 + b, 'M' if b == v else R2[v][b])     # and of x2(v) in G2
        for i2, (u2, _) in enumerate(mp[:i]): s(w, n1 + n2 + i2, R1[u][u2])  # w's induce U
    return R
def glue3(Rs, tri):
    offs = [0, len(Rs[0]), len(Rs[0]) + len(Rs[1])]; base = offs[2] + len(Rs[2]); c = len(tri); n = base + 3 * c
    R = [[0] * n for _ in range(n)]
    def s(a, b, t): R[a][b] = R[b][a] = t
    for k in range(3):
        for a, b in itertools.combinations(range(len(Rs[k])), 2): s(offs[k] + a, offs[k] + b, Rs[k][a][b])
    pairs = [(0, 1), (0, 2), (1, 2)]
    for i, us in enumerate(tri):
        for a, b in pairs: s(offs[a] + us[a], offs[b] + us[b], 'I')
        for t, e in enumerate(pairs):
            w = base + 3 * i + t
            for k in range(3):
                if k in e:
                    for a in range(len(Rs[k])): s(w, offs[k] + a, 'M' if a == us[k] else Rs[k][us[k]][a])
                else: s(w, offs[k] + us[k], 'I')
            for i2 in range(i + 1):
                for t2 in range(3):
                    w2 = base + 3 * i2 + t2
                    if w2 >= w: continue
                    s(w, w2, 'M' if i2 == i else Rs[0][us[0]][tri[i2][0]])   # E5 (all types meet), no E6
    return R
def to_nx(R):
    G = nx.Graph(); G.add_nodes_from(range(len(R)))
    for a, b in itertools.combinations(range(len(R)), 2):
        if R[a][b]: G.add_edge(a, b, t=R[a][b])
    return G
class Pool:
    def __init__(s): s.d = {}
    def add(s, R):
        G = to_nx(R); h = nx.weisfeiler_lehman_graph_hash(G, edge_attr='t')
        L = s.d.setdefault(h, [])
        for H in L:
            if nx.is_isomorphic(G, H[1], edge_match=lambda x, y: x['t'] == y['t']): return
        L.append((R, G))
    def all(s): return [R for L in s.d.values() for R, _ in L]
S = {1: [[[0]]]}; best = {}
for r in range(2, RMAX + 1):
    full = r <= FULLMAX; pool = Pool(); b = -1; how = None
    for a in range(1, r // 2 + 1):
        for R1 in S[a]:
            A1 = adm_sets(R1)
            for R2 in S[r - a]:
                for mp in maps(R1, R2, A1):
                    ext = len(R1) + len(R2) + len(mp) - r
                    if ext > b: b, how = ext, ('pair', a, r - a, len(mp))
                    if full: pool.add(glue2(R1, R2, mp))
    if useH:
        for a in range(1, r):
            for bb in range(a, r):
                c = r - a - bb
                if c < bb: continue
                for R1 in S[a]:
                    A1 = adm_sets(R1)
                    for R2 in S[bb]:
                        m12 = maps(R1, R2, A1)
                        for R3 in S[c]:
                            m13 = {}
                            for mp in maps(R1, R3, A1): m13.setdefault(tuple(u for u, _ in mp), []).append(mp)
                            for x in m12:
                                for y in m13.get(tuple(u for u, _ in x), []):
                                    tri = [(u, v, w) for (u, v), (_, w) in zip(x, y)]
                                    ext = len(R1) + len(R2) + len(R3) + 3 * len(tri) - r
                                    if ext > b: b, how = ext, ('triple', a, bb, c, len(tri))
                                    if full: pool.add(glue3((R1, R2, R3), tri))
    best[r] = b
    if full: S[r] = pool.all()
    print(f"q={q} r={r} best extra = {b}m via {how}; structures kept {len(S.get(r, []))}", flush=True)
