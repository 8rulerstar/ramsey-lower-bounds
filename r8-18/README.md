# R(8,18) >= 1054

DS1 rev. 18 lists R(8,18) >= 1049; google-research (ramsey_number_bounds, 2026-10-22) lists 1052. The graph
`R8_18_1053.txt` has 1053 vertices, no K_8 and no independent set of size 18.

**Construction (DS1 2.3.h with a larger common part).** G816 = the 816-vertex (8,13)-graph of `../r8-19`, built from the
204-vertex (7,7)-graph H204 (`H204.txt`) by the 4-layer rule of XXER (DS1 2.3.i, complement form): vertices (i, j),
i = 0..3, j in V(H204); same layer: edges of H204; layers {0,1} or {2,3}: edge iff same j; other layers: edge iff
j != j' and jj' is an edge of H204. Then alpha(G816) <= 2 alpha(H204) = 12 and omega(G816) <= 7.
C133 (`C133.txt`) is a 133-vertex (8,6)-graph. The two graphs share an induced 104-vertex subgraph M with omega(M) = 6:
P(101) inside a vertex neighbourhood, plus 3 vertices that exist in G816 because of its layers (closed twins placed in
layer 1). 2.3.h glues them: 816 + 133 + 104 = 1053 vertices, so R(8,18) >= 1054.

Proof of alpha(G816) <= 12: for an independent set I let S_i be its projection to layer i. S_0, S_1 are disjoint, as are
S_2, S_3, and S_0 + S_2 + (S_1 n S_3) and S_1 + S_3 + (S_0 n S_2) are independent in H204 with total size |I|.

## Checks
- `python3 check_structure.py`: the first 816 vertices are exactly the layer graph of `H204.txt`; the only edges between
  G816 and C133 are the 104 matching edges x_G(i) x_C(i); each new vertex w_i is a twin of x_G(i) in G816 and of x_C(i)
  in C133 and adjacent to neither; M is induced in both parts (0 violations).
- `sh check.sh` runs all checks below.
- `verify 8 6 C133.txt`: C133 is an (8,6)-graph. `verify 8 7 H204.txt`: alpha(H204) <= 6 (only the upper bound is needed).
- No K_8: `vpar 8 R8_18_1053.txt 0 0 1053` (all roots, about 2 x 10^8 nodes).
- No independent 18-set: map each w_i in I to x_G(i) if x_G(i) is not in I, else to x_C(i) (x_G(i), x_C(i) are adjacent,
  so not both are in I); the image is independent in G816 and C133, so alpha <= 12 + 5 = 17. This rests on the proof of
  alpha(G816) <= 12 above, not on a direct search.

Made with the help of an AI coding assistant (Claude); checks rerun by a second, independently written script.
