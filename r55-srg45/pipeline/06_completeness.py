"""Step 6. Ledger check: for every job, the result file exists, ends with #END, and its R lines cover idx 0..cnt-1
exactly (duplicate lines from resumed runs must agree). Prints totals; exit code 1 if there are problems.
Usage: python pipeline/06_completeness.py RESULTS_DIR [--present] [--summary FILE]
  --present: check only the jobs whose result file exists (for partial reruns). --summary FILE: write the per-job table."""
import os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
PRESENT = '--present' in sys.argv; SUMMARY = sys.argv[sys.argv.index('--summary') + 1] if '--summary' in sys.argv else None
rdir = [a for a in sys.argv[1:] if not a.startswith('--') and a != SUMMARY][0]; bad = []; rows = []; tot = dict(jobs=0, pairs=0, nsol=0, nwin=0, cpu_s=0.0)
for jf in ('jobs.txt', 'jobs_e15.txt'):
    for l in open(os.path.join(D, jf)):
        if not l.strip(): continue
        jid, k, bf, st, cnt = l.split(); cnt = int(cnt); f = os.path.join(rdir, jid + '.txt')
        if not os.path.exists(f):
            if not PRESENT: bad.append((jid, 'missing'))
            continue
        raw = open(f, 'rb').read(); txt = raw.decode(); seen = {}
        for r in txt.splitlines():
            if r.startswith('R '):
                p = r.split()
                if len(p) < 6: bad.append((jid, 'truncated R line')); continue
                i = int(p[1]); v = tuple(p[2:4])
                if i in seen and seen[i] != v: bad.append((jid, f'conflict idx {i}'))
                seen[i] = v; 
        if '#END' not in txt: bad.append((jid, 'no #END'))
        if set(seen) != set(range(cnt)): bad.append((jid, f'idx {len(seen)}/{cnt}'))
        ns = sum(int(v[0]) for v in seen.values()); nw = sum(int(v[1]) for v in seen.values())
        us = 0.0; done = set()
        for r in txt.splitlines():
            if r.startswith('R '):
                p = r.split()
                if len(p) < 6: continue
                i = int(p[1])
                if i not in done: done.add(i); us += float(p[5])
        rows.append(f'{jid}\t{k}\t{cnt}\t{len(seen)}\t{ns}\t{nw}\t{us / 1e6:.1f}\t{hashlib.sha256(raw).hexdigest()}')
        tot['jobs'] += 1; tot['pairs'] += len(seen); tot['nsol'] += ns; tot['nwin'] += nw; tot['cpu_s'] += us / 1e6
if SUMMARY: open(SUMMARY, 'w', newline='\n').write('job\tK\tpairs_expected\tpairs_found\tsolutions\twindow\tcpu_seconds\tsha256\n' + '\n'.join(rows) + '\n')
print(f"jobs {tot['jobs']}, pairs {tot['pairs']}, solutions {tot['nsol']}, window {tot['nwin']}, cpu hours {tot['cpu_s'] / 3600:.1f}")
if tot['jobs'] == 0: bad.append(('-', 'no result files found in ' + rdir))
print('problems', len(bad), bad[:20])
sys.exit(1 if bad else 0)
