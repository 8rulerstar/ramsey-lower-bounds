/* glue_srg.c: glue2.c 의 SRG 증인 판 (exp_glue2/srg/README.md). 바뀐 점: maxsol 0 = 해 전부, sym 과 함께 써도 됨(Aut(A) 궤도 대표마다 해 하나 이상 남음),
   해마다 22정점 전체 행렬에서 창 검사(λ_min >= s 이고 λ_2 <= r, 여유 1e-9, Cholesky), Gale-Ryser 사전 거르기(차수 창 dlo=dhi 일 때).
   출력: "R idx nsol nwin nodes usec [GR]", 창 안 해와 처음 PRINTCAP 개 해는 "S idx win 원뿔..." 줄.
   (원래 머리말) glue2.c: (s,t)=(4,5) 목록 x 목록 접착 (McKay-Radziszowski 1995 식, 원뿔 정의역 비트셋 + 앞질러 검사).
   입력: A = N(u) 그래프 하나 (argv[1] 의 g6 파일 첫 줄, (3,5)-그래프), 표준입력 = B 목록 (g6, (4,4)-그래프).
   각 h in B 에 원뿔 C_h = N(h) ∩ A 를 고른다. 조건 (README 1절 증명):
     단일   a(A - C_h) <= 3
     h~h'   C_h ∩ C_h' 가 A 에서 독립 (변 없음)
     h!~h'  a(A - (C_h ∪ C_h')) <= 2
     B 의 삼각형   C ∩ C' ∩ C'' = 공집합
     B 의 독립 3집합 a(A - (C ∪ C' ∪ C'')) <= 1
   u 를 더한 그래프가 (4,5)-그래프 <=> 위 조건 전부 (A 가 (3,5), B 가 (4,4) 일 때).
   사용: ./glue2 Afile [maxsol] [sym] [dlo dhi] < Blist.g6  (dlo..dhi: 전체 그래프 차수 범위, n=25 면 7 13, n=24 면 6 13; 생략하면 차수 조건 없음)
     maxsol 0 (기본): 해 하나 찾으면 그 B 끝. k>0: 해를 k 개까지 세고 출력.  sym 1: Aut(A) 로 첫 원뿔을 궤도 대표로 제한 (존재 판정만).
   출력: 각 B 마다 "R idx SAT|UNSAT nodes usec [cones...]" 한 줄. 끝에 "#END" 집계.
   STOP 파일(현재 폴더)이 있으면 1000 건마다 확인해 멈춘다 ("#STOPPED").
   환경변수 OUT=파일: 그 파일에 이어 쓰고, 이미 있는 완결 R 줄 수만큼 입력 앞부분을 건너뛴다(재개).
   환경변수 NOPROP: 미배정 쌍 전파를 끈다. 컴파일 -DROUNDS=k: 전파 반복 횟수(기본 1). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

#define MAXB 20
typedef uint64_t u64;
static int nA, nB, W;
static unsigned Aadj[32];
static unsigned char *alpha;     /* alpha(mask) capped at 4 */
static unsigned char *hasE;      /* mask 안에 A 의 변이 있는가 */
static int nF; static unsigned *F; /* 단일 조건 통과 원뿔 */
static u64 *Erow, *Nrow;         /* [nF][W] */
static u64 *noE, *n2;
static u64 *disj, *cov;          /* [2^nA][W]: Y ∩ m = 0 / a(m - Y) <= 1 */
static int Badj[MAXB][MAXB];
static u64 dom[MAXB + 1][MAXB][64 * 4];
static int assigned[MAXB]; static unsigned cone[MAXB];
static int dlo = 0, dhi = 99; static int cnt[32], cap[32], need[32]; static u64 *avoid; /* [nA][W] 원뿔이 a 를 안 가짐 */
static long long nodes, nsol, maxsol;
static int symrep; static unsigned char *isrep; /* 궤도 대표 표시 [nF] */
static int nAut; static int aut[100000][16];

static inline int popc(u64 x) { return __builtin_popcountll(x); }

