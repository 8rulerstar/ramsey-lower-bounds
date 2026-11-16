// pair2424 placement enumerator + K5 unit-propagation filter. See README.md.
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
#include <cadical.hpp>
using namespace std; typedef uint64_t u64;
const int n=45; int NV=45; // active vertices (check mode env NV, for controls)
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
// ---- propagation: R/B = assigned red/blue adjacency masks
static inline bool tri(const u64*A,u64 S){ // triangle in S using adjacency A
 u64 s=S; while(s){int a=__builtin_ctzll(s); s&=s-1; u64 T=A[a]&s; while(T){int b=__builtin_ctzll(T); T&=T-1; if(A[b]&T) return true;}} return false;}
long sweeps=0, mism=0;
// returns true if conflict
bool propagate(u64*R,u64*B){
 for(int x=0;x<n;x++) for(u64 s=R[x]>>(x+1)<<(x+1);s;s&=s-1){int y=__builtin_ctzll(s); if(tri(R,R[x]&R[y])) return true;}
 for(int x=0;x<n;x++) for(u64 s=B[x]>>(x+1)<<(x+1);s;s&=s-1){int y=__builtin_ctzll(s); if(tri(B,B[x]&B[y])) return true;}
 const u64 ALL=(NV==64?~0ULL:(1ULL<<NV)-1); bool ch=true;
 while(ch){ch=false; sweeps++;
  for(int x=0;x<n;x++){u64 fr=ALL&~R[x]&~B[x]&~((2ULL<<x)-1);
   for(;fr;fr&=fr-1){int y=__builtin_ctzll(fr);
    bool nr=tri(R,R[x]&R[y]), nb=tri(B,B[x]&B[y]);
    if(nr&&nb) return true;
    if(nr){B[x]|=1ULL<<y;B[y]|=1ULL<<x;ch=true;} else if(nb){R[x]|=1ULL<<y;R[y]|=1ULL<<x;ch=true;}
    // after assigning, the new edge itself cannot complete a mono K5 (it was not forced that way)
   }}}
 return false;}
