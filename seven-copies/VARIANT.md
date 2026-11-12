# Seven copies: R(k+1, 3s-2) >= 7R(k,s) - 6, and R(7,16) >= 708

**Theorem.** Let G be a graph with clique number w and independence number a. The graph F below has 7|V(G)| vertices,
omega(F) = max(w+1, 4) for w >= 2, and alpha(F) = 3a. Hence for k >= 4 and s >= 2

**R(k+1, 3s-2) >= 7R(k,s) - 6**

(take G a (k,s)-graph on R(k,s)-1 vertices: omega(F) <= max(k, 4) = k, alpha(F) <= 3(s-1)).

The closest results I know are DS1 2.3.i (Xu, Xie, Exoo, Radziszowski: R(2k-1, l) >= 4R(k, l-1) - 3, Electron. J. Combin. 11
(2004) #R35; in complement form four copies with the independence number doubled) and DS1 2.3.c (Chung, Cleve, Dagum: R(3, 4k+1) >= 6R(3, k+1) - 5, triangle-free only).
I have not found this statement in the literature (DS1 rev. 18 sections 2.3 and 6.2, and the papers listed at the end);
if it is known, I would be glad to learn the reference.

| bound | DS1 rev. 18 | input G | how checked |
|---|---|---|---|
| R(7,16) >= 708 | 629 (our 649 in `../r7-16`) | Paley graph P(101), w = a = 5 | graph `R7_16_707_variant.txt`: no K_7 by search over all roots; independent side by the theorem (direct search for independent 16-sets running, see Checks) |
| R(8,19) >= 1429 | 1237 (our 1267 in `../triple-gluing`) | the 204-vertex (7,7)-graph H204 of `../triple-gluing`, w = a = 6 | no K_8 by search over all 1428 roots (graph built from `../triple-gluing/H204.txt`, not included); independent side by the theorem |

For most cells the theorem is weaker than known bounds (from (4,4), (5,5), (4,6) graphs it gives values below DS1);
it wins only where a very good (k,s)-graph is known, as for P(101) and H204.

## Construction

Copies are numbered 0..6. Let C be the 7-cycle 0-5-2-3-4-1-6-0 and R the graph C plus the two chords {0,1}, {0,2}.
F has the vertices (j, c), j in V(G), c in 0..6 (vertex number 7j + c in the files), and the edges
- (j, c) ~ (j, d) iff cd is an edge of C (inside a fibre);
- for every edge jl of G: (j, c) ~ (l, d) iff cd is not an edge of R (this includes c = d);
- no edges between fibres j, l with jl not an edge of G.

`build.py` encodes the same graph by a 21-character pattern over pairs of copies ('2' = edge of C, '0' = chord of R,
'1' = all other pairs).

## Proof

Finite facts about C and R (all checked by `tables.py`):
- (T1) phi(0) = phi(4) = 1, phi(1) = phi(2) = 2, phi(3) = phi(5) = phi(6) = 3 is a proper 3-colouring of R.
- (T2) each of the 14 pairs of copies non-adjacent in C has at most one common R-neighbour.
- (T3) each of the 7 triples independent in C has no common R-neighbour, and C has no independent 4-set.

**alpha(F) <= 3a.** Let I be independent and S_j = {c : (j,c) in I}. Each S_j is independent in C, and if jl is an
edge of G then every c in S_j and d in S_l satisfy cd in R (in particular c != d); call S_j, S_l compatible.
For i = 1, 2, 3 let A_i be the family of nonempty C-independent sets S with: |S| = 1 and phi(S) = i; or |S| = 2 and no
common R-neighbour of S has colour i; or |S| = 3. Two sets in the same A_i are never compatible: two singletons have
the same colour, so they are not R-adjacent (T1); a singleton {e} and a pair U would need e to be a common neighbour of U
of colour i; a triple has no common neighbour (T3); two sets of size >= 2 would need two common neighbours of a pair (T2).
So J_i = {j : S_j in A_i} is independent in G and |J_i| <= a. A singleton lies in exactly one A_i, a pair in at least
two (its common neighbours, at most one by (T2), have at most one colour), a triple in all three. Hence
|I| = sum |S_j| <= |J_1| + |J_2| + |J_3| <= 3a. Equality: put a C-independent triple, e.g. {0,3,1}, in each fibre of a
maximum independent set of G.

**omega(F) <= max(w+1, 4).** Let K be a clique, S_j its part in fibre j, Q = {j : S_j nonempty}. Fibres are joined only
along edges of G, so Q is a clique of G and |Q| <= w. C has no triangle, so |S_j| <= 2, and between S_j and S_l (j != l)
there is no R-edge. (a) If S_j = {c, c'} (an edge of C) and d in S_l, then d is not c or c' and not C-adjacent to them (d must be
adjacent to both c and c' across fibres, i.e. cd and c'd are not in R; d = c fails because cc' is in C, a subset of R).
(b) If two fibres carry 2 copies, their C-edges e, f are disjoint with no C-edge between them; the remaining 3 vertices of
the 7-cycle are each C-adjacent to an end of e or f, so by (a) no third fibre can join: |K| = 4. (c) Otherwise
|K| <= |Q| + 1 <= w + 1. Lower bound: on a w-clique of G put {0,5} in one fibre and copy 3 in the others.
The bound 4 in (b) is where w >= 3 matters: for w = 2, {0,5} and {3,4} on the two ends of an edge of G give a
4-clique (03, 04, 53, 54 are not in R), so omega(F) = 4 = w + 2. For w = 1, omega(F) = 2.

## Checks

- `tables.py`: the finite facts (T1) to (T3) and the clique-side case (b).
- Exhaustive check (separate C code): all labelled graphs on 2 to 7 vertices (2,097,152 on 7) and 20,000 random graphs on
  8 vertices give omega(F) = max(w+1, 4) and alpha(F) = 3a exactly.
- Exact computation (separate code): F from Paley graphs P(13), P(17) (119 vertices) and P(29) (203 vertices, checked
  with `verify`) has exactly omega = w + 1 and alpha = 3a.
- `sh check_variant.sh` rebuilds `R7_16_707_variant.txt` from P(101), checks the facts, searches for K_7 over all 707 roots (none) and for
  independent 16-sets. Symmetry used in the last step: (j, c) -> (j+1 mod 101, c) is an automorphism of F (checked
  directly on the file), so every independent set has a translate whose smallest vertex lies in fibre 0, and roots 0..6
  cover all cases. Status of this search: see the commit history; a full search over all roots without the symmetry is
  also being run.

The construction was found, and the proof written, with the help of an AI coding assistant (Claude); I checked the
finite facts and the argument, but no expert has read the proof yet.

Literature read in full without finding this statement: DS1 rev. 18 (sections 2.3, 6.1, 6.2); Xu, Xie, Exoo,
Radziszowski, Electron. J. Combin. 11 (2004) #R35; Xu, Xie, Radziszowski,
J. Graph Theory 47 (2004); Xu, Shao, Radziszowski, SIAM J. Discrete Math. 25 (2011); Xu and Radziszowski's survey
(sur14) and slides (slides68); Rowley, Australas. J. Combin. 68 (2017); Zhu, Xu, Radziszowski (arXiv 1507.01133);
Morris (arXiv 2601.05221). Not read in full: Chung, Cleve, Dagum, J. Combin. Theory B 57 (1993).
