#!/bin/bash
# Run before tagging a release: no placeholders, results present, CITATION version and date shown for a manual check.
cd "$(dirname "$0")/.."
fail=0
git rev-parse --git-dir > /dev/null 2>&1 || { echo "STOP: not a git repository"; exit 1; }
if git grep -nE '[A-Z]+_PENDING' -- . ':!r55-srg45/release_check.sh'; then echo "STOP: placeholders remain"; fail=1; fi
for f in ledger.txt jobs_summary.tsv window_solutions.tsv window_check.txt SHA256SUMS; do
  [ -s "r55-srg45/results/$f" ] || { echo "STOP: missing r55-srg45/results/$f"; fail=1; }
done
echo "CITATION: $(grep -E '^(version|date-released)' CITATION.cff | tr '\n' ' ') (must match the tag and the release date)"
exit $fail
