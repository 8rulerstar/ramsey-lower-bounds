# No (5,5,45)-colouring has an automorphism of order 11 with one fixed point

**This is not a bound.** 43 <= R(5,5) <= 46 is unchanged. The result excludes one symmetry type for a hypothetical
2-colouring of K45 with no monochromatic K5. It is computer-assisted: 630 SAT cases, each UNSAT with a DRAT proof checked
by drat-trim (630/630 VERIFIED, run twice). The reduction to the 630 cases is a short hand argument (section "Coverage")
plus computed lists: the list L of 1,430 two-orbit graphs is computed twice by different methods; the representative lists R1 and R2 are computed by one routine (copied into three scripts) and checked by the sum of their orbit sizes. It has not been read by an expert.

## Statement

A (5,5,n)-colouring is a red/blue colouring of the edges of K_n with no monochromatic K5. An automorphism of a colouring
is a permutation of the vertices that maps every red edge to a red edge and every blue edge to a blue edge.

**Proposition.** No (5,5,45)-colouring has an automorphism sigma of order 11 whose cycle type is four 11-cycles and one fixed point.

Equivalently: no graph on 45 vertices with no K5 and no independent 5-set has such an automorphism. Colour-swapping
symmetries are not considered. Other cycle types of order 11 on 45 points (12, 23 or 34 fixed points) are not covered here
(see "Limitations").

## Method

**Coordinates.** Choose a point in each 11-cycle of sigma and number vertices so that vertex 11i + a (i = 0..3, a in Z11) is
element a of orbit i, vertex 44 is the fixed point and sigma(11i + a) = 11i + (a+1). A sigma-invariant colouring is then
given by 90 Boolean variables (true = red), numbered as in `stage2.py setup()`:

| variables | meaning | DIMACS numbers |
|---|---|---|
| d(i,d), i = 0..3, d = 1..5 | colour of {11i+a, 11i+b} with b - a = +-d | 1..20 (i-major) |
| o(i,j,s), i < j, s in Z11 | colour of {11i+a, 11j+b} with b - a = s; pairs (0,1),(0,2),(0,3),(1,2),(1,3),(2,3) | 21..86 |
| f(i), i = 0..3 | colour of {44, 11i+a} (constant in a) | 87..90 |

**Base CNF.** `full_p11.cnf` has, for every 5-set of the 45 vertices, the clause "not all 10 edges red" and the clause
"not all 10 edges blue" over the corresponding variables; 5-sets with the same sorted variable row are written once.
90 variables, 221,930 clauses (110,965 rows x 2), no symmetry breaking, SHA-256
`eceb0c8e5e56522e1f93c4a4ddde31d95b39342a0ffc5423ff0d6ca94045e8d9`. It is written by `recheck.py`.

**Step 1: the fixed point (hand argument).** The red neighbourhood of vertex 44 is a union of k orbits, so it has 11k
vertices and the blue neighbourhood 11(4-k). The red neighbourhood has no red K4 (with 44 it would be a red K5) and no blue
K5, so 11k <= R(4,5) - 1; likewise 11(4-k) <= R(4,5) - 1. With R(4,5) <= R(3,5) + R(4,4) = 14 + 18 = 32 (or R(4,5) = 25,
McKay and Radziszowski 1995) this forces k = 2. Renumbering orbits, f(0) = f(1) = red and f(2) = f(3) = blue.

**Step 2: the two links (`stage1.c`).** The red graph G1 on orbits 0, 1 (22 vertices) is Z11-invariant, has no K4 and no
independent 5-set. It is given by a triple (S1, S2, T): S1, S2 subsets of {1..5} (red differences inside orbits 0 and 1),
T subset of Z11 (red differences b - a between 11*0+a and 11*1+b). `stage1.c` tests all 2^21 triples and lists the 1,430
that pass in `L.txt` (one line "S1mask S2mask Tmask edges"). The blue graph G2 on orbits 2, 3 satisfies the same
conditions, so it is also a triple (B1, B2, BT) in L, with the same conventions for orbits 2, 3.

