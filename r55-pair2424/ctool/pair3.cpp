// pair3: pair.cpp run with u-side state reuse (UP of u-only literals saved per placement i), fast v-side bitsets, sharding.
// modes: prof AUT c maxN | run AUT c OUT [k K] [maxN]  (k-th of K contiguous shards of the unordered enumeration of class size c)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <climits>
#include <string>
#include <vector>
#include <array>
#include <map>
#include <unordered_map>
#include <fstream>
#include <chrono>
using namespace std; typedef uint64_t u64;
const int n=45; int NV=45;
vector<array<u64,24>> GR;
struct Cls{int c; vector<vector<int>> G; vector<int> pgi,pa; vector<vector<int>> pK; vector<int> pH; vector<vector<int>> Hs;};
vector<Cls> CL;
void load(const char*p){ifstream f(p); string t; int ng; f>>t>>ng; GR.resize(ng);
 for(auto&g:GR) for(int x=0;x<24;x++) f>>g[x];
 int nc; f>>t>>nc; CL.resize(nc);
 for(auto&k:CL){int ngr,np; f>>t>>k.c>>ngr>>np; k.G.assign(ngr,vector<int>(k.c));
  for(auto&p:k.G) for(auto&x:p) f>>x;
  map<vector<int>,int> hid;
  for(int i=0;i<np;i++){int gi,a,h; f>>gi>>a; vector<int> K(k.c); for(auto&x:K) f>>x; f>>h; vector<int> H(h); for(auto&x:H) f>>x;
   k.pgi.push_back(gi); k.pa.push_back(a); k.pK.push_back(K);
   auto it=hid.find(H); if(it==hid.end()){it=hid.emplace(H,k.Hs.size()).first; k.Hs.push_back(H);} k.pH.push_back(it->second);}}
}
static inline bool tri(const u64*A,u64 S){
 u64 s=S; while(s){int a=__builtin_ctzll(s); s&=s-1; u64 T=A[a]&s; while(T){int b=__builtin_ctzll(T); T&=T-1; if(A[b]&T) return true;}} return false;}
long mism=0; bool DBG=getenv("DBG"),SLOW=getenv("SLOW");
// identical to pair.cpp propagate
long stg[8];
bool propagate(u64*R,u64*B){
 for(int x=0;x<n;x++) for(u64 s=R[x]>>(x+1)<<(x+1);s;s&=s-1){int y=__builtin_ctzll(s); if(tri(R,R[x]&R[y])) {stg[0]++;return true;}}
 for(int x=0;x<n;x++) for(u64 s=B[x]>>(x+1)<<(x+1);s;s&=s-1){int y=__builtin_ctzll(s); if(tri(B,B[x]&B[y])) {stg[1]++;return true;}}
 const u64 ALL=(NV==64?~0ULL:(1ULL<<NV)-1); bool ch=true; int sw=0;
 while(ch){ch=false; sw++;
  for(int x=0;x<n;x++){u64 fr=ALL&~R[x]&~B[x]&~((2ULL<<x)-1);
   for(;fr;fr&=fr-1){int y=__builtin_ctzll(fr);
    bool nr=tri(R,R[x]&R[y]), nb=tri(B,B[x]&B[y]);
    if(nr&&nb) {stg[min(sw+1,7)]++; return true;}
    if(nr){B[x]|=1ULL<<y;B[y]|=1ULL<<x;ch=true;} else if(nb){R[x]|=1ULL<<y;R[y]|=1ULL<<x;ch=true;}
   }}}
 return false;}
// fast equivalent of propagate for a merged placement state: only u-only x v-only pairs are free
// (other unassigned pairs touch unused slots whose adjacency stays empty, so they are never forced).
// mono K5 among assigned edges: one inside Vv+{1} is excluded by the per-j check, any other contains a u-only vertex.
bool k5check(const u64*R,const u64*B,u64 Uo){
 for(u64 s=Uo;s;s&=s-1){int x=__builtin_ctzll(s); for(u64 t=R[x];t;t&=t-1){int y=__builtin_ctzll(t); if(tri(R,R[x]&R[y])) return true;}
  for(u64 t=B[x];t;t&=t-1){int y=__builtin_ctzll(t); if(tri(B,B[x]&B[y])) return true;}} return false;}
