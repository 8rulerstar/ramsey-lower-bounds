// check3: second checker, written separately from verify.c on 2026-11-10 by the same author (no shared code).
// Usage: ./check3 s t graph.txt   -> "OK3" iff no clique of size s and no independent set of size t.
// Plain byte adjacency matrix and int candidate lists; bound = greedy colouring of the candidate list.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 1024
static unsigned char a[N][N], m[N][N]; static int n, need; static long long cnt;
static int rec(int *cand, int nc, int size) {
    cnt++;
    if (size >= need) return 1;
    if (nc == 0) return 0;
    // per-call arrays on the heap (sized nc): keeps stack frames small for deep searches on large n
    int *col = malloc(sizeof(int) * nc), *order = malloc(sizeof(int) * nc), *csz = malloc(sizeof(int) * nc), ncol = 0, k = 0;
    static int cls[N][N];
    if (!col || !order || !csz) { puts("out of memory"); exit(2); }
    for (int i = 0; i < nc; i++) {              // greedy colouring: colour classes are independent in m
        int v = cand[i], c = 0;
        for (; c < ncol; c++) { int ok = 1; for (int j = 0; j < csz[c]; j++) if (m[v][cls[c][j]]) { ok = 0; break; } if (ok) break; }
        if (c == ncol) csz[ncol++] = 0;
        cls[c][csz[c]++] = v;
    }
    for (int c = 0; c < ncol; c++) for (int j = 0; j < csz[c]; j++) { order[k] = cls[c][j]; col[k++] = c + 1; }
    int res = 0;
    for (int i = nc - 1; i >= 0; i--) {
        if (size + col[i] < need) break;
        int v = order[i], *nw = malloc(sizeof(int) * (i + 1)), nn = 0;
        if (!nw) { puts("out of memory"); exit(2); }
        for (int j = 0; j < i; j++) if (m[v][order[j]]) nw[nn++] = order[j];
        int r = rec(nw, nn, size + 1); free(nw);
        if (r) { res = 1; break; }
    }
    free(col); free(order); free(csz);
    return res;
}
static int has(int k, int comp) {
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) m[i][j] = (i != j) && (comp ? !a[i][j] : a[i][j]);
    int all[N]; for (int i = 0; i < n; i++) all[i] = i;
    need = k; cnt = 0; return rec(all, n, 0);
}
int main(int argc, char **argv) {
    if (argc != 4) return 2;
    int s = atoi(argv[1]), t = atoi(argv[2]); FILE *f = fopen(argv[3], "r"); char row[N + 8];
    if (s < 1 || t < 1) { puts("bad s or t"); return 2; }
    if (!f || fscanf(f, "%d", &n) != 1 || n < 1 || n > N) { puts("bad input"); return 2; }
    for (int i = 0; i < n; i++) { if (fscanf(f, "%1030s", row) != 1 || (int)strlen(row) != n) { puts("bad row"); return 2; }
        for (int j = 0; j < n; j++) { if (row[j] != '0' && row[j] != '1') { puts("bad char"); return 2; } a[i][j] = row[j] == '1'; } }
    for (int i = 0; i < n; i++) { if (a[i][i]) { puts("loop"); return 2; } for (int j = 0; j < n; j++) if (a[i][j] != a[j][i]) { puts("asymmetric"); return 2; } }
    if (fscanf(f, "%1030s", row) == 1) { puts("trailing data"); return 2; }
    int c = has(s, 0); long long c1 = cnt; int d = c ? 0 : has(t, 1);
    if (c || d) { printf("FAIL3: %s found\n", c ? "clique" : "independent set"); return 1; }
    printf("OK3: n=%d no K%d (%lld nodes), no independent %d-set (%lld nodes)\n", n, s, c1, t, cnt); return 0;
}
