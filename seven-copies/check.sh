#!/bin/sh
# Checks for R(7,16) >= 708 and R(8,19) >= 1429 (a few minutes on 8 cores).
set -e
cc -O3 -o verify verify.c && cc -O3 -o vpar vpar.c && cc -O3 -o vpar1536 vpar1536.c
python3 heptaglue.py P101.txt P101.txt P101.txt maps_id101.txt regen707.txt && cmp regen707.txt R7_16_707.txt && echo "R7_16_707 rebuilt: identical"
python3 heptaglue.py H204c.txt H204c.txt H204c.txt maps_id204.txt regen1428.txt && cmp regen1428.txt R8_19_1428.txt && echo "R8_19_1428 rebuilt: identical"
rm -f regen707.txt regen1428.txt
./verify 6 6 P101.txt
./verify 7 7 H204c.txt
./vpar 7 R7_16_707.txt 0 0 707
pids=""; for i in 0 1 2 3 4 5 6 7 8 9; do ./vpar1536 8 R8_19_1428.txt 0 $((i*143)) $(( i==9 ? 1428 : (i+1)*143 )) & pids="$pids $!"; done; for p in $pids; do wait $p || { echo "FAILED (process $p)"; exit 1; }; done
python3 certifyD.py P101.txt P101.txt P101.txt maps_id101.txt R7_16_707.txt
python3 certifyD.py H204c.txt H204c.txt H204c.txt maps_id204.txt R8_19_1428.txt