**Step 3: cases.** A case is a pair (r1, r2) of representatives (next section) with 46 unit literals (`assum()` in
`recheck.py`, copied in `drat11.py`): f(0), f(1) true, f(2), f(3) false (4); d(0,d) = [d in S1], d(1,d) = [d in S2] (10);
o(0,1,x) = [x in T] (11); d(2,d) = [d not in B1], d(3,d) = [d not in B2] (10); o(2,3,x) = [x not in BT] (11). The 44
variables o(i,j,s) with i in {0,1}, j in {2,3} stay free. The case CNF is `full_p11.cnf` with these 46 unit clauses appended.
There are 9 x 70 = 630 cases; all 630 are UNSAT with a drat-trim VERIFIED DRAT proof.

## Coverage (why 630 cases suffice)

Each map below is a permutation pi of the 45 vertices that fixes vertex 44 and satisfies pi sigma pi^-1 = sigma^m for
some m, so it maps sigma-invariant (5,5,45)-colourings to sigma^m-invariant ones, that is, again sigma-invariant ones.
None of them moves orbits 0, 1 to orbits 2, 3, so f(0) = f(1) = red, f(2) = f(3) = blue is kept.

- Translation of orbit 1 by u (11+b -> 11+b+u): T -> T + u. G2 unchanged.
- Multiplication by m in Z11* on all orbits (11i+a -> 11i+ma, pi sigma pi^-1 = sigma^m): (S1, S2, T) -> (mS1, mS2, mT)
  and also (B1, B2, BT) -> (mB1, mB2, mBT). Here mS = {min(md mod 11, 11 - md mod 11) : d in S}.
- Swap of orbits 0 and 1 (a <-> 11+a): (S1, S2, T) -> (S2, S1, -T). G2 unchanged.
- Translation of orbit 3 by u: BT -> BT + u. Swap of orbits 2 and 3: (B1, B2, BT) -> (B2, B1, -BT). G1 unchanged.

The first three, together called H1, act on triples through 220 maps (as vertex permutations they generate a larger group, 2,420 elements, because the swap conjugates translation of orbit 1 into translation of orbit 0; this does not change the orbits on triples) by T -> mT + u (with or without the swap); the maps
x -> mx + u and x -> -(mx + u) are closed under composition, so `images(g, range(1, 11), True)` lists exactly the
H1-orbit of g. The last two, together called H2, act on the blue triples through 22 maps (`images(g, [1], True)`), which fixes orbits 0 and 1 pointwise.

`reps()` walks L in sorted order and takes every triple not yet in the orbit of an earlier representative, so every
element of L is in the orbit of exactly one representative: R1 = 9 representatives under H1, R2 = 70 under H2.
`stage2.py glue` asserts that every image lies in L (L is closed under both groups, as it must be, since these are graph
isomorphisms), and `recheck.py` checks that the orbit sizes sum to 1,430 for both groups.

Now let chi be a colouring as in the proposition, in the coordinates above with f(0) = f(1) = red. Its links G1, G2 are in L.
Apply the element of H1 that takes G1 to its representative r1; G2 becomes some element of L (multiplication may change
it). Then apply the element of H2 that takes this G2 to its representative r2; G1 = r1 is not changed. The result is a
sigma-invariant (5,5,45)-colouring that satisfies the 46 units of case (r1, r2) and all clauses of `full_p11.cnf`, so that case
would be SAT. All 630 cases are UNSAT, so chi does not exist.

What the argument uses from computation: L is exactly the set of Z11-invariant triples with no K4 and no independent 5-set
(`stage1.c`, rechecked by `recount_L.py`, which enumerates all models of the CNF's own one-side clauses and gets the same
1,430 triples), the representative lists R1, R2 (code in `recheck.py`/`drat11.py`, a few lines), and the 630 UNSAT results.

## Results

