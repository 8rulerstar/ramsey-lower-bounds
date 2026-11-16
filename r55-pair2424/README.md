# The (24,24) extremal-pair lemma for (5,5,45)-graphs

**This is not a bound.** 43 <= R(5,5) <= 46 is unchanged. The lemma restricts how two vertices of a hypothetical
(5,5,45)-colouring with large, edge-rich neighbourhoods can sit next to each other. The proof is computer-assisted:
the exhaustive computation is complete, but the written covering argument (that the placements cover all cases) and
DRAT certificates are still missing, and it has not been read by an expert. See "Limitations".

## Statement

A (5,5,n)-colouring is a red/blue colouring of the edges of K_n with no monochromatic K5. An (s,t,m)-graph is a graph
on m vertices with no K_s and no independent t-set.

**Lemma.** In a (5,5,45)-colouring there are no two vertices u, v joined by a red edge such that deg_R(u) = deg_R(v) = 24
and both red neighbourhoods N_R(u), N_R(v) induce graphs with at least 127 edges.

Equivalently, the vertices of red degree 24 whose red neighbourhood has at least 127 red edges form an independent set
in the red graph (and the same holds for blue).

Why 127: a (4,5,24)-graph has at most 132 edges; 127 is the threshold (deficit <= 5 from the maximum) at which the
list of such graphs is small (4,428 graphs) and the pair check is cheap. Lemmas of this kind feed the deficit-identity
approach of Angeltveit and McKay to R(5,5) <= 46; on their own they do not exclude 45-vertex colourings.

## Definitions and setup

- N_R(u) has no K4 (with u it would give a red K5) and no independent 5-set (a blue K5), so it is a (4,5,24)-graph.
- `d24_e127.g6`: the 4,428 (4,5,24)-graphs with at least 127 edges, selected from McKay's complete list of
  (4,5,24)-graphs (352,366 graphs).
- Since u, v are red neighbours, v is a vertex of X = N_R(u) and u is a vertex of Y = N_R(v). The common red
  neighbourhood C = N_R(u) ∩ N_R(v) is N_X(v) and also N_Y(u), so G[C] is the same graph K seen from both sides;
  c = |C| = deg_X(v). Only c = 8, ..., 12 occurs in the list.

## Placements and how they are counted

A placement is (isomorphism class of X, orbit of v in Aut(X), class of Y, orbit of u in Aut(Y), an isomorphism
between the two copies of K on C). Placements that give the same partial colouring are identified via double cosets
H_v \ Aut(K) / H_u (H_v the image in Aut(K) of the stabiliser of v in Aut(X), H_u likewise for u in Aut(Y)), and the swap of u and v is handled by Burnside
(unordered = (ordered + self-inverse diagonal double cosets) / 2). Aut groups are enumerated in full with networkx VF2
(`count_exact.py`; the same data are exported for the C tools by `ctool/export.py` to `ctool/aut.txt`).

| c | K classes | pointed (X, v) | ordered pairs | ordered placements | unordered placements |
|---|---|---|---|---|---|
| 8 | 11 | 44 | 436 | 11,382 | 5,928 |
| 9 | 57 | 3,197 | 1,882,493 | 9,169,195 | 4,591,890 |
| 10 | 109 | 33,500 | 151,978,154 | 347,321,420 | 173,715,603 |
| 11 | 61 | 59,694 | 848,373,770 | 9,311,338,655 | 4,655,830,437 |
| 12 | 8 | 1,234 | 367,366 | 3,615,905 | 1,812,874 |
| total | | | | | **4,835,956,732** |

Source: `cnt/count_exact.json`, `cnt/count_exact.log`.

Each placement fixes the colours of all edges inside {u, v} ∪ N_R(u) ∪ N_R(v) that are determined by X, Y and the
identification on C, on 45 vertices in total; all other edges are free. The question is whether the free edges can be
coloured with no monochromatic K5.

## Decision in three stages

| stage | tool | input | UNSAT | left | CPU time |
|---|---|---|---|---|---|
| 1. bitset propagation (designed to equal unit propagation of the K5 clauses; checked against the earlier engine and CaDiCaL, see Verification) | `ctool/pair3.cpp` | 4,835,956,732 | 4,830,176,240 | 5,780,492 | 5,214 s |
| 2. failed-literal probing (assign an open edge red, propagate; on conflict fix it blue; both conflict = UNSAT; repeat) | `ctool/pair2.cpp probe` | 5,780,492 | 5,779,531 | 961 | 2,449 s |
| 3. CaDiCaL 3.0.1, 300 s limit | `ctool/full/resid_cad.py` | 961 | 961 | 0 | 91.8 s (max 0.19 s) |

