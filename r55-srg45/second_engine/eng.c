/* Independent gluing engine (written without reading src/glue_srg*.c).
   Search is over K-vertices: each k in V(K) gets its B-neighbourhood N_k (subset of 11 B vertices,
   |N_k| = 9 - deg_K k). No symmetry reduction. Conditions (A = w + K + B, w ~ all of K):
     K4-free : N_k triangle-free in B; for edge kk' of K, N_k & N_k' independent in B.
     I5-free : nonedge kk': B \ (N_k|N_k') has no independent 3-set;
               independent triple of K: complement of union is a clique of B;
               independent 4-set of K: union = V(B).
     degrees : each h in B gets exactly 10 - deg_B h neighbours in K.
   Window test: cyclic Jacobi eigenvalues, accept lmin >= s - 1e-7 and l2 <= r + 1e-7.
   Usage: eng K.g6 < Blines ; prints "R idx nsol nwin" and "W idx g6" lines. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

static int nK, nB, bK[16], bB[16];
static unsigned char triF[2048], indep[2048], noI3[2048], clique[2048];
static int needK[16], needB[16], ord[16], pos[16];
static int cand[16][2048], ncand[16];
static int N[16], cnt[16];
static int i3[200][3], ni3, i4[300][4], ni4;
static long nsol, nwin;
static unsigned char kI2[1024],kI3[1024],kI4[1024];static int bpairs[64][2],nbp,btr[200][3],nbt;
static int curidx;

static int g6read(const char *s, int *adj) {
    int n = s[0] - 63, k = 0;
    for (int i = 0; i < n; i++) adj[i] = 0;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++, k++) {
        int v = s[1 + k / 6] - 63;
        if ((v >> (5 - k % 6)) & 1) { adj[i] |= 1 << j; adj[j] |= 1 << i; }
    }
    return n;
}
static void g6write(int n, int A[22][22], char *o) {
    int k = 0, v = 0, p = 0; o[p++] = 63 + n;
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
        v = (v << 1) | A[i][j]; if (++k == 6) { o[p++] = 63 + v; k = v = 0; }
    }
    if (k) o[p++] = 63 + (v << (6 - k));
    o[p] = 0;
}

static void jacobi(double a[22][22], int n, double *ev) {
    for (int sweep = 0; sweep < 100; sweep++) {
        double off = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) off += a[i][j] * a[i][j];
        if (off < 1e-26) break;
        for (int p = 0; p < n; p++) for (int q = p + 1; q < n; q++) {
            if (fabs(a[p][q]) < 1e-300) continue;
            double th = (a[q][q] - a[p][p]) / (2 * a[p][q]);
            double t = (th >= 0 ? 1 : -1) / (fabs(th) + sqrt(th * th + 1));
            double c = 1 / sqrt(t * t + 1), s = t * c;
            for (int k = 0; k < n; k++) {
                double akp = a[k][p], akq = a[k][q];
                a[k][p] = c * akp - s * akq; a[k][q] = s * akp + c * akq;
            }
            for (int k = 0; k < n; k++) {
                double apk = a[p][k], aqk = a[q][k];
                a[p][k] = c * apk - s * aqk; a[q][k] = s * apk + c * aqk;
            }
        }
    }
    for (int i = 0; i < n; i++) ev[i] = a[i][i];
}
static int dcmp(const void *x, const void *y) { double a = *(double *)x, b = *(double *)y; return a < b ? -1 : a > b; }

static int check_direct(int A[22][22]){
  int a[22];for(int i=0;i<22;i++){a[i]=0;for(int j=0;j<22;j++)if(A[i][j])a[i]|=1<<j;}
  for(int i=0;i<22;i++)for(int j=i+1;j<22;j++)if(a[i]>>j&1){int c=a[i]&a[j]&~((2<<j)-1);
    while(c){int k=__builtin_ctz(c);c&=c-1;if(a[i]&a[j]&a[k]&~((2<<k)-1))return 0;}}
  for(int i=0;i<22;i++){int r1=~a[i]&~((2<<i)-1)&0x3fffff;
    while(r1){int j=__builtin_ctz(r1);r1&=r1-1;int r2=r1&~a[j];
      while(r2){int k=__builtin_ctz(r2);r2&=r2-1;int r3=r2&~a[k];
        while(r3){int l=__builtin_ctz(r3);r3&=r3-1;if(r3&~a[l])return 0;}}}}
  return 1;
}
static void solution(void) {
    int A[22][22]; memset(A, 0, sizeof A);
    for (int k = 0; k < nK; k++) { A[0][1 + k] = A[1 + k][0] = 1;
        for (int j = 0; j < nK; j++) if (bK[k] >> j & 1) A[1 + k][1 + j] = 1;
        for (int h = 0; h < nB; h++) if (N[k] >> h & 1) A[1 + k][11 + h] = A[11 + h][1 + k] = 1; }
    for (int h = 0; h < nB; h++) for (int j = 0; j < nB; j++) if (bB[h] >> j & 1) A[11 + h][11 + j] = 1;
    for (int i = 0; i < 22; i++) { int d = 0; for (int j = 0; j < 22; j++) d += A[i][j];
        if (d != 10) { fprintf(stderr, "degree bug\n"); exit(3); } }
    if(!check_direct(A)){fprintf(stderr,"K4/I5 bug\n");exit(4);}
    nsol++;
    double a[22][22], ev[22];
    for (int i = 0; i < 22; i++) for (int j = 0; j < 22; j++) a[i][j] = A[i][j];
    jacobi(a, 22, ev); qsort(ev, 22, sizeof(double), dcmp);
    double s = (-1 - sqrt(45.)) / 2, r = (-1 + sqrt(45.)) / 2;
    if (ev[0] >= s - 1e-7 && ev[20] <= r + 1e-7) {
        char o[100]; g6write(22, A, o); nwin++;
        printf("W %d %s %.9f %.9f\n", curidx, o, ev[0], ev[20]);
    }
}


#define W 8
typedef unsigned long long u64;
static u64 compat[10][10][512][W], hasH[10][11][W];
static int asg[16];
static int ccount(u64 *d){int c=0;for(int i=0;i<W;i++)c+=__builtin_popcountll(d[i]);return c;}
static int anyand(u64 *a,u64 *b){for(int i=0;i<W;i++)if(a[i]&b[i])return 1;return 0;}
static void build_compat(void){
  for(int k=0;k<nK;k++)for(int h=0;h<nB;h++){memset(hasH[k][h],0,sizeof hasH[k][h]);
    for(int c=0;c<ncand[k];c++)if(cand[k][c]>>h&1)hasH[k][h][c>>6]|=1ULL<<(c&63);}
  int full=(1<<nB)-1;
  for(int k=0;k<nK;k++)for(int j=0;j<nK;j++)if(j!=k){int e=bK[k]>>j&1;
    for(int c=0;c<ncand[k];c++){u64*o=compat[k][j][c];memset(o,0,W*8);int m=cand[k][c];
      for(int d=0;d<ncand[j];d++){int q=cand[j][d];
        if(e?indep[m&q]:noI3[full&~(m|q)])o[d>>6]|=1ULL<<(d&63);}}}
}
static void dfs2(int lv,u64 D[16][W]){
  if(lv==nK){for(int k=0;k<nK;k++)N[k]=asg[k];solution();return;}
  int k=-1,best=1<<30;
  for(int j=0;j<nK;j++)if(asg[j]<0){int c=ccount(D[j]);if(c<best){best=c;k=j;}}
  if(best==0)return;
  for(int w=0;w<W;w++){u64 bits=D[k][w];while(bits){int c=w*64+__builtin_ctzll(bits);bits&=bits-1;
    int m=cand[k][c];asg[k]=m;int ok=1;
    for(int h=0;h<nB;h++)cnt[h]+=m>>h&1;
    /* triple and 4-set checks for fully assigned sets */
    for(int t=0;t<ni3&&ok;t++){int a=i3[t][0],b=i3[t][1],d=i3[t][2];
      if((a==k||b==k||d==k)&&asg[a]>=0&&asg[b]>=0&&asg[d]>=0&&!clique[((1<<nB)-1)&~(asg[a]|asg[b]|asg[d])])ok=0;}
    for(int t=0;t<ni4&&ok;t++){int*q=i4[t],in=0,all=1;
      for(int u=0;u<4;u++){if(q[u]==k)in=1;if(asg[q[u]]<0)all=0;}
      if(in&&all&&(asg[q[0]]|asg[q[1]]|asg[q[2]]|asg[q[3]])!=(1<<nB)-1)ok=0;}
    u64 ND[16][W];
    if(ok)for(int j=0;j<nK&&ok;j++)if(asg[j]<0){
      for(int i=0;i<W;i++)ND[j][i]=D[j][i]&compat[k][j][c][i];
      for(int h=0;h<nB;h++)if(cnt[h]==needB[h])for(int i=0;i<W;i++)ND[j][i]&=~hasH[j][h][i];
      {int full=(1<<nB)-1;
       for(int t=0;t<ni3;t++){int*q=i3[t],o=-1,na=0,U=0;for(int u=0;u<3;u++){if(q[u]==j)o=u;else if(asg[q[u]]>=0){na++;U|=asg[q[u]];}}
         if(o<0||na<2)continue;
         for(int i=0;i<W;i++){u64 b=ND[j][i];while(b){int d=i*64+__builtin_ctzll(b);b&=b-1;if(!clique[full&~(U|cand[j][d])])ND[j][i]&=~(1ULL<<(d&63));}}}
       for(int t=0;t<ni4;t++){int*q=i4[t],o=-1,na=0,U=0;for(int u=0;u<4;u++){if(q[u]==j)o=u;else if(asg[q[u]]>=0){na++;U|=asg[q[u]];}}
         if(o<0||na<3)continue;
         for(int i=0;i<W;i++){u64 b=ND[j][i];while(b){int d=i*64+__builtin_ctzll(b);b&=b-1;if(((U|cand[j][d])&full)!=full)ND[j][i]&=~(1ULL<<(d&63));}}}}
      if(!ccount(ND[j]))ok=0;}
    if(ok&&lv<ACL)for(int j=0;j<nK&&ok;j++)if(asg[j]<0){
      for(int j2=0;j2<nK;j2++)if(j2!=j&&asg[j2]<0){
        for(int i=0;i<W;i++){u64 b=ND[j][i];while(b){int d=i*64+__builtin_ctzll(b);b&=b-1;if(!anyand(compat[j][j2][d],ND[j2]))ND[j][i]&=~(1ULL<<(d&63));}}}
      if(!ccount(ND[j]))ok=0;}
    if(ok)for(int h=0;h<nB&&ok;h++){int av=0;
      for(int j=0;j<nK;j++)if(asg[j]<0&&anyand(ND[j],hasH[j][h]))av++;
      int must=0;for(int j=0;j<nK;j++)if(asg[j]<0){int all=1;for(int i=0;i<W;i++)if(ND[j][i]&~hasH[j][h][i]){all=0;break;}must+=all;}
      if(needB[h]-cnt[h]>av||cnt[h]+must>needB[h])ok=0;}
    if(ok){int P[16],fk=(1<<nK)-1;
      for(int h=0;h<nB;h++){P[h]=0;for(int j=0;j<nK;j++){if(asg[j]>=0){if(asg[j]>>h&1)P[h]|=1<<j;}else if(anyand(ND[j],hasH[j][h]))P[h]|=1<<j;}
        if(!kI4[fk&~P[h]]){ok=0;break;}}
      for(int t=0;t<nbp&&ok;t++)if(!kI3[fk&~(P[bpairs[t][0]]|P[bpairs[t][1]])])ok=0;
      for(int t=0;t<nbt&&ok;t++)if(!kI2[fk&~(P[btr[t][0]]|P[btr[t][1]]|P[btr[t][2]])])ok=0;}
    if(ok)dfs2(lv+1,ND);
    for(int h=0;h<nB;h++)cnt[h]-=m>>h&1;
    asg[k]=-1;}}
}
static void dfs(int lv){(void)lv;
  build_compat();u64 D[16][W];memset(D,0,sizeof D);
  for(int k=0;k<nK;k++){asg[k]=-1;for(int c=0;c<ncand[k];c++)D[k][c>>6]|=1ULL<<(c&63);}
  dfs2(0,D);}
