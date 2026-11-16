# Second engine (cross-check)

`eng.c` is a second search engine for window graphs, written from the mathematical definitions by a separate
instance of the AI assistant that was not given the source of `src/glue_srg.c`. It chooses, for each vertex of K,
its neighbourhood in B (instead of a cone for each vertex of B), uses no symmetry reduction, checks 10-regularity,
K4 and independent 5-sets directly on every complete graph, and tests the window with Jacobi eigenvalues
(tolerance 1e-7 on the accepting side).

- `tasks_win.txt`: all 454 (job, pair) entries of `results/window_solutions.tsv`.
- `tasks_sample.txt`: first up to 200 pairs of 200 random jobs. `tasks_all.txt` = both, 40,453 pairs in total.
- Build: `gcc -O2 -march=native -DACL=0 -o eng eng.c -lm` (the build used for the run). `runjob.sh`: runs one task line. `compare.py`: compares, pair by pair and up to isomorphism, with
  `results/window_solutions.tsv`, and writes the exact determinants of the distinct window graphs to `dets.txt`.
- Result: 0 mismatches, 52 isomorphism classes, no square determinant. Not run on all 6,313,538 pairs
  (estimated about 1,500 CPU hours).
Both engines were produced with AI assistance; they share no code but are not independent in authorship.
