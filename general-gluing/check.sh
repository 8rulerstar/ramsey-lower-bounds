#!/bin/sh
# Checks for R(8,18) >= 1133 (a few minutes on 10 cores).
set -e
cc -O3 -o verify verify.c && cc -O3 -o vpar vpar.c
python3 verify_colourings.py | tail -1
python3 gluegen.py spec_R8_18.json regen.txt && cmp regen.txt R8_18_1132.txt && echo "R8_18_1132 rebuilt: identical" && rm regen.txt
./verify 7 7 H204.txt
./verify 7 6 G114.txt
./verify 6 6 P101.txt
pids=""; for b in "0 113" "113 226" "226 339" "339 452" "452 565" "565 678" "678 791" "791 904" "904 1017" "1017 1132"; do set -- $b; ./vpar 8 R8_18_1132.txt 0 $1 $2 & pids="$pids $!"; done
for p in $pids; do wait $p || { echo "FAILED (process $p)"; exit 1; }; done
python3 certifyDgen.py spec_R8_18.json R8_18_1132.txt 7 7 6 H204.txt H204.txt G114.txt
