#!/usr/bin/env python3
"""DRAT certification of the 630 cases excluding the order-11 automorphism with one fixed point (2026-11-24, macOS).

Case = full_p11.cnf (all K5 clauses, no assumptions) with the 46 assumptions of the case appended as unit clauses.
Solved with command-line CaDiCaL (not pysat), which writes a text DRAT proof, checked by drat-trim.
The case list and assumptions are the definitions R1, R2, assum of recheck.py (the code below is copied from that file).

Usage: python3 drat11.py [workers] [max number of cases]
Output: results.tsv in the current directory (g1 g2 cadical_result drat_trim_result proof_bytes seconds); cases already VERIFIED there
are skipped. CNF and proof are written to TMPDIR and deleted after the check.
Public copy: K is this folder; drat-trim is $DRAT_TRIM or 'drat-trim' on PATH.
"""
import os, sys, time, subprocess, tempfile, importlib.util, hashlib
from concurrent.futures import ProcessPoolExecutor

K = os.path.dirname(os.path.abspath(__file__))
DRAT = os.environ.get('DRAT_TRIM', 'drat-trim')
CNF = os.path.join(K, 'full_p11.cnf')


def cases():
    spec = importlib.util.spec_from_file_location('stage2', os.path.join(K, 'stage2.py'))
    st = importlib.util.module_from_spec(spec)
    argv = sys.argv; sys.argv = ['x']; spec.loader.exec_module(st); sys.argv = argv
    p = 11; n, h, vid, pv = st.setup(p)
    L = [tuple(map(int, l.split()[:3])) for l in open(os.path.join(K, 'L.txt'))]

    def unpack(g):
        s1, s2, t = g
        return (frozenset(d for d in range(1, 6) if s1 >> (d - 1) & 1), frozenset(d for d in range(1, 6) if s2 >> (d - 1) & 1),
                frozenset(s for s in range(11) if t >> s & 1))
    Ls = {unpack(g) for g in L}
    nd = lambda d: min(d % 11, 11 - d % 11)

    def images(g, mults, swap):
        S1, S2, T = g; out = []
        for m in mults:
            A1 = frozenset(nd(m * d) for d in S1); A2 = frozenset(nd(m * d) for d in S2)
            for u in range(11):
                TT = frozenset((m * s + u) % 11 for s in T); out.append((A1, A2, TT))
                if swap: out.append((A2, A1, frozenset((-x) % 11 for x in TT)))
        return out
    key = lambda g: (sorted(g[0]), sorted(g[1]), sorted(g[2]))

    def reps(mults, swap):
        seen = set(); R = []
        for g in sorted(Ls, key=key):
            if g in seen: continue
            seen.update(images(g, mults, swap)); R.append(g)
        return R
    R1 = reps(range(1, 11), True); R2 = reps([1], True)
    lit = lambda k, red: vid[k] if red else -vid[k]

    def assum(g1, g2):
        a = [lit(('f', 0), True), lit(('f', 1), True), lit(('f', 2), False), lit(('f', 3), False)]
        S1, S2, T = g1
        a += [lit(('d', 0, d), d in S1) for d in range(1, 6)] + [lit(('d', 1, d), d in S2) for d in range(1, 6)]
        a += [lit(('o', 0, 1, x), x in T) for x in range(11)]
        B1, B2, BT = g2
        a += [lit(('d', 2, d), d not in B1) for d in range(1, 6)] + [lit(('d', 3, d), d not in B2) for d in range(1, 6)]
        a += [lit(('o', 2, 3, x), x not in BT) for x in range(11)]
        return a
    out = [(i1, i2, assum(g1, g2)) for i1, g1 in enumerate(R1) for i2, g2 in enumerate(R2)]
    return out, len(vid)


def run_case(args):
    i1, i2, units, body, nvars, tmp = args
    t0 = time.time()
    cnf = os.path.join(tmp, f'c_{i1}_{i2}.cnf'); prf = os.path.join(tmp, f'c_{i1}_{i2}.drat')
    with open(cnf, 'w') as f:
        f.write(f'p cnf {nvars} {body[0] + len(units)}\n'); f.write(body[1])
        f.writelines(f'{u} 0\n' for u in units)
    r = subprocess.run(['timeout', '600', 'cadical', '-q', '--no-binary', cnf, prf], capture_output=True, text=True)
    status = {20: 'UNSAT', 10: 'SAT'}.get(r.returncode, f'rc{r.returncode}')
    dres = '-'
    if status == 'UNSAT':
        d = subprocess.run(['timeout', '1200', DRAT, cnf, prf], capture_output=True, text=True)
        dres = 'VERIFIED' if 's VERIFIED' in d.stdout else ('NOT_VERIFIED' if 's NOT VERIFIED' in d.stdout else f'rc{d.returncode}')
    psize = os.path.getsize(prf) if os.path.exists(prf) else 0
    for x in (cnf, prf):
        if os.path.exists(x): os.remove(x)
    return i1, i2, status, dres, psize, time.time() - t0


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    cs, nvars = cases()
    print('cases', len(cs), 'vars', nvars, flush=True)
    raw = open(CNF).read().split('\n', 1)
    hdr = raw[0].split(); assert hdr[:2] == ['p', 'cnf'] and int(hdr[2]) == nvars
    body = (int(hdr[3]), raw[1])
    print('full_p11.cnf sha256', hashlib.sha256(open(CNF, 'rb').read()).hexdigest(), flush=True)
    tmp = tempfile.mkdtemp(prefix='drat11_', dir=os.environ.get('TMPDIR'))
    done = set()
    if os.path.exists('results.tsv'):
        for l in open('results.tsv'):
            f = l.split('\t')
            if f[0].isdigit() and f[3] == 'VERIFIED': done.add((int(f[0]), int(f[1])))
    todo = [(i1, i2, u, body, nvars, tmp) for i1, i2, u in cs if (i1, i2) not in done][:limit]
    print('todo', len(todo), 'already verified', len(done), flush=True)
    new = not os.path.exists('results.tsv')
    with open('results.tsv', 'a') as out, ProcessPoolExecutor(workers) as ex:
        if new: out.write('g1\tg2\tcadical\tdrat_trim\tproof_bytes\tseconds\n')
        for res in ex.map(run_case, todo):
            out.write('\t'.join(map(str, res[:4])) + f'\t{res[4]}\t{res[5]:.2f}\n'); out.flush()
    os.rmdir(tmp)


if __name__ == '__main__':
    main()
