# Computational results on classical Ramsey numbers

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24128875.svg)](https://doi.org/10.5281/zenodo.24128875)

Graphs and colourings that improve lower bounds for classical Ramsey numbers, with the constructions, their proofs and
checkers you can run. Comparison values are from the dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, DS1
rev. 18, 2026) or, where newer, the google-research ramsey_number_bounds repository.

The repository also contains results of a different kind about (5,5)-graphs on 45 vertices, that is, graphs with no K5 and
no independent 5-set: a computer-assisted proof that no strongly regular graph SRG(45,22,10,11) is a (5,5)-graph, and two
partial results (section "Nonexistence results"). None of them is a bound.

## Main results (new lower bounds)

- **R(7,16) >= 708** (DS1 rev. 18: 629) and **R(8,19) >= 1429** (1237), from theorem D (heptagon gluing).
- **R(6,16) >= 454** (434), **R(7,17) >= 736** (729), **R(7,19) >= 919** (908), from triple gluing (theorem H); also R(7,18) >= 827 (797).
- **R(8,18) >= 1133** (1049; google-research 1052), from theorem DG.
- In cells the survey does not list: **R(8,25) >= 2449** (2049 is the best value I could derive from published results),
  from theorem D12; **R(7,20) >= 933** (931 from known results).

## Nonexistence results

| statement | effect on bounds | method | folder |
|---|---|---|---|
| No SRG(45,22,10,11) is a (5,5)-graph; more generally no (5,5)-graph on 45 vertices has a vertex of degree 22 whose neighbours have the degrees and codegrees they would have in an SRG(45,22,10,11) (Theorem 2 in the folder) | none (43 <= R(5,5) <= 46 unchanged) | local Gram identity, exhaustive gluing over McKay's lists (912 CPU hours), exact determinant test | [`r55-srg45`](r55-srg45) |
| (24,24) extremal-pair lemma: in a (5,5,45)-colouring, two vertices of red degree 24 whose red neighbourhoods have >= 127 edges are not joined by a red edge (computation complete; written covering argument pending; DRAT certificates for the 961 SAT-solver cases and a 1,000-placement sample) | none (43 <= R(5,5) <= 46 unchanged) | exhaustive check of 4,835,956,732 placements (propagation, failed-literal probing, CaDiCaL), independent engine on 100,000 samples | [`r55-pair2424`](r55-pair2424) |
| No (5,5)-graph on 45 vertices has an automorphism of order 11 with four 11-cycles and one fixed point (the other order-11 actions, with 12, 23 or 34 fixed points, are not covered here) | none (43 <= R(5,5) <= 46 unchanged) | split by the fixed point's two links, 630 SAT cases, each checked with a DRAT proof by drat-trim (proofs regenerated, not archived) | [`r55-aut11`](r55-aut11) |

None of these is a bound. The first row rules out one natural family of highly regular candidates for a (5,5)-graph on 45
vertices. Its proof is computer-assisted and has not yet been read by an expert; the statement and proof are in
[`r55-srg45/NOTE.md`](r55-srg45/NOTE.md), what it depends on is listed in [`r55-srg45/README.md`](r55-srg45/README.md), and
[`r55-srg45/audit454`](r55-srg45/audit454) is a SAT recount of its 454 positive pairs. The other rows are documented in their folders.

## Constructions

All of them glue known Ramsey graphs along a common induced subgraph M. I have not found theorems H, P, D, D1, D12 and DG in
the literature (the search is described in each folder); if any is known, I would be glad to learn the reference. Each
folder has the statement and a written proof; the proofs have not yet been read by an expert.

