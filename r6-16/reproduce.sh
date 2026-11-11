#!/bin/sh
# Rebuild the 453-vertex (6,16)-graph and check it. Needs a C compiler and python3. A few seconds.
set -e
cd "$(dirname "$0")"
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA=sha256sum; fi
$SHA -c SHA256SUMS
cc -O3 -o verify verify.c
cc -O3 -o vpar vpar.c
sh build.sh
cmp rebuilt.txt R6_16_453.txt || { echo "FAIL: rebuilt graph differs"; exit 1; }
echo "rebuilt graph matches R6_16_453.txt"
./verify 6 6 P101.txt                                     # P(101): no K6, no independent 6-set (alpha = 5)
./vpar 6 R6_16_453.txt 0 0 453                            # no K6 (all 453 roots)
python3 certify.py P101.txt P101.txt P101.txt maps101.txt R6_16_453.txt   # alpha <= 5 + 5 + 5 = 15
