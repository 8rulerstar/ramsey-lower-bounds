#!/bin/sh
set -e
cc -O3 -o verify verify.c && cc -O3 -o vpar vpar.c
python3 build_d1.py && cmp regen.txt R8_12_520.txt && echo "rebuilt: identical" && rm regen.txt
./verify 7 7 H204.txt
./verify 7 6 G114.txt
./vpar 8 R8_12_520.txt 0 0 520
python3 certifyD1.py H204.txt G114.txt maps_P101_H204_G114.txt R8_12_520.txt
