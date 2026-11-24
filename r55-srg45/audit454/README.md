# SAT recount of the 454 positive pairs (2026-11-24)

**Result.** For each of the 454 pairs (K, B) on which the original search reported window solutions, a separately written SAT encoding of the gluing problem has a recorded or replayable check that its gluings are exactly an enumerated list (stored here for 451 pairs; for 3 sample pairs only the log row exists), and on every stored gluing the exact integer determinant of M = 11I + 10J - A - A^2 is not a perfect square. The per-pair number of window gluings agrees with `../recheck/out/orbits_per_pair.tsv` on all 454 pairs (2,392 in total). The ledger script below ends with `remaining 454 0`.

This is a recount of the pairs already reported positive. It says nothing about the other 6,313,084 of the 6,313,538 pairs (see Limits).

## Evidence by group

| pairs | source | what is stored here | what was rechecked on 2026-11-24 |
|---:|---|---|---|
| 314 | `ledgers/results_pos.tsv` (historical run, 2026-11-20) | one row per pair: `UNSAT VERIFIED`, solution and window counts; all 5,279 labelled gluings in `ledgers/sols_pos/` | every stored gluing re-read and checked (below); 1,670 window gluings, each pair equal to the expected count |
| 3 | `ledgers/cmp_result.tsv` (historical sample, 40 rows: 20 pairs with window solutions, of which 17 overlap the 314, and 20 pairs without window solutions, which are not among the 454) | log rows only: `UNSAT VERIFIED`, 36 labelled gluings, 8 window | row consistency only; no solutions stored |
| 137 | `certs/*.json` (new, 2026-11-21 to 2026-11-24) | full certificate per pair; 8 proofs in `certs/*.drat.gz` | ledger check of all 137; DRAT recheck (below) |

**314 historical pairs.** The historical run used the same encoder `enc.py`: it enumerated all gluings of the pair, added one blocking clause per gluing, solved the blocked CNF with CaDiCaL and checked the UNSAT proof with drat-trim. All 314 rows say `UNSAT VERIFIED`. The proofs were deleted after checking and the proof hash column is `-` in all 314 rows, so the original DRAT proofs are not archived and cannot be rechecked. What was rechecked here is the stored solution list: for each of the 5,279 graphs, the K and B parts equal the input catalogues, every vertex has degree 10, there is no K4 and no independent 5-set, the exact integer determinant is not a square, and the window count (exact, see below) equals the row and the expected count. That the list is complete rests on the historical log. Each pair can be re-proved with `replay.py`; this was not run.

**3 sample-only pairs** (`K68_e28_100000[3487]`, `K68_e28_80000[3617]`, `K94_e28_68000[3647]`). Evidence is the historical log row only (`UNSAT VERIFIED`, with window counts 2, 2 and 4 matching the expected counts). Their gluings were not stored, so nothing beyond the row was rechecked.

