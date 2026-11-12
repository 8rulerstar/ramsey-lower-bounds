# Independent implementation (repro): exact clique, gadget checks, construction F of theorem B.
import itertools, random

def maxclique(adj, cand):
    """adj: list of int bitmasks. Exact max clique within mask cand (greedy-colouring bound)."""
    best = 0
    def col_order(P):
        order = []; bounds = []; c = 0; U = P
        while U:
            c += 1; Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~adj[v] & ~(1 << v); U &= ~(1 << v)
                order.append(v); bounds.append(c)
        return order, bounds
    def ex(P, size):
        nonlocal best
        order, bounds = col_order(P)
        for i in range(len(order) - 1, -1, -1):
            if size + bounds[i] <= best: return
            v = order[i]
            NP = P & adj[v]
            if NP: ex(NP, size + 1)
            elif size + 1 > best: best = size + 1
            P &= ~(1 << v)
    if cand: ex(cand, 0)
    return best

def omega(adj): return maxclique(adj, (1 << len(adj)) - 1)
def alpha(adj):
    n = len(adj); full = (1 << n) - 1
    return maxclique([full & ~adj[i] & ~(1 << i) for i in range(n)], full)

def adj_from(n, edges):
    a = [0] * n
    for u, v in edges: a[u] |= 1 << v; a[v] |= 1 << u
    return a

def is_pseudoforest(edges):
    par = {}
    def f(x):
        while par.setdefault(x, x) != x: x = par[x]
        return x
    for u, v in edges:
        ru, rv = f(u), f(v)
        if ru != rv: par[ru] = rv
    cv, ce = {}, {}
    for x in list(par): cv[f(x)] = cv.get(f(x), 0) + 1
    for u, v in edges: ce[f(u)] = ce.get(f(u), 0) + 1
    return all(ce[c] <= cv[c] for c in ce)

def q2_violation(T, Qset):
    """Return a Q-independent non-pseudoforest edge set, or None. T list of tuples, Qset set of frozenset{e,f}."""
    T = [tuple(sorted(e)) for e in T]; n = len(T)
    partner = [[j for j in range(n) if frozenset((T[i], T[j])) in Qset] for i in range(n)]
    cur = []
    def ex(i, banned):
        if i == n: return None
        r = ex(i + 1, banned)
        if r: return r
        if not (banned >> i & 1):
            cur.append(T[i])
            if not is_pseudoforest(cur):
                res = list(cur); cur.pop(); return res
            b2 = banned
            for j in partner[i]: b2 |= 1 << j
            r = ex(i + 1, b2); cur.pop()
            if r: return r
        return None
    return ex(0, 0)

def gadget_params(r, T, Qset):
    T = [tuple(sorted(e)) for e in T]; Ts = set(T)
    per4 = {}
    for q in Qset:
        e, f = tuple(q); s = frozenset(e) | frozenset(f)
        assert not (set(e) & set(f)) and e in Ts and f in Ts
        per4[s] = per4.get(s, 0) + 1
    d = max(per4.values(), default=0)
    idx = {e: i for i, e in enumerate(T)}
    qa = [0] * len(T)
    for q in Qset:
        e, f = tuple(q); qa[idx[e]] |= 1 << idx[f]; qa[idx[f]] |= 1 << idx[e]
    kappa = 0
    for sz in range(r + 1):
        for P in itertools.combinations(range(r), sz):
            if all(tuple(sorted(p)) in Ts for p in itertools.combinations(P, 2)):
                cand = sum(1 << i for i, e in enumerate(T) if not (set(e) & set(P)))
                kappa = max(kappa, sz + maxclique(qa, cand))
    return d, kappa

def build_F(Gs, xs, M, T, Qset):
    """Gs: list of (n, edges); xs[a][j] vertex of G_a for M-vertex j; M=(m, edges)."""
    T = [tuple(sorted(e)) for e in T]
    m, Me = M; Madj = adj_from(m, Me)
    off = []; N = 0
    for n, _ in Gs: off.append(N); N += n
    W = {}
    for e in T:
        for j in range(m): W[(e, j)] = N; N += 1
    E = []
    Gadj = []
    for a, (n, ed) in enumerate(Gs):
        Gadj.append(adj_from(n, ed))
        E += [(off[a] + u, off[a] + v) for u, v in ed]
    Tset = set(T); r = len(Gs)
    for j in range(m):
        for a, b in itertools.combinations(range(r), 2):
            if (a, b) in Tset: E.append((off[a] + xs[a][j], off[b] + xs[b][j]))   # E2
        for e in T:
            w = W[(e, j)]
            for a in range(r):
                if a in e:   # E3
                    nb = Gadj[a][xs[a][j]]
                    E += [(w, off[a] + y) for y in range(Gs[a][0]) if nb >> y & 1]
                else: E.append((w, off[a] + xs[a][j]))   # E4
    for (e, j), w in W.items():
        for (f, l), u in W.items():
            if u <= w: continue
            if j != l:
                if (Madj[j] >> l & 1) and set(e) & set(f): E.append((w, u))   # E5
            elif frozenset((e, f)) in Qset: E.append((w, u))   # E6
    return N, adj_from(N, E)

def rand_graph_with_M(rng, M, extra, p):
    m, Me = M; n = m + extra
    perm = list(range(n)); rng.shuffle(perm); x = perm[:m]
    inM = {frozenset((x[u], x[v])) for u, v in Me}
    pos = {v: i for i, v in enumerate(x)}
    ed = []
    for u, v in itertools.combinations(range(n), 2):
        if u in pos and v in pos:
            if frozenset((u, v)) in inM: ed.append((u, v))
        elif rng.random() < p: ed.append((u, v))
    return (n, ed), x

def rand_M(rng, m, p):
    return (m, [(u, v) for u, v in itertools.combinations(range(m), 2) if rng.random() < p])
