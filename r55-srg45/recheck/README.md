# Recount of the 52 window classes (2026-11-20)

**From the published search output alone, the 799 window solutions of the main engine fall into 52 isomorphism classes, none with a square determinant. On the 454 pairs where the main engine found solutions, the 2,451 labelled solutions of the second engine give the same 52 classes.**

This folder only reads files already in `r55-srg45/` (`results/window_solutions.tsv`, `data/`, `second_engine/`). No new search is run. It is a recount of published outputs, not an independent recomputation.

## Run

```
cd r55-srg45/recheck
pip install python-igraph numpy        # tested with python-igraph 1.0.0, numpy 2.5.4
mkdir -p indep && tar xzf ../second_engine/raw_out.tar.gz -C indep
python canon_selftest.py     # canonical form check: 100 relabellings of one graph give 1 class
python s2_classes.py         # writes out/classes_summary.txt, out/window52.tsv, out/window52.g6, out/orbits_per_pair.tsv
```

`exact.py` does the exact rational checks (positive semidefiniteness, determinant, factorisation).

## What `out/classes_summary.txt` checks

- 799 main solutions: exact window 799, positive definite 799, determinant equal to `window_solutions.tsv` for all 799; 52 classes.
- Second engine: it covered 40,453 pairs (not all 6,313,538). Its window solutions lie in the same 454 pairs as the main engine's. On these 454 pairs its 2,451 labelled solutions all pass the exact window and give the same 52 classes.
- Orbit consistency: summed over the 454 pairs, the Aut(K) x Aut(B)-orbits of window solutions number 488. Summed over the 52 classes, the Aut-orbits of roots w with e(N(w)) in {15,16,18,19} also number 488.
- 52 distinct determinants, none a square. The multiset equals `../second_engine/dets.txt` (the summary line calls it `indep/dets.txt`).

## Limits

Both engines read the same `data/` catalogues, and this recount shares `exact.py` and the canonical-form code between them. The second engine was written separately, but its independence is not verified here. A fully independent reimplementation has not been run (see `../README.md`).

## Note on an earlier count

An earlier recount script applied the canonical permutation in the wrong direction, so relabellings of one graph were counted as different classes. `canon_selftest.py` guards against this.

Release v1.6 of the manuscript states that "all 318 expected (graph, root class) pairs appear". No script here reproduces that count, and its definition of a root class is not recorded. The manuscript now states the orbit consistency check above instead.
