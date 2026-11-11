#!/bin/sh
# Check the 444-vertex graph for K5 and, if r55_42some.g6 is present, rebuild it and check the hypotheses of the
# construction (G384 is a (5,17)-graph, H42 a (5,5)-graph). Needs a C compiler and python3. About 3 minutes.
# The independent-set side of the 444-vertex graph is not checked directly (see README).
set -e
cd "$(dirname "$0")"
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA=sha256sum; fi
$SHA -c SHA256SUMS
cc -O3 -o verify verify.c
cc -O3 -o vpar vpar.c
./vpar 5 R5_21_444.txt 0 0 444                           # no K5 (all roots)
if [ -f r55_42some.g6 ]; then
  python3 build.py r55_42some.g6 rebuilt.txt
  cmp rebuilt.txt R5_21_444.txt || { echo "FAIL: rebuilt graph differs"; exit 1; }
  echo "rebuilt graph matches R5_21_444.txt"
  ./vpar 5 G384.txt 0 0 384                              # G384: no K5
  ./vpar 17 G384.txt 1 0 384                             # G384: no independent 17-set (about 1.5 minutes)
  ./verify 5 5 H42.txt                                   # H42: no K5, no independent 5-set
else
  echo "r55_42some.g6 not found: skipping the rebuild and the hypothesis checks (see README)"
fi
