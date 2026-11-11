#!/bin/sh
# Check the 1238-vertex graph for K8 and, if g78.218 is present, rebuild it and check the hypotheses of the construction.
# Needs a C compiler and python3. About 2 minutes. The independent-set side is not checked directly (see README).
set -e
cd "$(dirname "$0")"
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA=sha256sum; fi
$SHA -c SHA256SUMS
cc -O3 -o verify verify.c
cc -O3 -o vpar vpar.c
./vpar 8 R8_19_1238.txt 0 0 1238                         # no K8 (all roots)
if [ -f g78.218 ]; then
  python3 build.py g78.218 rebuilt.txt
  cmp rebuilt.txt R8_19_1238.txt || { echo "FAIL: rebuilt graph differs"; exit 1; }
  echo "rebuilt graph matches R8_19_1238.txt (build.py also asserts the two induced copies of H204)"
  awk 'NF' g78.218 | { n=$(awk 'NF' g78.218 | wc -l | tr -d " "); echo $n; cat; } > g218.txt
  ./verify 8 7 g218.txt                                  # the 218-vertex part: no K8, no independent 7-set
else
  echo "g78.218 not found: skipping the rebuild and the hypothesis checks (see README)"
fi
