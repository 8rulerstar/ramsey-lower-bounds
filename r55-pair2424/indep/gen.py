#!/usr/bin/env python3
# Independent placement sampler. Usage: gen.py main SEED COUNT_PER_C  |  gen.py pos COUNT  |  gen.py brute COUNT
import sys, random, itertools
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
import os; _H = os.path.dirname(os.path.abspath(__file__)); LIST = os.path.join(_H, '..', 'd24_e127.g6')
R42 = os.path.join(_H, '..', 'data', 'r55_42some.g6')

def g6(s):
    s = s.strip(); d = [ord(ch) - 63 for ch in s]
    n = d[0]; bits = []
    for x in d[1:]:
        bits += [(x >> (5 - k)) & 1 for k in range(6)]
    A = [[0] * n for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: A[i][j] = A[j][i] = 1
            k += 1
    return A

def emit(M, tag):
    n = len(M); out = [f"{n} {tag}"]
    for i in range(n):
        out.append(''.join('.' if i == j else M[i][j] for j in range(n)))
    sys.stdout.write('\n'.join(out) + '\n')

def build(Xu, p, Xv, q, phi):
    # Xu, Xv: adjacency (24x24). p: v's index in Xu. q: u's index in Xv. phi: dict Cu index -> Cv index.
    Cu = [i for i in range(24) if Xu[p][i]]; c = len(Cu)
    Au = [i for i in range(24) if i != p and not Xu[p][i]]
    Bv = [j for j in range(24) if j != q and not Xv[q][j]]
    nD = c - 3; n = 2 + c + len(Au) + len(Bv) + nD; assert n == 45
    U, V = 0, 1
    gid_u = {p: V}; gid_v = {q: U}
    for k, i in enumerate(Cu): gid_u[i] = 2 + k; gid_v[phi[i]] = 2 + k
    off = 2 + c
    for k, i in enumerate(Au): gid_u[i] = off + k
    off += len(Au)
    for k, j in enumerate(Bv): gid_v[j] = off + k
    M = [['?'] * n for _ in range(n)]
    def put(a, b, col):
        if a == b: return
        if M[a][b] != '?' and M[a][b] != col: raise Exception('inconsistent')
        M[a][b] = M[b][a] = col
    Xus = set(gid_u.values()); Xvs = set(gid_v.values())  # Xu as global set incl v ; Xv incl u
    for w in range(n):
        if w != U: put(U, w, '1' if w in Xus else '0')
        if w != V: put(V, w, '1' if w in Xvs else '0')
    for i in range(24):
        for j in range(i + 1, 24):
            put(gid_u[i], gid_u[j], '1' if Xu[i][j] else '0')
            put(gid_v[i], gid_v[j], '1' if Xv[i][j] else '0')
    return M

def main(seed, per_c):
    rnd = random.Random(seed)
    G = [g6(l) for l in open(LIST) if l.strip()]
    nb = {}  # c -> list of (gi, vertex, nbhd graph)
    buckets = {}
    for gi, A in enumerate(G):
        for x in range(24):
            N = [y for y in range(24) if A[x][y]]
            H = nx.Graph(); H.add_nodes_from(N)
            H.add_edges_from((a, b) for a, b in itertools.combinations(N, 2) if A[a][b])
            key = (len(N), nx.weisfeiler_lehman_graph_hash(H, iterations=4))
            buckets.setdefault(key, []).append((gi, x, H))
            nb.setdefault(len(N), []).append((gi, x, H, key))
    sys.stderr.write('cs ' + str({c: len(v) for c, v in sorted(nb.items())}) + '\n')
    for c in sorted(nb):
        done = 0; tries = 0
        while done < per_c and tries < 50 * per_c:
            tries += 1
            gi, x, H, key = rnd.choice(nb[c])
            gj, y, H2 = rnd.choice(buckets[key])
            GM = GraphMatcher(H, H2)
            isos = list(itertools.islice(GM.isomorphisms_iter(), 20000))
            if not isos: continue
            phi = rnd.choice(isos)
            M = build(G[gi], x, G[gj], y, phi)
            emit(M, f"c{c}_g{gi}v{x}_g{gj}u{y}_n{len(isos)}_{done}")
            done += 1

def pos(cnt):
    rnd = random.Random(7)
    Gs = [g6(l) for l in open(R42) if l.strip()]
    for t in range(cnt):
        A = rnd.choice(Gs); n = len(A)
        col = rnd.choice([0, 1])
        R = [[(A[i][j] if col == 1 else 1 - A[i][j]) if i != j else 0 for j in range(n)] for i in range(n)]
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if R[i][j]]
        u, v = rnd.choice(edges)
        Xu = {w for w in range(n) if R[u][w]}; Xv = {w for w in range(n) if R[v][w]}
        M = [['?'] * n for _ in range(n)]
        for w in range(n):
            if w != u: M[u][w] = M[w][u] = str(R[u][w])
            if w != v: M[v][w] = M[w][v] = str(R[v][w])
        for S in (Xu, Xv):
            for a in S:
                for b in S:
                    if a != b: M[a][b] = str(R[a][b])
        emit(M, f"pos{t}_d{len(Xu)}_{len(Xv)}")

def brute(cnt):
    # small random partial colourings; prints instance and also exact answer to stderr file
    rnd = random.Random(11); ans = open('brute_truth.txt', 'w')
    for t in range(cnt):
        n = rnd.choice([11, 12]); k = rnd.randint(8, 13)
        while True:
            M = [[None] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    M[i][j] = M[j][i] = ('1' if rnd.random() < 0.56 else '0')
            pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
            U = set()
            for S in itertools.combinations(range(n), 5):
                if len({M[x][y] for x, y in itertools.combinations(S, 2)}) == 1:
                    U.add(rnd.choice(list(itertools.combinations(S, 2))))
            if len(U) > 12: continue
            rest = [e for e in pairs if e not in U]
            unk = list(U) + rnd.sample(rest, 0); k = len(unk)
            for i, j in unk: M[i][j] = M[j][i] = '?'
            break
        def ok(M):
            for S in itertools.combinations(range(n), 5):
                cs = {M[a][b] for a, b in itertools.combinations(S, 2)}
                if len(cs) == 1: return False
            return True
        sat = False
        for bits in itertools.product('01', repeat=k):
            for (i, j), b in zip(unk, bits): M[i][j] = M[j][i] = b
            if ok(M): sat = True; break
        for i, j in unk: M[i][j] = M[j][i] = '?'
        emit(M, f"br{t}"); ans.write(f"br{t} {'SAT' if sat else 'UNSAT'}\n")

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'main': main(int(sys.argv[2]), int(sys.argv[3]))
    elif m == 'pos': pos(int(sys.argv[2]))
    else: brute(int(sys.argv[2]))
