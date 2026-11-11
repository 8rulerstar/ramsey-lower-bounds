"""Build the 1238-vertex (8,19)-graph by DS1 2.2.h / 2.3.h, using Tatarevic's 218-vertex (7,8)-colouring.
Usage: python3 build.py g78.218 out.txt
  g78.218: graphs/g78.218 from https://github.com/milostatarevic/ramsey-numbers (not included here).
Steps: H204 = Taylor double cover of the Paley graph P(101), a (7,7)-graph; G816 = XXER Theorem 9 (DS1 2.3.i) applied
to the complement of H204 with k = 7, l = 8, then complemented: an (8,13)-graph whose vertices 0..203 induce H204;
G218 = colour 1 of g78.218, an (8,7)-graph, whose vertices phi[i] (phi.txt) induce H204 (vertex i -> phi[i]);
F = G816 + G218 + a third copy W of H204, W_i joined to the neighbours of i in G816 and of phi[i] in G218, plus the
edges i -- phi[i]. 816 + 218 + 204 = 1238."""
import sys
p = 101; qr = {x * x % p for x in range(1, p)}
NH = 2 * p + 2; H = [[0] * NH for _ in range(NH)]
def eh(a, b): H[a][b] = H[b][a] = 1
for x in range(p):
    eh(2 * p, x); eh(2 * p + 1, p + x)
    for y in range(p):
        d = (x - y) % p
        if d == 0: continue
        if d in qr: eh(x, y); eh(p + x, p + y)
        else: eh(x, p + y)
m = NH
Hc = [[(i != j) and not H[i][j] for j in range(m)] for i in range(m)]     # complement of H204
def edge816(a, b):                                                         # XXER Theorem 9 on Hc, then complement
    i1, j1 = divmod(a, m); i2, j2 = divmod(b, m)
    if a == b: return False
    if i1 == i2: e = Hc[j1][j2]
    elif {i1, i2} not in ({0, 1}, {2, 3}): e = True if j1 == j2 else Hc[j1][j2]
    else: e = j1 != j2
    return not e
nG = 4 * m
rows = [l.strip() for l in open(sys.argv[1]) if l.strip()]
A = [[int(c) for c in r] for r in rows]; nH = len(A)
phi = [int(x) for x in open("phi.txt").read().split()]
for i in range(m):
    for j in range(m):
        if i != j:
            assert edge816(i, j) == bool(H[i][j]), "G816 part"
            assert A[phi[i]][phi[j]] == H[i][j], "G218 part"
N = nG + nH + m; U, V, W = 0, nG, nG + nH
F = [bytearray(b"0" * N) for _ in range(N)]
def e(a, b): F[a][b] = F[b][a] = 49
for a in range(nG):
    for b in range(a):
        if edge816(a, b): e(U + a, U + b)
for a in range(nH):
    for b in range(a):
        if A[a][b]: e(V + a, V + b)
for i in range(m):
    e(U + i, V + phi[i])
    for j in range(i):
        if H[i][j]: e(W + i, W + j)
    for j in range(nG):
        if edge816(i, j): e(W + i, U + j)
    for j in range(nH):
        if A[phi[i]][j]: e(W + i, V + j)
open(sys.argv[2], "w").write(f"{N}\n" + "\n".join(r.decode() for r in F) + "\n")
print("built", N, "vertices")
