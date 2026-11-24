#!/bin/sh
# Recheck all certificates with verify_proof.py (window count compared with the expected count) and compare each
# proof hash with the recorded drat_sha256. Usage: DRAT_TRIM=/abs/path/to/drat-trim sh verify_all.sh > verify_all.log
cd "$(dirname "$0")"
python3 - "$DRAT_TRIM" <<'PY'
import json, subprocess, sys, time, glob, csv
drat = sys.argv[1]
exp = {}
for row in csv.reader(open('../recheck/out/orbits_per_pair.tsv'), delimiter='\t'):
    if len(row) >= 4 and row[1].isdigit(): exp[(row[0], int(row[1]))] = int(row[3])
ok = same = 0; t0 = time.time(); files = sorted(glob.glob('certs/*.json'))
for f in files:
    r = json.load(open(f))
    p = subprocess.run([sys.executable, '-B', 'verify_proof.py', '../data', f, '--drat-trim', drat, '--expected-window', str(exp[(r['job'], int(r['idx']))])], capture_output=True, text=True)
    line = p.stdout.strip().splitlines()[-1] if p.returncode == 0 and p.stdout.strip() else 'FAIL ' + p.stderr[-300:]
    h = line.split()[-1] if p.returncode == 0 else ''
    ok += p.returncode == 0; same += h == r['drat_sha256']
    print(line, 'hash', 'same' if h == r['drat_sha256'] else 'differs', flush=True)
print(f'certificates {len(files)} passed {ok} failed {len(files)-ok} proof hash equal to recorded {same} seconds {time.time()-t0:.0f}')
PY
