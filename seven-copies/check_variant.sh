#!/bin/sh
# Checks for R(7,16) >= 708 (about 1 to 3 hours on 8 cores, most of it in step 4).
set -e
cc -O3 -o vpar vpar.c
python3 build.py 101 regen.txt && cmp regen.txt R7_16_707_variant.txt && echo "graph rebuilt from P(101): identical"
python3 tables.py | tail -1
# 3. no K_7: all roots
./vpar 7 R7_16_707_variant.txt 0 0 707
# 4. no independent 16-set. The map (j,c) -> (j+1 mod 101, c) is an automorphism (vertex 7j+c), so every
#    independent set can be moved to one whose smallest vertex lies in fibre 0: roots 0..6 cover all cases.
pids=""; for r in 0 1 2 3 4 5 6; do ./vpar 16 R7_16_707_variant.txt 1 $r $((r+1)) & pids="$pids $!"; done; for p in $pids; do wait $p || { echo "FAILED (process $p)"; exit 1; }; done
