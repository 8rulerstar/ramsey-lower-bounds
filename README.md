# New lower bounds for classical Ramsey numbers

Graphs and colourings that improve lower bounds for classical Ramsey numbers, each with a checker you can run. The clique side is always checked by search; where the independent side rests on a published theorem instead of a computation, the table says so. Most bounds here come from constructions listed in the dynamic survey *Small Ramsey Numbers* (DS1), applied to newer input graphs. R(6,16) and the `triple-gluing` bounds use a construction that glues three graphs along a common induced subgraph (theorem and proof in [`triple-gluing`](triple-gluing)); I have not found it in the literature.

| bound | previous | graph | folder |
|---|---|---|---|
| R(8,19) >= 1267 | 1237 (DS1 #18) | 1266 vertices, three (8,7)-graphs glued along a 204-vertex common part | [`triple-gluing`](triple-gluing) |
| R(7,19) >= 919 | 908 (DS1 #18) | 918 vertices, triple gluing | [`triple-gluing`](triple-gluing) |
| R(7,18) >= 826 | 797 (DS1 #18) | 825 vertices, triple gluing | [`triple-gluing`](triple-gluing) |
| R(7,17) >= 736 | 729 (DS1 #18) | 735 vertices, triple gluing | [`triple-gluing`](triple-gluing) |
| R(6,16) >= 454 | 434 (DS1 #18) | 453 vertices, three Paley graphs P(101) glued along a common part (triple gluing) | [`r6-16`](r6-16) |
| R(3,3,16) >= 293 | 291 (DS1 #18, Table XIb) | 3-colouring of K_292 (DS1 6.2.g), checked directly | [`r3-3-16`](r3-3-16) |
| R(5,21) >= 445 | 441 (DS1 #18) | 444 vertices, gluing (XSR2 Theorem 3) with a common part found by search; independent side by the theorem | [`r5-21`](r5-21) |
| R(8,19) >= 1239 (superseded by 1267 above) | 1237 (DS1 #18) | 1238 vertices, gluing (DS1 2.2.h) with a newer (7,8)-graph; independent side by the theorem | [`r8-19`](r8-19) |
| R(7,12) >= 420 | 417 (DS1 #18) | 419 vertices, gluing construction (DS1 2.3.h) | [`r7-12`](r7-12) |
| R(7,16) >= 649 | 629 (DS1 #18) | 648 vertices | [`r7-16`](r7-16) |

All results are in this repository. R(7,16) was first published in [ramsey-r7-16](https://github.com/8rulerstar/ramsey-r7-16) (2026-11-10), now archived and pointing here.

Byungkun Jang, independent researcher, bkbkjang@gmail.com

The work was done with the help of an AI coding assistant (Claude); see each folder.

Code: MIT (see `LICENSE`). `r7-16/R(4, 15) >= 163.txt` and `r3-3-16/R3_15_73_input.txt` come from google-research under the Apache License 2.0 (copy in `r7-16/LICENSES/Apache-2.0.txt`). Graph files built from other authors' graphs contain those graphs (see `LICENSE`). Input graphs from other authors keep their source; see each folder.
