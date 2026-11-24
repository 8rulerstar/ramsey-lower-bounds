// stage1: enumerate all 2^21 graphs on 22 vertices on which Z11 acts with two orbits and no fixed point.
// Those with no K4 (red) and no independent 5-set (no blue K5) = the Z11-invariant (4,5,22)-graphs.
// Vertices (from 0): element a of orbit i = 11i+a. S_i = set of differences +-d (d=1..5) inside orbit i, T = set of differences (b-a) between the orbits.
// Output: one line "S1mask S2mask Tmask edges" per graph; counts by |S1|,|S2| on stderr. Usage: stage1 > L.txt
#include <stdio.h>
#include <stdint.h>
static uint32_t adj[22], cadj[22];
static const uint32_t ALL=(1u<<22)-1;
static int hasK4(const uint32_t *g){ // K4 through an orbit representative 0 or 11
    for(int ri=0;ri<2;ri++){ int r=ri*11; uint32_t N=g[r];
        for(uint32_t m=N;m;m&=m-1){ int u=__builtin_ctz(m);
            uint32_t nu=N&g[u]&~((2u<<u)-1);
            for(uint32_t m2=nu;m2;m2&=m2-1){ int v=__builtin_ctz(m2);
                if(nu&g[v]&~((2u<<v)-1)) return 1; } } }
    return 0; }
static int hasK5(const uint32_t *g){ // K5 through an orbit representative
    for(int ri=0;ri<2;ri++){ int r=ri*11; uint32_t N=g[r];
        for(uint32_t m=N;m;m&=m-1){ int u=__builtin_ctz(m);
            uint32_t nu=N&g[u]&~((2u<<u)-1);
            for(uint32_t m2=nu;m2;m2&=m2-1){ int v=__builtin_ctz(m2);
                uint32_t nv=nu&g[v]&~((2u<<v)-1);
                for(uint32_t m3=nv;m3;m3&=m3-1){ int w=__builtin_ctz(m3);
                    if(nv&g[w]&~((2u<<w)-1)) return 1; } } } }
    return 0; }
int main(void){
    long cnt=0, tab[6][6]={{0}}, pre=0;
    for(int s1=0;s1<32;s1++) for(int s2=0;s2<32;s2++) for(int t=0;t<2048;t++){
        for(int v=0;v<22;v++) adj[v]=0;
        for(int i=0;i<2;i++){ int s=i?s2:s1;
            for(int d=1;d<=5;d++) if(s>>(d-1)&1) for(int a=0;a<11;a++){
                int x=11*i+a, y=11*i+(a+d)%11; adj[x]|=1u<<y; adj[y]|=1u<<x; } }
        for(int d=0;d<11;d++) if(t>>d&1) for(int a=0;a<11;a++){
            int x=a, y=11+(a+d)%11; adj[x]|=1u<<y; adj[y]|=1u<<x; }
        for(int v=0;v<22;v++) cadj[v]=ALL&~adj[v]&~(1u<<v);
        pre++;
        if(hasK4(adj)) continue;
        if(hasK5(cadj)) continue;
        int e=0; for(int v=0;v<22;v++) e+=__builtin_popcount(adj[v]); e/=2;
        printf("%d %d %d %d\n",s1,s2,t,e); cnt++;
        tab[__builtin_popcount(s1)][__builtin_popcount(s2)]++;
    }
    fprintf(stderr,"candidates %ld  (4,5,22) graphs %ld\n",pre,cnt);
    for(int a=0;a<6;a++) for(int b=0;b<6;b++) if(tab[a][b]) fprintf(stderr,"|S1|=%d |S2|=%d : %ld\n",a,b,tab[a][b]);
    return 0; }
