"""Replay a positive SRG45 pair using the published pair CNF and a checked DRAT."""
import argparse
import gzip
import hashlib
import itertools
import json
from math import isqrt
from pathlib import Path
import subprocess
import sys
import tempfile


def read_inputs(data, job, idx):
    jobs = [row.split() for name in ("jobs.txt", "jobs_e15.txt")
            for row in (data / name).read_text().splitlines() if row.startswith(job + " ")]
    assert len(jobs) == 1
    _, root, partner, start, length = jobs[0]
    assert 0 <= idx < int(length)
    k = (data / "K" / ("K_" + root + ".g6")).read_text().splitlines()[0]
    with (data / partner).open() as file:
        b = next(itertools.islice(file, int(start) + idx, None)).strip()
    return k, b


def edges(g):
    n = ord(g[0]) - 63
    bits = ''.join(f"{ord(c) - 63:06b}" for c in g[1:])
    return {(u, v) for (u, v), bit in zip(((i, j) for j in range(n) for i in range(j)), bits)
            if bit == "1"}


def det(matrix):
    a = [row[:] for row in matrix]
    n, den, sign = len(a), 1, 1
    for k in range(n - 1):
        if not a[k][k]:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[pivot], a[k] = a[k], a[pivot]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * a[k][k] - a[i][k] * a[k][j]
                assert num % den == 0
                a[i][j] = num // den
        den = a[k][k]
    return sign * a[-1][-1]


def witness(k, b, assignments):
    e = {(0, v) for v in range(1, 11)} | {(u + 1, v + 1) for u, v in edges(k)}
    e.update(edge for edge, active in assignments if active)
    assert {(i - 11, j - 11) for i, j in e if i >= 11} == edges(b)
    nb = [{j for j in range(22) if (min(i, j), max(i, j)) in e} for i in range(22)]
    assert all(len(s) == 10 for s in nb)
    for size, forbidden in ((4, 6), (5, 0)):
        assert all(sum(p in e for p in itertools.combinations(sub, 2)) != forbidden
                   for sub in itertools.combinations(range(22), size))
    gram = [[11 * (i == j) + 10 - (j in nb[i]) - len(nb[i] & nb[j])
             for j in range(22)] for i in range(22)]
    value = det(gram)
    assert value < 0 or isqrt(value) ** 2 != value
    bits = ''.join(str(int((i, j) in e)) for j in range(22) for i in range(j))
    bits += '0' * (-len(bits) % 6)
    return chr(22 + 63) + ''.join(chr(63 + int(bits[i:i + 6], 2)) for i in range(0, len(bits), 6)), value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("job")
    parser.add_argument("idx", type=int)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "certs")
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--drat-trim", default="drat-trim")
    parser.add_argument("--limit", type=int, default=90)
    parser.add_argument("--proof-cap", type=int, default=3_000_000,
                        help="maximum compressed proof bytes to retain, at most 3 MB")
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    import enc
    from pysat.solvers import Solver

    k, b = read_inputs(args.data, args.job, args.idx)
    cnf, primary = enc.build(k, b)
    nsol = []
    with Solver(name="cadical195", bootstrap_with=cnf.cl) as solver:
        while solver.solve():
            pos = {v for v in solver.get_model() if v > 0}
            assignment = [(pair, n in pos) for n, pair in enumerate(primary, 2)]
            nsol.append(witness(k, b, assignment))
            block = [(-n if on else n) for n, (_, on) in enumerate(assignment, 2)]
            solver.add_clause(block)
            cnf.add(block)
    assert len({g for g, _ in nsol}) == len(nsol)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "blocked.cnf"
        proof = Path(tmp) / "blocked.drat"
        with path.open("w", newline="\n") as file:
            enc.write(cnf, file)
        sat = subprocess.run([args.cadical, "-q", str(path), str(proof)], capture_output=True, timeout=args.limit)
        assert sat.returncode == 20, sat
        check = subprocess.run([args.drat_trim, str(path), str(proof), "-t", str(args.limit)], capture_output=True,
                               timeout=args.limit)
        assert check.returncode == 0 and b"s VERIFIED" in check.stdout, check
        drat = proof.read_bytes()
        result = {"job": args.job, "idx": args.idx, "K_g6": k, "B_g6": b, "enumerated": len(nsol),
                  "sols_g6_and_exact_det": nsol, "blocked_cnf_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "drat_sha256": hashlib.sha256(drat).hexdigest(), "drat_bytes": len(drat),
                  "drat_result": "VERIFIED"}
        base = args.out / f"{args.job}_{args.idx}"
        # Persist the compressed raw proof only below the project's per-file limit.
        zipped = gzip.compress(drat, compresslevel=3, mtime=0)
        if len(zipped) <= min(args.proof_cap, 3_000_000):
            base.with_suffix(".drat.gz").write_bytes(zipped)
        base.with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(args.job, args.idx, len(nsol), "exact nonsquare determinants; blocked CNF VERIFIED", len(drat), flush=True)


if __name__ == "__main__":
    main()
