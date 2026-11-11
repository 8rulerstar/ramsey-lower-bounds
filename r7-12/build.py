# Build the 419-vertex (7,12)-graph by the gluing construction of DS1 section 2.3.h.
# Usage: python3 build.py R6_7_114_input.txt out.txt
import sys
inp, out = sys.argv[1], sys.argv[2]
L = open(inp).read().split(); n = int(L[0])
X = [[int(c) for c in L[1 + i]] for i in range(n)]
G = [[0 if i == j else 1 - X[i][j] for j in range(n)] for i in range(n)]   # complement: a (7,6)-graph
p = 101; qr = {x * x % p for x in range(1, p)}
# vertices 0..100 of G induce the Paley graph P(101) (checked here)
assert all(G[i][j] == ((i - j) % p in qr) for i in range(p) for j in range(p) if i != j)
# H: Taylor double cover of P(101), a (7,7)-graph on 204 vertices; its vertices 0..100 also induce P(101)
NH = 2 * p + 2; H = [[0] * NH for _ in range(NH)]
def eh(a, b): H[a][b] = H[b][a] = 1
for x in range(p):
    eh(2 * p, x); eh(2 * p + 1, p + x)
    for y in range(p):
        d = (x - y) % p
        if d == 0: continue
        if d in qr: eh(x, y); eh(p + x, p + y)
        else: eh(x, p + y)
assert all(H[i][j] == G[i][j] for i in range(p) for j in range(p))
# glue: G (114) + H (204) + a third copy W of P(101). W_i is adjacent to the neighbours of vertex i in G and in H;
# G_i and H_i (i < 101) are joined by an edge.
N = n + NH + p; U, V, W = 0, n, n + NH
F = [[0] * N for _ in range(N)]
def e(a, b): F[a][b] = F[b][a] = 1
for i in range(n):
    for j in range(i):
        if G[i][j]: e(U + i, U + j)
for i in range(NH):
    for j in range(i):
        if H[i][j]: e(V + i, V + j)
for i in range(p):
    e(U + i, V + i)
    for j in range(i):
        if G[i][j]: e(W + i, W + j)
    for j in range(n):
        if G[i][j]: e(W + i, U + j)
    for j in range(NH):
        if H[i][j]: e(W + i, V + j)
open(out, 'w').write(str(N) + '\n' + '\n'.join(''.join(map(str, r)) for r in F) + '\n')
print('built', N, 'vertices')
