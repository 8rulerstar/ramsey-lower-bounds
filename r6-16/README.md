# A (6,16)-graph on 453 vertices: R(6,16) >= 454

`R6_16_453.txt` is a graph on 453 vertices with no K6 and no independent set of size 16, verified by computer, so

**R(6,16) >= 454.**

The dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, Electron. J. Combin. DS1, revision #18, 2026) lists
R(6,16) >= 434 in Table IIa [SLLL, 2002].

## Construction: gluing three graphs (new)

The graph comes from a construction that glues **three** graphs along a common induced subgraph. It extends the
two-graph construction of Xu, Xie and Radziszowski (DS1 item 2.3.h; a refinement is Theorem 3 of Xu, Shao and
Radziszowski, SIAM J. Discrete Math. 25 (2011)), which would give n_1 + n_2 + n_3 + 2m when applied twice:

> **Claim (triple gluing).** Let k >= 4. If (k, s_i)-graphs G_1, G_2, G_3 on n_i vertices share an induced subgraph M
> on m vertices with no K_{k-1}, then there is a (k, s_1 + s_2 + s_3 - 2)-graph on n_1 + n_2 + n_3 + 3m vertices.

Here G_1 = G_2 = G_3 = the Paley graph P(101), a (6,6)-graph, and M = the neighbourhood of vertex 0 (the 50 quadratic
residues, no K5): 3 * 101 + 3 * 50 = 453 vertices, (6, 6 + 6 + 6 - 2) = (6,16). The construction is in
`tripleglue.py` (rules E1 to E5 in its header). The proof of the general claim is in [`../triple-gluing`](../triple-gluing). This folder does not rely on it: for this graph the
argument is checked exhaustively by `certify.py` (see Verification).

## Quick start

```sh
sh reproduce.sh      # rebuilds the graph from P(101) and checks it; a few seconds
```

## Verification (2026-11-11, Apple M4 Pro)

1. Rebuild from P(101) matches the file byte for byte. `verify 6 6` on P(101): no K6 and no independent 6-set.
2. No K6 in the 453-vertex graph: `vpar` over all 453 roots (direct search).
3. No independent 16-set: `certify.py` checks, exhaustively, that every independent set of the 453-vertex graph maps
   injectively onto an independent set of the disjoint union of the three copies of P(101), so its size is at most
   5 + 5 + 5 = 15. The map sends each vertex to one copy, depending only on the independent set inside the vertex's
   "fibre" (the six vertices x_1(j), x_2(j), x_3(j), w_12(j), w_23(j), w_13(j)); injectivity and independence of the
   image are conditions on pairs, and the script checks all 1,004,703 admissible pairs (0 violations). The rule is in
   the header of `certify.py`. Controls: the script fails on the 75-vertex case with one E4 edge or one E5 edge removed.
4. Small cases of the claim checked by direct search (`verify`): three copies of P(13), P(17), P(29), P(37), P(41)
   give (4,10)-graphs on 57 and 75 vertices, (5,13)-graphs on 129 and 165 vertices and a (6,16)-graph on 183 vertices.
5. Not done: a direct branch-and-bound search for an independent 16-set in the 453-vertex graph (started, too slow).
6. The checkers and scripts were written by me with the help of an AI coding assistant (Claude).
