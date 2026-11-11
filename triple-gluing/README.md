# Gluing three Ramsey graphs: R(7,17) >= 736, R(7,18) >= 826, R(7,19) >= 919, R(7,20) >= 933, R(8,19) >= 1267

Five more graphs from the same construction as [`../r6-16`](../r6-16) (R(6,16) >= 454). Values in the dynamic survey
*Small Ramsey Numbers* (S. P. Radziszowski, Electron. J. Combin. DS1, revision #18, 2026):

| bound | DS1 #18 | graph | parts G_1, G_2, G_3 | common part M |
|---|---|---|---|---|
| R(7,17) >= 736 | 729 | `R7_17_735.txt` | G114, G114, H204 | Paley graph P(101), m = 101 |
| R(7,18) >= 826 | 797 | `R7_18_825.txt` | G114, H204, H204 | P(101), m = 101 |
| R(7,19) >= 919 | 908 | `R7_19_918.txt` | three copies of the complement of H204 | neighbourhood of a vertex, m = 102 |
| R(7,20) >= 933 | no entry (931 follows from 919 above and R(k,s+1) >= R(k,s) + 2k - 2) | `R7_20_932.txt` | complement of H204 twice, complement of G218 (a (7,8)-graph) | neighbourhood of a vertex, m = 102 |
| R(8,19) >= 1267 | 1237 | `R8_19_1266.txt` | three copies of G218 | H204, m = 204 |

G114 = complement of the 114-vertex (6,7)-graph of Exoo and Tatarevic (a (7,6)-graph); H204 = Taylor double cover of
P(101) (a (7,7)-graph, as is its complement); G218 = Tatarevic's 218-vertex (8,7)-graph (see `../r7-12`, `../r8-19`
for sources). In each file the first n_1, next n_2, next n_3 vertices are the three parts, followed by 3m new vertices.

## Theorem (triple gluing)

Let k >= 4. For i = 1, 2, 3 let G_i be a (k, s_i)-graph on n_i vertices (no K_k, no independent set of size s_i). Let M
be a graph on m vertices with no K_{k-1}, and let x_i : V(M) -> V(G_i) be injective maps whose images induce copies of
M (jl is an edge of M iff x_i(j) x_i(l) is an edge of G_i). Then there is a (k, s_1 + s_2 + s_3 - 2)-graph on
n_1 + n_2 + n_3 + 3m vertices, so

**R(k, s_1 + s_2 + s_3 - 2) >= n_1 + n_2 + n_3 + 3m + 1.**

The two-graph construction of Xu, Xie and Radziszowski (DS1 item 2.3.h) applied twice with the same M gives n_1 + n_2 + n_3 + 2m + 1.
I have not found the three-graph statement in the literature; if it is known, I would be glad to learn the reference.

**Construction.** F has the vertices of G_1, G_2, G_3 and new vertices w_ab(j) for ab in {12, 23, 13} and j in V(M).
- (E1) the edges of each G_a;
- (E2) x_a(j) ~ x_b(j) for a != b;
- (E3) w_ab(j) ~ every neighbour of x_a(j) in G_a and every neighbour of x_b(j) in G_b;
- (E4) w_ab(j) ~ x_c(j), where c is the third index;
- (E5) w_e(j) ~ w_f(l) iff jl is an edge of M (for any types e, f; never when j = l).

**No K_k.** Let K be a clique. Its W-vertices have distinct indices, and these indices form a clique J of M (E5), so
|J| <= k - 2. The only edges between different G_a, G_b are x_a(j) x_b(j).
- K meets no G_a: |K| = |J| <= k - 2.
- K meets exactly one G_a. If K contains some w_bc(j0) (type without a), its only neighbour in G_a is x_a(j0), so
  K meets G_a in {x_a(j0)}; a second w_bc(l) would not be adjacent to x_a(j0). The other W-vertices have a type
  containing a and are adjacent to x_a(j0), so their indices are neighbours of j0 in M (M is induced); with j0 they
  form a clique of M, hence |K| <= 1 + 1 + (k - 3). If K contains no such vertex, map each w(l) in K to x_a(l): the
  images are distinct, differ from the G_a-vertices of K (w(l) is not adjacent to x_a(l)), and together with them
  form a clique of G_a of size |K|, so |K| <= k - 1.
