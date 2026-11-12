# New lower bounds for classical Ramsey numbers

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24128875.svg)](https://doi.org/10.5281/zenodo.24128875)

Archived snapshots: Zenodo, all versions DOI [10.5281/zenodo.24128875](https://doi.org/10.5281/zenodo.24128875); v1.0 of 2026-11-11 is [10.5281/zenodo.24128876](https://doi.org/10.5281/zenodo.24128876). v1.1 of 2026-11-12 (seven-copy theorem, R(7,16) >= 708, R(8,19) >= 1429, R(8,18) >= 1054, R(7,18) >= 827) is [10.5281/zenodo.24149479](https://doi.org/10.5281/zenodo.24149479).

Graphs and colourings that improve lower bounds for classical Ramsey numbers, each with a checker you can run. The clique side is always checked by search. The table says how the independent side is established: by direct search, by an exhaustive certificate check on the graph (the triple-gluing rows: a program verifies the conditions of the proof on that graph), or by a published theorem. Most bounds here come from constructions listed in the dynamic survey *Small Ramsey Numbers* (DS1), applied to newer input graphs. R(6,16) and the `triple-gluing` bounds use a construction that glues three graphs along a common induced subgraph (theorem and proof in [`triple-gluing`](triple-gluing)); I have not found it in the literature. The [`seven-copies`](seven-copies) bounds use a new construction R(k+1, 3s-2) >= 7R(k,s) - 6 (theorem and proof in that folder), also not found in the literature.

| bound | previous | graph | folder |
|---|---|---|---|
| R(8,12) >= 521 | 511 (google-research 2026) | 520 vertices, theorem D1: a (7,7)- and a (7,6)-graph glued along P(101) with k raised by one; no K_8 by search, independent side by an exhaustive certificate check on the graph | [`r8-12`](r8-12) |
| R(8,19) >= 1429 | 1237 (DS1 #18) | 1428 vertices, seven copies of the 204-vertex (7,7)-graph; no K_8 by search over all roots, independent side by the theorem | [`seven-copies`](seven-copies) |
| R(7,16) >= 708 | 629 (DS1 #18) | 707 vertices, seven copies of P(101); no K_7 by search, independent side by the theorem (direct search running) | [`seven-copies`](seven-copies) |
| R(8,18) >= 1054 | 1049 (DS1 #18), 1052 (google-research 2026-10-22) | 1053 vertices, DS1 2.3.h with a 104-vertex common part; independent side by a short proof | [`r8-18`](r8-18) |
| R(7,18) >= 827 | 797 (DS1 #18) | 826 vertices, triple gluing with different common parts per pair; independent side by an exhaustive certificate check on the graph | [`triple-gluing`](triple-gluing) |
| R(8,19) >= 1267 (superseded by 1429 above) | 1237 (DS1 #18) | 1266 vertices, three (8,7)-graphs glued along a 204-vertex common part; independent side by an exhaustive certificate check on the graph | [`triple-gluing`](triple-gluing) |
| R(7,20) >= 933 | no entry in DS1 #18 (931 from known results) | 932 vertices, triple gluing; independent side by an exhaustive certificate check on the graph | [`triple-gluing`](triple-gluing) |
| R(7,19) >= 919 | 908 (DS1 #18) | 918 vertices, triple gluing; independent side by an exhaustive certificate check on the graph | [`triple-gluing`](triple-gluing) |
| R(7,18) >= 826 (superseded by 827 above) | 797 (DS1 #18) | 825 vertices, triple gluing; independent side by an exhaustive certificate check on the graph | [`triple-gluing`](triple-gluing) |
| R(7,17) >= 736 | 729 (DS1 #18) | 735 vertices, triple gluing; independent side by an exhaustive certificate check on the graph | [`triple-gluing`](triple-gluing) |
| R(6,16) >= 454 | 434 (DS1 #18) | 453 vertices, three Paley graphs P(101) glued along a common part (triple gluing); independent side by an exhaustive certificate check on the graph | [`r6-16`](r6-16) |
| R(3,3,16) >= 293 | 291 (DS1 #18, Table XIb) | 3-colouring of K_292 (DS1 6.2.g), all three colours checked by direct search | [`r3-3-16`](r3-3-16) |
| R(5,21) >= 445 | 441 (DS1 #18) | 444 vertices, gluing (XSR2 Theorem 3) with a common part found by search; independent side by the theorem | [`r5-21`](r5-21) |
| R(8,19) >= 1239 (superseded by 1267 above) | 1237 (DS1 #18) | 1238 vertices, gluing (DS1 2.2.h) with a newer (7,8)-graph; independent side by the theorem | [`r8-19`](r8-19) |
| R(7,12) >= 420 | 417 (DS1 #18) | 419 vertices, gluing construction (DS1 2.3.h); independent side by direct search | [`r7-12`](r7-12) |
| R(7,16) >= 649 (superseded by 708 above) | 629 (DS1 #18) | 648 vertices; independent side by direct search | [`r7-16`](r7-16) |

All results are in this repository. R(7,16) was first published in [ramsey-r7-16](https://github.com/8rulerstar/ramsey-r7-16) (2026-11-10), now archived and pointing here.

Byungkun Jang, independent researcher, bkbkjang@gmail.com

The work was done with the help of an AI coding assistant (Claude); see each folder.

Code: MIT (see `LICENSE`). `r7-16/R(4, 15) >= 163.txt` and `r3-3-16/R3_15_73_input.txt` come from google-research under the Apache License 2.0 (copy in `r7-16/LICENSES/Apache-2.0.txt`). Graph files built from other authors' graphs contain those graphs (see `LICENSE`). Input graphs from other authors keep their source; see each folder.
