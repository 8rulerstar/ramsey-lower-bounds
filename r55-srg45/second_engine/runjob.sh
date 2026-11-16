#!/bin/bash
# Build (as used for the 40,453-pair run): gcc -O2 -march=native -DACL=0 -o eng eng.c -lm. runjob.sh JOBID NPAIRS(0=all) OFFSET : runs indep engine on a job slice, writes out/JOBID[_OFF].txt
D="$(cd "$(dirname "$0")/../data" && pwd)"
cd "$(dirname "$0")"; mkdir -p out
L=$(grep -h "^$1 " $D/jobs.txt $D/jobs_e15.txt); set -- $1 $2 ${3:-0} $L
id=$1; np=$2; off=$3; k=$5; bf=$6; st=$7; cnt=$8
[ "$np" = 0 ] && np=$cnt
o=out/${id}_${off}_${np}.txt; [ -f $o.done ] && exit 0
s=$(date +%s)
tail -n +$((st + off + 1)) $D/$bf | head -n $np | ./eng $D/K/K_$k.g6 > $o && echo "$off $(( $(date +%s)-s ))" > $o.done
