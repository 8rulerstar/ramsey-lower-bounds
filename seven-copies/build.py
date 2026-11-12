"""Seven-copy construction. usage: python3 build.py p out.txt  (G = Paley graph P(p))
F has vertices (j, c), j in V(G), c in 0..6, numbered j*7 + c.
Pattern P on pairs of copies c < d, index d*(d-1)/2 + c:
  '2': (j,c) ~ (j,d) inside every fibre j;
  for every edge jl of G: (j,c) ~ (l,c) for all c, and (j,c) ~ (l,d) for c != d with P = '1'."""
import sys, itertools
P = "001112121221211221111"
def idx(c, d):
    if c > d: c, d = d, c
    return d * (d - 1) // 2 + c
def paley(p):
    sq = {x * x % p for x in range(1, p)}
    return [(a, b) for a in range(p) for b in range(a + 1, p) if (b - a) % p in sq]
def build(n, E):
    N = 7 * n; A = [[0] * N for _ in range(N)]
    def add(u, v): A[u][v] = A[v][u] = 1
    for j in range(n):
        for c, d in itertools.combinations(range(7), 2):
            if P[idx(c, d)] == '2': add(7 * j + c, 7 * j + d)
    for j, l in E:
        for c in range(7):
            add(7 * j + c, 7 * l + c)
            for d in range(7):
                if c != d and P[idx(c, d)] == '1': add(7 * j + c, 7 * l + d)
    return A
if __name__ == "__main__":
    p = int(sys.argv[1]); A = build(p, paley(p))
    open(sys.argv[2], "w").write(f"{len(A)}\n" + "\n".join("".join(map(str, r)) for r in A) + "\n")
