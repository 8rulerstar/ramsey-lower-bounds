# General copy patterns (theorem DG) and R(8,18) >= 1133

DS1 rev. 18 lists R(8,18) >= 1049; google-research (2026) lists 1052, and `../r8-18` gave 1054. The graph
`R8_18_1132.txt` has 1132 vertices, no K_8 and no independent set of size 18, so **R(8,18) >= 1133**.

It comes from one theorem that contains theorems D, D1 and D12 (`../seven-copies`, `../r8-12`, `../twelve-copies`) as
special cases. I have not found it in the literature; it was found with the help of an AI coding assistant (Claude) and
no expert has read the proof yet.

## Setting

A pattern is a set of positions with three relations between two different positions: P (only copies of the same
vertex are joined), Q (twin rule) and none. The heptagon pattern of theorem D has positions Z_7, P for difference
+-1 and Q otherwise; the pattern of theorem D12 has positions Z_12, P for differences 4, 6, 8, none for 3, 9, Q otherwise.

Let Gamma be a graph and give each vertex j of Gamma a nonempty set pos(j) of positions. F(Gamma, pos) has the vertices
(j, c), c in pos(j); (j, c) ~ (l, c') iff (same position or Q, and jl is an edge of Gamma) or (P, and j = l).

A label is a P-independent set of positions; two labels are separated if they are disjoint and no pair between them is
Q-related. A valid colouring with t colours gives each label L a set C(L) of colours with |C(L)| >= |L|, such that
separated labels get disjoint colour sets. Let W_i be the set of vertices j such that colour i occurs in C(L) for some label
L inside pos(j).

## Theorem DG

For a valid colouring of the pattern, alpha(F) <= alpha(Gamma[W_0]) + ... + alpha(Gamma[W_{t-1}]), and F is an induced
subgraph of the full product, so for the Z_7 and Z_12 patterns omega(F) <= max(omega(Gamma) + 1, 4).

**Proof (independent sets).** Let I be independent and I_j = {c : (j, c) in I}; two positions in P relation in one fibre
are adjacent, so I_j is empty or a label inside pos(j). Let T_i = {j : I_j nonempty, i in C(I_j)}; then T_i is a subset of
W_i. If j, l in T_i were adjacent in Gamma, then for c in I_j, d in I_l the vertices (j,c), (l,d) are non-adjacent, so c, d
are neither equal nor Q-related: I_j and I_l are separated, their colour sets are disjoint, yet both contain i. So T_i is
independent in Gamma[W_i], and |I| = sum |I_j| <= sum |C(I_j)| = sum |T_i| <= sum alpha(Gamma[W_i]).
**Cliques.** F is an induced subgraph of the full product F(Gamma, pos) with pos(j) = all positions for every j, so
omega(F) is at most the clique number of that product, which is max(omega(Gamma) + 1, 4) for the Z_7 and Z_12 patterns: the
clique arguments in `../seven-copies` (case without private vertices) and `../twelve-copies` apply verbatim to any Gamma.

**Gluing.** Glue graphs A_1, ..., A_r along a common induced subgraph M (no edges between private vertices of different
A_p) to get Gamma; then omega(Gamma) = max omega(A_p). Put M on all positions and the private vertices of A_p on a set S_p.
If there is a valid colouring in which the labels inside S_p use only a colour set B_p, with the B_p pairwise disjoint,
then each Gamma[W_i] is one of the A_p or M.

## The case used here (Z_7, "layer + side")

A (k,p)-graph H on positions {0,1,3,4} (two colours) and a (k,q)-graph G on position 2 (one colour), M on all seven
positions. The valid colouring is in `colourings.json` (key in `spec_R8_18.json`) and is re-checked from the definition by
`verify_colourings.py`. This gives, for k >= 4,

**R(k+1, 2p+q-2) >= 4n_H + n_G + 2m + 1.**

(Gluing the 2.3.i graph of H, which has 4n_H vertices, to G by 2.3.h along the same M gives 4n_H + n_G + m; this has m
more.)

With H = H204 (the 204-vertex (7,7)-graph, `H204.txt`), G = G114 (the 114-vertex (7,6)-graph, `G114.txt`) and M = P(101)
(`maps_P101_H204_G114.txt`): 4 * 204 + 114 + 2 * 101 = 1132 vertices, an (8, 2*7+6-2) = (8,18)-graph.

## Checks (`sh check.sh`, about 20 seconds on 10 cores)

- `verify_colourings.py` re-checks the stored colourings from the definition.
- `gluegen.py spec_R8_18.json` rebuilds `R8_18_1132.txt` identically; `verify` checks H204 (7,7), G114 (7,6), P(101) (6,6).
- No K_8: `vpar` over all 1132 roots in 10 parallel parts (the script fails if any part fails).
- Independent side: `certifyDgen.py` reads the graph file and checks that every independent position set in a fibre is a
  label, that any two fibre states with no edge between them and a shared colour come from vertices non-adjacent in Gamma,
  and that each W_i is exactly H204, H204, G114 (3,665 elements, 3,498,853 admissible pairs, 0 violations). With alpha of
  the inputs from `verify` this gives alpha <= 6 + 6 + 5 = 17 without relying on the written proof.
- Separately (code not included): about 145 million random exact instances of theorem DG (several patterns and layouts)
  with no violation, and negative controls (impossible layouts, enlarged layers, changed pattern) that do fail.
