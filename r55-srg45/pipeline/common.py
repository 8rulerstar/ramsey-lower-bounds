"""Shared helpers: graph6 decoding and the SRG(45,22,10,11) eigenvalue window [s, r] (roots of x^2 + x - 11)."""
import numpy as np
S = (-1 - 45 ** .5) / 2
R = (-1 + 45 ** .5) / 2
EPS = 1e-9


def g6dec(t):
    t = t.strip(); n = ord(t[0]) - 63; bits = []
    for ch in t[1:]:
        v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    A = np.zeros((n, n), dtype=np.int64); k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: A[i, j] = A[j, i] = 1
            k += 1
    return A