static int readg6(const char *s, int nn_out[1], int adj[MAXB > 32 ? MAXB : 32][32]) {
    int nn = s[0] - 63, bit = 0, v = 0; const char *p = s + 1;
    for (int i = 0; i < nn; i++) for (int j = 0; j < nn; j++) adj[i][j] = 0;
    for (int j = 1; j < nn; j++) for (int i = 0; i < j; i++) {
        if (bit == 0) { v = *p++ - 63; bit = 6; }
        bit--; adj[i][j] = adj[j][i] = (v >> bit) & 1;
    }
    nn_out[0] = nn; return nn;
}

static int wlo[MAXB], whi[MAXB];
static int cmpF(const void *a, const void *b) { unsigned x = *(const unsigned *)a, y = *(const unsigned *)b; int px = __builtin_popcount(x), py = __builtin_popcount(y); if (px != py) return px - py; return (x > y) - (x < y); }
static void tables(void) {
    unsigned full = (1u << nA) - 1;
    alpha = malloc(full + 1); hasE = malloc(full + 1);
    alpha[0] = 0; hasE[0] = 0;
    for (unsigned T = 1; T <= full; T++) {
        int v = __builtin_ctz(T); unsigned R = T & ~(1u << v);
        int a1 = alpha[R], a2 = 1 + alpha[R & ~Aadj[v]];
        int a = a1 > a2 ? a1 : a2; alpha[T] = a > 4 ? 4 : a;
        hasE[T] = hasE[R] || (R & Aadj[v]);
    }
    F = malloc(sizeof(unsigned) * (full + 1)); nF = 0;
    for (unsigned X = 0; X <= full; X++) if (alpha[full & ~X] <= 3) F[nF++] = X;
    qsort(F, nF, sizeof(unsigned), cmpF); /* 크기순: 차수 조건이 원뿔 크기 구간이므로 정의역이 연속 단어 구간이 된다 */
    W = (nF + 63) / 64;
    if (W > 64 * 4) { fprintf(stderr, "nF too big %d\n", nF); exit(2); }
    Erow = calloc((size_t)nF * W, 8); Nrow = calloc((size_t)nF * W, 8);
    for (int i = 0; i < nF; i++) for (int j = 0; j < nF; j++) {
        unsigned X = F[i], Y = F[j];
        if (!hasE[X & Y]) Erow[(size_t)i * W + j / 64] |= 1ull << (j % 64);
        if (alpha[full & ~(X | Y)] <= 2) Nrow[(size_t)i * W + j / 64] |= 1ull << (j % 64);
    }
    avoid = calloc((size_t)nA * W, 8);
    for (int a = 0; a < nA; a++) for (int j = 0; j < nF; j++) if (!(F[j] >> a & 1)) avoid[(size_t)a * W + j / 64] |= 1ull << (j % 64);
    noE = calloc((size_t)(full + 1) * W, 8); n2 = calloc((size_t)(full + 1) * W, 8);
    for (unsigned m = 0; m <= full; m++) for (int j = 0; j < nF; j++) {
        if (!hasE[m & F[j]]) noE[(size_t)m * W + j / 64] |= 1ull << (j % 64);
        if (alpha[full & ~(m | F[j])] <= 2) n2[(size_t)m * W + j / 64] |= 1ull << (j % 64);
    }
    disj = calloc((size_t)(full + 1) * W, 8); cov = calloc((size_t)(full + 1) * W, 8);
    for (unsigned m = 0; m <= full; m++) for (int j = 0; j < nF; j++) {
        if (!(m & F[j])) disj[(size_t)m * W + j / 64] |= 1ull << (j % 64);
        if (alpha[m & ~F[j]] <= 1) cov[(size_t)m * W + j / 64] |= 1ull << (j % 64);
    }
}

