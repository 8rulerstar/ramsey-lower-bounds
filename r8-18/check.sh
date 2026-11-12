#!/bin/sh
# Checks for R(8,18) >= 1054 (a few minutes on 8 cores).
set -e
cc -O3 -o verify verify.c && cc -O3 -o vpar vpar.c
python3 check_structure.py
./verify 8 6 C133.txt                 # C133 is an (8,6)-graph
./verify 8 7 H204.txt                 # no K_8, no independent 7-set in H204 (alpha(H204) <= 6)
pids=""; for i in 0 1 2 3 4 5 6 7 8 9; do ./vpar 8 R8_18_1053.txt 0 $((i*106)) $(( i==9 ? 1053 : (i+1)*106 )) & pids="$pids $!"; done; for p in $pids; do wait $p || { echo "FAILED (process $p)"; exit 1; }; done
