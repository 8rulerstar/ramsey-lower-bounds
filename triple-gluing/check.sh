#!/bin/sh
# Check the four graphs: (1) each of the three glued parts is a (k,s_i)-graph (verify), (2) the whole graph has no
# K_k (vpar, all roots), (3) certify.py: alpha(F) <= alpha(G_1) + alpha(G_2) + alpha(G_3) <= s_1 + s_2 + s_3 - 3.
# Needs a C compiler and python3. About 5 to 15 minutes (the K8 search on 1266 vertices and the last certificate dominate).
set -e
cd "$(dirname "$0")"
if command -v shasum >/dev/null 2>&1; then SHA="shasum -a 256"; else SHA=sha256sum; fi
$SHA -c SHA256SUMS
cc -O3 -o verify verify.c
cc -O3 -o vpar vpar.c
one() { # file k n1 n2 n3 s1 s2 s3 maps
  n=$(head -1 $1); echo "== $1: $n vertices, claim: no K$2, no independent set of size $(($6 + $7 + $8 - 2))"
  python3 blocks.py $1 $3 $4 $5
  ./verify $2 $6 G1.txt; ./verify $2 $7 G2.txt; ./verify $2 $8 G3.txt      # each stops the script (set -e) on failure
  ./vpar $2 $1 0 0 $n
  python3 certify.py G1.txt G2.txt G3.txt $9 $1
}
one R7_17_735.txt  7 114 114 204 6 6 7 maps_P101.txt
one R7_18_825.txt  7 114 204 204 6 7 7 maps_P101.txt
one R7_19_918.txt  7 204 204 204 7 7 7 maps_N102.txt
one R7_20_932.txt  7 204 204 218 7 7 8 maps_N102_R7_20.txt
one R8_19_1266.txt 8 218 218 218 7 7 7 maps_H204_in_G218.txt