// mono K5 containing assigned pair (p,q) and at least one vertex of Uo
static inline bool k5pairU(const u64*A,int p,int q,u64 Uo){u64 S=A[p]&A[q]; for(u64 s=S&Uo;s;s&=s-1){int a=__builtin_ctzll(s); u64 T=A[a]&S; while(T){int b=__builtin_ctzll(T); T&=T-1; if(A[b]&T) return true;}} return false;}
bool propfast(u64*R,u64*B,u64 Uo,u64 Vo,bool pre=true){
 if(pre) for(u64 s=Uo;s;s&=s-1){int x=__builtin_ctzll(s); for(u64 t=R[x];t;t&=t-1){int y=__builtin_ctzll(t); if(tri(R,R[x]&R[y])) {stg[0]++;return true;}}
  for(u64 t=B[x];t;t&=t-1){int y=__builtin_ctzll(t); if(tri(B,B[x]&B[y])) {stg[1]++;return true;}}}
 bool ch=true; int sw=0;
 while(ch){ch=false; sw++;
  for(u64 s=Uo;s;s&=s-1){int x=__builtin_ctzll(s); u64 fr=Vo&~R[x]&~B[x];
   for(;fr;fr&=fr-1){int y=__builtin_ctzll(fr);
    bool nr=tri(R,R[x]&R[y]), nb=tri(B,B[x]&B[y]);
    if(nr&&nb) {stg[min(sw+1,5)]++; return true;}
    if(nr){B[x]|=1ULL<<y;B[y]|=1ULL<<x;ch=true;} else if(nb){R[x]|=1ULL<<y;R[y]|=1ULL<<x;ch=true;}
   }}}
 return false;}
