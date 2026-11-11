# A (5,21)-graph on 444 vertices: R(5,21) >= 445

`R5_21_444.txt` is a graph on 444 vertices built so that it has no K5 and no independent set of size 21, which gives

**R(5,21) >= 445.**

The dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, Electron. J. Combin. DS1, revision #18, 2026) lists
R(5,21) >= 441 in Table IIa (from 2.3.i). This bound uses the gluing theorem of Xu, Shao and Radziszowski
(SIAM J. Discrete Math. 25 (2011) 394-400, Theorem 3, the general form of DS1 2.3.h): if a (k,s)-graph G and a
(k,t)-graph H share an induced subgraph M whose vertices split into two parts with no K_{k-2}, then
R(k, s+t-1) >= n(G) + n(H) + n(M) + 1. Here k = 5, s = 17, t = 5: 384 + 42 + 18 + 1 = 445.

## Ingredients

- G384: a (5,17)-graph on 384 vertices: the cubic-residue colouring of Mathon for p = 127 (in the form of Xu and
  Radziszowski, EJC 16 (2009) #N1), one colour, on 3p + 3 vertices (`build.py` has the exact rule). Xu, Shao and
  Radziszowski used a 387-vertex extension of it; I could not reproduce that extension, so the smaller graph is used.
- H42: graph number 2 (0-based) of B. D. McKay's list of 42-vertex (5,5)-graphs
  ([r55_42some.g6](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html), not included here).
- M: 18 vertices of H42 (`common_part.txt`), split into two triangle-free parts of 9 vertices, with an induced copy
  in G384 (the map in the same file). Found by a randomized local search; larger common parts may exist.

## Quick start

```sh
sh reproduce.sh      # put r55_42some.g6 next to it to also rebuild and check the ingredients (about 3 minutes)
```

## Verification (2026-11-11, Apple M4 Pro)

1. `vpar` over all 444 roots: no K5.
2. Rebuild from `r55_42some.g6` matches the file byte for byte. `build.py` checks the induced copy of M and that both
   parts are triangle-free. G384: no K5 and no independent 17-set (`vpar` over all 384 roots, 3.5e8 nodes, 75 s).
   H42: `verify 5 5`.
3. **Not done: a direct check that the 444-vertex graph has no independent set of size 21.** A root-by-root search was
   started on 2026-11-11 and stopped as infeasible. The independent-set side rests on the theorem above with
   machine-checked hypotheses.
4. The checkers and scripts were written by me with the help of an AI coding assistant (Claude).
