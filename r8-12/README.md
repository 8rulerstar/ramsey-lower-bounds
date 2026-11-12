# R(8,12) >= 521

The best lower bound I know is R(8,12) >= 511 (google-research, ramsey_number_bounds, 2026); in DS1 rev. 18 Table Ia
the R(8,12) cell has no lower bound printed, as far as I can read the table. The graph `R8_12_520.txt` has 520 vertices, no K_8 and no independent
set of size 12.

## Theorem D1

Let k >= 4, G_1 a (k,p)-graph on n_1 vertices, G_2 a (k,q)-graph on n_2 vertices, and M a graph on m vertices that is an
induced subgraph of both (copies x_1(j), x_2(j); no condition on M). Then there is a (k+1, p+q-1)-graph on
n_1 + n_2 + 2m vertices, so

**R(k+1, p+q-1) >= n_1 + n_2 + 2m + 1.**

With G_1 = G_2 = M this is DS1 2.3.i (Xu, Xie, Exoo, Radziszowski 2004, in complement form: R(k+1, 2s-1) >= 4R(k,s) - 3).
The new point is that the two graphs may differ and only a common induced subgraph is needed.

**Construction.** Four positions 0, 1, 2, 3; position a in {0,1} carries G_{a+1}, positions 2 and 3 carry copies W_2,
W_3 of M. Vertices of M (in G_a or in W_c) have an index j; we write (j, c). The other vertices of G_1, G_2 are private.
- same position: the edges of G_a, or of M;
- positions {0,1} and {2,3} ("neighbours"): only (j,c) ~ (j,c') with the same index;
- other pairs of positions (twin rule): (j,c) ~ (l,c') iff jl is an edge of M; a private vertex y of G_c and (l,c') are
  adjacent iff y ~ x_c(l) in G_c; private vertices of different sides are not adjacent.

**No K_{k+1}.** For a clique K let K_j be the set of positions of its vertices with index j. Inside an index only neighbour
positions are adjacent, so K_j is one position, {0,1} or {2,3}. Vertices with different indices lie in the same or in
non-neighbour positions and have adjacent indices. If some K_j = {0,1}, every other indexed vertex is at position 2 or 3;
two such pairs {0,1}, {2,3} leave no room for a third index, and then |K| = 4 <= k. Likewise at most one index carries
the pair {2,3}. If K has no private vertex, the indices
form a clique of M (so at most k-1 of them, M being induced in G_1) and at most one index carries a pair: |K| <= k.
If K has private vertices, they lie in one side G_c, the other side position has no vertex of K (its vertices are not
adjacent to private vertices of G_c), and mapping each indexed vertex (l, c') to x_c(l) (twin rule) sends K onto a clique
of G_c, where only a pair {2,3} can collapse to one vertex: |K| <= (k-1) + 1 = k.

**No independent set of size p+q-1.** Let I be independent and I_j the positions of its index-j vertices; I_j is a
single position or a non-neighbour pair {0,2}, {0,3}, {1,2}, {1,3}. Colour positions 0, 2 with colour 0 and 1, 3 with
colour 1. For a in {0,1} let F_a contain all pairs and the singletons of colour a, and let T_a be the private vertices of
G_{a+1} in I together with x_{a+1}(j) for every j with I_j in F_a. Each singleton lies in one F_a and each pair in both,
so |I| <= |T_0| + |T_1|. T_a is independent in G_{a+1}: if I_j, I_l are in F_a and jl is an edge of M, then every
position of I_j must be a neighbour of every position of I_l, which forces two singletons at neighbour positions, and
those have different colours, a contradiction; so jl is not an edge and x(j), x(l) are not adjacent (M induced). A
private y in I and I_j in F_a: I_j contains position a or a non-neighbour of a (singletons of colour a are a itself or the
position opposite to it; pairs contain 2 or 3), and that vertex is not adjacent to y, so by the twin rule neither is
x(j). Hence |I| <= alpha(G_1) + alpha(G_2) <= (p-1) + (q-1).

## The graph

G_1 = H204, the 204-vertex (7,7)-graph (Taylor double cover of P(101), `H204.txt`, same file as in `../triple-gluing`);
G_2 = G114, the complement of the 114-vertex (6,7)-graph of Exoo and Tatarevic, a (7,6)-graph (`G114.txt`);
M = the Paley graph P(101), induced in both (`maps_P101_H204_G114.txt`: line a gives x_a(j) for j = 0..100).
204 + 114 + 2 * 101 = 520 vertices, so R(8, 7+6-1) = R(8,12) >= 521.

## Checks (`sh check.sh`)
- `python3 build_d1.py` rebuilds the graph from the inputs (identical to `R8_12_520.txt`) and checks the copies are induced.
- `verify 7 7 H204.txt`, `verify 7 6 G114.txt`: the inputs are (7,7)- and (7,6)-graphs.
- No K_8: `vpar 8 R8_12_520.txt 0 0 520` (all roots, about 1.3 x 10^7 nodes).
- Independent side: `python3 certifyD1.py H204.txt G114.txt maps_P101_H204_G114.txt R8_12_520.txt` checks on this graph,
  for every pair of elements that can lie together in an independent set, the conditions of the assignment above
  (924 elements, 227,509 admissible pairs, 0 violations), so alpha <= 6 + 5 = 11 does not rest on the written proof (the certificate uses the same assignment as the proof and
alpha(G_i) from `verify`).

Found with the help of an AI coding assistant (Claude); no expert has read the proof yet. I have not found theorem D1
in the literature (DS1 rev. 18 and the papers listed in `../seven-copies`).
