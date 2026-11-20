"""Exact-arithmetic helpers for the revision checks (pure Python integers / Fractions, no floating point).
- g6dec/g6enc: graph6 <-> 0/1 adjacency lists.
- Mmat(A): M(A) = 11I + 10J - A - A^2 (integer matrix).
- psd_exact(M): exact positive-semidefiniteness of a symmetric integer matrix. Fraction-free Bareiss elimination
  without pivoting gives the leading principal minors D_1..D_n; if all are > 0 the matrix is positive definite.
  If some D_k < 0 (with D_1..D_{k-1} > 0) it is not PSD (a principal minor is negative). If some D_k = 0 we fall back to
  symmetric Gaussian elimination over Q with the Schur-complement rule (pivot < 0: not PSD; pivot = 0 with a non-zero
  row: not PSD; pivot = 0 with a zero row: drop the index), which decides PSD exactly in all cases.
  Returns (is_psd, is_pd, det) with det exact.
- window_exact(A): A 10-regular and M(A) PSD  <=>  every eigenvalue of A on 1^perp lies in [s, r] (s, r roots of x^2+x-11),
  since M(A) has eigenvalue 121 on 1 and 11 - theta - theta^2 on 1^perp.
- factor(n): prime factorisation (Miller-Rabin with the first 12 prime bases, deterministic for n < 3.3e24, + Pollard rho).
Self-test: python3 exact.py   (compares psd_exact with numpy eigenvalues on random and constructed matrices)."""
from fractions import Fraction
import math, random

def g6dec(t):
    t = t.strip(); n = ord(t[0]) - 63; bits = []
    for ch in t[1:]:
        v = ord(ch) - 63; bits += [(v >> (5 - i)) & 1 for i in range(6)]
    A = [[0] * n for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: A[i][j] = A[j][i] = 1
            k += 1
    return A

def g6enc(A):
    n = len(A); bits = [A[i][j] for j in range(1, n) for i in range(j)]
    bits += [0] * (-len(bits) % 6)
    return chr(63 + n) + ''.join(chr(63 + int(''.join(map(str, bits[i:i + 6])), 2)) for i in range(0, len(bits), 6))

def Mmat(A):
    n = len(A)
    A2 = [[sum(A[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return [[11 * (i == j) + 10 - A[i][j] - A2[i][j] for j in range(n)] for i in range(n)]

def _psd_frac(M):
    n = len(M); M = [[Fraction(x) for x in r] for r in M]; idx = list(range(n)); det_zero = False
    while idx:
        i = idx[0]; p = M[i][i]; rest = idx[1:]
        if p < 0: return False, False
        if p == 0:
            if any(M[i][j] != 0 for j in rest): return False, False
            det_zero = True; idx = rest; continue
        for j in rest:
            f = M[j][i] / p
            if f:
                for k in rest: M[j][k] -= f * M[i][k]
        idx = rest
    return True, not det_zero

def psd_exact(M):
    n = len(M); X = [r[:] for r in M]; prev = 1
    for k in range(n):
        d = X[k][k]  # = leading principal minor D_{k+1}
        if d < 0: return False, False, None
        if d == 0:
            ok, pd = _psd_frac(M); return ok, pd, (0 if ok else None)
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                X[i][j] = (d * X[i][j] - X[i][k] * X[k][j]) // prev
        prev = d
    return True, True, X[n - 1][n - 1]

def det_bareiss(M):
    M = [r[:] for r in M]; n = len(M); prev = 1; sign = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k]), None)
            if sw is None: return 0
            M[k], M[sw] = M[sw], M[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]

def window_exact(A):
    if any(sum(r) != 10 for r in A): return False, False, None
    return psd_exact(Mmat(A))

def is_prime(n):
    if n < 2: return False
    P = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in P:
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in P:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True

def _rho(n):
    if n % 2 == 0: return 2
    while True:
        y, c, m = random.randrange(1, n), random.randrange(1, n), 128; g = r = q = 1
        while g == 1:
            x = y
            for _ in range(r): y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)): y = (y * y + c) % n; q = q * abs(x - y) % n
                g = math.gcd(q, n); k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1: ys = (ys * ys + c) % n; g = math.gcd(abs(x - ys), n)
        if g != n: return g

def factor(n):
    f = {}
    def rec(n):
        if n == 1: return
        if is_prime(n): f[n] = f.get(n, 0) + 1; return
        for p in (2, 3, 5, 7, 11, 13):
            if n % p == 0: f[p] = f.get(p, 0) + 1; rec(n // p); return
        d = _rho(n); rec(d); rec(n // d)
    rec(n); return dict(sorted(f.items()))

def fmt_factor(f): return ' * '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in f.items())

if __name__ == '__main__':
    import numpy as np
    random.seed(1); bad = 0; cases = 0
    for t in range(3000):
        n = random.randint(1, 9); kind = t % 3
        if kind == 0: X = [[random.randint(-3, 3) for _ in range(n)] for _ in range(n)]; M = [[X[i][j] + X[j][i] for j in range(n)] for i in range(n)]
        else:
            r = random.randint(0, n); Y = [[random.randint(-2, 2) for _ in range(r)] for _ in range(n)]
            M = [[sum(Y[i][k] * Y[j][k] for k in range(r)) for j in range(n)] for i in range(n)]
            if kind == 2 and n > 1: M[0][0] -= 1  # often breaks PSD by a small amount
        ok, pd, d = psd_exact(M); w = np.linalg.eigvalsh(np.array(M, float)) if n else [0]
        truth_psd = w[0] > -1e-9; truth_pd = w[0] > 1e-9; cases += 1
        if ok != truth_psd or (ok and pd != truth_pd) or (ok and d != det_bareiss(M)): bad += 1
    print(f'psd_exact self-test: {cases} matrices, disagreements with numpy {bad}')
    for n in [2 ** 4 * 11 ** 6 * 101 * 65101, 1023526940100489, 3 * 9493715299 ** 2]:
        f = factor(n); assert math.prod(p ** e for p, e in f.items()) == n and all(is_prime(p) for p in f); print(n, fmt_factor(f))
    A = g6dec(g6enc([[0, 1, 1], [1, 0, 0], [1, 0, 0]])); print('g6 round trip', A == [[0, 1, 1], [1, 0, 0], [1, 0, 0]])
