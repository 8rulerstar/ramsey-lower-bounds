"""Reconstruct the blocked CNF from stored graph6 solutions; check or generate DRAT."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from audit_ledger import validate_graph
from replay import read_inputs, edges


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--cadical", default="cadical")
    parser.add_argument("--drat-trim", default="drat-trim")
    parser.add_argument("--expected-window", type=int)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    import enc
    r = json.loads(args.manifest.read_text())
    k, b = read_inputs(args.data, r["job"], r["idx"])
    assert (k, b) == (r["K_g6"], r["B_g6"])
    cnf, pairs = enc.build(k, b)
    sols = r["sols_g6_and_exact_det"]
    assert r["enumerated"] == len(sols) == len({g for g, _ in sols})
    in_window = 0
    for g, d in sols:
        value, positive = validate_graph(g, k, b, with_window=True)
        assert value == d
        in_window += positive
        graph = edges(g)
        cnf.add([-idx if pair in graph else idx for idx, pair in enumerate(pairs, 2)])
    if args.expected_window is not None:
        assert in_window == args.expected_window
    with tempfile.TemporaryDirectory() as tmp:
        path, proof = (Path(tmp) / n for n in ("blocked.cnf", "blocked.drat"))
        with path.open("w", newline="\n") as f:
            enc.write(cnf, f)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == r["blocked_cnf_sha256"]
        archived = args.manifest.with_suffix(".drat.gz")
        if archived.exists():
            raw = gzip.decompress(archived.read_bytes())
            assert hashlib.sha256(raw).hexdigest() == r["drat_sha256"]
            proof.write_bytes(raw)
        else:
            s = subprocess.run([args.cadical, "-q", str(path), str(proof)], capture_output=True, timeout=90)
            assert s.returncode == 20, s
        c = subprocess.run([args.drat_trim, str(path), str(proof), "-t", "90"], capture_output=True, timeout=90)
        assert c.returncode == 0 and b"s VERIFIED" in c.stdout, c
        print(r["job"], r["idx"], f"{len(sols)} valid exact arithmetic witnesses, {in_window} window,",
              "fixed-CNF DRAT verified,", "archived" if archived.exists() else "regenerated",
              hashlib.sha256(proof.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
