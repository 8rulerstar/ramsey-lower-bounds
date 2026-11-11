# A 3-colouring of K_292: R(3,3,16) >= 293

`R3_3_16_292.txt` is a colouring of the edges of the complete graph on 292 vertices with colours 1, 2, 3 (row i,
column j = colour of edge ij; 0 on the diagonal) with no triangle in colour 1, no triangle in colour 2 and no K16 in
colour 3, so

**R(3,3,16) >= 293.**

The dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, Electron. J. Combin. DS1, revision #18, 2026) lists
R(3,3,16) >= 291 in Table XIb [ExT]. Its item 6.2.g, R(3,k,l) >= 4R(k,l-1) - 3 for k >= 3, l >= 5 [XuX2, XXER], with
k = 3, l = 16 and R(3,15) >= 74 (Table Ia) gives 4 * 74 - 3 = 293. This folder builds that colouring explicitly and
checks it directly. Nothing new is invented: it is the survey's construction applied to a current table value.

## Construction

From a (3,15)-graph G on 73 vertices (no triangle, no independent 15-set), the colouring of Xu, Xie, Exoo and
Radziszowski (EJC 11 (2004) #R35, Theorem 7) on 4 * 73 = 292 vertices, see `build.py`. `R3_15_73_input.txt` is the
73-vertex graph `R(3, 15) >= 74.txt` of google-research `ramsey_number_bounds/improved_bounds` (AlphaEvolve, Nagda,
Raghavan and Thakurta, arXiv:2603.09172), converted to this plain format; Apache License 2.0 (copy in `../r7-16/LICENSES/Apache-2.0.txt`).

## Verification (2026-11-11, Apple M4 Pro)

`sh reproduce.sh`: the input is a (3,15)-graph (`verify`), the rebuilt colouring matches the file, colours 1 and 2
have no triangle and colour 3 has no K16 (`vpar` over all 292 roots, 7.0e9 nodes, 22 minutes). This is a direct
check of every property; nothing rests on the theorem. The checkers were written by me with the help of an AI coding
assistant (Claude).