/* Aut(A) 를 역추적으로 전부 구한다 (nA <= 16). */
static int perm[16], used[16];
static void autsearch(int k) {
    if (k == nA) { if (nAut < 100000) { memcpy(aut[nAut], perm, sizeof perm); nAut++; } return; }
    for (int x = 0; x < nA; x++) if (!used[x]) {
        int ok = 1;
        for (int i = 0; i < k && ok; i++) if (((Aadj[i] >> k) & 1) != ((Aadj[perm[i]] >> x) & 1)) ok = 0;
        if (!ok || __builtin_popcount(Aadj[k]) != __builtin_popcount(Aadj[x])) continue;
        used[x] = 1; perm[k] = x; autsearch(k + 1); used[x] = 0;
    }
}
static void orbits(void) {
    nAut = 0; autsearch(0);
    isrep = calloc(nF, 1);
    for (int i = 0; i < nF; i++) {
        unsigned X = F[i], mn = X;
        for (int g = 0; g < nAut; g++) { unsigned Y = 0; for (int a = 0; a < nA; a++) if (X >> a & 1) Y |= 1u << aut[g][a]; if (Y < mn) mn = Y; }
        isrep[i] = (mn == X);
    }
}

/* 미배정 두 정점 사이 전파: L_g = 정의역 원뿔들의 교집합, U_g = 합집합.
   g~g': 어떤 해든 C_g ⊇ L_g 이므로 Y ∩ L_g 에 변이 있으면 g' 의 Y 불가 (noE[L_g]).
   g!~g': C_g ⊆ U_g 이므로 a(A - (U_g ∪ Y)) > 2 이면 Y 불가 (n2[U_g]). */
static int useprop = 1;
#ifndef ROUNDS
#define ROUNDS 1
#endif
static int prop(int dp) {
    unsigned L[MAXB], U[MAXB];
    for (int round = 0; round < ROUNDS; round++) {
        for (int g = 0; g < nB; g++) if (!assigned[g]) {
            u64 *D = dom[dp][g]; unsigned l = 0, u = 0;
            for (int a = 0; a < nA; a++) {
                const u64 *M = avoid + (size_t)a * W; u64 in = 0, out = 0;
                for (int x = wlo[g]; x < whi[g]; x++) { in |= D[x] & ~M[x]; out |= D[x] & M[x]; }
                if (in) u |= 1u << a;
                if (!out) l |= 1u << a;
            }
            L[g] = l; U[g] = u;
        }
        int changed = 0;
        for (int g = 0; g < nB; g++) if (!assigned[g]) for (int g2 = 0; g2 < nB; g2++) if (g2 != g && !assigned[g2]) {
            const u64 *M = Badj[g][g2] ? noE + (size_t)L[g] * W : n2 + (size_t)U[g] * W;
            u64 *D = dom[dp][g2]; u64 any = 0, ch = 0;
            for (int x = wlo[g2]; x < whi[g2]; x++) { u64 v = D[x] & M[x]; ch |= v ^ D[x]; D[x] = v; any |= v; }
            if (!any) return 0;
            if (ch) changed = 1;
        }
        if (!changed) break;
    }
    return 1;
}

#ifndef PRINTCAP
#define PRINTCAP 3
#endif
static long long nwin, nprinted, curidx;
/* 22정점 전체 행렬: 0 = u, 1..nA = A, nA+1.. = B. M 이 양의 정부호인지 (Cholesky). */
static int chol_pd(double *M, int n) {
    for (int j = 0; j < n; j++) {
        double d = M[j * n + j];
        for (int k = 0; k < j; k++) d -= M[j * n + k] * M[j * n + k];
        if (d <= 0) return 0;
        d = sqrt(d); M[j * n + j] = d;
        for (int i = j + 1; i < n; i++) {
            double v = M[i * n + j];
            for (int k = 0; k < j; k++) v -= M[i * n + k] * M[j * n + k];
            M[i * n + j] = v / d;
        }
    }
    return 1;
}
static int fullG[40][40];
/* 창 경계 (기본 s, r). 대조용으로 환경변수 SWIN, RWIN 으로 바꿀 수 있다. */
static double SW, RW; static int eigprune = 0;
/* 교차(Cauchy) 가지치기: H 가 창 안(λ_min(H) >= s)이면 모든 유도 부분그래프도 λ_min >= s.
   배정된 정점 {u} ∪ A ∪ {배정된 h} 의 유도 행렬이 λ_min < s 이면 이 가지에는 창 안 해가 없다. 해 전부가 아니라 창 안 해만 찾을 때 쓴다(EIGPRUNE=1). */
