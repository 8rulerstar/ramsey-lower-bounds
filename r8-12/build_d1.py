"""Rebuild R8_12_520.txt by theorem D1: python3 build_d1.py  (writes regen.txt)"""
from patglue import build, read_graph
Gs = [read_graph("H204.txt"), read_graph("G114.txt")]
maps = [[int(x) for x in l.split()] for l in open("maps_P101_H204_G114.txt") if l.strip()]
n, adj, info = build(Gs, maps, sides=(0, 1), npos=4, ipairs={frozenset((0, 1)), frozenset((2, 3))})
rows = ["".join("1" if v in adj[u] else "0" for v in range(n)) if isinstance(adj[u], set) else "".join(map(str, adj[u])) for u in range(n)]
open("regen.txt", "w").write(f"{n}\n" + "\n".join(rows) + "\n")
assert info["induced"], "copies of M are not induced"
print(n, "induced copies: True")
