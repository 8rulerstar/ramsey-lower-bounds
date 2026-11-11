# A (8,19)-graph on 1238 vertices: R(8,19) >= 1239

`R8_19_1238.txt` is a graph on 1238 vertices built so that it has no K8 and no independent set of size 19, which gives

**R(8,19) >= 1239.**

The dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, Electron. J. Combin. DS1, revision #18, 2026) lists
R(8,19) >= 1237 in Table IIa (item 2.2.h). That bound glues an 816-vertex (8,13)-graph, an (8,7)-graph and their common
204-vertex induced subgraph (the witness of R(7,7) >= 205): 816 + 216 + 204 + 1 = 1237, so it used a 216-vertex
(8,7)-graph, from R(7,8) >= 217 (2011). Table Ia of the same revision has R(7,8) >= 219 (Tatarevic, 2020). The same
construction with Tatarevic's 218-vertex graph gives 816 + 218 + 204 + 1 = 1239. Nothing new is invented here: it is
the survey's construction with a newer input graph.

## Construction (DS1 2.2.h, 2.3.h, 2.3.i)

- H204: the Taylor double cover of the Paley graph P(101), a (7,7)-graph on 204 vertices.
- G816: XXER Theorem 9 (DS1 2.3.i, R(2k-1, l) >= 4R(k, l-1) - 3) with k = 7, l = 8, applied to the complement of
  H204 and complemented: an (8,13)-graph on 816 vertices whose vertices 0..203 induce H204.
- G218: colour 1 of `graphs/g78.218` in [milostatarevic/ramsey-numbers](https://github.com/milostatarevic/ramsey-numbers)
  (the witness of R(7,8) >= 219), an (8,7)-graph. Its vertices `phi[i]` (`phi.txt`) induce H204.
- DS1 2.3.h: since H204 has no K7, gluing G816, G218 and a third copy of H204 gives an (8,19)-graph on
  816 + 218 + 204 = 1238 vertices.

`build.py` rebuilds the graph from `g78.218` (not included: the source repository has no license) and asserts that
both G816 and G218 contain H204 on the stated vertices.

## Quick start

```sh
sh reproduce.sh      # about 2 minutes; put g78.218 next to it to also rebuild and check the 218-vertex part
```

## Verification (2026-11-11, Apple M4 Pro)

1. `vpar` over all 1238 roots: no K8 (5.6e8 nodes, 47 s).
2. Rebuild from `g78.218` matches the file byte for byte; `verify 8 7` on the 218-vertex part: no K8, no
   independent 7-set; both induced copies of H204 are checked entry by entry; H204 is a (7,7)-graph (checked with
   `verify`, see `../r7-12`).
3. **Not done: a direct check that the graph has no independent set of size 19.** Single low roots of `vpar` take
   more than 5 minutes each, and there are 1238 roots. The independent-set side rests on DS1 2.3.h and 2.3.i (XXER
   Theorem 9) with the hypotheses above checked by machine. A direct check that G816 is an (8,13)-graph is running.
4. The checkers and scripts were written by me with the help of an AI coding assistant (Claude).
