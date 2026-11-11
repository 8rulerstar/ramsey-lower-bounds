# New lower bounds for classical Ramsey numbers

Graphs and colourings that improve lower bounds for classical Ramsey numbers, each with a checker you can run. The bounds here come from constructions listed in the dynamic survey *Small Ramsey Numbers* (DS1), applied to newer input graphs; they are not found by computer search.

| bound | previous | graph | folder |
|---|---|---|---|
| R(3,3,16) >= 293 | 291 (DS1 #18, Table XIb) | 3-colouring of K_292 (DS1 6.2.g), checked directly | [`r3-3-16`](r3-3-16) |
| R(5,21) >= 445 | 441 (DS1 #18) | 444 vertices, gluing (XSR2 Theorem 3) with a common part found by search | [`r5-21`](r5-21) |
| R(8,19) >= 1239 | 1237 (DS1 #18) | 1238 vertices, gluing (DS1 2.2.h) with a newer (7,8)-graph | [`r8-19`](r8-19) |
| R(7,12) >= 420 | 417 (DS1 #18) | 419 vertices, gluing construction (DS1 2.3.h) | [`r7-12`](r7-12) |
| R(7,16) >= 649 | 629 (DS1 #18) | 648 vertices | [`r7-16`](r7-16) |

All results are in this repository. R(7,16) was first published in [ramsey-r7-16](https://github.com/8rulerstar/ramsey-r7-16) (2026-11-10), now archived and pointing here.

Byungkun Jang, independent researcher, bkbkjang@gmail.com

Code: MIT (see `LICENSE`). `r7-16/R(4, 15) >= 163.txt` is from google-research under the Apache License 2.0 (see `r7-16/LICENSE_r7-16` and `r7-16/LICENSES`). Input graphs from other authors keep their source; see each folder.
