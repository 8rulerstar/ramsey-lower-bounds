# Twelve copies: R(k+1, 4s-3) >= 12R(k,s) - 11, and R(8,25) >= 2449 (a cell not in the survey tables)

**Theorem D12.** For every graph G with clique number w and independence number a, the graph F below has 12|V(G)|
vertices, alpha(F) = 4a, and omega(F) = w + 1 if w >= 3 (4 if w = 2, 3 if w = 1). Hence for k >= 4

**R(k+1, 4s-3) >= 12R(k,s) - 11.**

This is the same kind of construction as theorem D in `../seven-copies` (there 7 positions, independence number tripled),
with 12 positions and the independence number multiplied by 4; it uses copies of a single graph only. For comparison,
DS1 2.3.i (Xu, Xie, Exoo, Radziszowski 2004) in complement form gives R(k+1, 2s-1) >= 4R(k,s) - 3 (k >= 4), and applying
it twice gives R(k+2, 4s-3) >= 16R(k,s) - 15, which raises k by 2. I have not found this statement in the literature;
it was found with the help of an AI coding assistant (Claude) and no expert has read the proof yet.

**What it gives.** For every cell listed in the dynamic survey *Small Ramsey Numbers* (DS1 rev. 18) the theorem is weaker
than the known bound; the closest is R(7,21): 1213 against 1214. It gives larger values in cells that the survey tables
do not list. The one checked on an actual graph:

| bound | best value I could derive from published results | graph | how checked |
|---|---|---|---|
| R(8,25) >= 2449 | 2049 (DS1 2.3.i with R(7,13) >= 513, google-research) | `R8_25_2448.txt`: twelve copies of the 204-vertex (7,7)-graph H204 (`H204.txt`, the same file as in `../triple-gluing`) | no K_8 by search over all 2448 roots; independent side by an exhaustive certificate check on the graph (`certifyD12.py`) |

"Best value I could derive" means: the survey tables and items 2.2.g, 2.3.g-i, 6.2.m-o, the google-research
ramsey_number_bounds files, recent papers I found (Yu 2026, Cremer 2026, Coniglio et al. 2026, AlphaEvolve 2026), closed
under monotonicity and the published recurrences (BEFS, XSR2, 2.3.g-i, products). It is not a search of all literature;
a cell outside the tables may simply not have been looked at. Other cells where theorems D or D12 give more than this
baseline (no graph built) are listed in `offtable.md`.

## Construction

