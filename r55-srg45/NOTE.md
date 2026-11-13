# No strongly regular graph SRG(45,22,10,11) is a (5,5)-Ramsey graph

Byungkun Jang, November 2026. Computer-assisted; all code and data are in this repository.

## Abstract

We show that every strongly regular graph with parameters (45,22,10,11) contains a clique of size 5 or an independent
set of size 5. No classification of these graphs is used. More generally, no (5,5)-graph on 45 vertices has a vertex v
of degree 22 whose neighbours all have degree 22, share 10 common neighbours with v, and pairwise share 10 (adjacent)
or 11 (non-adjacent) common neighbours. The proof combines a local Gram identity, which forces an eigenvalue window and
a perfect-square determinant on the neighbourhood graph, with an exhaustive gluing computation over McKay's lists of
(3,5,10)- and (4,4,11)-graphs.

## 1. Context

43 <= R(5,5) <= 46 (lower bound Exoo 1989, upper bound Angeltveit and McKay, arXiv:2409.15709). A (5,5)-graph on 45 vertices would give R(5,5) = 46.
The graphs SRG(45,22,10,11) (conference graphs on 45 vertices) are a natural highly regular candidate for such a graph; their
classification is open (many are known). A SAT-based attack on the same question was reported by Braginsky,
Yellenki and Zhu (with J. Mackey) at the 57th Southeastern Conference, March 2026, settling 141 of 313 cases
(https://www.cs.rit.edu/~spr/COURSES/CCOMP/srg_r55.pdf). We found no published complete answer.

## 2. Results

**Theorem 1.** Every SRG(45,22,10,11) contains K5 or an independent 5-set.

**Theorem 2 (local version).** Let G be a graph on 45 vertices without K5 and without independent 5-sets. Then G has no
vertex v such that: deg v = 22; every neighbour x of v has deg x = 22 and exactly 10 common neighbours with v; any two
neighbours x, y of v have exactly 10 common neighbours if adjacent and 11 if not.

Theorem 1 follows from Theorem 2, since every vertex of an SRG(45,22,10,11) satisfies the hypotheses.

## 3. Local identity

Let v be a vertex of degree 22 in a graph G on 45 vertices, A the graph induced on N(v), and N the 22 x 22 0/1 matrix
of adjacencies between N(v) and the 22 non-neighbours of v. Counting walks of length 2,

    (N N^T)_xx = deg x - 1 - deg_A x,    (N N^T)_xy = codeg(x,y) - 1 - (A^2)_xy   (x != y).

Hence, under the hypotheses of Theorem 2,

    N N^T = M(A) := 11 I + 10 J - A - A^2,   and A is 10-regular.

**Lemma 1 (window).** M(A) is positive semidefinite. Since A is 10-regular, M(A) 1 = 121 1, and every eigenvalue
theta of A on the orthogonal complement of 1 satisfies 11 - theta - theta^2 >= 0, that is s <= theta <= r with
s, r = (-1 -+ sqrt 45)/2.

**Lemma 2 (determinant).** N is square with integer entries, so det M(A) = (det N)^2 is a perfect square.

**Lemma 3 (Ramsey).** A has no K4 (with v it would give K5) and no independent 5-set.

For strongly regular graphs the identity and Lemma 1 are standard facts about subconstituents (cf. Koolen, Lee and
Tan, arXiv:2102.00105, Lemma 5.2); here they are obtained by direct counting at a single vertex. A 22-vertex 10-regular graph satisfying Lemmas 1 and 3 is called a *window graph*.

## 4. Reduction to a finite search

Fix a window graph A and a vertex w of A. Let K = N_A(w) (10 vertices) and B = A - N[w] (11 vertices).

**Lemma 4.** K is a (3,5)-graph (triangle-free since A has no K4; independence number at most 4), B is a (4,4)-graph
(an independent 4-set of B together with w is independent), and e(B) = 10 + e(K): the 110 edges of A are the 10 edges
at w, the e(K) edges inside K, the 90 - 2e(K) edges between K and B, and the edges of B.

**Lemma 5 (quotient filter).** The quotient matrix of the partition {w}, the 10 vertices of K separately, and B is
determined by K because A is 10-regular; by Haemers interlacing its eigenvalues satisfy lambda_min >= s and
lambda_2 <= r (lambda_2 denotes the second largest eigenvalue). Of the 313 (3,5,10)-graphs, 147 pass (pipeline/01_filter_K.py).

**Lemma 6.** For every vertex w of a window graph, 15 <= e(N_A(w)) <= 20. Lower bound: for e <= 14 the 3 x 3 quotient
matrix of {w}, N(w), rest has an eigenvalue below s = -3.854... (for e = 14 it is -3.943, for e = 15 it is -3.687). Upper bound: N(w) is triangle-free with independence number at
most 4, so every degree inside N(w) is at most 4 and e <= 20.

**Lemma 7 (mod 3).** Every window graph has a vertex w with e(N_A(w)) in {15, 16, 18, 19}.
Proof: the sum over w of e(N_A(w)) is 3 t(A), where t(A) is the number of triangles of A, so it is divisible by 3. If every term were 17 or 20 (both 2 mod 3), the sum
would be 22 * 2 = 2 (mod 3).

The search below finds every window graph A from each vertex w whose K is in the list searched (it puts no further
condition on the root), so by Lemma 7 it suffices to take K with e(K) in {15, 16, 18, 19}. For B we use
the (4,4,11)-graphs with e(B) = 10 + e(K) that satisfy, for S = B and for S = {w} u B (both induced subgraphs of A), the three conditions
lambda_min(A_S) >= s, lambda_2(A_S) <= r and 11I + 10J - A_S - A_S^2 >= 0, and a second quotient filter on the partition {w}, K, and the 11 vertices of B separately
(pipeline/02_build_B.py). For an induced subgraph S of A the condition 11I + 10J - A_S - A_S^2 >= 0 holds because this
matrix equals the principal submatrix of N N^T on S plus C C^T, where C records the edges from S to A - S.

## 5. Gluing computation

For every pair (K, B) the engine src/glue_srg.c enumerates all ways to choose, for each vertex h of B, its
neighbourhood in K (its *cone*) such that the result is a 10-regular graph on 22 vertices with no K4 and no independent
5-set. The conditions on single cones, pairs of cones and triples of cones are those of the gluing method of McKay
and Radziszowski (1995). Every complete solution is tested for the window by Cholesky factorisation; the tolerance
1e-9 is applied so that borderline cases are accepted as window solutions. Window solutions are printed. Orbit
representatives under Aut(K) are used for the first cone.

Jobs: data/jobs.txt (e(K) = 16, 18, 19; 1,555 jobs) and data/jobs_e15.txt (e(K) = 15; 68 jobs). In total 6,313,538
pairs (K, B) were processed in 912 CPU hours, giving 1,030,818 gluings (counted with the first cone restricted to
orbit representatives), of which 799 are window solutions. Per-job counts
and checksums are in results/ledger.txt and results/jobs_summary.tsv.

## 6. Determinant test

Every window solution is rebuilt and checked with exact integer arithmetic (pipeline/05_check_windows.py, output
results/window_solutions.tsv). The script also checks, job by job, that the number of printed window solutions equals
the number counted in the ledger. None of the 799 window solutions has a perfect-square det M(A) (a zero determinant would count as a square;
none occurs). By Lemma 2 none is the neighbourhood of a vertex as
in Theorem 2, which proves Theorems 2 and 1.

## 7. Verification and limitations

- The filters were rebuilt from McKay's lists of (3,5,10)- and (4,4,11)-graphs and agree with the lists used
  (pipeline/01, 02); the job list is rebuilt by pipeline/03. The proof relies on the completeness of those lists.
- Every worker ran a control instance (K = data/K/K_2.g6 against the 30 graphs of data/ctrl_B.g6) and compared
  solution counts and node counts with data/ctrl_expected.txt before starting. All 30 control pairs have no solution,
  so the control tests the search but not the output of solutions. A variant engine (src/glue_srg_inc.c, interlacing pruning
  by incremental Cholesky) was run on the first 400 pairs of 124 distinct jobs (126 runs, two jobs appear twice). For each run the list of
  per-pair window counts was compared with the original and agreed; the logs in results/crosscheck/ record the
  per-job totals and the outcome. Only 4 of these jobs contain window solutions, so this cross-check mainly tests the
  search, not the window test. It shares the input lists
  and most of the code, so it is a cross-check, not an independent implementation.
- During the distributed run, 60 result files were overwritten by partial copies of themselves (a second worker
  restarted those jobs). Each was resumed after its last complete line with the same engine and build. The ledger
  check (pipeline/06_completeness.py) requires every pair index of every job to be present, and repeated lines (from resumed runs) to agree in their counts. The lines written before the resumption were not recomputed.
- Closure check (pipeline/07_reroot_check.py, results/reroot_check.txt): the 799 window solutions are 52 graphs up
  to a graph invariant. Each of them must reappear from every vertex whose neighbourhood has 15, 16, 18 or 19 edges;
  all 318 expected (graph, root class) pairs are present in the results and no unexpected one occurs. This tests the
  search on instances that do have solutions.
- Floating point is used only in the window test of complete solutions, with tolerance on the accepting side; the
  final decision on every window solution is the exact determinant.

## 8. Remarks

- The proof has not yet been read by an expert.

- For the adjacency matrix F of any SRG(45,22,10,11), rk_5(F - 2I) = 23; this is a special case of Peeters (1995); see Brouwer and Van Maldeghem,
  *Strongly Regular Graphs*, Proposition 9.3.5. It is not used here.
- Theorem 1 does not change the bounds on R(5,5). It rules out a natural family of highly regular candidates for a (5,5)-graph
  on 45 vertices and agrees with
  the conjecture of McKay and Radziszowski that R(5,5) = 43.

## References

- V. Angeltveit, B. D. McKay, R(5,5) <= 46, arXiv:2409.15709.
- G. Exoo, A lower bound for R(5,5), J. Graph Theory 13 (1989).
- B. D. McKay, S. P. Radziszowski, R(4,5) = 25, J. Graph Theory 19 (1995).
- B. D. McKay, S. P. Radziszowski, Subgraph counting identities and Ramsey numbers, J. Combin. Theory Ser. B 69 (1997).
- B. D. McKay, Ramsey graphs (data), https://users.cecs.anu.edu.au/~bdm/data/ramsey.html.
- S. P. Radziszowski, Small Ramsey Numbers, Electron. J. Combin. Dynamic Survey DS1, rev. 18 (2026).
- A. E. Brouwer, H. Van Maldeghem, Strongly Regular Graphs, Cambridge University Press 2022.
- J. H. Koolen, J.-H. Lee, Y.-Y. Tan, Remarks on pseudo-vertex-transitive graphs with small diameter, arXiv:2102.00105.
- W. H. Haemers, Interlacing eigenvalues and graphs, Linear Algebra Appl. 226-228 (1995).
- R. Peeters, Uniqueness of strongly regular graphs having minimal p-rank, Linear Algebra Appl. 226-228 (1995).
- Braginsky, Yellenki, Zhu (with J. Mackey), Exploring srg(45,22,10,11) and implications for R(5,5), slides, 2026.
