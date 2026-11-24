"""Reconcile corrected pair keys, optionally recheck the archived labelled graphs."""
import argparse
import csv
from functools import lru_cache
import json
from math import isqrt
from pathlib import Path

from replay import det, edges


def read_legacy(path, expected):
    accepted = {}
    for row in csv.reader(path.open(encoding="utf-8"), delimiter="\t"):
        if len(row) < 11 or row[4:6] != ["UNSAT", "VERIFIED"]:
            continue
        key = row[0], int(row[1])
        if key not in expected:
            continue
        assert key not in accepted
        assert int(row[6]) == expected[key]
        assert int(row[7]) + int(row[8]) == int(row[3]) and row[9:11] == ["0", "0"]
        accepted[key] = tuple(map(int, (row[3], row[6])))
    return accepted


def has_clique(nb, pool, size):
    if size == 1:
        return pool != 0
    while pool.bit_count() >= size:
        bit = pool & -pool
        pool ^= bit
        if has_clique(nb, pool & nb[bit.bit_length()-1], size - 1):
            return True
    return False


def positive_definite(a):
    """Integer Sylvester criterion; fraction-free updates give leading minors."""
    a = [r[:] for r in a]
    denominator = 1
    n = len(a)
    for k in range(n):
        pivot = a[k][k]
        if pivot <= 0:
            return False
        for i in range(k + 1, n):
            for j in range(i, n):
                num = a[i][j] * pivot - a[i][k] * a[k][j]
                assert num % denominator == 0
                a[i][j] = a[j][i] = num // denominator
        denominator = pivot
    return True


def validate_graph(g, k, b, with_window=False):
    e = edges(g)
    assert ord(g[0]) - 63 == 22 and len(g) == 40 and not ((ord(g[-1])-63) & 7)
    assert {v for u, v in e if u == 0} == set(range(1, 11))
    assert {(u-1, v-1) for u, v in e if u and v < 11} == edges(k)
    assert {(u-11, v-11) for u, v in e if u >= 11} == edges(b)
    nb = [0] * 22
    for i, j in e:
        nb[i] |= 1 << j
        nb[j] |= 1 << i
    assert all(mask.bit_count() == 10 for mask in nb)
    pool = (1 << 22) - 1
    assert not has_clique(nb, pool, 4)
    comp = [pool ^ mask ^ (1 << i) for i, mask in enumerate(nb)]
    assert not has_clique(comp, pool, 5)
    gram = [[11*(i == j) + 10 - ((nb[i] >> j) & 1) - (nb[i] & nb[j]).bit_count()
             for j in range(22)] for i in range(22)]
    d = det(gram)
    assert d < 0 or isqrt(d) ** 2 != d
    return (d, positive_definite(gram)) if with_window else d


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="if supplied, validate all archived solutions")
    parser.add_argument("--new", type=Path, default=Path(__file__).resolve().parent / "certs")
    parser.add_argument("--pending", action="store_true", help="append unfinished job, idx keys to output")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    archive = here / "ledgers"
    source = here.parent / "recheck/out/orbits_per_pair.tsv"
    with source.open() as f:
        expected = {(r["job"], int(r["idx"])): int(r["labelled"]) for r in csv.DictReader(f, delimiter="\t")}
    prior = read_legacy(archive / "results_pos.tsv", expected)
    sample = read_legacy(archive / "cmp_result.tsv", expected)
    assert all(prior[k] == sample[k] for k in prior.keys() & sample.keys())
    merged = prior | sample
    print("source positive, batch, sample positive, overlap, unique",
          len(expected), len(prior), len(sample), len(prior.keys() & sample.keys()), len(merged))
    print("archived unique labelled completions, window sum", *(sum(t[i] for t in merged.values()) for i in (0, 1)))
    print("sample-only pairs", sorted(sample.keys()-prior.keys()))
    if args.data:
        data = args.data
        jobs = {s[0]: s[1:] for n in ("jobs.txt", "jobs_e15.txt")
                for line in (data / n).read_text().splitlines() if (s := line.split())}
        @lru_cache(maxsize=None)
        def lines(name):
            return (data / name).read_text().splitlines()
        checked = 0
        archived_windows = 0
        for (job, idx), (count, target_windows) in prior.items():
            k, name, start, size = jobs[job]
            assert 0 <= idx < int(size)
            kg = lines(f"K/K_{k}.g6")[0]
            bg = lines(name)[int(start) + idx]
            sols = (archive / f"sols_pos/p_{job}_{idx}.sols").read_text().splitlines()
            assert len(sols) == len(set(sols)) == count
            measured_windows = sum(validate_graph(g, kg, bg, with_window=True)[1] for g in sols)
            assert measured_windows == target_windows
            checked += len(sols)
            archived_windows += measured_windows
        print("archived graphs checked by exact determinant and pair validation, exact window positives",
              checked, archived_windows)
    added = set()
    for file in sorted(args.new.glob("K*.json")):
        r = json.loads(file.read_text())
        key = r["job"], r["idx"]
        assert key in expected and key not in merged and key not in added
        assert r["drat_result"] == "VERIFIED"
        sols = r["sols_g6_and_exact_det"]
        assert r["enumerated"] == len(sols) == len({g for g, _ in sols})
        checked = [validate_graph(g, r["K_g6"], r["B_g6"], with_window=True) for g, _ in sols]
        assert [v for v, _ in checked] == [d for _, d in sols]
        assert sum(in_window for _, in_window in checked) == expected[key]
        if args.data:
            k, name, start, _ = jobs[key[0]]
            assert r["K_g6"] == lines(f"K/K_{k}.g6")[0] and r["B_g6"] == lines(name)[int(start)+key[1]]
        added.add(key)
    print("new certificate manifests", sorted(added))
    print("positive pairs with historical verified log or new proof, remaining",
          len(merged) + len(added), len(expected.keys()-merged.keys()-added))
    if args.pending:
        for job, idx in sorted(expected.keys() - merged.keys() - added):
            print(job, idx)


if __name__ == "__main__":
    main()
