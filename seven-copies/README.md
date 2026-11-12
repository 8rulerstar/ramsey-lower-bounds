# Heptagon gluing: R(k+1, s_1+s_2+s_3-2) >= n_1+n_2+n_3+4m+1, R(7,16) >= 708, R(8,19) >= 1429

**Theorem D.** Let k >= 4. For i = 1, 2, 3 let G_i be a (k, s_i)-graph on n_i vertices (no K_k, no independent set of
size s_i), and let M be a graph on m vertices that is an induced subgraph of all three (copies x_i(j), j in V(M); no other
condition on M). Then there is a (k+1, s_1 + s_2 + s_3 - 2)-graph on n_1 + n_2 + n_3 + 4m vertices, so

**R(k+1, s_1 + s_2 + s_3 - 2) >= n_1 + n_2 + n_3 + 4m + 1.**

With G_1 = G_2 = G_3 = M = G a (k,s)-graph on R(k,s) - 1 vertices: **R(k+1, 3s-2) >= 7R(k,s) - 6** (k >= 4).
The two-graph version (theorem D1, `../r8-12`) gives R(k+1, p+q-1) >= n_1 + n_2 + 2m + 1 and contains DS1 2.3.i
(Xu, Xie, Exoo, Radziszowski, Electron. J. Combin. 11 (2004) #R35: R(2k-1, l) >= 4R(k, l-1) - 3; in complement form four
copies with the independence number doubled) as the case G_1 = G_2 = M. The closest other result I know is DS1 2.3.c
(Chung, Cleve, Dagum: R(3, 4k+1) >= 6R(3, k+1) - 5, triangle-free only). I have not found theorem D in the literature
(see the end); if it is known, I would be glad to learn the reference.

| bound | DS1 rev. 18 | graph | how checked |
|---|---|---|---|
| R(7,16) >= 708 | 629 | `R7_16_707.txt`: three copies of the Paley graph P(101), M = P(101) | no K_7 by search over all roots; independent side by an exhaustive certificate check on the graph (`certifyD.py`) |
| R(8,19) >= 1429 | 1237 | `R8_19_1428.txt`: three copies of H204c, the complement of the 204-vertex (7,7)-graph of `../triple-gluing`, M = H204c | no K_8 by search over all roots; independent side by `certifyD.py` |

For most cells the theorem is weaker than known bounds (from the (4,4), (5,5), (4,6) critical graphs it gives values below
DS1); it wins where a very good (k,s)-graph is known, as P(101) and H204.

## Construction

Positions are Z_7. Three distinct positions sigma_1, sigma_2, sigma_3 (the files use 0, 1, 6) carry G_1, G_2, G_3; each of
the other four positions c carries a copy W_c of M. A vertex of M inside G_i or W_c has an index j and is written (j, c);
the other vertices of the G_i are private.
- same position: the edges of G_i, or of M;
- neighbouring positions (c' = c +- 1): only (j, c) ~ (j, c') with the same index;
- all other pairs of positions (twin rule): (j, c) ~ (l, c') iff jl is an edge of M; a private vertex y of G_c and (l, c')
  are adjacent iff y ~ x_c(l) in G_c; private vertices of different sides are not adjacent.

`heptaglue.py G1 G2 G3 maps out [s1 s2 s3]` builds the graph; the files here are rebuilt identically from `P101.txt`,
`H204c.txt` and the identity maps `maps_id101.txt`, `maps_id204.txt`.

## Proof

**No K_{k+1}.** Let K be a clique and K_j the set of positions of its vertices with index j. Inside one index only
neighbouring positions are adjacent, and C_7 has no triangle, so K_j is one position or two neighbouring positions
{d, d+1}. Two vertices with different indices lie in equal or non-neighbouring positions and have adjacent indices.
If K_j = {d, d+1}, every other indexed vertex of K lies in {d+3, d+4, d+5}; if a second index also uses two positions
({d+3, d+4} or {d+4, d+5}), no position is left for a third index, and |K| = 4 <= k (this is where k >= 4 is used).
- No private vertex in K: if all K_j are single positions, the indices form a clique of M, so |K| <= omega(M) <= k - 1
  (M is induced in G_1); with one pair, |K| <= omega(M) + 1 <= k.