| item | value | where |
|---|---|---|
| Z11-invariant (4,5,22)-graphs on two orbits | 1,430 of 2,097,152 (by sizes of S1, S2: 2 and 2: 605; 2 and 3: 275; 3 and 2: 275; 3 and 3: 275) | `L.txt`, `rerun_2026-11-24.log` |
| same list by SAT model enumeration | 1,430, same set | `recount_L.py` |
| representatives | R1 = 9, R2 = 70, orbit sizes sum to 1,430 and 1,430 | `recheck.py` |
| base CNF | 90 variables, 221,930 clauses, SHA-256 eceb0c8e...4045e8d9 (regenerated, matches) | `recheck.py` |
| 630 cases, pysat solvers | CaDiCaL 1.9.5 630/630 UNSAT; Glucose4 630/630; MiniSat22 630/630 | `stage2.py glue`, `recheck.py` |
| 630 cases, DRAT, original run (2026-11-24) | 630/630 UNSAT and VERIFIED; max 2.05 s per case, 702 s in total | `results_2026-11-24.tsv` |
| 630 cases, DRAT, rerun from this folder (2026-11-24) | 630/630 UNSAT and VERIFIED; max 1.86 s, 577 s in total, 112 s wall with 6 workers | `results_rerun_2026-11-24.tsv`, `rerun_2026-11-24.log` |
| DRAT proofs | text DRAT, 5,090,332 to 13,576,132 bytes per case, 4,781,233,777 bytes in total; per-case sizes identical in both runs | same |

Columns of the results tables: g1 = index in R1, g2 = index in R2 (both from 0), cadical result, drat-trim result, proof
size in bytes, seconds (CaDiCaL plus drat-trim, wall clock of one worker).

The original run was interrupted and resumed; two resumed processes overlapped and wrote most cases twice (1,153 lines,
all VERIFIED). `results_2026-11-24.tsv` keeps the first line of each case. The rerun here was a single clean run of all 630.

## Controls

| control | expected | result |
|---|---|---|
| `stage2.py full 7`: the same encoding for p = 7 (n = 29, four 7-orbits and a fixed point), a reduced control | SAT, and the solution has no monochromatic K5 by a separate count | SAT, K5 count (red, blue) = (0, 0) |
| `stage2.py glue` control 1: one-side clauses (5-sets using the fixed point and only orbits 0, 1 or only orbits 2, 3) with case units, R1 x R2[:8] | 72/72 SAT | 72/72 SAT |
| same, 20 random G1 not in L | 20/20 UNSAT | 20/20 UNSAT |
| `controls.py` (1): one-side clauses + units of cases (0,0)..(0,7), command-line CaDiCaL | 8/8 SAT | 8/8 SAT |
| `controls.py` (2): proof of case (0,0) cut to its first 80% of lines | drat-trim rejects | rejected |
| `controls.py` (4): proof of case (0,0) on the satisfiable one-side CNF | drat-trim rejects | rejected |
| `controls.py` (3), reference only: proof of (0,0) on its CNF with the last unit flipped | VERIFIED if the proof does not use that unit | VERIFIED |

