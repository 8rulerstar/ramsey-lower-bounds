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

## Generalization to r graphs (theorem B)

This section does not raise any entry of the survey tables; it records how far the idea goes. With r graphs the
second parameter grows to s_1 + ... + s_r - (r - 1), so for r >= 4 it is large and other known bounds for those entries
are much higher. Example: R(7,23) >= 1253 follows from DS1 rev. 18 item 2.3.i with R(4,22) >= 314, far above what
theorem B gives from the available (7,s)-graphs.

**Gadget.** T is a simple graph on {1..r} (its edges are the "types"), and Q is a set of pairs {e, f} of disjoint edges of T.
- (Q2) every Q-independent set of edges (no pair of Q inside it) is a pseudoforest: in each component, edges <= vertices.
- d = the largest number of Q-pairs lying on one 4-set (0..3).
- A Q-clique is a set of types that are pairwise in Q. kappa = the maximum, over cliques P of T (including the empty set), of |P| + the largest Q-clique among types disjoint from P.

**Theorem B.** Let (T, Q) satisfy (Q2). For a = 1..r let G_a be a (k, s_a)-graph on n_a vertices, and let x_a : V(M) -> V(G_a)
be injective maps whose images induce copies of a graph M on m vertices. If
- (H1) kappa <= k - 1,
- (H2) omega(M) <= k - 2,
- (H3) omega(M) + min(omega(M), d) <= k - 1,

then there is a (k, s_1 + ... + s_r - (r - 1))-graph on n_1 + ... + n_r + |E(T)| m vertices.

**Construction.** New vertices w_e(j) for e in E(T), j in V(M); the fibre of j is {x_a(j)} together with {w_e(j)}, and w(j) means some w_e(j).
- (E1) the edges of each G_a;
- (E2) x_a(j) ~ x_b(j) iff ab is in E(T) (joining all pairs a, b also works, then kappa is taken over all subsets P of {1..r});
- (E3) w_e(j) ~ every neighbour of x_a(j) in G_a, for each a in e (not x_a(j) itself);
- (E4) w_e(j) ~ x_c(j) for c not in e;
- (E5) for j != l: w_e(j) ~ w_f(l) iff jl is in E(M) and e, f share an end;
- (E6) w_e(j) ~ w_f(j) iff {e, f} is in Q.

The triple gluing above is r = 3, T = triangle, Q empty (kappa = 3). Gadgets found:

| r | T | Q | d | kappa | added vertices | earlier methods iterated |
|---|---|---|---|---|---|---|
| 2 | one edge | none | 0 | 2 | m | m (2.3.h) |
| 3 | triangle | none | 0 | 3 | 3m | 3m (triple gluing; 2m with 2.3.h alone) |
| 4 | K_4 minus one edge | one pair {12, 34} (vertices 1..4, 23 removed) | 1 | 3 | 5m | 4m |
| 5 | K_{2,2,1} | 5 pairs (`Q5_mine.txt`) | 1 | 4 | 8m | 6m |
| 6 | K_{2,2,2} | 14 pairs (`Q6_mine.txt`) | 1 | 4 | 12m | 9m |
| 7 | K_{3,2,2} | 30 pairs (`Q7_mine.txt`) | 1 | 5 | 16m | not computed |
| 8 | K_{3,3,2} | 58 pairs (`Q8_mine.txt`) | 1 | 5 | 21m | not computed |

The Q files are in `theorem-b/` and number the vertices of T from 0; the parts of T are {0,3},{1,4},{2} (r = 5),
{0,3},{1,4},{2,5} (r = 6), {0,3,6},{1,4},{2,5} (r = 7), {0,3,6},{1,4,7},{2,5} (r = 8). The last column is the best
coefficient found by iterating 2.3.h and the triple gluing with unions of copies of M as common parts (`baseline.py`,
searched with omega(M) = 2 and at most 6 graphs; not a proof that nothing better exists). Two caveats:
- For a specific M the earlier methods can do a little better. With M = K_{k-2}, three uses of 2.3.h on r = 4 reach
  5m - 2 (`caveat.py`), so theorem B gains only 2 vertices there.
- With d = 1, T contains no K_4 (on a K_4 there is only one Q-pair, and removing one of its edges leaves 5 Q-independent
  edges on 4 vertices). So |E(T)| <= floor(r^2/3) by Turan's theorem; r = 4..8 attain it.

**Proof, independent sets.** Let I be independent. For each j let A_j = {a : x_a(j) in I}, B_j = {e : w_e(j) in I}.
B_j is Q-independent (E6), A_j is T-independent (E2), and every type in B_j contains all of A_j (E4); so if |A_j| >= 2
then B_j is empty. If A_j is empty, B_j is a pseudoforest, and so is each subset of it; so every set S of its edges has
at least |S| ends, and by Hall's theorem each edge gets one of its ends, all different. If A_j = {c}, the types in B_j
pass through c; send each to its other end (distinct, as T is simple). So each w_e(j) in I goes to a side
sigma in e with x_sigma(j) not in I, and no two vertices of one fibre go to the same side. Let I_d be I restricted to G_d
together with x_d(j) for every w(j) sent to side d; sizes add up. I_d is independent in G_d: for y in I in G_d, w_e(j)
is a twin of x_d(j) inside G_d (E3) and y is not adjacent to w, so not to x_d(j); two added x_d(j), x_d(l) come from
types both containing d, which share an end, so jl is not in E(M) (E5) and, M being induced, x_d(j), x_d(l) are
non-adjacent. Hence |I| <= sum (s_d - 1).

