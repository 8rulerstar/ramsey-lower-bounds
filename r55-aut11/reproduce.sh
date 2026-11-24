#!/bin/sh
# Rebuild and recheck everything in this folder. Usage: sh reproduce.sh [workers]
# Needs: cc, python3 with numpy and python-sat, cadical on PATH, drat-trim ($DRAT_TRIM or on PATH), timeout, shasum or sha256sum.
# Writes build/ and full_p11.cnf (8 MB) here; case CNFs and proofs go to $TMPDIR and are deleted after each check (about 22 MB per worker at a time).
# Rerunning skips cases already VERIFIED in build/results.tsv.
set -e
cd "$(dirname "$0")"
W=${1:-4}
mkdir -p build

echo "== 1. Z11-invariant (4,5,22)-graphs on two orbits (stage1.c), compared with L.txt"
cc -O2 -o build/stage1 stage1.c
./build/stage1 > build/L.txt
cmp build/L.txt L.txt && echo "L.txt identical"

echo "== 2. second count of L by SAT enumeration"
python3 -B recount_L.py

echo "== 3. base CNF full_p11.cnf, SHA-256, and the 630 cases with Glucose4 and MiniSat22"
python3 -B recheck.py
if command -v sha256sum >/dev/null 2>&1; then sha256sum full_p11.cnf; else shasum -a 256 full_p11.cnf; fi
echo "expected: eceb0c8e5e56522e1f93c4a4ddde31d95b39342a0ffc5423ff0d6ca94045e8d9"

echo "== 4. stage2: positive control p = 7, and the 630 cases with CaDiCaL (pysat) plus control 1"
(cd build && python3 -B ../stage2.py full 7 && python3 -B ../stage2.py glue ../L.txt | grep -v '^G1 [1-8]/')

echo "== 5. DRAT controls"
python3 -B controls.py

echo "== 6. all 630 cases: cadical -q --no-binary, then drat-trim (results in build/results.tsv)"
(cd build && python3 -B ../drat11.py "$W")
awk -F'\t' 'NR>1{c[$3" "$4]++} END{for(k in c) print k, c[k]}' build/results.tsv