void fromF(const char*F,u64*R,u64*B){for(int i=0;i<n;i++){R[i]=B[i]=0; for(int j=0;j<n;j++) if(i!=j){if(F[i*n+j]=='1')R[i]|=1ULL<<j; else if(F[i*n+j]=='0')B[i]|=1ULL<<j;}}}
// build F exactly as build2.build(outside=True)
void build(int c,int gi,int a,const vector<int>&Ku,int hj,int b,const vector<int>&Kvg,char*F){
 int m=23-c; int mu[24],mv[24]; for(int x=0;x<24;x++)mu[x]=mv[x]=-1;
 mu[a]=1; for(int t=0;t<c;t++) mu[Ku[t]]=2+t; int i=0; for(int x=0;x<24;x++) if(mu[x]<0) mu[x]=2+c+i++;
 mv[b]=0; for(int t=0;t<c;t++) mv[Kvg[t]]=2+t; i=0; for(int y=0;y<24;y++) if(mv[y]<0) mv[y]=2+c+m+i++;
 memset(F,'.',n*n); for(int k=0;k<n;k++) F[k*n+k]='0';
 for(int w=0;w<2;w++){auto&G=GR[w?hj:gi]; int*mm=w?mv:mu;
  for(int x=0;x<n;x++) if(x!=w) F[w*n+x]=F[x*n+w]='0';
  for(int x=0;x<24;x++){F[w*n+mm[x]]=F[mm[x]*n+w]='1'; for(int y=0;y<24;y++) if(x!=y){char e=(G[x]>>y&1)?'1':'0'; char&d=F[mm[x]*n+mm[y]]; if(w==1&&mm[x]>=2&&mm[y]>=2&&d!='.'&&d!=e) mism++; d=e;}}}
}
int main(int argc,char**argv){
 if(argc<2){fprintf(stderr,"usage: pair check FILE | cadcheck FILE | count AUT c | run AUT c OUT [maxN]\n");return 1;}
 string md=argv[1];
 if(md=="check"||md=="cadcheck"){ if(getenv("NV")) NV=atoi(getenv("NV"));ifstream f(argv[2]); string s; int k=0,nc=0; double tt=0;
  CaDiCaL::Solver*S=nullptr; map<pair<int,int>,int> var;
  while(getline(f,s)){ if(s.size()!=n*n) continue; bool conf;
   auto t0=chrono::steady_clock::now();
   if(md=="check"){u64 R[n],B[n]; fromF(s.data(),R,B); conf=propagate(R,B);}
   else { if(!S){ // frame = rows 0,1 of this instance, all else free; clauses via mono-K5 of frame
      S=new CaDiCaL::Solver; char Fr[n*n]; memset(Fr,'.',n*n); for(int i=0;i<n;i++)Fr[i*n+i]='0';
      for(int w=0;w<2;w++) for(int x=0;x<n;x++){Fr[w*n+x]=s[w*n+x];Fr[x*n+w]=s[x*n+w];}
      for(int i=0;i<n;i++)for(int j=i+1;j<n;j++) if(Fr[i*n+j]=='.') {int v=var.size()+1; var[{i,j}]=v;}
      long ncl=0; int q[5];
      for(q[0]=0;q[0]<n;q[0]++)for(q[1]=q[0]+1;q[1]<n;q[1]++)for(q[2]=q[1]+1;q[2]<n;q[2]++)for(q[3]=q[2]+1;q[3]<n;q[3]++)for(q[4]=q[3]+1;q[4]<n;q[4]++)
       for(char col: {'1','0'}){bool ok=true; vector<int> L; for(int u=0;u<5&&ok;u++)for(int v=u+1;v<5;v++){char e=Fr[q[u]*n+q[v]]; if(e=='.') L.push_back(col=='1'?-var[{q[u],q[v]}]:var[{q[u],q[v]}]); else if(e!=col){ok=false;break;}}
        if(ok){for(int l:L)S->add(l); S->add(0); ncl++;}}
      fprintf(stderr,"cadical frame vars %zu clauses %ld\n",var.size(),ncl); t0=chrono::steady_clock::now();}
     for(auto&[e,v]:var){char x=s[e.first*n+e.second]; if(x!='.') S->assume(x=='1'?v:-v);}
     S->limit("decisions",0); int r=S->solve(); conf=(r==20); }
   tt+=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
   printf("%d %s\n",k,conf?"UNSAT":"OPEN"); nc+=conf; k++;}
  fprintf(stderr,"%s n=%d conflict=%d total %.4fs per %.6fs sweeps %ld\n",md.c_str(),k,nc,tt,tt/k,sweeps); return 0;}
 load(argv[2]); int c=atoi(argv[3]); bool run=md=="run"; long maxN=argc>5?atol(argv[5]):LONG_MAX;
 FILE*out=run?fopen(argv[4],"w"):nullptr;
 long tot=0,conf=0,open_=0; auto T0=chrono::steady_clock::now(); char F[n*n];
 for(size_t ci=0;ci<CL.size();ci++){auto&K=CL[ci]; if(K.c!=c) continue;
  int g=K.G.size(); unordered_map<u64,int> gid; auto key=[&](const vector<int>&p){u64 h=0; for(int x:p) h=h*16+x; return h;};
  for(int i=0;i<g;i++) gid[key(K.G[i])]=i;
  vector<int> inv(g); for(int i=0;i<g;i++){vector<int> q(c); for(int t=0;t<c;t++) q[K.G[i][t]]=t; inv[i]=gid[key(q)];}
  vector<int> mul((size_t)g*g); for(int i=0;i<g;i++)for(int j=0;j<g;j++){vector<int> q(c); for(int t=0;t<c;t++) q[t]=K.G[i][K.G[j][t]]; mul[(size_t)i*g+j]=gid[key(q)];}
  map<pair<int,int>,pair<vector<int>,vector<int>>> dcc; // (Hj,Hi)-> (dcid per g, reps)
  auto dc=[&](int hj,int hi)->pair<vector<int>,vector<int>>&{auto it=dcc.find({hj,hi}); if(it!=dcc.end()) return it->second;
   vector<int> id(g,-1),reps; for(int x=0;x<g;x++) if(id[x]<0){int k=reps.size(); reps.push_back(x);
    for(int a:K.Hs[hj]) for(int b:K.Hs[hi]) id[mul[(size_t)mul[(size_t)a*g+x]*g+b]]=k;}
   return dcc[{hj,hi}]={id,reps};};
  int np=K.pgi.size();
  for(int i=0;i<np;i++) for(int j=i;j<np;j++){auto&[id,reps]=dc(K.pH[j],K.pH[i]);
   for(int k=0;k<(int)reps.size();k++){int x=reps[k]; if(i==j && id[inv[x]]<k) continue;
    tot++; if(!run) continue; if(tot>maxN) goto done;
    vector<int> Kvg(c); for(int t=0;t<c;t++) Kvg[t]=K.pK[j][K.G[x][t]];
    build(c,K.pgi[i],K.pa[i],K.pK[i],K.pgi[j],K.pa[j],Kvg,F);
    u64 R[n],B[n]; fromF(F,R,B);
    if(propagate(R,B)) conf++; else {open_++; fprintf(out,"%zu %d %d %d %.*s\n",ci,i,j,x,n*n,F);} }}}
 done: if(tot>maxN) tot=maxN;
 double el=chrono::duration<double>(chrono::steady_clock::now()-T0).count();
 printf("c=%d unordered=%ld",c,tot); if(run) printf(" conflict=%ld open=%ld time %.3fs per %.3fus",conf,open_,el,el/tot*1e6); printf(" CCmismatch=%ld\n",mism);
 if(out) fclose(out); return 0;}