**Proof, cliques.** Let K be a clique and P = {a : K meets G_a}. Between different G_a, G_b the only edges are
x_a(j) x_b(j) with ab in E(T). Note: w_e(l) ~ y in G_a means (a in e and y ~ x_a(l)) or (a not in e and y = x_a(l)).
- P empty: the fibres used by K form a clique J of M; inside a fibre the types form a Q-clique C_j, and types in
  different fibres share an end. If some |C_j| >= 3, a type from another fibre cannot meet three disjoint edges, so K
  lies in one fibre and |K| <= kappa. If |C_j| = |C_l| = 2 with j != l, the four types are the perfect matchings of one 4-set;
  at most d fibres have two. So |K| <= |J| + min(|J|, d) <= k - 1 (H3).
- |P| >= 2: K meets the union of the G_a in {x_a(j0) : a in P} and P is a clique of T. A vertex w_e(l) of K has either l = j0 and e disjoint
  from P, or l != j0, e = P and l adjacent to j0 in M. The two kinds are non-adjacent (disjoint types, E5). So
  |K| <= kappa, or |K| <= 2 + (omega(M) - 1) <= k - 1 (H2).
- P = {a} and K has some w_e(j0) with a not in e: then K meets G_a only in x_a(j0); other fibres give at most one vertex
  each, of types containing a, indexed by a clique in the neighbourhood of j0 in M. If fibre j0 has |C| >= 2 types, a type
  containing a cannot meet two disjoint ones, so |K| = 1 + |C| <= kappa; if |C| = 1, |K| <= 2 + omega(M) - 1 <= k - 1.
- P = {a} and every w in K has a type containing a: one per fibre; w(l) -> x_a(l) is injective, misses K inside G_a
  (w(l) is not adjacent to x_a(l)) and keeps adjacency (E3, E5, M induced), so K becomes a clique of G_a: |K| <= k - 1.

**Checks** (run inside `theorem-b/`, plain Python 3 with networkx; not a substitute for a careful reading of the proof).
- `python3 testB.py B4 SECONDS SEED` and `python3 testB.py B7 SECONDS SEED Q7_mine.txt` (B5..B8 likewise) build F from
  random G_a, M and embeddings, set k - 1 to the largest of omega(G_a), kappa and the bounds in (H2), (H3), and compute
  omega(F), alpha(F) exactly. Runs stop after SECONDS, so counts vary by machine. Our runs
  (about 1.2 million instances for B4, 0.5 million B5, 0.35 million B6, 0.27 million B7, 0.08 million B8, with the
  argument `big` forcing omega(M) = k - 2): no violation, and omega(F) was always equal to k - 1. With `noQ` (dropping E6) the independence bound fails at once, so the checker detects errors.
- `python3 findQ.py r SEED` finds Q for r = 4..8 with (Q2) and d = 1.
- `python3 baseline.py 2 6 6` prints 4m, 6m, 9m for r = 4, 5, 6; `python3 caveat.py 60` checks the 5m - 2 case.

These scripts were written without reusing the code of an earlier referee-style check, which found the same values.
I have not found theorem B in the literature (DS1 rev. 18 and a short web search); an expert reading is welcome.

## Verification (2026-11-11, Apple M4 Pro)

`sh check.sh` (about 5 to 15 minutes) does, for each of the five graphs: (1) cuts the three parts out of the file and checks
with `verify` that each is a (k, s_i)-graph; (2) searches the whole graph for K_k with `vpar` over all roots (none);
(3) runs `certify.py`, which checks exhaustively, on this graph, the pair conditions behind the independent-set
argument above (every independent set maps injectively onto an independent set of the disjoint union of the parts):
0 violations in 3,641,900 / 3,857,158 / 4,193,262 / 4,236,024 / 14,001,039 admissible pairs. So the independent-set side does not
rest on the written proof. Not done: a direct branch-and-bound search for large independent sets (infeasible here).

The triple-gluing statement and proof were also reviewed by two independent passes (a fresh proof written without reading this one,
and a referee-style check), with 8,000 and 100,000 random small instances (different G_i, arbitrary embeddings of M,
k = 4..10) computed exactly (those scripts are not included here): no counterexample; removing E4, taking k = 3, or a non-induced M gives counterexamples.
The construction, the proof and the checks were made with the help of an AI coding assistant (Claude); a careful
reading by an expert is still welcome.

## Files

`tripleglue.py` (construction from three graphs, the maps and M), `certify.py` (certificate check), `blocks.py`,
`check.sh`, `verify.c`, `vpar.c`, the five graphs, `maps_*.txt` (the vertices x_i(j) in each part, one line per part). `theorem-b/`: scripts for the section on theorem B.
