#!/bin/sh
# Build the 453-vertex graph: three copies of the Paley graph P(101), M = neighbourhood of vertex 0 (the 50 quadratic
# residues), glued by tripleglue.py (triple gluing). Needs python3.
set -e
cd "$(dirname "$0")"
python3 - <<'PY'
p = 101; qr = {x * x % p for x in range(1, p)}
open("P101.txt", "w").write(f"{p}\n" + "\n".join("".join("1" if (i != j and (i - j) % p in qr) else "0" for j in range(p)) for i in range(p)) + "\n")
N0 = sorted(qr)
open("maps101.txt", "w").write("\n".join(" ".join(map(str, N0)) for _ in range(3)) + "\n")
open("M101.txt", "w").write("\n".join("".join("1" if (a != b and (a - b) % p in qr) else "0" for b in N0) for a in N0) + "\n")
PY
python3 tripleglue.py P101.txt P101.txt P101.txt maps101.txt M101.txt rebuilt.txt