int main(int argc, char **argv) {
    char line[256];
    FILE *f = fopen(argv[1], "r"); if (!f || !fgets(line, 256, f)) return 1; fclose(f);
    nK = g6read(line, bK);
    ni3 = ni4 = 0;
    for (int a = 0; a < nK; a++) for (int b = a + 1; b < nK; b++) if (!(bK[a] >> b & 1))
        for (int c = b + 1; c < nK; c++) if (!(bK[a] >> c & 1) && !(bK[b] >> c & 1)) {
            i3[ni3][0] = a; i3[ni3][1] = b; i3[ni3][2] = c; ni3++;
            for (int d = c + 1; d < nK; d++) if (!((bK[a] | bK[b] | bK[c]) >> d & 1)) {
                i4[ni4][0] = a; i4[ni4][1] = b; i4[ni4][2] = c; i4[ni4][3] = d; ni4++; }
        }
    for(int m=0;m<(1<<nK);m++){int i2=1,i3=1,i4=1;
      for(int a=0;a<nK;a++)if(m>>a&1)for(int b=a+1;b<nK;b++)if((m>>b&1)&&!(bK[a]>>b&1)){i2=0;
        for(int c=b+1;c<nK;c++)if((m>>c&1)&&!((bK[a]|bK[b])>>c&1)){i3=0;
          for(int d=c+1;d<nK;d++)if((m>>d&1)&&!((bK[a]|bK[b]|bK[c])>>d&1))i4=0;}}
      kI2[m]=i2;kI3[m]=i3;kI4[m]=i4;}
    for (int k = 0; k < nK; k++) needK[k] = 9 - __builtin_popcount(bK[k]);
    /* order: greedy, highest degree first then most K-edges to placed vertices */
    int used = 0;
    for (int l = 0; l < nK; l++) { int best = -1, bs = -1;
        for (int k = 0; k < nK; k++) if (!(used >> k & 1)) {
            int sc = 10 * __builtin_popcount(bK[k] & used) + __builtin_popcount(bK[k]);
            if (sc > bs) { bs = sc; best = k; } }
        ord[l] = best; pos[best] = l; used |= 1 << best; }
    int idx = 0;
    while (fgets(line, 256, stdin)) {
        if (line[0] < 63) continue;
        nB = g6read(line, bB);
        for (int m = 0; m < (1 << nB); m++) {
            int t = 1, in = 1, i3f = 1, cl = 1;
            for (int a = 0; a < nB; a++) if (m >> a & 1) for (int b = a + 1; b < nB; b++) if (m >> b & 1) {
                int ab = bB[a] >> b & 1;
                if (ab) in = 0; else cl = 0;
                for (int c = b + 1; c < nB; c++) if (m >> c & 1) {
                    if (ab && (bB[a] >> c & 1) && (bB[b] >> c & 1)) t = 0;
                    if (!ab && !(bB[a] >> c & 1) && !(bB[b] >> c & 1)) i3f = 0;
                }
            }
            triF[m] = t; indep[m] = in; noI3[m] = i3f; clique[m] = cl;
        }
        nbp=nbt=0;for(int a=0;a<nB;a++)for(int b=a+1;b<nB;b++)if(!(bB[a]>>b&1)){bpairs[nbp][0]=a;bpairs[nbp][1]=b;nbp++;
          for(int c=b+1;c<nB;c++)if(!((bB[a]|bB[b])>>c&1)){btr[nbt][0]=a;btr[nbt][1]=b;btr[nbt][2]=c;nbt++;}}
        for (int h = 0; h < nB; h++) needB[h] = 10 - __builtin_popcount(bB[h]);
        for (int k = 0; k < nK; k++) { ncand[k] = 0;
            for (int m = 0; m < (1 << nB); m++)
                if (__builtin_popcount(m) == needK[k] && triF[m]) cand[k][ncand[k]++] = m; }
        memset(cnt, 0, sizeof cnt); nsol = nwin = 0; curidx = idx;
        dfs(0);
        printf("R %d %ld %ld\n", idx, nsol, nwin); fflush(stdout);
        idx++;
    }
    return 0;
}
