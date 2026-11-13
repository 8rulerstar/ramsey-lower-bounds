#!/bin/bash
# Step 4. Run one job with the engine exactly as in the original run: gcc -O2 -march=native, environment NOPROP=1.
# Usage: pipeline/04_run_job.sh JOB_ID [jobs-file]   (jobs-file default data/jobs.txt; e(K)=15 jobs are in data/jobs_e15.txt)
# Output: out/JOB_ID.txt with lines "R idx nsol nwin nodes usec" per B graph and "S idx win cones..." for window solutions,
# ending with "#END". Re-running resumes after the last complete R line.
set -e
cd "$(dirname "$0")/.."
ID=$1; JF=${2:-data/jobs.txt}
[ -x build/glue_srg ] || { mkdir -p build; gcc -O2 -march=native -o build/glue_srg src/glue_srg.c -lm; }
L=$(grep "^$ID " "$JF" | tr -d "\r") || true
[ -n "$L" ] || { echo "job $ID not found in $JF"; exit 2; }
set -- $L; k=$2; bf=$3; st=$4; cnt=$5
mkdir -p out
tail -n +$((st + 1)) "data/$bf" | head -n "$cnt" | OUT=out/$ID.txt NOPROP=1 build/glue_srg data/K/K_$k.g6 0 1 10 10