- Private vertices Y in K: private vertices of different sides are not adjacent, so Y lies in one G_c. Vertices at
  positions c +- 1 are not adjacent to Y, so they are not in K. Then at most one K_j is a pair (in each of the cases
  {c+2, c+3}, {c+3, c+4}, {c+4, c+5}, removing c +- 1 from the remaining allowed positions leaves no second pair).
  Mapping each indexed vertex (l, c') to x_c(l) (twin rule, M induced) sends Y and the indices onto a clique of G_c,
  so |Y| + (number of indices) <= k - 1 and |K| <= k.

**No independent set of size s_1 + s_2 + s_3 - 2.** Let I be independent and I_j = {c : (j, c) in I}, an independent set
of C_7 (size at most 3). Colour C_7 properly with 3 colours so that sigma_1, sigma_2, sigma_3 get the colours 1, 2, 3
(possible for any three positions), and let E_i be the positions of colour i. Let F_i be the family of labels: all
labels of size 3, all pairs {e, e+3}, the singletons {e} with e in E_i, and the pairs {d-1, d+1} with d not in E_i.
A label L lies in at least |L| of the families: size 3 in all three; pairs {e, e+3} in all; {e} in one; {d-1, d+1} in the
two families other than the colour of d. Let T_i be the private vertices of G_i in I together with x_{sigma_i}(j) for
every j with I_j in F_i. Then |I| <= |T_1| + |T_2| + |T_3|, and T_i is independent in G_i:
- (a) Let j != l with I_j, I_l in F_i and jl an edge of M. Since I is independent, every position of I_j must be a
  neighbour of every position of I_l. In C_7 this happens only when one label is {e} and the other is {e-1}, {e+1} or
  {e-1, e+1}. If {e} is in F_i then e is in E_i, so e +- 1 are not in E_i and {e-1, e+1} is not in F_i, a contradiction.
  So jl is not an edge of M, and x(j), x(l) are not adjacent because M is induced.
- (b) A private y in I and I_j in F_i: no label in F_i is contained in {sigma_i - 1, sigma_i + 1} (sigma_i is in E_i, so
  the singletons {sigma_i +- 1} and the pair {sigma_i - 1, sigma_i + 1} are not in F_i). So I_j has a position c equal to
  sigma_i or not a neighbour of it, (j, c) is not adjacent to y, and therefore (directly if c = sigma_i, by the twin rule
  otherwise) y and x(j) are not adjacent.
Hence |I| <= alpha(G_1) + alpha(G_2) + alpha(G_3) <= (s_1 - 1) + (s_2 - 1) + (s_3 - 1).

## Checks (`sh check.sh`)

- `heptaglue.py` rebuilds both graphs identically from the inputs; `verify 6 6 P101.txt` and `verify 7 7 H204c.txt` check
  the inputs.
- No K_7 in `R7_16_707.txt` and no K_8 in `R8_19_1428.txt`: `vpar` over all roots (MAXN 1536 for the larger graph).
- `certifyD.py G1 G2 G3 maps F` checks on the graph file, for every pair of elements that can lie together in an
  independent set (private vertices and fibre states (j, L) with L independent in F), that the assignment in the proof
  sends them to distinct non-adjacent vertices of the same G_i: R(7,16): 2,828 elements, 2,050,300 admissible pairs;
  R(8,19): 5,712 elements, 8,368,080 pairs; 0 violations each, about 2 and 4 seconds. So the independent side does not
  rest on the written proof (the check uses the same assignment as the proof and alpha(G_i) from `verify`).
- Random exact computation (separate code, not included): about 2.29 million small instances with different G_i, arbitrary
  M and embeddings and arbitrary side positions, no counterexample; removing a matching edge between neighbouring
  positions or adding a twin edge there, allowing k = 3 or a non-induced M all give counterexamples.

`VARIANT.md` describes an earlier variant of the seven-copy graph (published in v1.1, `R7_16_707_variant.txt`, built by
`build.py`) with its own proof, kept for reference.

The construction and the proofs were found with the help of an AI coding assistant (Claude); I checked the finite facts
and reran the checks, but no expert has read the proofs yet.

Literature read in full without finding this statement: DS1 rev. 18 (sections 2.3, 6.1, 6.2); Xu, Xie, Exoo,
Radziszowski, Electron. J. Combin. 11 (2004) #R35; Xu, Xie, Radziszowski, J. Graph Theory 47 (2004); Xu, Shao,
Radziszowski, SIAM J. Discrete Math. 25 (2011); Xu and Radziszowski's survey (sur14) and slides (slides68); Rowley,
Australas. J. Combin. 68 (2017); Zhu, Xu, Radziszowski (arXiv 1507.01133); Morris (arXiv 2601.05221). Not accessible:
Chung, Cleve, Dagum, J. Combin. Theory B 57 (1993).
