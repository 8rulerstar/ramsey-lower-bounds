"""Step 3. Job list. A job = (root class K, consecutive block of at most 4000 lines of the B list with e(B) = 10 + e(K)).
Lemma L7 (mod 3): every window local graph has a vertex w with e(N(w)) in {15,16,18,19} (all e(N(w)) lie in 15..20 and
sum e(N(w)) = 3t; if all were 17 or 20 the sum would be 2 mod 3). The search does not restrict the root, so classes with
e(K) in {17, 20} are not needed. e(K) = 15 jobs are listed separately (data/jobs_e15.txt, run on a local machine).
Output: compared with data/jobs.txt (e(K) = 16, 18, 19; 1,555 jobs) and data/jobs_e15.txt (68 jobs)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); from common import *
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data'); CH = 4000
ks = [int(x) for x in open(os.path.join(D, 'quotient_pass.txt')).read().split()]
eK = {k: int(g6dec(open(os.path.join(D, 'K', f'K_{k}.g6')).read()).sum() // 2) for k in ks}
nB = {e: sum(1 for l in open(os.path.join(D, 'B', f'Bq_e{e}.g6')) if l.strip()) for e in range(25, 31)}
jobs = []; j15 = []
for k in ks:
    if eK[k] in (17, 20): continue
    e = eK[k] + 10
    for st in range(0, nB[e], CH):
        (j15 if eK[k] == 15 else jobs).append(f'K{k}_e{e}_{st} {k} B/Bq_e{e}.g6 {st} {min(CH, nB[e] - st)}')
ref = [l.strip() for l in open(os.path.join(D, 'jobs.txt')) if l.strip()]
print(f'e(K) distribution {sorted(__import__("collections").Counter(eK.values()).items())}')
print(f'jobs (e(K)=16,18,19): {len(jobs)}, equal to data/jobs.txt: {jobs == ref}; e(K)=15 jobs: {len(j15)}')
ref15 = [l.strip() for l in open(os.path.join(D, 'jobs_e15.txt')) if l.strip()]
print(f'e(K)=15 jobs equal to data/jobs_e15.txt: {j15 == ref15}')
