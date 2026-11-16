#!/bin/zsh
# (24,24) full first pass with pair3 (sharded) then pair2 probing on opens. 4 parallel. Stop: pkill -f p3_pair3; pkill -f p2_pair2
cd ${0:A:h}/..
jobs=()
for c in 8 9 12; do jobs+=("$c 0 1"); done
for k in 0 1 2 3 4 5 6 7; do jobs+=("10 $k 8"); done
for k in $(seq 0 23); do jobs+=("11 $k 24"); done
printf '%s\n' "${jobs[@]}" | xargs -P 4 -L 1 zsh -c './p3_pair3 run aut.txt $0 full/open_c$0_s$1.txt $1 $2 > full/log_c$0_s$1.txt 2>&1'
cat full/open_c*_s*.txt > full/open_all.txt
./p2_pair2 probe full/open_all.txt full/resid_all.txt > full/probe.log 2>&1
echo done; wc -l full/open_all.txt full/resid_all.txt
