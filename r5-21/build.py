"""Build the 444-vertex (5,21)-graph (XSR2 Theorem 3, k = 5) and check its hypotheses.
Usage: python3 build.py r55_42some.g6 out.txt
  r55_42some.g6: B. D. McKay's list of 42-vertex (5,5)-graphs, https://users.cecs.anu.edu.au/~bdm/data/ramsey.html
  (not included here). Graph number 2 (0-based line index) is used.
G384: vertices U (3) and V (381) of the cubic-residue colouring M_p of Mathon, p = 127, in the form of Xu and
Radziszowski, EJC 16 (2009) #N1: vertices (0, beta^i) and (beta^i, a), colour of {(x,y),(s,t)} = cubic character of
x*t - y*s (beta = 3); the p disjoint triangles of the special colour are recoloured to colour 0; U-U edges as in
their Fig. 1 (with colours relabelled 0->2, 1->0, 2->1). G384 = colour 0. reproduce.sh checks that it is a (5,17)-graph.
M: the 18 vertices W1 + W2 of H (common_part.txt), both classes triangle-free, with an induced copy in G384 (map).
F = G384 + H + copies of M[W1] and M[W2] (no edges between them); w ~ u_j iff its G384 vertex is adjacent to u_j,
w ~ v_j iff its H vertex is adjacent to v_j; plus the matching between the two copies of M. 384 + 42 + 18 = 444."""
import ast, re, sys
p = 127; beta = 3; logt = {pow(beta, e, p): e for e in range(p - 1)}; ch = lambda v: logt[v % p] % 3
U = [(0, 1), (0, beta), (0, beta * beta % p)]; V = [(pow(beta, i, p), a) for i in range(3) for a in range(p)]
X = U + V; n = len(X); sg = [2, 0, 1]
C = [[-1] * n for _ in range(n)]
for i in range(n):
    for j in range(i + 1, n):
        (x, y), (s, t) = X[i], X[j]; d = (x * t - y * s) % p
        C[i][j] = C[j][i] = ch(d) if d else 0
for i, row in enumerate(("x01", "0x2", "12x")):
    for j, c in enumerate(row):
        if c != "x": C[i][j] = C[j][i] = sg[int(c)]
G = [[i != j and C[i][j] == 0 for j in range(n)] for i in range(n)]
open("G384.txt", "w").write(f"{n}\n" + "\n".join("".join("1" if x else "0" for x in r) for r in G) + "\n")
def g6(s):
    s = s.strip(); N = ord(s[0]) - 63; bits = []
    for ch_ in s[1:]: v = ord(ch_) - 63; bits += [(v >> k) & 1 for k in range(5, -1, -1)]
    A = [[False] * N for _ in range(N)]; k = 0
    for j in range(1, N):
        for i in range(j): A[i][j] = A[j][i] = bool(bits[k]); k += 1
    return A
line = open("common_part.txt").read()
h = int(re.search(r"h=(\d+)", line).group(1))
H = g6([l for l in open(sys.argv[1]) if l.strip()][h]); nH = len(H)
open("H42.txt", "w").write(f"{nH}\n" + "\n".join("".join("1" if x else "0" for x in r) for r in H) + "\n")
W1 = ast.literal_eval(re.search(r"W1=(\[[^\]]*\])", line).group(1)); W2 = ast.literal_eval(re.search(r"W2=(\[[^\]]*\])", line).group(1))
inv = {hv: gv for gv, hv in ast.literal_eval(re.search(r"map=(\{.*\})", line).group(1)).items()}
Ms = W1 + W2; m = len(Ms)
for a in Ms:
    for b in Ms:
        if a != b: assert H[a][b] == G[inv[a]][inv[b]], "not an induced copy"
for Wc in (W1, W2):
    assert not any(H[a][b] and H[a][c] and H[b][c] for a in Wc for b in Wc for c in Wc if a < b < c), "triangle in a class"
N = n + nH + m; Wo = n + nH
F = [bytearray(b"0" * N) for _ in range(N)]
def e(x, y): F[x][y] = F[y][x] = 49
for i in range(n):
    for j in range(i):
        if G[i][j]: e(i, j)
for i in range(nH):
    for j in range(i):
        if H[i][j]: e(n + i, n + j)
part = {hv: (0 if hv in W1 else 1) for hv in Ms}
for t, hv in enumerate(Ms):
    gv = inv[hv]; e(gv, n + hv)
    for s, hw in enumerate(Ms[:t]):
        if part[hv] == part[hw] and H[hv][hw]: e(Wo + t, Wo + s)
    for j in range(n):
        if G[gv][j]: e(Wo + t, j)
    for j in range(nH):
        if H[hv][j]: e(Wo + t, n + j)
open(sys.argv[2], "w").write(f"{N}\n" + "\n".join(r.decode() for r in F) + "\n")
print("built", N, "vertices; induced copy and triangle-free classes checked")
