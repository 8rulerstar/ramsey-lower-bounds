"""Certificate for the pair-specific triple gluing on a concrete graph F (layout of pairglue.build).
Checks exhaustively the pair conditions behind the independent-set proof: for every independent set I of F the map
phi_I (below) sends I injectively onto an independent set of the disjoint union G_0 + G_1 + G_2, hence
alpha(F) <= alpha(G_0) + alpha(G_1) + alpha(G_2).
fibre(j) = {x_a(j) : j in D_a} + {w_e(j) : j in S_e}.  phi_I(v) depends only on T = I cap fibre(v):
  G-vertex -> itself;  no x in T: w_01 -> side 0, w_12 -> side 1, w_02 -> side 2;  x_c(j) in T: w_e (c in e) -> other end
  of e (w_e with c not in e cannot be in T).  Image of w_e(j) on side d is x_d(j).
Written independently of pairglue.py: reads F from the file and only uses the maps to know the fibres.
Usage: python3 certifyP.py G0 G1 G2 maps.txt F.txt"""
import itertools, sys
def load(f):
    L = open(f).read().split(); n = int(L[0]); return n, [[c == "1" for c in r] for r in L[1:]]
Gs = [load(f) for f in sys.argv[1:4]]
lines = open(sys.argv[4]).read().split("\n")
X = [dict((int(p.split(':')[0]), int(p.split(':')[1])) for p in lines[a].split()) for a in range(3)]
S = [sorted(map(int, lines[3 + t].split())) for t in range(3)]
N, F = load(sys.argv[5])
types = [(0, 1), (1, 2), (0, 2)]
off = [0, Gs[0][0], Gs[0][0] + Gs[1][0]]; nG = off[2] + Gs[2][0]
assert N == nG + sum(len(s) for s in S)
for a in range(3):
    assert len(set(X[a].values())) == len(X[a]), 'maps must be injective'
    need = set()
    for t, e in enumerate(types):
        if a in e: need |= set(S[t])
    assert need <= set(X[a]), 'x_a must be defined on D_a'
W = {}; v = nG
for t in range(3):
    for j in S[t]: W[(t, j)] = v; v += 1
wtype = {v: t for (t, j), v in W.items()}
idxs = sorted(set().union(*[set(x) for x in X]))
fibres = {j: [off[a] + X[a][j] for a in range(3) if j in X[a]] + [W[(t, j)] for t in range(3) if (t, j) in W] for j in idxs}
fib = {}
for j, fv in fibres.items():
    for v in fv: assert v not in fib; fib[v] = j
def side(v):
    if v >= nG: return None
    return 2 if v >= off[2] else (1 if v >= off[1] else 0)
def image(v, T, j):
    s = side(v)
    if s is not None: return (s, v - off[s])
    t = wtype[v]; a, b = types[t]
    xs = [c for c in range(3) if j in X[c] and off[c] + X[c][j] in T]
    assert len(xs) <= 1, 'two x of one fibre in an independent set'
    if not xs: tgt = t                      # type index t = 0, 1, 2 goes to side 0, 1, 2 (each lies in its type)
    else:
        c = xs[0]; assert c in (a, b), 'w_e with x_c, c not in e, in an independent fibre subset'
        tgt = b if c == a else a
    assert tgt in (a, b)
    return (tgt, X[tgt][j])
indep = lambda Sx: all(not F[p][q] for p, q in itertools.combinations(Sx, 2))
elems = []
for j, fv in fibres.items():
    for r in range(1, len(fv) + 1):
        for T in itertools.combinations(fv, r):
            if indep(T):
                for v in T: elems.append((v, frozenset(T), j))
for v in range(nG):
    if v not in fib: elems.append((v, frozenset([v]), None))
img = [image(v, T, j) for v, T, j in elems]
bad = pairs = 0
for i in range(len(elems)):
    u, Tu, ju = elems[i]; Fu = F[u]; iu = img[i]
    for k in range(i + 1, len(elems)):
        v, Tv, jv = elems[k]
        if u == v or Fu[v]: continue
        if ju is not None and ju == jv:
            if Tu != Tv: continue
        elif not all(not F[p][q] for p in Tu for q in Tv): continue
        pairs += 1
        iv = img[k]
        if iu == iv or (iu[0] == iv[0] and Gs[iu[0]][1][iu[1]][iv[1]]):
            bad += 1
            if bad <= 5: print('VIOLATION', u, sorted(Tu), iu, v, sorted(Tv), iv)
print('elements %d, admissible pairs %d, violations %d' % (len(elems), pairs, bad))
print('CERTIFICATE OK: alpha(F) <= alpha(G_0)+alpha(G_1)+alpha(G_2)' if bad == 0 else 'CERTIFICATE FAILED')
sys.exit(0 if bad == 0 else 1)
