"""Rebuild 92 split-test CNFs and verify the archived DRAT proofs."""

import argparse
import csv
import hashlib
from itertools import combinations
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / "r55-srg45" / "recheck"))
from exact import g6dec, g6enc


def split_clauses(red):
    # True puts a vertex on the blue-safe side. Every red four must meet
    # that side and every blue four must meet the opposite side.
    for a, b, c, d in combinations(range(len(red)), 4):
        color = red[a][b]
        if red[a][c] == red[a][d] == red[b][c] == red[b][d] == red[c][d] == color:
            sign = 1 if color else -1
            yield tuple(sign * (v + 1) for v in (a, b, c, d))


def verify_record(record, proofs, checker, work):
    name = record["case"]
    encoded = record["red_graph6"]
    red = g6dec(encoded)
    n = len(red)
    assert n == int(record["vertices"]) and g6enc(red) == encoded, name
    clauses = list(split_clauses(red))
    deletion = record["unsplit_deletion_0based"]
    if record["split_critical"] == "1":
        assert deletion == "", name
        # Every deletion has the partition given by the removed vertex's
        # own incident colours. Check that assignment against every clause.
        for v in range(n):
            side = {(i + 1) * (-1 if red[v][i] else 1) for i in range(n) if i != v}
            assert all(any(abs(lit) == v + 1 or lit in side for lit in cl) for cl in clauses), name
    else:
        assert record["split_critical"] == "0", name
        v = int(deletion)
        assert 0 <= v < n, name
        clauses = [cl for cl in clauses if all(abs(lit) != v + 1 for lit in cl)]

    dimacs = f"p cnf {n} {len(clauses)}\n" + "".join(
        " ".join(map(str, cl)) + " 0\n" for cl in clauses
    )
    raw = dimacs.encode("ascii")
    assert hashlib.sha256(raw).hexdigest() == record["cnf_sha256"], name
    cnf, proof = work / "split.cnf", work / "split.drat"
    cnf.write_bytes(raw)
    proof.write_bytes(proofs.read(name + ".drat"))
    result = subprocess.run([checker, cnf, proof], capture_output=True, timeout=60)
    if result.returncode != 0 or b"s VERIFIED" not in result.stdout:
        raise RuntimeError(f"{name}: drat-trim did not verify the proof\n{result.stdout[-500:]!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drat-trim", default="drat-trim", help="path to the drat-trim executable")
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Run without -O so the verification assertions are enabled.")
    with (HERE / "controls.tsv").open(encoding="ascii", newline="") as stream:
        records = list(csv.DictReader(stream, delimiter="\t"))
    names = {record["case"] for record in records}
    assert len(records) == len(names) == 92
    assert sum((r["vertices"], r["split_critical"], r["unsplit_deletion_0based"]) ==
               ("45", "0", "0") for r in records) == 89
    assert sum((r["vertices"], r["split_critical"]) == ("42", "1") for r in records) == 3
    with ZipFile(HERE / "control-proofs.zip") as proofs, TemporaryDirectory() as temp:
        assert sorted(proofs.namelist()) == sorted(name + ".drat" for name in names)
        for record in records:
            verify_record(record, proofs, args.drat_trim, Path(temp))
    distinct = len({record["red_graph6"] for record in records})
    print(f"{len(records)} DRAT proofs verified for {distinct} distinct labelled inputs")
    print("45 vertices: deleting vertex 0 leaves an unsplittable graph in all 89 records")
    print("42 vertices: all 3 graphs are unsplittable and all 126 deletion splits verified")


if __name__ == "__main__":
    main()
