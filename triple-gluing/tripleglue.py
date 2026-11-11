"""Independent implementation of candidate theorem H (triple gluing), from the rules in notes/THEORY_A_step1.md:
G_1, G_2, G_3 (k,s_i)-graphs, M (K_{k-1}-free, m vertices) induced in each via maps x_a(j). New vertices w_ab(j) for
ab in {12, 23, 13}. Edges: E1 edges of each G_a; E2 x_a(j) ~ x_b(j); E3 w_ab(j) ~ N_{G_a}(x_a(j)) and N_{G_b}(x_b(j));
E4 w_ab(j) ~ x_c(j) (c the third index); E5 w_e(j) ~ w_f(l) iff jl in E(M) (any e, f; never for j = l).
Claim: a (k, s_1+s_2+s_3-2)-graph on n_1+n_2+n_3+3m vertices.
Usage: python tripleglue.py G1 G2 G3 maps.txt Medges.txt out.txt   (maps: three lines of m vertex numbers)"""
import sys
def load(f):
    L = open(f).read().split(); n = int(L[0]); return n, [[c == "1" for c in r] for r in L[1:]]
Gs = [load(f) for f in sys.argv[1:4]]
X = [list(map(int, l.split())) for l in open(sys.argv[4]).read().strip().split("\n")]
m = len(X[0]); ME = [[c == "1" for c in r] for r in open(sys.argv[5]).read().split()]
off = [0, Gs[0][0], Gs[0][0] + Gs[1][0]]; nG = off[2] + Gs[2][0]
types = [(0, 1), (1, 2), (0, 2)]; W = {ab: nG + t * m for t, ab in enumerate(types)}; N = nG + 3 * m
F = [bytearray(b"0" * N) for _ in range(N)]
def e(a, b): F[a][b] = F[b][a] = 49
for a in range(3):                                            # E1
    n, A = Gs[a]
    for i in range(n):
        for j in range(i):
            if A[i][j]: e(off[a] + i, off[a] + j)
for j in range(m):                                            # E2
    for a in range(3):
        for b in range(a):
            e(off[a] + X[a][j], off[b] + X[b][j])
for (a, b) in types:                                          # E3, E4
    c = 3 - a - b
    for j in range(m):
        w = W[(a, b)] + j
        for q in (a, b):
            n, A = Gs[q]
            for v in range(n):
                if A[X[q][j]][v]: e(w, off[q] + v)
        e(w, off[c] + X[c][j])
for t1 in types:                                              # E5
    for t2 in types:
        for j in range(m):
            for l in range(m):
                if j != l and ME[j][l]: e(W[t1] + j, W[t2] + l)
for i in range(N): assert F[i][i] == 48
open(sys.argv[6], "w").write(f"{N}\n" + "\n".join(r.decode() for r in F) + "\n")
print("built", N)
