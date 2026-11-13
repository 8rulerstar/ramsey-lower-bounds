#!/bin/bash
# Collects the raw outputs of the run, checks the ledger, tests every window solution, and writes results/.
# Usage: bash finalize.sh RAW_DIR E15_TGZ [RAW_ARCHIVE_OUT]
#   RAW_DIR: folder with one <job>.txt per job of data/jobs.txt; E15_TGZ: archive with out/<job>.txt for data/jobs_e15.txt.
#   RAW_ARCHIVE_OUT (optional): where to write the tar.gz of all raw outputs (kept outside the repository).
set -e
RAW=$(realpath "$1"); E15=$(realpath "$2"); ARC=${3:+$(realpath -m "$3")}; PY=${PY:-python3}
cd "$(dirname "$0")"
rm -rf staging && mkdir -p staging/raw results && rm -f results/SHA256SUMS
cp "$RAW"/*.txt staging/raw/
tar xzf "$E15" -C staging out && cp staging/out/*.txt staging/raw/ && rm -rf staging/out
echo "== ledger"; $PY pipeline/06_completeness.py staging/raw --summary results/jobs_summary.tsv > results/ledger.txt || { cat results/ledger.txt; echo "LEDGER PROBLEMS: stop"; exit 1; }
cat results/ledger.txt
echo "== windows"; $PY pipeline/05_check_windows.py staging/raw > results/window_solutions.tsv 2> results/window_check.txt || { cat results/window_check.txt; echo "WINDOW CHECK PROBLEMS: stop"; exit 1; }
cat results/window_check.txt
if [ -n "$ARC" ]; then tar czf "$ARC" -C staging raw; sha256sum "$ARC" | sed "s#  .*/#  #" > results/raw_archive.sha256; fi
(cd data && find . -type f ! -name SHA256SUMS | sort | xargs sha256sum > SHA256SUMS)
$PY pipeline/07_reroot_check.py > results/reroot_check.txt || { cat results/reroot_check.txt; echo "CLOSURE CHECK PROBLEMS: stop"; exit 1; }
(cd results && sha256sum jobs_summary.tsv window_solutions.tsv ledger.txt window_check.txt reroot_check.txt $(ls raw_archive.sha256 crosscheck/*.txt 2>/dev/null) > SHA256SUMS)
(cd src && sha256sum *.c > SHA256SUMS)
rm -rf staging; echo "done"
