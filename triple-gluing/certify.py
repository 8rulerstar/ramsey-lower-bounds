"""Certificate check for the triple gluing on a concrete graph F (layout of tripleglue.py).
Claim checked: for EVERY independent set I of F, the map phi_I below sends I injectively onto an independent set of
the disjoint union G_0 + G_1 + G_2. Hence alpha(F) <= alpha(G_0) + alpha(G_1) + alpha(G_2).
phi_I(v) depends only on T = I cap fibre(v), fibre(j) = {x_0(j), x_1(j), x_2(j), w_01(j), w_12(j), w_02(j)}:
  a vertex of G_a -> (a, itself);
  no x in T:      w_01 -> (0, x_0(j)), w_12 -> (1, x_1(j)), w_02 -> (2, x_2(j));
  x_a(j) in T:    w_ab -> (b, x_b(j)), w_ac -> (c, x_c(j))   (w_bc cannot be in T: it is adjacent to x_a(j)).
Injectivity and independence of the image are conditions on PAIRS (u, T_u), (v, T_v), so the check enumerates every
pair of vertices u != v, non-adjacent in F, with every pair of independent fibre subsets T_u (containing u), T_v
(containing v), equal if u and v share a fibre, and T_u + T_v independent in F; it requires different images, and
non-adjacent images when on the same side. Exhaustive over all such pairs: a rigorous proof for this F.
Usage: python certify.py G0 G1 G2 maps.txt F.txt"""
import itertools, sys
def load(f):
    L = open(f).read().split(); n = int(L[0]); return n, [[c == "1" for c in r] for r in L[1:]]
Gs = [load(f) for f in sys.argv[1:4]]
X = [list(map(int, l.split())) for l in open(sys.argv[4]).read().strip().split("\n")]; m = len(X[0])
N, F = load(sys.argv[5])
off = [0, Gs[0][0], Gs[0][0] + Gs[1][0]]; nG = off[2] + Gs[2][0]; assert N == nG + 3 * m
types = [(0, 1), (1, 2), (0, 2)]
xv = lambda a, j: off[a] + X[a][j]
wv = lambda t, j: nG + t * m + j
for a in range(3): assert len(set(X[a])) == m, 'maps must be injective'
fib = {}                                        # vertex -> fibre index
for j in range(m):
    for a in range(3): fib[xv(a, j)] = j
    for t in range(3): fib[wv(t, j)] = j
def side(v):                                    # copy index of a G vertex, or None for W
    if v >= nG: return None
    return 2 if v >= off[2] else (1 if v >= off[1] else 0)
def image(v, T, j):
    s = side(v)
    if s is not None: return (s, v - off[s])
    t = (v - nG) // m; a, b = types[t]
    xs = [c for c in range(3) if xv(c, j) in T]
    assert len(xs) <= 1
    if not xs: tgt = {0: 0, 1: 1, 2: 2}[t]      # w_01 -> 0, w_12 -> 1, w_02 -> 2
    else:
        c = xs[0]; assert c in (a, b), "w_bc together with x_a in an independent fibre subset"
        tgt = b if c == a else a
    return (tgt, X[tgt][j])
indep = lambda S: all(not F[p][q] for p, q in itertools.combinations(S, 2))
elems = []                                      # (vertex, frozenset T, fibre or None)
for j in range(m):
    fv = [xv(0, j), xv(1, j), xv(2, j), wv(0, j), wv(1, j), wv(2, j)]
    for r in range(1, 7):
        for T in itertools.combinations(fv, r):
            if indep(T):
                for v in T: elems.append((v, frozenset(T), j))
for v in range(nG):
    if v not in fib: elems.append((v, frozenset([v]), None))
img = [image(v, T, j) if j is not None else (side(v), v - off[side(v)]) for v, T, j in elems]
bad = 0; pairs = 0
for i in range(len(elems)):
    u, Tu, ju = elems[i]
    for k in range(i + 1, len(elems)):
        v, Tv, jv = elems[k]
        if u == v or F[u][v]: continue
        if ju is not None and ju == jv:
            if Tu != Tv: continue
        elif not all(not F[p][q] for p in Tu for q in Tv): continue
        pairs += 1
        (sa, pa), (sb, pb) = img[i], img[k]
        if sa == sb and (pa == pb or Gs[sa][1][pa][pb]):
            bad += 1
            if bad <= 5: print("VIOLATION", u, sorted(Tu), "->", img[i], "|", v, sorted(Tv), "->", img[k])
print(f"elements {len(elems)}, pairs checked {pairs}, violations {bad}")
print("CERTIFIED: alpha(F) <= alpha(G0)+alpha(G1)+alpha(G2)" if bad == 0 else "FAILED")
