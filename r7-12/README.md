# A (7,12)-graph on 419 vertices: R(7,12) >= 420

`R7_12_419.txt` is a graph on 419 vertices with no K7 and no independent set of size 12, so

**R(7,12) >= 420.**

The best bound I know of is R(7,12) >= 417 (Xu, Shao, Radziszowski 2011, listed in the dynamic survey *Small Ramsey Numbers*, S. P. Radziszowski, Electron. J. Combin. DS1, revision #18, 2026, Table Ia). A search on 2026-11-10 (DS1 #18, the google-research `ramsey_number_bounds` repository as of its 2026-10-22 commit, arXiv) found no bound above 417.

## Construction

The graph is not found by search. It is the gluing construction described in DS1 section 2.3.h, with k = 7, p = 6, q = 7, m = 101:

- G: the complement of the 114-vertex (6,7)-graph of Exoo and Tatarevic (a (7,6)-graph). Its vertices 0..100 induce the Paley graph P(101).
- H: the Taylor double cover of P(101), a (7,7)-graph on 204 vertices. Its vertices 0..100 also induce P(101).
- The common part P(101) has no K6, so the glued graph on 114 + 204 + 101 = 419 vertices is a (7,12)-graph.

`build.py` rebuilds the graph from the 114-vertex input graph and checks that both G and H contain P(101) on vertices 0..100. The input graph is not included here. It is the (6,7)-graph of G. Exoo and M. Tatarevic, New lower bounds for 28 classical Ramsey numbers, Electron. J. Combin. 22(3) (2015) #P3.11 ([journal page](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11), [arXiv:1504.02403](https://arxiv.org/abs/1504.02403)), whose graphs are available from the journal. To rebuild, save it as `R6_7_114_input.txt` in the plain format below (first line 114, then 114 rows of 0/1); `reproduce.sh` checks its SHA-256 (b3458603...5f0384fe) and skips the rebuild if the file is missing. The checks of `R7_12_419.txt` itself do not need it.

## Quick start

```sh
sh reproduce.sh      # 5 parallel jobs by default (J=8 sh reproduce.sh for 8); about 25 to 40 minutes. Progress: wc -l ind12.log (419 lines at the end)
```

Expected output: checksums OK, the rebuild lines (or a note that the input is missing), `NONE mode=0 k=7 ...` (no K7), `roots with NONE (expect 419): 419`, `OK: R(7,12) > 419`.

## Files

| file | content |
|---|---|
| `R7_12_419.txt` | the graph: first line n, then n rows of 0/1 (1 = edge) |
| `build.py` | the construction |
| `verify.c` | branch-and-bound checker (bitsets, greedy colouring bound) |
| `vpar.c` | the same search split by root vertex: root v searches the (non-)neighbours of v above v, so roots 0..n-1 together cover every set, with no symmetry assumption |
| `check3.c` | second checker written separately (byte matrix, candidate lists), shares no code with `verify.c` |
| `reproduce.sh` | rebuild and check |

## Verification (2026-11-10 and 2026-11-11, Apple M4 Pro)

1. `vpar` over all 419 roots: no K7 (9.5e6 nodes, under 1 s) and no independent 12-set (all 419 roots NONE, 8.4e10 nodes, about 23 minutes on 5 cores).
2. `check3 7 12`: same result from a separate implementation (no K7, 3.0e6 nodes; no independent 12-set, 2.2e10 nodes; 1 h 58 min on one core).
3. The graph equals the 2.3.h construction entry by entry, checked by a second derivation written separately from `build.py`.
4. A networkx run was stopped unfinished after about 8 hours.
5. The checkers and scripts were written by me with the help of an AI coding assistant (Claude).