static int trirule = 0, elo = 15;
/* 유도 부분그래프 V' = {u} ∪ A ∪ {배정된 h} 의 인접 비트 (V' 안 번호). full=1 이면 전부 배정된 상태. */
static int buildV(unsigned *row) {
    int idxs[40], m = 0;
    idxs[m++] = -1; for (int a = 0; a < nA; a++) idxs[m++] = a; for (int h = 0; h < nB; h++) if (assigned[h]) idxs[m++] = nA + h;
    for (int i = 0; i < m; i++) { row[i] = 0; for (int j = 0; j < m; j++) if (i != j) {
        int x = idxs[i], y = idxs[j], e;
        if (x < 0 || y < 0) { int z = x < 0 ? y : x; e = z < nA; }
        else if (x < nA && y < nA) e = (Aadj[x] >> y) & 1;
        else if (x >= nA && y >= nA) e = Badj[x - nA][y - nA];
        else { int a = x < nA ? x : y, h = (x < nA ? y : x) - nA; e = (cone[h] >> a) & 1; }
        if (e) row[i] |= 1u << j; } }
    return m;
}
/* 삼각형 뿌리 규칙: u 는 e(N(w)) 최대 정점이므로 모든 w 에 e(N(w)) <= e(A).
   V' 안에서 센 e(N(w) ∩ V') 는 최종 e(N(w)) 의 하한(정점이 늘면 줄지 않음). 완성 때는 elo <= e(N(w)) 도. */
static int tri_ok(unsigned *row, int m, int full) {
    int eA = 0; for (int a = 0; a < nA; a++) eA += __builtin_popcount(Aadj[a]); eA /= 2;
    for (int w = 0; w < m; w++) {
        int t = 0; unsigned nw = row[w];
        for (unsigned x = nw; x; x &= x - 1) t += __builtin_popcount(row[__builtin_ctz(x)] & nw);
        t /= 2;
        if (t > eA) return 0;
        if (full && t < elo) return 0;
    }
    return 1;
}
/* 교차(Cauchy): H 가 창 안이면 모든 유도 부분그래프가 λ_min >= s, λ_2 <= r.
   λ_min: A - (s - eps) I 양의 정부호(Cholesky). λ_2: (r + eps) I - A 의 음의 고윳값 수 <= 1 (LDL^T 관성, 피벗이 1e-10 보다 작으면 판정 안 함 = 자르지 않음). */
