"""3-colouring of K_292 for R(3,3,16) >= 293 by DS1 6.2.g / XXER (EJC 11 (2004) #R35, Theorem 7 colouring):
from a (3,15)-graph G on m = 73 vertices, vertices (i, j), i = 0..3, j = 0..m-1:
  inside a copy: G-edge -> colour 2, else colour 3
  between {0,1} and {2,3}: j1 == j2 -> 1; else G-edge -> 2, non-edge -> 3
  between 0-1 and between 2-3: j1 == j2 -> 3; else -> 1
Claim: colour 1 and colour 2 have no triangle, colour 3 has no K16. Writes c1.txt, c2.txt, c3.txt (graph of each colour)
and colouring.txt (rows of digits 0..3, 0 on the diagonal). Usage: python3 build.py G73.txt"""
import sys
t = open(sys.argv[1]).read().split(); m = int(t[0]); G = [[c == "1" for c in r] for r in t[1:]]
N = 4 * m
def col(a, b):
    i1, j1 = divmod(a, m); i2, j2 = divmod(b, m)
    if i1 == i2: return 2 if G[j1][j2] else 3
    if {i1, i2} not in ({0, 1}, {2, 3}): return 1 if j1 == j2 else (2 if G[j1][j2] else 3)
    return 3 if j1 == j2 else 1
C = [[0 if a == b else col(a, b) for b in range(N)] for a in range(N)]
assert all(C[a][b] == C[b][a] for a in range(N) for b in range(N))
open("colouring.txt", "w").write(f"{N}\n" + "\n".join("".join(map(str, r)) for r in C) + "\n")
for c in (1, 2, 3):
    open(f"c{c}.txt", "w").write(f"{N}\n" + "\n".join("".join("1" if x == c else "0" for x in r) for r in C) + "\n")
print("built", N)
