#!/bin/sh
# Checks for R(8,25) >= 2449 (a few minutes on 10 cores).
set -e
cc -O3 -o verify verify.c && cc -O3 -o vpar2560 vpar2560.c
python3 prove12.py
python3 glue12.py H204.txt regen.txt && cmp regen.txt R8_25_2448.txt && echo "R8_25_2448 rebuilt: identical" && rm regen.txt
./verify 7 7 H204.txt
pids=""; for b in "0 40" "40 80" "80 120" "120 170" "170 230" "230 300" "300 400" "400 550" "550 850" "850 2448"; do set -- $b; ./vpar2560 8 R8_25_2448.txt 0 $1 $2 & pids="$pids $!"; done
for p in $pids; do wait $p || { echo "FAILED (process $p)"; exit 1; }; done
python3 certifyD12.py H204.txt R8_25_2448.txt