Open counts after stage 1 by c: 596 / 27,867 / 3,154,885 / 2,533,451 / 63,693 (c = 8..12). No placement is
satisfiable, so the lemma holds subject to the covering argument below. Sources: `ctool/full/log_*.txt`,
`ctool/full/probe.log`, `ctool/full/resid_cad_{0,1,2}.txt`, `ctool/full/RESULT.md` (Korean summary).
Machine: Apple M4 Pro, about 2.1 CPU hours in total.

## Verification

- **Counts.** The C enumerator reproduces, for each c, the unordered counts of the independent Python count
  (`count_exact.py`); stage 1 logs report n per shard summing to 4,835,956,732, `CCmismatch=0` (the two copies of K
  agree on every C-C edge).
- **pair3 vs pair.** The open set of the optimised `pair3` equals line by line that of the first implementation
  `pair.cpp` for c = 8, 9, 12 in full and for the first 2,000,000 placements of c = 10, 11 (the c = 8 file is
  `ctool/open_c8.txt`; larger lists are not included).
- **CaDiCaL cross-checks.** 200 probe-UNSAT placements re-solved by CaDiCaL: 200 UNSAT (`ctool/p2_val200.txt`);
  50 c = 12 probe residuals: 50 UNSAT (`ctool/p2_resid50.txt`). 500 instances of an earlier incremental-SAT
  experiment, replayed (`ctool/replay_incr.py`, `ctool/incr500.txt`): bitset check and a CaDiCaL frame give the same
  verdicts (499 conflict, 1 open; `ctool/cad.txt` = `ctool/chk.txt`). The earlier experiment itself is not included.
- **Positive controls.** 100 partial assignments taken from a (5,5,41)-colouring (`data/found_R5_5_n41.txt`,
  `ctool/ctl.py`): 0 conflicts (`ctool/ctl.txt`; rerun for this release: 100 OPEN). 8 placements built from
  (5,5,42)-colourings (`data/r55_42some.g6`) were solved SAT by the second engine and the models checked
  (`indep/pos.out`, `indep/sat_pos*.txt`).
- **Second engine** (`indep/`), written without looking at the first engine's code, derives the placement layout
  itself (u, v, C of size c, two private parts of size 23 - c, outside part of size c - 3; total 45). Random
  placements, 10,000 per c in each of two runs (100,000 in total): all UNSAT, 0 SAT, max 0.285 s
  (`indep/main1.out`, `indep/main2.out`; result counts UP / PROBE / CAD_UNSAT = 48,039 / 1,949 / 12 and
  48,034 / 1,955 / 11). Also: 3,000 small instances with brute-force truth, all agree (`indep/brute_truth.txt`,
  `indep/brute.out`); 200 full CNFs solved by CaDiCaL without propagation, all UNSAT (`indep/xnoprop.out`).

## Limitations

- **Partial cross-check of the fast path.** For c = 10 and c = 11 the fast table path of `pair3` was compared line by line with the slower `pair.cpp` only on the first 2,000,000 placements (a later spot check of three further shards also agreed); c = 8, 9, 12 were compared in full.
- **No DRAT certificates.** Stage 1 and 2 conflicts are decided by my own C code; the 961 CaDiCaL runs did not
  store proofs. Planned: short RUP proofs per placement checked with drat-trim, or at least a large random sample
  checked with CaDiCaL + drat-trim.
- **Covering argument not yet written up.** That every counterexample appears as one of the placements (in particular
  the double-coset reduction and the Burnside treatment of the u, v swap) is argued in our notes but not yet written
  as a proof and not independently checked.
- **The second engine is sampled, not exhaustive.** Placements are random (many repeats for c = 8), and the
  isomorphism on C is chosen among at most 20,000 enumerated ones. The seeds of `main1.out` and `main2.out` were
  not recorded (they are not 1 and 2).
- **Authorship.** Both engines, the scripts and parts of this text were written with the help of an AI assistant
  (Claude, Anthropic). The two engines are independent implementations, but not independent in authorship.
  The author checked the mathematical statements; all computational claims can be rechecked from this folder.

## Reproduce

Requirements: clang++ (C++17), CaDiCaL (library and `cadical` binary on PATH; the run used CaDiCaL 3.0.1 from
Homebrew), Python 3 with networkx. Run commands from the folder indicated.