Vertices (j, c) with j in V(G) and c in Z_12; let d = c - c' (mod 12).
- d = 0: (j, c) ~ (l, c) iff jl is an edge of G;
- d = 4, 6, 8 (type P): only the same index, (j, c) ~ (j, c');
- d = 1, 2, 5, 7, 10, 11 (type Q, twin rule): (j, c) ~ (l, c') iff jl is an edge of G (j != l);
- d = 3, 9: no edges.

`python3 glue12.py G.txt out.txt` builds F. In coordinates (x, y) = (c mod 4, c mod 3) on a 4 x 3 grid: P = same column
(different row), or same row and opposite columns (x, x+2); "none" = same row and neighbouring columns; Q = different row
and different column.

## Proof

A fibre is the set of 12 vertices with one index j.

**Cliques.** Let K be a clique and K_j its positions in fibre j. K_j is a P-clique: one position, two or three positions of
one column, or two opposite positions of one row. Vertices in different fibres j, l are at equal or Q-related positions and
jl is an edge of G, so the fibres used form a clique of G (r <= w fibres).
- If K_j has two positions (x,y), (x,y') of a column, any other fibre lies in a different column and in the remaining row
  y''. A whole column (three positions) admits no other fibre (|K| = 3).
- If K_j = {(x,y), (x+2,y)}, any other fibre lies in columns x +- 1 and rows other than y.
- Two fibres with more than one position each admit no third fibre: (column pair, row pair) must be
  {(x,y),(x,y')} and {(x+1,y''),(x+3,y'')}, and a third fibre would need row y'' and a row other than y''; (row pair, row
  pair) is {(x,y),(x+2,y)}, {(x+1,y'),(x+3,y')} and leaves no column; (column pair, column pair) is impossible.
So |K| <= r + 1 for r >= 3, |K| <= 4 for r = 2, |K| <= 3 for r = 1. Equality: on a maximum clique j_1..j_r of G take
(j_1,0), (j_1,6), (j_2,1), ..., (j_r,1). For k >= 4 and w <= k - 1 this gives omega(F) <= k.

**Independent sets: alpha(F) <= 4a.** For an independent set I let I_j = {c : (j,c) in I}. I_j is a label: a P-independent
set of positions (at most one per column, no opposite pair in a row). There are 168 labels (12, 48, 72, 36 of sizes 1..4).
If jl is an edge of G, I_j and I_l must be separated: disjoint with no Q-related pair, i.e. every cross pair lies in one
column or one row. The 198 separated pairs fall into six types (c != b rows):
A (30) two single positions in one row or one column; B (24) {(x',c)} and {(u,c),(v,c)} with u, v neighbouring columns and
x' the remaining column; C (72) {(x',c)} and {(x',b),(u,c)}; D (48) {(x',c)} and {(x',b),(u,c),(v,c)} with u, v
neighbouring; E (6) {(x,c),(x+1,c)} and {(x+2,c),(x+3,c)}; F (18) {(x1,a),(x2,b)} and {(x1,b),(x2,a)} (swap).

Colour kappa(c) = floor(c/3) = (y - x) mod 4. Give each label L a colour set C(L) in {0,1,2,3}:
- |L| = 1: C(L) = {kappa(c)}; |L| = 4: all four colours;
- |L| = 3: all colours except kappa(x',c) if L is the three-position label of a type D pair with partner (x',c) (there is
  at most one such partner), otherwise all four;
- |L| = 2, L = {(x1,a),(x2,b)}: if kappa takes two values on L, C(L) = kappa(L); if one value k0, let S be the colours of the
  swapped pair {(x1,b),(x2,a)}; C(L) = all colours minus S if |S| = 2, and {k0, k0+1} if |S| = 1.
Lemma (all 168 labels and 198 separated pairs checked by `prove12.py`): |C(L)| >= |L|, and separated labels have disjoint
colour sets. Then T_i = {j : i in C(I_j)} is an independent set of G for each i, and
|I| = sum |I_j| <= sum |C(I_j)| = |T_0| + |T_1| + |T_2| + |T_3| <= 4a. Conversely, positions {0,1,2,3} are P-independent,
so a maximum independent set of G gives an independent set of size 4a in F.

## Checks (`sh check.sh`)

- `prove12.py` verifies every finite claim of the proof (grid translation, labels, the six types of separated pairs, the
  colour-set lemma, the clique facts) and writes the four families to `families.txt`.
- `glue12.py H204.txt` rebuilds `R8_25_2448.txt` identically; `verify 7 7 H204.txt` checks the input.
- No K_8: `vpar2560` (vpar with MAXN 2560) over all roots, in 10 parallel parts; the script fails if any part fails.
- Independent side: `certifyD12.py H204.txt R8_25_2448.txt` checks on the graph file, for every pair of fibre states that
  can lie together in an independent set, the colour-set conditions above (34,272 elements, 297,722,088 admissible pairs,
  0 violations, under a minute). It uses the same assignment as the proof and alpha(H204) from `verify`; it does not check
  the clique side (that is the vpar search) and deleting any single edge of a test graph makes it fail.
- Separately (code not included): exact omega and alpha for all labelled graphs on up to 6 vertices, all 1,044 graphs on 7
  vertices, about 100,000 random graphs on 7 to 12 vertices, and F from the Paley graphs P(13), P(17): no violation;
  changing the pattern (d = 3 as Q, d = 6 as none, d = 3 as P) gives violations.
