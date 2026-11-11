#!/bin/sh
# Rebuild the 3-colouring of K_292 and check it: colours 1 and 2 have no triangle, colour 3 has no K16.
# Needs a C compiler and python3. About 25 minutes on one core (the K16 check).
set -e
cd "$(dirname "$0")"
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA=sha256sum; fi
$SHA -c SHA256SUMS
cc -O3 -o verify verify.c
cc -O3 -o vpar vpar.c
./verify 3 15 R3_15_73_input.txt                          # input: no triangle, no independent 15-set
python3 build.py R3_15_73_input.txt
cmp colouring.txt R3_3_16_292.txt || { echo "FAIL: rebuilt colouring differs"; exit 1; }
echo "rebuilt colouring matches R3_3_16_292.txt"
./vpar 3 c1.txt 0 0 292                                   # colour 1: no triangle
./vpar 3 c2.txt 0 0 292                                   # colour 2: no triangle
./vpar 16 c3.txt 0 0 292                                  # colour 3: no K16 (about 20 minutes)
