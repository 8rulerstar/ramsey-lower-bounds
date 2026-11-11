"""Cut the three glued graphs G_1, G_2, G_3 out of a triple-gluing graph F (they are the induced subgraphs on the
first n1, next n2, next n3 vertices). Usage: python3 blocks.py F.txt n1 n2 n3  ->  writes G1.txt G2.txt G3.txt"""
import sys
L = open(sys.argv[1]).read().split(); M = L[1:]; o = 0
for i, n in enumerate(map(int, sys.argv[2:5]), 1):
    open(f"G{i}.txt", "w").write(f"{n}\n" + "\n".join(M[o + a][o:o + n] for a in range(n)) + "\n"); o += n