- K meets exactly G_a and G_b: then K meets each of them in exactly one vertex, x_a(j) and x_b(j) for some j. A vertex w_ac(l) or w_bc(l) cannot be adjacent to
  both. Each w_ab(l) in K has l adjacent to j in M (and l != j, since w_ab(j) is not adjacent to x_a(j)), so J together with j
  is a clique of M: |J| <= k - 3 and |K| <= k - 1.
- K meets all three: K contains x_1(j), x_2(j), x_3(j) and no W-vertex (w_ab(l) ~ x_c(j) forces l = j, but w_ab(j)
  is not adjacent to x_a(j)). |K| = 3 <= k - 1. This is where k >= 4 is used.

**No independent set of size s_1 + s_2 + s_3 - 2.** Let I be independent. For each index j, I contains at most one
of x_1(j), x_2(j), x_3(j) (E2). Assign each w(j) in I to a side: if no x_c(j) is in I, send w_12(j) to side 1, w_23(j)
to side 2, w_13(j) to side 3; if x_c(j) is in I, then w_ab(j) is not in I (E4), and send w_ac(j) to side a, w_bc(j) to
side b. In every case the side d belongs to the type of w, x_d(j) is not in I, and no two vertices with the same index
go to the same side. Let I_d be the vertices of I in G_d together with x_d(j) for every w(j) sent to side d. This
union has as many elements as were put in. I_d is independent in G_d: a vertex y of I in G_d is not adjacent to w(j),
hence not to x_d(j) (E3); and x_d(j), x_d(l) for two W-vertices of I are non-adjacent because jl is not an edge of M
(E5) and the copy of M is induced. So |I| = |I_1| + |I_2| + |I_3| <= (s_1 - 1) + (s_2 - 1) + (s_3 - 1).

**Corollary.** With M = K_{k-2} (contained in every Ramsey-critical (k,s)-graph for s >= 2):
R(k, s_1 + s_2 + s_3 - 2) >= R(k,s_1) + R(k,s_2) + R(k,s_3) + 3k - 8, in particular R(k, s + 2) >= R(k, s) + 5k - 8 for s >= 2.
This general form is not new strength for k >= 5: Corollary 3 of Xu, Shao and Radziszowski (2011) with t = 3 gives
R(k, s + 2) >= R(k, s) + R(3, k) + k - 2, which is equal for k = 5, 6 and larger for k >= 7. The gain of the theorem is in
the structured cases above, where the three graphs share a large common part.

## Verification (2026-11-11, Apple M4 Pro)

`sh check.sh` (about 5 to 15 minutes) does, for each of the five graphs: (1) cuts the three parts out of the file and checks
with `verify` that each is a (k, s_i)-graph; (2) searches the whole graph for K_k with `vpar` over all roots (none);
(3) runs `certify.py`, which checks exhaustively, on this graph, the pair conditions behind the independent-set
argument above (every independent set maps injectively onto an independent set of the disjoint union of the parts):
0 violations in 3,641,900 / 3,857,158 / 4,193,262 / 4,236,024 / 14,001,039 admissible pairs. So the independent-set side does not
rest on the written proof. Not done: a direct branch-and-bound search for large independent sets (infeasible here).

The statement and proof were also reviewed by two independent passes (a fresh proof written without reading this one,
and a referee-style check), with 8,000 and 100,000 random small instances (different G_i, arbitrary embeddings of M,
k = 4..10) computed exactly (those scripts are not included here): no counterexample; removing E4, taking k = 3, or a non-induced M gives counterexamples.
The construction, the proof and the checks were made with the help of an AI coding assistant (Claude); a careful
reading by an expert is still welcome.

## Files

`tripleglue.py` (construction from three graphs, the maps and M), `certify.py` (certificate check), `blocks.py`,
`check.sh`, `verify.c`, `vpar.c`, the five graphs, `maps_*.txt` (the vertices x_i(j) in each part, one line per part).