**137 new pairs.** Each `certs/<job>_<idx>.json` holds the K and B graph6 strings, the complete list of labelled gluings (2,697 in total) each with its exact integer determinant, the SHA-256 of the blocked CNF, the SHA-256 and size of the DRAT proof, and `drat_result: VERIFIED`. They were produced by `replay.py` (enumeration with PySAT's CaDiCaL 1.9.5, then CaDiCaL on the blocked CNF and drat-trim), followed by a second, separate check (`verify_proof.py`) that rebuilds the blocked CNF from the stored gluings, compares its SHA-256, and checks a DRAT proof with drat-trim again and compares the exact window count with the expected count. For 135 certificates (made by the batch driver) the output of that second check is stored in the JSON under `verified_repeat`; the first two (`K277_e26_20000[1487]`, `K278_e26_20000[1800]`) were checked the same way by hand and have no such field. The producing runs kept a compressed proof only within a per-file cap of 3 MB and a folder budget of 16 MB: 8 of 137 were kept, all under 3 MB, all included here. For the other 129 only the SHA-256 is stored; `verify_proof.py` regenerates the proof with CaDiCaL. Window gluings in the new pairs: 714.

**Exact window test.** A is 10-regular, so M has eigenvalue 121 on the all-ones vector and 11 - l - l^2 on each other eigenvector of A with eigenvalue l. All non-trivial eigenvalues of A lie in the window exactly when M is positive semidefinite. The determinants here are all non-zero, so the scripts test positive definiteness with Sylvester's criterion using fraction-free integer elimination. No floating point is used.

## Rerun

Requirements: Python 3 (tested with 3.13.5) (standard library only for the ledger and for `verify_proof.py` on the 8 archived proofs), CaDiCaL for the 129 regenerated proofs, drat-trim. `replay.py` (regenerating a certificate from scratch) also needs `python-sat`.

From `r55-srg45/audit454/`:

```
python3 -B audit_ledger.py --data ../data --pending
python3 -B verify_proof.py ../data certs/K277_e26_20000_1487.json --drat-trim /path/to/drat-trim
python3 -B verify_proof.py ../data certs/K278_e26_20000_1800.json --drat-trim /path/to/drat-trim
```

Output on 2026-11-24 (macOS arm64, Python 3.13.5, CaDiCaL 3.0.1 from Homebrew, drat-trim). The ledger, 4.8 s (the line listing the 137 new keys is omitted):

```
source positive, batch, sample positive, overlap, unique 454 314 20 17 317
archived unique labelled completions, window sum 5315 1678
sample-only pairs [('K68_e28_100000', 3487), ('K68_e28_80000', 3617), ('K94_e28_68000', 3647)]
archived graphs checked by exact determinant and pair validation, exact window positives 5279 1670
positive pairs with historical verified log or new proof, remaining 454 0
```

The two certificates (9.9 s and 2.0 s):

```
K277_e26_20000 1487 3 valid exact arithmetic witnesses, 1 window, fixed-CNF DRAT verified, regenerated 27cc03e0d0c0e08ec9926b7ec8193db8d68a27209c2a51a166dbc89cb678b482
K278_e26_20000 1800 2 valid exact arithmetic witnesses, 1 window, fixed-CNF DRAT verified, archived 0cf996da49e5df10382726967b2c634dafd3a11e506d39fe6766c2d3e543cfc7
```

All 137 certificates are rechecked by `verify_all.sh`, which runs `verify_proof.py` with `--expected-window` and compares each proof hash with the recorded one. Its output is `verify_all_2026-11-24.log`; the last line gives the totals.

`verify_proof.py` itself checks that an archived proof matches the recorded SHA-256 but does not compare a regenerated proof; `verify_all.sh` does, and marks each line `hash same` or `hash differs`. A regenerated proof can differ in bytes from the recorded one (different CaDiCaL version or platform; according to the working notes some certificates were first made under WSL, which is not logged here). The DRAT check is always on the same CNF (its SHA-256 is compared), so the recount does not depend on byte-identical proofs.

`audit_ledger.py` without `--data` skips the re-read of the 5,279 historical gluings and the comparison of the K and B strings in each certificate with `../data`.

## Files

- `enc.py`: the encoder. Its header (in Korean) says it was written from the definitions in the manuscript, without reading `../src/glue_srg.c` or the second engine (the header calls it `indep/eng.c`, published here as `../second_engine/eng.c`). Variables: the 110 K-B pairs and 55 B-B pairs (the latter fixed by unit clauses to B). Constraints: no K4 on all 4-subsets of the 22 vertices, no independent 5-set on all 5-subsets, every degree exactly 10 (sequential counter). It does not use the cone lemma of the original engine.
- `replay.py`: enumerates and certifies one pair; also provides the graph6 decoding and exact determinant used by the other scripts.
- `audit_ledger.py`: joins the expected counts, the two historical ledgers and the certificates; with `--data` validates every stored gluing.
- `verify_proof.py`: rebuilds the blocked CNF of one certificate and checks a DRAT proof.
- `ledgers/results_pos.tsv`, `ledgers/cmp_result.tsv`, `ledgers/sols_pos/` (314 files): historical logs and stored gluings.
- `certs/`: 137 JSON certificates and 8 `.drat.gz` proofs (largest 2,790,759 bytes). Every proof kept by the producing runs is included; the other 129 were never kept (3 MB cap, see above).
- `verify_all.sh`, `verify_all_2026-11-24.log`: recheck of all 137 certificates. Last line: 137 passed, 0 failed, proof hash equal to the recorded one for 133; the 4 that differ are listed with `hash differs` (all four are regenerated proofs of certificates first made on another machine).
- The K and B graph6 strings in `certs/` and `ledgers/` are taken from `../data`, which is derived from B. D. McKay's Ramsey graph data (see `../README.md`).

Changes from the working copies (logic unchanged; `enc.py` and all data files are byte-identical copies):

- `audit_ledger.py`: removed the positional `repo` argument; the expected counts are read from `../recheck/out/orbits_per_pair.tsv` (byte-identical to the file used before), the historical ledgers and gluings from `ledgers/`, and the default certificate folder is `certs/`.
- `verify_proof.py`: removed the positional `repo` argument and the `sys.path` line pointing to the encoder's old folder; `enc.py` is imported from this folder.
- `replay.py`: same two changes; default `--out` is `certs/`.

The batch driver that called `replay.py` and `verify_proof.py` in sequence with time limits and wrote `verified_repeat` is not included; `audit_ledger.py` and `verify_proof.py` repeat its checks from the stored files.

## Limits

- Only the 454 pairs that the original computation reported positive are checked. Whether any of the other 6,313,084 filtered pairs has a window gluing that the original engine missed is not checked here. The second engine covered 40,453 pairs (0.64 %); see `../second_engine/` and `../recheck/`.
- The K and B catalogues, the job lists and the filters that produced them (`../data`, `../pipeline/01` to `03`, which use a floating-point interlacing test) are shared with the original run. They are inputs here, not rechecked.
- The recount trusts `enc.py` to encode the gluing problem correctly, and drat-trim, which is not a formally verified checker. No LRAT or verified-checker run was made.
- For the 314 historical pairs and the 3 sample pairs the completeness of the gluing lists rests on logs from 2026-11-20; their proofs were not archived.
- The encoder and these scripts were written by the same author with the help of an AI assistant, as were the search engines. Their independence from the engines rests on how they were written; it has not been checked by anyone else.