| name | statement | where |
|---|---|---|
| H (triple gluing) | R(k, s_1+s_2+s_3-2) >= n_1+n_2+n_3+3m+1, M with no K_{k-1}, k >= 4 | [`triple-gluing`](triple-gluing) |
| P | theorem H with a different common part for each pair of graphs | [`triple-gluing`](triple-gluing), section "Different common parts" |
| B | r graphs instead of 3 (improves no table entry) | [`triple-gluing`](triple-gluing), section "Generalization to r graphs" |
| D | R(k+1, s_1+s_2+s_3-2) >= n_1+n_2+n_3+4m+1, any common M, k >= 4; in particular R(k+1, 3s-2) >= 7R(k,s) - 6 | [`seven-copies`](seven-copies) |
| D1 (two-graph version of D) | R(k+1, p+q-1) >= n_1+n_2+2m+1, any common M, k >= 4 (contains DS1 2.3.i) | [`r8-12`](r8-12) |
| D12 | R(k+1, 4s-3) >= 12R(k,s) - 11, k >= 4 (copies of one graph) | [`twelve-copies`](twelve-copies) |
| DG | general copy patterns containing D, D1, D12; e.g. R(k+1, 2p+q-2) >= 4n_H + n_G + 2m + 1 | [`general-gluing`](general-gluing) |

## Current bounds

| bound | previous | graph | folder |
|---|---|---|---|
| R(8,25) >= 2449 | not in DS1 rev. 18 (2049, best value I could derive) | 2448 vertices, theorem D12, twelve copies of the 204-vertex (7,7)-graph H204 | [`twelve-copies`](twelve-copies) |
| R(8,19) >= 1429 | 1237 | 1428 vertices, theorem D, three copies of H204c (the complement of H204) | [`seven-copies`](seven-copies) |
| R(7,16) >= 708 | 629 | 707 vertices, theorem D, three copies of P(101) | [`seven-copies`](seven-copies) |
| R(8,18) >= 1133 | 1049; 1052 (google-research) | 1132 vertices, theorem DG: H204 as a layer on four positions and a (7,6)-graph as a side, glued along P(101) | [`general-gluing`](general-gluing) |
| R(7,20) >= 933 | not in DS1 rev. 18 (931 from known results) | 932 vertices, theorem H | [`triple-gluing`](triple-gluing) |
| R(7,19) >= 919 | 908 | 918 vertices, theorem H | [`triple-gluing`](triple-gluing) |
| R(7,18) >= 827 | 797 | 826 vertices, theorem P | [`triple-gluing`](triple-gluing) |
| R(7,17) >= 736 | 729 | 735 vertices, theorem H | [`triple-gluing`](triple-gluing) |
| R(6,16) >= 454 | 434 | 453 vertices, theorem H, three copies of P(101) | [`r6-16`](r6-16) |
| R(5,21) >= 445 | 441 | 444 vertices, Theorem 3 of Xu, Shao, Radziszowski (2011) with a common part found by search; independent side by that published theorem | [`r5-21`](r5-21) |
| R(7,12) >= 420 | 417 | 419 vertices, DS1 2.3.h with a newer input graph; independent side by direct search | [`r7-12`](r7-12) |
| R(3,3,16) >= 293 | 291 (Table XIb) | 3-colouring of K_292 (DS1 6.2.g), all three colours checked by direct search | [`r3-3-16`](r3-3-16) |

## How the results are checked

For every graph the clique side (no clique of the forbidden size) is checked by exhaustive search (`vpar`, all roots). For the graphs from
theorems H, P, D, D1, D12 and DG the independent side is checked, in addition to the written proof, by an exhaustive
certificate on the graph file: a program verifies, for every pair of elements that can lie together in an independent set,
the conditions of the proof's assignment, so the bound on the independence number does not rest on the written argument
(it uses the independence numbers of the input graphs, checked by `verify`). Each of these folders has a `check.sh` (`reproduce.sh` in `r6-16`) that
rebuilds the graph from its inputs and runs all checks. To start reading: [`seven-copies`](seven-copies), then
[`r8-12`](r8-12) and [`triple-gluing`](triple-gluing).

The nonexistence result in [`r55-srg45`](r55-srg45) is of a different kind: an exhaustive search rather than a graph with a
checker. Its folder has the filters rebuilt from McKay's lists, the job list, a ledger of all jobs, every window solution
with its exact determinant, and scripts that recheck them.

## Citing

