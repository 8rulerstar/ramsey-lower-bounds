"""enc.py: 독립 SAT 인코딩 (엔진 src/glue_srg.c, indep/eng.c 의 코드를 읽거나 가져오지 않고 논문 정의에서 직접 작성).

대상: 22정점 그래프 A. 정점 0 = w, 1..10 = K (w 의 이웃), 11..21 = B (w 의 비이웃).
고정: w~K 전부, w 와 B 는 비인접, K 내부 변은 주어진 (3,5,10)-그래프.
변수: K-B 쌍 110개, B-B 쌍 55개 (모드 pair 에서는 B-B 를 단위 절로 고정).
제약 (A 의 정의 그대로, McKay-Radziszowski 원뿔 보조정리는 쓰지 않음):
  K4 없음   : 22정점의 모든 4-부분집합에 대해 "6쌍이 모두 변"을 금지
  I5 없음   : 모든 5-부분집합에 대해 "10쌍이 모두 비변"을 금지
  10-정칙   : 모든 정점 차수 = 10 (순차 계수기, 양방향 동치)
  대칭 깨기 : 모드 perK 에서만. B 정점의 원뿔(K 쪽 인접 10비트)을 사전식 비감소로 정렬.
              건전성: 어떤 해든 B 정점을 원뿔 순으로 다시 번호 매기면 이 제약을 만족하는 해가 된다(K 번호는 그대로).
사용: python3 enc.py K.g6줄 [B.g6줄] > out.cnf   (B 를 주면 pair 모드)
주 변수 번호: pairs() 순서대로 1..len. 해 복원은 primary_pairs() 로.
"""
import sys, itertools

NV = 22
W, KV, BV = 0, list(range(1, 11)), list(range(11, 22))


def g6decode(s):
    s = s.strip()
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits.extend((v >> (5 - i)) & 1 for i in range(6))
    adj = [[0] * n for _ in range(n)]
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i][j] = adj[j][i] = 1
            k += 1
    return n, adj


def primary_pairs(pair_mode):
    """주 변수 쌍 목록. pair 모드에서도 B-B 변수를 만들되 단위 절로 고정한다(번호 체계를 하나로)."""
    P = [(a, h) for a in KV for h in BV]
    P += [(h, g) for h, g in itertools.combinations(BV, 2)]
    return P


class CNF:
    def __init__(self):
        self.nv = 0
        self.cl = []
        self.T = self.new()
        self.cl.append([self.T])

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, c):
        self.cl.append(c)

    def exactly(self, xs, k):
        """순차 계수기: s[i][j] <-> (앞 i 개 중 참이 j 개 이상), j=0..k+1. 끝에서 s[n][k]=참, s[n][k+1]=거짓."""
        n = len(xs)
        if k < 0 or k > n:
            self.add([])  # 불가능
            return
        T = self.T
        prev = [T] + [-T] * (k + 1)  # i=0: 0개 이상만 참
        for i, x in enumerate(xs):
            cur = [T]
            for j in range(1, k + 2):
                s = self.new()
                a, b = prev[j], prev[j - 1]
                # s -> a or b ; s -> a or x ; a -> s ; (b and x) -> s
                self.add([-s, a, b])
                self.add([-s, a, x])
                self.add([-a, s])
                self.add([-b, -x, s])
                cur.append(s)
            prev = cur
        self.add([prev[k]])
        self.add([-prev[k + 1]])

    def lex_le(self, xs, ys):
        """xs <=lex ys (첫 원소가 최상위)."""
        eq = self.T
        for x, y in zip(xs, ys):
            self.add([-eq, -x, y])
            e2 = self.new()
            self.add([-eq, -x, -y, e2])
            self.add([-eq, x, y, e2])
            eq = e2


def build(Kg6, Bg6=None, symbreak=None):
    nk, Kadj = g6decode(Kg6)
    assert nk == 10
    pair_mode = Bg6 is not None
    if symbreak is None:
        symbreak = not pair_mode
    f = CNF()
    P = primary_pairs(pair_mode)
    var = {}
    for p in P:
        v = f.new()
        var[p] = v
        var[(p[1], p[0])] = v
    # 고정 쌍의 값: 1 = 변, 0 = 비변, None = 변수
    def val(i, j):
        if i > j:
            i, j = j, i
        if i == W:
            return 1 if j in KV else 0
        if i in KV and j in KV:
            return Kadj[i - 1][j - 1]
        return None
    if pair_mode:
        nb, Badj = g6decode(Bg6)
        assert nb == 11
        for h, g in itertools.combinations(BV, 2):
            f.add([var[(h, g)] if Badj[h - 11][g - 11] else -var[(h, g)]])
    V = range(NV)
    # K4 없음
    for S in itertools.combinations(V, 4):
        c = []
        ok = True
        for i, j in itertools.combinations(S, 2):
            t = val(i, j)
            if t == 0:
                ok = False
                break
            if t is None:
                c.append(-var[(i, j)])
        if ok:
            f.add(c)  # c 가 비면 고정 부분이 이미 K4 (K 가 삼각형 없음이면 생기지 않음)
    # I5 없음
    for S in itertools.combinations(V, 5):
        c = []
        ok = True
        for i, j in itertools.combinations(S, 2):
            t = val(i, j)
            if t == 1:
                ok = False
                break
            if t is None:
                c.append(var[(i, j)])
        if ok:
            f.add(c)
    # 10-정칙
    for x in V:
        fixed = 0
        xs = []
        for y in V:
            if y == x:
                continue
            t = val(x, y)
            if t is None:
                xs.append(var[(x, y)])
            else:
                fixed += t
        if not xs:
            if fixed != 10:
                f.add([])
            continue
        f.exactly(xs, 10 - fixed)
    if symbreak:
        cones = [[var[(a, h)] for a in KV] for h in BV]
        for h in range(len(BV) - 1):
            f.lex_le(cones[h], cones[h + 1])
    return f, P


def write(f, out):
    out.write("p cnf %d %d\n" % (f.nv, len(f.cl)))
    out.write("".join(" ".join(map(str, c)) + " 0\n" for c in f.cl))


if __name__ == "__main__":
    f, P = build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    write(f, sys.stdout)