static int eig_ok(unsigned *row, int m) {
    static double M[1600];
    for (int i = 0; i < m; i++) for (int j = 0; j < m; j++) M[i * m + j] = ((row[i] >> j) & 1) - (i == j ? (SW - 1e-9) : 0);
    if (!chol_pd(M, m)) return 0;
    for (int i = 0; i < m; i++) for (int j = 0; j < m; j++) M[i * m + j] = (i == j ? RW + 1e-9 : 0) - ((row[i] >> j) & 1);
    int neg = 0;
    for (int j = 0; j < m; j++) {
        double d = M[j * m + j];
        if (fabs(d) < 1e-10) return 1;
        if (d < 0) neg++;
        for (int i = j + 1; i < m; i++) { double l = M[i * m + j] / d; for (int k = j + 1; k <= i; k++) M[i * m + k] -= l * M[k * m + j]; }
    }
    return neg <= 1;
}
/* 깊이 0 원뿔 사전 삭제: 원뿔 Y 하나로 {u} ∪ A ∪ {h} 유도 그래프가 정해진다(B 와 무관). A 마다 한 번 계산해 모든 정의역에 AND. */
static u64 *okcone = 0;
static void build_okcone(void) {
    okcone = calloc(W, 8);
    for (int j = 0; j < nF; j++) {
        unsigned row[40]; int m = 1 + nA + 1;
        row[0] = ((1u << nA) - 1) << 1;
        for (int a = 0; a < nA; a++) row[1 + a] = 1u | (Aadj[a] << 1) | (((F[j] >> a) & 1u) << (1 + nA));
        row[1 + nA] = F[j] << 1;
        int ok = 1;
        if (trirule && !tri_ok(row, m, 0)) ok = 0;
        if (ok && eigprune && !eig_ok(row, m)) ok = 0;
        if (ok) okcone[j / 64] |= 1ull << (j % 64);
    }
    int c = 0; for (int x = 0; x < W; x++) c += popc(okcone[x]);
    fprintf(stderr, "# okcone %d of %d\n", c, nF);
}
static int partial_ok(void) {
    unsigned row[40]; int m = buildV(row);
    if (trirule && !tri_ok(row, m, 0)) return 0;
    if (eigprune && !eig_ok(row, m)) return 0;
    return 1;
}
static int inwindow(void) {
    int n = 1 + nA + nB; static double M[1600];
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) fullG[i][j] = 0;
    for (int a = 0; a < nA; a++) { fullG[0][1 + a] = fullG[1 + a][0] = 1; for (int b = 0; b < nA; b++) fullG[1 + a][1 + b] = (Aadj[a] >> b) & 1; }
    for (int h = 0; h < nB; h++) {
        for (int g = 0; g < nB; g++) fullG[1 + nA + h][1 + nA + g] = Badj[h][g];
        for (int a = 0; a < nA; a++) if (cone[h] >> a & 1) fullG[1 + a][1 + nA + h] = fullG[1 + nA + h][1 + a] = 1;
    }
    const double s = SW, r = RW, eps = 1e-9;
    /* λ_min >= s  <=>  A - (s - eps) I 양의 정부호 */
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) M[i * n + j] = fullG[i][j] - (i == j ? (s - eps) : 0);
    if (!chol_pd(M, n)) return 0;
    /* 정칙(차수 k)이면 1 이 고유벡터. λ_2 <= r  <=>  (r + eps) I - A + c J 양의 정부호, c = (k - r) / n + eps */
    int k = 0; for (int j = 0; j < n; j++) k += fullG[0][j];
    double c = (k - r) / n + eps;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) M[i * n + j] = (i == j ? r + eps : 0) - fullG[i][j] + c;
    return chol_pd(M, n);
}
/* Gale-Ryser: A 쪽 정점 a 는 B 쪽 이웃 dlo-1-deg_A(a), B 쪽 h 는 A 쪽 이웃 dlo-deg_B(h) 가 정확히 필요(dlo=dhi 일 때). */
static int gale_ryser(void) {
    int da[32], db[32], sa = 0, sb = 0;
    for (int a = 0; a < nA; a++) { da[a] = dlo - 1 - __builtin_popcount(Aadj[a]); if (da[a] < 0 || da[a] > nB) return 0; sa += da[a]; }
    for (int h = 0; h < nB; h++) { int g0 = 0; for (int g = 0; g < nB; g++) g0 += Badj[h][g]; db[h] = dlo - g0; if (db[h] < 0 || db[h] > nA) return 0; sb += db[h]; }
    if (sa != sb) return 0;
    for (int i = 0; i < nB; i++) for (int j = i + 1; j < nB; j++) if (db[j] > db[i]) { int t = db[i]; db[i] = db[j]; db[j] = t; }
    int left = 0;
    for (int k = 1; k <= nB; k++) { left += db[k - 1]; int right = 0; for (int a = 0; a < nA; a++) right += da[a] < k ? da[a] : k; if (left > right) return 0; }
    return 1;
}
static unsigned *solbuf; static char outline[4096];
static int search(int depth) {
    if (depth == nB) {
        if (trirule) { unsigned row[40]; int m = buildV(row); if (!tri_ok(row, m, 1)) return 0; }
        nsol++;
        int w = inwindow();
        nwin += w;
        if (w || nprinted < PRINTCAP) { nprinted++; printf("S %lld %d", curidx, w); for (int h = 0; h < nB; h++) printf(" %u", cone[h]); printf("\n"); }
        return maxsol > 0 && nsol >= maxsol;
    }
    nodes++;
    int best = -1, bc = 1 << 30;
    for (int h = 0; h < nB; h++) if (!assigned[h]) {
        int c = 0; for (int w = wlo[h]; w < whi[h]; w++) c += popc(dom[depth][h][w]);
        if (c < bc) { bc = c; best = h; }
    }
    int h = best; u64 *D = dom[depth][h];
    unsigned full = (1u << nA) - 1;
    for (int w = wlo[h]; w < whi[h]; w++) {
        u64 bits = D[w];
        while (bits) {
            int j = w * 64 + __builtin_ctzll(bits); bits &= bits - 1;
            if (depth == 0 && symrep && !isrep[j]) continue;
            unsigned Y = F[j];
            int ok = 1, remain = nB - depth - 1;
            for (int a = 0; a < nA; a++) { cnt[a] += Y >> a & 1; if (cnt[a] > cap[a] || cnt[a] + remain < need[a]) ok = 0; }
            if (!ok) { for (int a = 0; a < nA; a++) cnt[a] -= Y >> a & 1; continue; }
            assigned[h] = 1; cone[h] = Y;
            for (int g = 0; g < nB && ok; g++) if (!assigned[g]) {
                u64 *src = dom[depth][g], *dst = dom[depth + 1][g];
                const u64 *R = Badj[h][g] ? Erow + (size_t)j * W : Nrow + (size_t)j * W;
                for (int x = wlo[g]; x < whi[g]; x++) dst[x] = src[x] & R[x];
                for (int a = 0; a < nA; a++) if (cnt[a] == cap[a] && (Y >> a & 1)) { const u64 *M = avoid + (size_t)a * W; for (int x = wlo[g]; x < whi[g]; x++) dst[x] &= M[x]; }
                for (int f = 0; f < nB; f++) if (assigned[f] && f != h) {
                    if (Badj[h][g] && Badj[h][f] && Badj[f][g]) {
                        const u64 *M = disj + (size_t)(Y & cone[f]) * W; for (int x = wlo[g]; x < whi[g]; x++) dst[x] &= M[x];
                    } else if (!Badj[h][g] && !Badj[h][f] && !Badj[f][g]) {
                        const u64 *M = cov + (size_t)(full & ~(Y | cone[f])) * W; for (int x = wlo[g]; x < whi[g]; x++) dst[x] &= M[x];
                    }
                }
                u64 any = 0; for (int x = wlo[g]; x < whi[g]; x++) any |= dst[x];
                if (!any) ok = 0;
            }
            if (ok && useprop) ok = prop(depth + 1);
            if (ok && (eigprune || trirule)) ok = partial_ok();
            int r = ok && search(depth + 1);
            assigned[h] = 0; for (int a = 0; a < nA; a++) cnt[a] -= Y >> a & 1;
            if (r) return 1;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: glue2 Afile [maxsol] [sym] < Blist\n"); return 2; }
    setvbuf(stdout, NULL, _IOLBF, 1 << 14);
    maxsol = argc > 2 ? atoll(argv[2]) : 0; symrep = argc > 3 ? atoi(argv[3]) : 0;
    if (getenv("NOPROP")) useprop = 0;
    SW = getenv("SWIN") ? atof(getenv("SWIN")) : (-1 - sqrt(45.0)) / 2; RW = getenv("RWIN") ? atof(getenv("RWIN")) : (-1 + sqrt(45.0)) / 2;
    if (getenv("EIGPRUNE")) eigprune = 1;
    if (getenv("TRIRULE")) { trirule = 1; if (getenv("ELO")) elo = atoi(getenv("ELO")); }
    if (argc > 5) { dlo = atoi(argv[4]); dhi = atoi(argv[5]); }
    static int adj[32][32]; int nn[1]; char line[256];
    FILE *fa = fopen(argv[1], "r"); if (!fa || !fgets(line, sizeof line, fa)) { fprintf(stderr, "bad A\n"); return 2; }
    line[strcspn(line, "\r\n")] = 0; readg6(line, nn, adj); nA = nn[0];
    for (int i = 0; i < nA; i++) { Aadj[i] = 0; for (int j = 0; j < nA; j++) if (adj[i][j]) Aadj[i] |= 1u << j; }
    tables();
    if (symrep) orbits();
    int nrep = 0; if (symrep) for (int i = 0; i < nF; i++) nrep += isrep[i];
    fprintf(stderr, "# nA=%d nF=%d W=%d aut=%d reps=%d\n", nA, nF, W, nAut, nrep);
    long long idx = 0, nsat = 0, nun = 0, done = 0; double tot = 0, tmax = 0;
    const char *outf = getenv("OUT");   /* 재개: OUT 파일의 완결된 "R " 줄 수만큼 입력을 건너뛰고 이어 쓴다 */
    if (outf) {
        FILE *fo = fopen(outf, "r"); int partial = 0;
        if (fo) { static char buf[1 << 16]; while (fgets(buf, sizeof buf, fo)) { size_t L = strlen(buf); partial = (L == 0 || buf[L - 1] != '\n'); if (!partial && buf[0] == 'R' && buf[1] == ' ') done++; } fclose(fo); }
        if (!freopen(outf, "a", stdout)) { fprintf(stderr, "cannot open OUT\n"); return 2; }
        setvbuf(stdout, NULL, _IOLBF, 1 << 14);
        if (partial) printf("\n");
        printf("#RESUME skip=%lld\n", done);
    }
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0; if (!line[0]) continue;
        if (idx < done) { idx++; continue; }
        if (idx % 1000 == 0 && access("STOP", F_OK) == 0) { printf("#STOPPED at %lld\n", idx); break; }
        readg6(line, nn, adj); nB = nn[0];
        if (nB > MAXB) { fprintf(stderr, "B too big\n"); return 2; }
        for (int i = 0; i < nB; i++) for (int j = 0; j < nB; j++) Badj[i][j] = adj[i][j];
        for (int h = 0; h < nB; h++) {
            int dg = 0; for (int g = 0; g < nB; g++) dg += Badj[h][g];
            assigned[h] = 0; memset(dom[0][h], 0, 8 * W);
            int jlo = nF, jhi = -1;
            for (int j = 0; j < nF; j++) { int sz = __builtin_popcount(F[j]); if (sz + dg >= dlo && sz + dg <= dhi) { dom[0][h][j / 64] |= 1ull << (j % 64); if (j < jlo) jlo = j; jhi = j; } }
            if (jhi < 0) { wlo[h] = 0; whi[h] = 1; } else { wlo[h] = jlo / 64; whi[h] = jhi / 64 + 1; }
        }
        for (int a = 0; a < nA; a++) { int da = __builtin_popcount(Aadj[a]); cnt[a] = 0; cap[a] = dhi - 1 - da; need[a] = dlo - 1 - da; }
        if (eigprune || trirule) { if (!okcone) build_okcone(); for (int h = 0; h < nB; h++) for (int x = 0; x < W; x++) dom[0][h][x] &= okcone[x]; }
        nodes = 0; nsol = 0; outline[0] = 0;
        struct timespec t0, t1; timespec_get(&t0, TIME_UTC);
        nwin = 0; nprinted = 0; curidx = idx;
        int gr = (dlo == dhi) ? gale_ryser() : 1;
        if (gr) search(0);
        timespec_get(&t1, TIME_UTC);
        double us = (t1.tv_sec - t0.tv_sec) * 1e6 + (t1.tv_nsec - t0.tv_nsec) / 1e3;
        tot += us; if (us > tmax) tmax = us;
        if (nsol) nsat++; else nun++;
        printf("R %lld %lld %lld %lld %.0f%s\n", idx, nsol, nwin, nodes, us, gr ? "" : " GR");
        idx++;
        if (idx % 10000 == 0) fflush(stdout);
    }
    printf("#END n=%lld sat=%lld unsat=%lld total_s=%.3f max_us=%.0f\n", idx, nsat, nun, tot / 1e6, tmax);
    return 0;
}