Please cite the Zenodo record, all versions: DOI [10.5281/zenodo.24128875](https://doi.org/10.5281/zenodo.24128875)
(see `CITATION.cff`). Versions:
- v1.0 (2026-11-11), [10.5281/zenodo.24128876](https://doi.org/10.5281/zenodo.24128876): triple gluing and the first bounds.
- v1.1 (2026-11-12), [10.5281/zenodo.24149479](https://doi.org/10.5281/zenodo.24149479): R(7,16) >= 708, R(8,19) >= 1429, R(8,18) >= 1054, R(7,18) >= 827.
- v1.2.1 (2026-11-12), [10.5281/zenodo.24150638](https://doi.org/10.5281/zenodo.24150638): theorems D and D1 with certificates, R(8,12) >= 521.
- v1.3 (2026-11-12), [10.5281/zenodo.24153490](https://doi.org/10.5281/zenodo.24153490): theorem D12, R(8,25) >= 2449.
- v1.4 (2026-11-12), [10.5281/zenodo.24154888](https://doi.org/10.5281/zenodo.24154888): theorem DG, R(8,18) >= 1133.
- v1.5 (2026-11-14), [10.5281/zenodo.24209919](https://doi.org/10.5281/zenodo.24209919): the nonexistence result for SRG(45,22,10,11) in `r55-srg45`. To cite that result alone, cite
  the v1.5 version DOI above and name the folder: B. Jang, *No strongly regular graph SRG(45,22,10,11) is a (5,5)-Ramsey graph*,
  in: Computational results on classical Ramsey numbers, v1.5, folder `r55-srg45`.
- v1.6 (2026-11-16), [10.5281/zenodo.24270339](https://doi.org/10.5281/zenodo.24270339): SRG(45,22,10,11) second engine cross-check.
- v1.7 (2026-11-20), [10.5281/zenodo.24383617](https://doi.org/10.5281/zenodo.24383617): SRG(45,22,10,11) recount of the 52 window classes (its note's count 2,451 was corrected to 2,392 in v1.8).
- v1.8 (2026-11-24), [10.5281/zenodo.24494057](https://doi.org/10.5281/zenodo.24494057): `r55-aut11` (no (5,5)-graph on 45 vertices with an order-11 automorphism with one fixed point) and `r55-srg45/audit454` (SAT recount of the 454 positive pairs).

<details>
<summary>Earlier bounds, now superseded or not new</summary>

| bound | superseded by | folder |
|---|---|---|
| R(8,19) >= 1239 | 1267, then 1429 | [`r8-19`](r8-19) |
| R(8,19) >= 1267 | 1429 | [`triple-gluing`](triple-gluing) |
| R(7,18) >= 826 | 827 | [`triple-gluing`](triple-gluing) |
| R(8,18) >= 1054 | 1133 | [`r8-18`](r8-18) |
| R(7,16) >= 649 | 708 | [`r7-16`](r7-16) (first published in [ramsey-r7-16](https://github.com/8rulerstar/ramsey-r7-16), 2026-11-09) |
| R(8,12) >= 521 | not a record when published: [quantavane-ramsey-records](https://github.com/arhancanli/quantavane-ramsey-records) had 519 (2026-11-03) and 523 (2026-11-06) | [`r8-12`](r8-12) |

</details>

## Author, AI use and license

Byungkun Jang, independent researcher, bkbkjang@gmail.com. The searches, constructions, proofs and checks were made with
the help of an AI coding assistant (Claude); see each folder.

Code: MIT. Documentation and the graphs constructed here: CC BY 4.0, please credit Byungkun Jang and cite the Zenodo DOI
(see `LICENSE`, `CITATION.cff`). `r7-16/R(4, 15) >= 163.txt` and `r3-3-16/R3_15_73_input.txt` come from google-research
under the Apache License 2.0 (copy in `r7-16/LICENSES/Apache-2.0.txt`). Graph files built from other authors' graphs
contain those graphs (see `LICENSE`). The lists in `r55-srg45/data`, `r55-pair2424/d24_e127.g6` and `r55-pair2424/data/r55_42some.g6` are copies of or selections from B. D. McKay's Ramsey graph
data (see `r55-srg45/README.md`).
