#!/bin/sh
# Rebuild the 419-vertex (7,12)-graph and check it. Needs a C compiler and python3.
# Quick part: about a minute. Independent-set part: about 30 minutes with 4 jobs (set J for the number of jobs, default 5).
set -e
cd "$(dirname "$0")"
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA=sha256sum; fi
$SHA -c SHA256SUMS
cc -O3 -o verify verify.c
cc -O3 -o vpar vpar.c
cc -O2 -o check3 check3.c
# Rebuild from the input graph, if present (not included here; see README)
if [ -f R6_7_114_input.txt ]; then
  echo "b3458603595b06abbfd34c72b940b87df29018dd0a288a5d75a1511a5f0384fe  R6_7_114_input.txt" | $SHA -c
  python3 build.py R6_7_114_input.txt rebuilt.txt
  cmp rebuilt.txt R7_12_419.txt && echo "rebuilt graph matches R7_12_419.txt"
  ./verify 6 7 R6_7_114_input.txt                         # input: no K6, no independent 7-set
else
  echo "R6_7_114_input.txt not found: skipping the rebuild (see README)"
fi
./vpar 7 R7_12_419.txt 0 0 419                            # no K7 (all roots)
# no independent 12-set: one job per root v (searches the non-neighbours of v above v), all 419 roots
J=${J:-5}
seq 0 418 | xargs -n 1 -P "$J" sh -c './vpar 12 R7_12_419.txt 1 "$0" "$(($0 + 1))"' > ind12.log
grep -c NONE ind12.log | sed 's/^/roots with NONE (expect 419): /'
if grep -q FOUND ind12.log; then echo "FAIL: independent 12-set found"; exit 1; fi
[ "$(grep -c NONE ind12.log)" -eq 419 ] && echo "OK: R(7,12) > 419"
# second checker, separate implementation (slow, about 2 hours on one core): ./check3 7 12 R7_12_419.txt
