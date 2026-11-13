# No SRG(45,22,10,11) is a (5,5)-Ramsey graph

**This is not a bound.** 43 <= R(5,5) <= 46 is unchanged. The result rules out one natural family of highly regular
candidates for a (5,5)-graph on 45 vertices. A (5,5)-graph is a graph with no K5 and no independent 5-set. The proof has not yet
been read by an expert.

**Theorem 1.** Every strongly regular graph with parameters (45,22,10,11) contains a 5-clique or an independent 5-set.

**Theorem 2 (local version).** A graph on 45 vertices with no K5 and no independent 5-set has no vertex v with:
deg v = 22; every neighbour of v has degree 22 and exactly 10 common neighbours with v; two neighbours of v have exactly
10 common neighbours in the whole graph if they are adjacent and 11 if they are not.

The proof is computer-assisted. Statement, lemmas and proofs: [NOTE.md](NOTE.md).

## What the proof depends on

- McKay's complete lists of (3,5,10)-graphs (313) and (4,4,11)-graphs (546,356).
- An exhaustive gluing computation (912 CPU hours, the engine in `src/`), with a floating-point eigenvalue test
  whose tolerance is set to accept borderline cases, followed by an exact integer determinant test.
- During the distributed run 60 result files were overwritten by partial copies and were resumed with the same engine;
  see NOTE.md, section 7.
- A variant engine reproduced the counts on a sample, and every window graph found reappears from all of its admissible
  roots (closure check); a fully independent implementation of the search has not been run.

## How it works

1. **Local identity.** At a vertex v as in Theorem 2, let A be the graph on N(v) and N the 22 x 22 adjacency matrix
   between N(v) and the non-neighbours of v. Then N N^T = 11I + 10J - A - A^2 and A is 10-regular. So every eigenvalue
   of A other than the trivial eigenvalue 10 lies in the window [s, r], s, r = (-1 -+ sqrt 45)/2, and
   det(11I + 10J - A - A^2) is a perfect square. A is also K4-free with no independent 5-set.
2. **Finite search.** Pick a vertex w of A. Its neighbourhood K in A is one of 147 graphs on 10 vertices (triangle-free,
   independence number at most 4, filtered by eigenvalue interlacing from McKay's 313), and the 11 vertices of A not
   adjacent to w induce a graph B from a filtered list of graphs with no K4 and no independent 4-set. A mod 3 argument
   shows that roots whose K has 15, 16, 18 or 19 edges suffice.
3. **Gluing.** For every pair (K, B) the engine enumerates all ways to join B to K giving a 10-regular graph with no K4
   and no independent 5-set, and keeps those whose eigenvalues lie in the window ("window solutions").
4. **Determinant.** Every window solution is checked exactly. None has a perfect-square determinant.

## Results

| item | value | file |
|---|---|---|
| jobs | 1,555 (K with 16, 18, 19 edges) + 68 (K with 15 edges) | data/jobs.txt, data/jobs_e15.txt |
| pairs (K, B) processed | 6,313,538 | results/ledger.txt, results/jobs_summary.tsv |
| gluings found (10-regular, no K4, no independent 5-set; first cone up to symmetry) | 1,030,818 | same |
| window solutions | 799 | results/window_solutions.tsv |
| CPU time of the gluing | 912 hours | results/ledger.txt |
| window solutions with perfect-square determinant | 0 (no zero determinant either) | results/window_solutions.tsv, results/window_check.txt |

Raw outputs of the run (one file per job, 79 MB) are attached to the v1.5 release of this repository as
`srg45_raw_outputs.tar.gz`; its checksum is in `results/raw_archive.sha256`.

## Reproduce

Requirements: a C compiler, Python 3 with numpy and sympy, and McKay's list `r44_11.g6.gz` of (4,4,11)-graphs from
https://users.cecs.anu.edu.au/~bdm/data/ramsey.html (keep it gzipped). The (3,5,10) list is included in `data/mckay/`.

```bash
python pipeline/01_filter_K.py                      # 313 -> 147 root classes, compared with data/
python pipeline/02_build_B.py path/to/r44_11.g6.gz   # rebuilds the B lists, compared with data/B (about 5 minutes)
python pipeline/03_make_jobs.py                     # rebuilds both job lists, compared with data/
bash pipeline/04_run_job.sh K69_e29_84000           # runs one job into out/ (minutes to an hour, depending on the job)
python pipeline/06_completeness.py out --present    # checks the jobs present in out/ (omit --present for the full ledger)
python pipeline/05_check_windows.py out             # exact determinant test of all window solutions in a folder
python pipeline/07_reroot_check.py                  # closure check of results/window_solutions.tsv
```

## Layout

- `src/glue_srg.c`: the engine used for the run (comments in Korean; the header also describes options of the engine it
  was derived from). `src/glue_srg_inc.c`: variant with extra pruning, used for a cross-check.
- `pipeline/`: filters, job lists, run script, checks.
- `data/`: K classes, filtered B lists, job lists, control instance, McKay's (3,5,10) list.
- `results/`: ledger, per-job summary with checksums, all window solutions with exact determinants, cross-check logs.

## Data sources and licence

`data/mckay/r35_10.g6` is a copy of, and `data/B/*.g6` and `data/K/*.g6` are selections from, the Ramsey graph lists of
Brendan D. McKay (https://users.cecs.anu.edu.au/~bdm/data/ramsey.html); see that page for the terms of use and cite it
when you use these files. The selection is described
in NOTE.md and reproduced by `pipeline/01` and `pipeline/02`. Everything else in this folder is covered by the licence
of this repository.

## Related work

A SAT-based attack on the same question (Braginsky, Yellenki, Zhu with J. Mackey, March 2026) settled 141 of 313 cases;
see NOTE.md for references.