void fromF(const char*F,u64*R,u64*B){for(int i=0;i<n;i++){R[i]=B[i]=0; for(int j=0;j<n;j++) if(i!=j){if(F[i*n+j]=='1')R[i]|=1ULL<<j; else if(F[i*n+j]=='0')B[i]|=1ULL<<j;}}}
// identical to pair.cpp build; wmax=1 -> u side only
void build(int c,int gi,int a,const vector<int>&Ku,int hj,int b,const vector<int>&Kvg,char*F,int wmax=2){
 int m=23-c; int mu[24],mv[24]; for(int x=0;x<24;x++)mu[x]=mv[x]=-1;
 mu[a]=1; for(int t=0;t<c;t++) mu[Ku[t]]=2+t; int i=0; for(int x=0;x<24;x++) if(mu[x]<0) mu[x]=2+c+i++;
 if(wmax==2){mv[b]=0; for(int t=0;t<c;t++) mv[Kvg[t]]=2+t; i=0; for(int y=0;y<24;y++) if(mv[y]<0) mv[y]=2+c+m+i++;}
 memset(F,'.',n*n); for(int k=0;k<n;k++) F[k*n+k]='0';
 for(int w=0;w<wmax;w++){auto&G=GR[w?hj:gi]; int*mm=w?mv:mu;
  for(int x=0;x<n;x++) if(x!=w) F[w*n+x]=F[x*n+w]='0';
  for(int x=0;x<24;x++){F[w*n+mm[x]]=F[mm[x]*n+w]='1'; for(int y=0;y<24;y++) if(x!=y){char e=(G[x]>>y&1)?'1':'0'; char&d=F[mm[x]*n+mm[y]]; if(w==1&&mm[x]>=2&&mm[y]>=2&&d!='.'&&d!=e) mism++; d=e;}}}
}
int main(int argc,char**argv){
 if(argc<3||(argc<4&&string(argv[1])!="check")){fprintf(stderr,"usage: p3_pair3 check FILE | prof AUT c maxN | run AUT c OUT [k K] [maxN]\n");return 1;}
 string md=argv[1];
 if(md=="check"){ if(getenv("NV")) NV=atoi(getenv("NV")); ifstream f(argv[2]); string s; int k=0,nc=0; // same as pair.cpp check
  while(getline(f,s)){ if(s.size()!=n*n) continue; u64 R[n],B[n]; fromF(s.data(),R,B); bool cf=propagate(R,B); printf("%d %s\n",k,cf?"UNSAT":"OPEN"); nc+=cf; k++;}
  fprintf(stderr,"check n=%d conflict=%d\n",k,nc); return 0;}
 load(argv[2]); int c=atoi(argv[3]); int m=23-c;
 bool prof=md=="prof"; long maxN=LONG_MAX; int sk=0,SK=1; FILE*out=nullptr;
 if(prof) maxN=atol(argv[4]); else { out=fopen(argv[4],"w"); if(argc>6){sk=atoi(argv[5]);SK=atoi(argv[6]);} if(argc>7) maxN=atol(argv[7]); }
 // pass 1: total count (for shard ranges)
 long total=0; struct DC{vector<int> id,reps;};
 vector<vector<int>> INV(CL.size()); vector<map<pair<int,int>,DC>> DCC(CL.size()); vector<vector<int>> GINV(CL.size()); // GINV[ci][x*c+s]
 for(size_t ci=0;ci<CL.size();ci++){auto&K=CL[ci]; if(K.c!=c) continue;
  int g=K.G.size(); unordered_map<u64,int> gid; auto key=[&](const vector<int>&p){u64 h=0; for(int x:p) h=h*16+x; return h;};
  for(int i=0;i<g;i++) gid[key(K.G[i])]=i;
  auto&inv=INV[ci]; inv.resize(g); GINV[ci].resize((size_t)g*c);
  for(int i=0;i<g;i++){vector<int> q(c); for(int t=0;t<c;t++){q[K.G[i][t]]=t;} inv[i]=gid[key(q)]; for(int s=0;s<c;s++) GINV[ci][(size_t)i*c+s]=q[s];}
  vector<int> mul((size_t)g*g); for(int i=0;i<g;i++)for(int j=0;j<g;j++){vector<int> q(c); for(int t=0;t<c;t++) q[t]=K.G[i][K.G[j][t]]; mul[(size_t)i*g+j]=gid[key(q)];}
  int np=K.pgi.size();
  for(int i=0;i<np;i++) for(int j=i;j<np;j++){auto kk=make_pair(K.pH[j],K.pH[i]); auto it=DCC[ci].find(kk);
   if(it==DCC[ci].end()){DC d; d.id.assign(g,-1); for(int x=0;x<g;x++) if(d.id[x]<0){int k=d.reps.size(); d.reps.push_back(x);
     for(int a:K.Hs[kk.first]) for(int b:K.Hs[kk.second]) d.id[mul[(size_t)mul[(size_t)a*g+x]*g+b]]=k;}
    it=DCC[ci].emplace(kk,move(d)).first;}
   auto&d=it->second; for(int k=0;k<(int)d.reps.size();k++){int x=d.reps[k]; if(i==j && d.id[inv[x]]<k) continue; total++;}}}
 long lim=min(total,maxN); long lo=lim*sk/SK, hi=lim*(sk+1)/SK;
 fprintf(stderr,"c=%d total=%ld range [%ld,%ld)\n",c,total,lo,hi);
 const u64 ALL=(1ULL<<n)-1; u64 Uo=0,Vo=0; for(int t=2+c;t<2+c+m;t++) Uo|=1ULL<<t; for(int t=2+c+m;t<2+c+2*m;t++) Vo|=1ULL<<t;
 u64 Vv=1ULL; for(int t=0;t<c;t++) Vv|=1ULL<<(2+t); for(int t=2+c+m;t<2+c+2*m;t++) Vv|=1ULL<<t; // v-side vertex set
 long idx=0,conf=0,open_=0,uconf=0; double tb=0,tp=0; auto T0=chrono::steady_clock::now(); char F[n*n];
 for(size_t ci=0;ci<CL.size();ci++){auto&K=CL[ci]; if(K.c!=c) continue; auto&inv=INV[ci]; int np=K.pgi.size();
  // per j: base v-side rows with x=identity (graph vertex pK[j][s] -> slot 2+s)
  vector<array<u64,n>> VB(np);
  for(int j=0;j<np;j++){int mv[24]; for(int y=0;y<24;y++) mv[y]=-1; mv[K.pa[j]]=0; for(int t=0;t<c;t++) mv[K.pK[j][t]]=2+t; int q=0; for(int y=0;y<24;y++) if(mv[y]<0) mv[y]=2+c+m+q++;
   auto&G=GR[K.pgi[j]]; auto&V=VB[j]; V.fill(0); for(int x=0;x<24;x++) for(int y=0;y<24;y++) if(G[x]>>y&1) V[mv[x]]|=1ULL<<mv[y];}
  vector<char> vbad(np,0); // mono K5 inside v structure (Vv+{1}) for this j
  for(int j=0;j<np;j++){u64 R[n],B[n]; memset(R,0,sizeof R); memset(B,0,sizeof B); auto&V=VB[j];
   for(int p=0;p<n;p++) if(Vv>>p&1){R[p]=V[p]|2; B[p]=Vv&~V[p]&~(1ULL<<p);} R[1]=Vv;
   for(int x=0;x<n&&!vbad[j];x++) for(u64 t=R[x];t;t&=t-1){int y=__builtin_ctzll(t); if(tri(R,R[x]&R[y])){vbad[j]=1;break;}}
   for(int x=0;x<n&&!vbad[j];x++) for(u64 t=B[x];t;t&=t-1){int y=__builtin_ctzll(t); if(tri(B,B[x]&B[y])){vbad[j]=1;break;}}}
  // phase-A tables (base coordinates): subsets of K (bits 0..c-1) plus vertex 0 (bit c); TT[j][S]: bit0 red triangle, bit1 blue triangle in v graph
  int NS=1<<(c+1); vector<vector<uint8_t>> TT(np); vector<array<uint16_t,24>> VR(np),VBl(np);
  for(int j=0;j<np;j++){auto&V=VB[j]; u64 cm=(1ULL<<c)-1; int Nr[13],Nb[13];
   auto toidx=[&](u64 r){return (int)(((r>>2)&cm)|((r&1)<<c));};
   for(int s2=0;s2<c;s2++){Nr[s2]=toidx(V[2+s2]); Nb[s2]=toidx(Vv&~V[2+s2]&~(1ULL<<(2+s2)))&(int)cm;} Nr[c]=toidx(V[0]); Nb[c]=0; // 0 blue to K? from v graph
   for(int s2=0;s2<c;s2++) if(!(V[0]>>(2+s2)&1)) {Nb[c]|=1<<s2; Nb[s2]|=1<<c;}
   auto&T=TT[j]; T.assign(NS,0);
   for(int S=1;S<NS;S++){int v=__builtin_ctz(S),P=S&(S-1); uint8_t r=T[P];
    auto has=[&](int A,const int*N){for(int a=A;a;a&=a-1){int u=__builtin_ctz(a); if(N[u]&A) return true;} return false;};
    if(!(r&1) && has(Nr[v]&P,Nr)) r|=1; if(!(r&2) && has(Nb[v]&P,Nb)) r|=2;
    if(!(r&4) && (T[Nr[v]&P]&1)) r|=4; if(!(r&8) && (T[Nb[v]&P]&2)) r|=8; if(Nr[v]&P) r|=16; if(Nb[v]&P) r|=32; T[S]=r;}
   for(int q=0;q<m;q++){int y=2+c+m+q; VR[j][q]=toidx(V[y]); VBl[j][q]=toidx(Vv&~V[y]&~(1ULL<<y))&(int)cm;}}
  for(int i=0;i<np;i++){
   // count placements of i in range first
   long cnt_i=0; for(int j=i;j<np;j++){auto&d=DCC[ci][{K.pH[j],K.pH[i]}]; for(int k=0;k<(int)d.reps.size();k++){if(i==j && d.id[inv[d.reps[k]]]<k) continue; cnt_i++;}}
   if(idx+cnt_i<=lo || idx>=hi){idx+=cnt_i; continue;}
   // u-state: u literals outside region overwritten by v side (row/col 1, pairs inside Vv)
   u64 RU[n],BU[n]; build(c,K.pgi[i],K.pa[i],K.pK[i],0,0,K.pK[i],F,1); fromF(F,RU,BU);
   for(int p=0;p<n;p++){u64 msk=(p==1)?ALL:((Vv>>p&1)?(Vv|2):2); RU[p]&=~msk; BU[p]&=~msk;}
   bool ucf=prof||DBG?false:propagate(RU,BU);
   if(!ucf && !prof && !DBG){ // K5 with a Uo vertex and no assigned pair inside K+{0}: same for every (j,x) of this i
    u64 R[n],B[n]; build(c,K.pgi[i],K.pa[i],K.pK[i],0,0,K.pK[i],F,1); fromF(F,R,B);
    for(int p=0;p<n;p++){u64 msk=(p==1)?ALL:((Vv>>p&1)?(Vv|2):2); R[p]&=~msk; B[p]&=~msk;}
    u64 b1=ALL&~Vv&~2ULL; R[1]=Vv; B[1]=b1; for(int p=0;p<n;p++){ if(Vv>>p&1) R[p]|=2; else if(p!=1) B[p]|=2;}
    if(k5check(R,B,Uo)) ucf=true;}
   // Uo-internal red/blue edges and triangles (u literals), for K5s with a Uo vertex and >=2 vertices of K+{0}
   vector<pair<int,int>> ER,EB; vector<array<int,3>> TR3,TB3;
   for(int q=0;q<m;q++) for(int w=q+1;w<m;w++){int a=2+c+q,b=2+c+w;
    if(RU[a]>>b&1){ER.push_back({q,w}); for(int z=w+1;z<m;z++) if((RU[a]>>(2+c+z)&1)&&(RU[b]>>(2+c+z)&1)) TR3.push_back({q,w,z});}
    if(BU[a]>>b&1){EB.push_back({q,w}); for(int z=w+1;z<m;z++) if((BU[a]>>(2+c+z)&1)&&(BU[b]>>(2+c+z)&1)) TB3.push_back({q,w,z});}}
   for(int j=i;j<np;j++){auto&d=DCC[ci][{K.pH[j],K.pH[i]}];
    for(int k=0;k<(int)d.reps.size();k++){int x=d.reps[k]; if(i==j && d.id[inv[x]]<k) continue;
     long me=idx++; if(me<lo) continue; if(me>=hi) goto done;
     if(prof){ // old path, split timing
      auto t0=chrono::steady_clock::now();
      vector<int> Kvg(c); for(int t=0;t<c;t++) Kvg[t]=K.pK[j][K.G[x][t]];
      build(c,K.pgi[i],K.pa[i],K.pK[i],K.pgi[j],K.pa[j],Kvg,F); u64 R[n],B[n]; fromF(F,R,B);
      auto t1=chrono::steady_clock::now(); bool cf=propagate(R,B); auto t2=chrono::steady_clock::now();
      tb+=chrono::duration<double>(t1-t0).count(); tp+=chrono::duration<double>(t2-t1).count(); cf?conf++:open_++; continue;}
     bool cf;
     if(ucf){cf=true; uconf++;}
     else {
      // permutation of K slots: base slot 2+s -> 2+ginv_x(s)
      const int*gv=&GINV[ci][(size_t)x*c]; int pm[n]; for(int p=0;p<n;p++) pm[p]=p; for(int s=0;s<c;s++) pm[2+s]=2+gv[s];
      auto&V=VB[j]; u64 R[n],B[n]; memcpy(R,RU,sizeof R); memcpy(B,BU,sizeof B); cf=false;
      for(int p=0;p<n;p++){ if(!(Vv>>p&1)) continue; u64 r=V[p], rr=r&~(0xFFFULL<<2); for(int s=0;s<c;s++) if(r>>(2+s)&1) rr|=1ULL<<pm[2+s];
       int q=pm[p]; u64 rv=rr|2, bv=Vv&~rr&~(1ULL<<q);
       if((R[q]&bv)|(B[q]&rv)){cf=true;break;} R[q]|=rv; B[q]|=bv;}
      if(!cf){ u64 b1=ALL&~Vv&~2ULL; if(B[1]&Vv || R[1]&b1) cf=true; else {R[1]|=Vv; B[1]|=b1; for(int p=0;p<n;p++) if(p!=1 && !(Vv>>p&1)){ if(R[p]&2){cf=true;break;} B[p]|=2;}}}
      if(DBG){vector<int> Kvg(c); for(int t=0;t<c;t++) Kvg[t]=K.pK[j][K.G[x][t]]; build(c,K.pgi[i],K.pa[i],K.pK[i],K.pgi[j],K.pa[j],Kvg,F); u64 R2[n],B2[n]; fromF(F,R2,B2);
       fprintf(stderr,"cf=%d\n",cf); for(int p=0;p<n;p++) if(R[p]!=R2[p]||B[p]!=B2[p]) fprintf(stderr,"row %d R %llx/%llx B %llx/%llx\n",p,R[p],R2[p],B[p],B2[p]); exit(0);}
      if(!cf){ if(vbad[j]||SLOW) cf=propagate(R,B);
       if(cf||vbad[j]||SLOW){}
       else { // phase A on the merged state: all free pairs are u-only x v-only, common nbhds lie in K+{0}
        int ip[16]; for(int s2=0;s2<c;s2++) ip[gv[s2]]=s2; uint16_t ur[24],ub[24]; u64 Km=((1ULL<<c)-1)<<2;
        for(int q=0;q<m;q++){int xx=2+c+q; u64 r=R[xx]&Km,b=B[xx]&Km; int a=(R[xx]&1)<<c,bb=0;
         for(;r;r&=r-1) a|=1<<ip[__builtin_ctzll(r)-2]; for(;b;b&=b-1) bb|=1<<ip[__builtin_ctzll(b)-2]; ur[q]=a; ub[q]=bb;}
        const uint8_t*T=TT[j].data();
        // mono K5 with a Uo vertex and >=2 vertices in K+{0} (others: <=1 such vertex, checked per i; none: vbad)
        for(int q=0;q<m&&!cf;q++) if((T[ur[q]]&4)||(T[ub[q]]&8)) cf=true;
        for(auto&e:ER) if(T[ur[e.first]&ur[e.second]]&1){cf=true;break;}
        if(!cf) for(auto&e:EB) if(T[ub[e.first]&ub[e.second]]&2){cf=true;break;}
        if(!cf) for(auto&t3:TR3) if(T[ur[t3[0]]&ur[t3[1]]&ur[t3[2]]]&16){cf=true;break;}
        if(!cf) for(auto&t3:TB3) if(T[ub[t3[0]]&ub[t3[1]]&ub[t3[2]]]&32){cf=true;break;} int nf=0; uint8_t fx[600],fy[600],fc[600];
        for(int q=0;q<m&&!cf;q++) for(int w=0;w<m;w++){int t=(T[ur[q]&VR[j][w]]&1)|(T[ub[q]&VBl[j][w]]&2);
          if(t==3){cf=true;break;} if(t){fx[nf]=2+c+q; fy[nf]=2+c+m+w; fc[nf++]=t; int xx=2+c+q,yy=2+c+m+w; if(t==1){B[xx]|=1ULL<<yy;B[yy]|=1ULL<<xx;} else {R[xx]|=1ULL<<yy;R[yy]|=1ULL<<xx;}}}
        if(!cf && nf){ for(int f=0;f<nf&&!cf;f++){int xx=fx[f],yy=fy[f]; u64*A=fc[f]==1?B:R; if(tri(A,A[xx]&A[yy])) cf=true;}
         if(!cf) cf=propfast(R,B,Uo,Vo,false);} }
      }
     }
     if(cf) conf++; else {open_++; vector<int> Kvg(c); for(int t=0;t<c;t++) Kvg[t]=K.pK[j][K.G[x][t]];
      build(c,K.pgi[i],K.pa[i],K.pK[i],K.pgi[j],K.pa[j],Kvg,F); fprintf(out,"%zu %d %d %d %.*s\n",ci,i,j,x,n*n,F);} }}
  }}
 done: double el=chrono::duration<double>(chrono::steady_clock::now()-T0).count(); long done_=conf+open_;
 printf("c=%d shard %d/%d range [%ld,%ld) n=%ld conflict=%ld open=%ld uconf=%ld time %.3fs per %.3fus",c,sk,SK,lo,hi,done_,conf,open_,uconf,el,el/max(1L,done_)*1e6);
 if(prof) printf(" build %.3fus prop %.3fus",tb/done_*1e6,tp/done_*1e6); printf(" CCmismatch=%ld\n",mism); fprintf(stderr,"stages"); for(long v:stg) fprintf(stderr," %ld",v); fprintf(stderr,"\n");
 if(out) fclose(out); return 0;}