Control (3) is not a negative control. Assumption cores of the cases use 17 to 34 of the 46 units (measured in the author's unpublished working notes, not included or rechecked here), so a proof need not depend on every unit.

## Reproduce

Requirements: a C compiler, Python 3 with numpy and python-sat, CaDiCaL on PATH (the runs used CaDiCaL 3.0.1 from
Homebrew), drat-trim (https://github.com/marijnheule/drat-trim, the runs used commit 2e3b2dc), `timeout`, and `shasum` or
`sha256sum`. About 8 MB in this folder and about 22 MB of temporary files per worker.

```sh
DRAT_TRIM=/absolute/path/to/drat-trim TMPDIR=/tmp sh reproduce.sh 4     # about 2 to 3 minutes with 4 to 6 workers
```

`reproduce.sh` runs, in order: `stage1.c` (compared with `L.txt` by `cmp`), `recount_L.py`, `recheck.py` (writes
`full_p11.cnf`, prints its SHA-256 next to the expected value, re-solves the 630 cases with Glucose4 and MiniSat22),
`stage2.py full 7` and `stage2.py glue L.txt`, `controls.py`, and `drat11.py` (each case: `cadical -q --no-binary case.cnf
case.drat`, then `drat-trim case.cnf case.drat`; CNF and proof are deleted after the check; results in `build/results.tsv`;
a rerun skips cases already VERIFIED there). The output of the run recorded here is `rerun_2026-11-24.log`.

To keep the proofs of single cases, run the two commands of `run_case()` in `drat11.py` by hand on a case CNF.

## Files

| file | what |
|---|---|
| `stage1.c` | enumerates the 2^21 Z11-invariant two-orbit graphs, writes L |
| `L.txt` | the 1,430 triples (S1mask S2mask Tmask edges) |
| `stage2.py` | encoding (`setup`, `k5_varsets`), `full p` and `glue` modes with control 1 |
| `recheck.py` | writes `full_p11.cnf`; R1, R2, `assum`; Glucose4 and MiniSat22 runs; orbit size check |
| `recount_L.py` | second count of L by SAT model enumeration |
| `drat11.py` | the 630 DRAT runs |
| `controls.py` | DRAT controls (1) to (4) |
| `reproduce.sh` | runs all of the above |
| `results_2026-11-24.tsv` | original DRAT run, 630 rows |
| `results_rerun_2026-11-24.tsv`, `rerun_2026-11-24.log` | rerun from this folder |

Not included: CNF files and DRAT proofs (about 4.8 GB in total; regenerate with `reproduce.sh`), executables.

### Changes from the private working copies

The scripts come from the author's unpublished working notes. Logic is unchanged.
Changes:
- `drat11.py`: `K` (location of `stage2.py`, `L.txt`, `full_p11.cnf`) is this folder instead of a private path; the
  drat-trim binary is `$DRAT_TRIM` or `drat-trim` on PATH instead of a private path.
- All files: Korean comments, docstrings and printed messages translated to English.
- `stage2.py`: the comment on control 1 said "first 200 pairs"; it now says R1 x R2[:8] (72 pairs), which is what the code does.
- `recheck.py`: the docstring said it also writes per-case unit clauses; it only writes `full_p11.cnf` (the units come from `assum()`).
- `controls.py`: the docstring called (3) a negative control and did not list (4); now (3) is described as a reference and (4) is listed.
- `results.tsv` renamed to `results_2026-11-24.tsv`. New files: `reproduce.sh`, `.gitignore`, the rerun table and log.

Checked after the changes: `stage1.c` reproduces `L.txt` byte for byte, `full_p11.cnf` has the original SHA-256, and the
630 cases with their 46 units from this folder's `drat11.py` are identical to those of the private copy.

## Limitations

- Only the action with one fixed point (four 11-cycles) is covered. An automorphism of order 11 on 45 points can also have
  12, 23 or 34 fixed points (three, two or one 11-cycles). Those cases are not part of this folder. A separate computation
  (12 fixed points) and a hand lemma (23 and 34 fixed points) exist in the author's unpublished working notes; they are not included
  here and were not re-reviewed for this folder. So this folder does not show that no (5,5,45)-colouring has an
  automorphism of order 11.
- The DRAT proofs are not archived. They are regenerated deterministically by `reproduce.sh` (the per-case proof sizes of
  the two runs agree), but a reader has to rerun CaDiCaL to obtain them.
- The proofs are checked with drat-trim, which is not a formally verified checker; no LRAT or verified-checker run was made.
- The reduction to 630 cases rests on the hand argument above and on `stage1.c`/`recount_L.py` and the representative code.
  These are not covered by the DRAT proofs. The two lists of L were computed by independent methods and agree.
- The bound R(4,5) <= 32 in step 1 is quoted from the literature (it follows from R(3,5) = 14 and R(4,4) = 18).
- I have not checked whether this result, or a stronger one, is already in the literature on automorphisms of
  (5,5)-graphs. If it is known, I would be glad to learn the reference.
- This is not a bound: 43 <= R(5,5) <= 46 is unchanged.

## AI use

The computation, the scripts and this text were made with the help of an AI coding assistant (Claude). The proposition
has not been read by an expert.