```bash
# counts (about 2 minutes, 1 core)
python3 count_exact.py                         # writes cnt/count_exact.json and .log

cd ctool
python3 export.py                              # rebuilds aut.txt (about 2 minutes); compare with the sha256 below
clang++ -O2 -std=c++17 -march=native pair3.cpp -o p3_pair3
clang++ -O2 -std=c++17 -march=native -I/opt/homebrew/include pair2.cpp -L/opt/homebrew/lib -lcadical -o p2_pair2
clang++ -O2 -std=c++17 -march=native -I/opt/homebrew/include pair.cpp  -L/opt/homebrew/lib -lcadical -o pair

# quick test (under a second): c = 8 gives 596 open, all refuted by probing
./p3_pair3 run aut.txt 8 open_c8_new.txt       # log line: n=5928 conflict=5332 open=596
cmp open_c8_new.txt open_c8.txt
./p2_pair2 probe open_c8_new.txt resid_c8.txt  # probe n=596 unsat=596 residual=0

# full run (4 parallel jobs; about 5,200 s + 2,450 s CPU). Writes full/open_all.txt (about 11 GB) and full/resid_all.txt
zsh full/run_full.sh
python3 full/resid_cad.py 0 1                  # CaDiCaL on all residuals -> full/resid_cad_0.txt (about 92 s of total solver time; the recorded run used 3 shards: 0 3, 1 3, 2 3)

# positive control
python3 ctl.py && NV=41 ./p3_pair3 check ctl.txt   # 100 lines, all OPEN

cd ../indep
clang++ -O2 -std=c++17 eng.cpp -o eng
python3 gen.py main SEED 10000 | ./eng > mainX.out  # one run: 50,000 random placements (c = 8..12); two runs give the 100,000.
# SEED is any integer (random seed for the sampler).
python3 gen.py pos 8 | ./eng > pos.out          # original invocations of gen.py were not recorded; reconstructed
```

`resid_cad.py k K` processes residual lines i with i mod K = k (the release run used K = 3). `p2_val.py` and
`p2_resid.py` need the c = 9..12 open lists from a full run and are included for reference.

Changes made to the copied scripts for this release (paths only, no logic): `count_exact.py`, `ctool/export.py`,
`ctool/replay_incr.py` resolve the data folder relative to the script instead of an absolute path; `ctool/ctl.py`
reads `../data/found_R5_5_n41.txt`; `indep/gen.py` reads `../d24_e127.g6` and `../data/r55_42some.g6`;
`indep/eng.cpp` calls `cadical` from PATH instead of `/opt/homebrew/bin/cadical`.

## Files

- `d24_e127.g6` (4,428 graphs), `count_exact.py`, `cnt/`: list and exact placement count.
- `enc.py`: CNF encoder of an earlier SAT-based prototype (kept for reference, not used by the run above).
- `ctool/`: `pair.cpp` (first implementation), `pair2.cpp` (probing, DIMACS export, model check), `pair3.cpp`
  (optimised stage 1), `export.py` + `aut.txt`, cross-check scripts and outputs, `full/` (logs and results of the run).
- `indep/`: second engine `eng.cpp`, generator `gen.py`, outputs.
- `data/`: `found_R5_5_n41.txt` (a (5,5,41)-colouring as a 0/1 matrix: the circulant graph on Z_41 with connection set {1,2,3,5,7,10,13,15,16,17,24,25,26,28,31,34,36,38,39,40}; clique and independence numbers 4, checked with networkx; anyone can regenerate it from this set), `r55_42some.g6` (328 (5,5,42)-graphs,
  a selection from McKay's lists).

Not included (too large): `ctool/full/open_*.txt` and `open_all.txt` (about 11 GB; regenerate with `full/run_full.sh`).

SHA-256 of data inputs and key outputs:

```
de6d32166cc8f66651e42772f546cfd278d7db00756e804c417ec95c1e329055  d24_e127.g6
d6c5d3f6bbe00e92de03aae587163a8549a8a001ec16231b257e7482f68d9088  ctool/aut.txt
067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb  data/r55_42some.g6
1bd46610676844b799a63223140c654c86e26ba4eae6c8fe7aa66d86b88759f0  data/found_R5_5_n41.txt
3a03daad7d86b10f512123d7577c6efbdae9bcba1152f85a6ab071d691457d1c  ctool/open_c8.txt
3edd588581b4515a815ee1ed5aa43fe859efe706ce36e7def2d2d5fdcafe4d95  ctool/full/resid_all.txt
c5a1904993aebde73dee535709ebd353d166a91bfdc9c514608a6b04fede2aee  ctool/incr500.txt
d6ebf6a4730af2af8b2500f65938799293742c7b45255a1aaaa3531a4ef5c598  ctool/ctl.txt
```

## Data sources and licence

`d24_e127.g6` and `data/r55_42some.g6` are selections from the Ramsey graph lists of Brendan D. McKay
(https://users.cecs.anu.edu.au/~bdm/data/ramsey.html); see that page for the terms of use and cite it when you use
these files. Everything else in this folder is covered by the licence of this repository.
