// Independent engine: partial 2-colouring of K_n, decide if it extends without mono K5.
// Input (stdin), repeated: line "n tag", then n lines of n chars: '1' red, '0' blue, '?' unknown, '.' diagonal.
// Output per instance: "tag RESULT" where RESULT in FIXED (fixed mono K5), UP, PROBE, CAD_UNSAT, CAD_SAT_OK, CAD_SAT_BAD, PROBE_SAT_OK
#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <chrono>
#include <cstdio>
#include <algorithm>
#include <unistd.h>
#include <cstdlib>
using namespace std;
int n; vector<string> M; vector<vector<int>> vid; int nv;
vector<vector<int>> cls; vector<vector<int>> watch; vector<int> val; vector<int> trail;
// lit: 2*var + s, s=0 means var true (red), s=1 means var false (blue)
inline int lv(int l){int x=val[l>>1]; if(x<0) return -1; return (l&1)? (x==0):(x==1);}
bool assign_lit(int l){int x=val[l>>1]; int want=(l&1)?0:1; if(x>=0) return x==want; val[l>>1]=want; trail.push_back(l); return true;}
// returns false on conflict; qhead index into trail
bool propagate(size_t qh){
  while(qh<trail.size()){
    int l=trail[qh++]; int fl=l^1; // literal fl became false
    vector<int>&W=watch[fl];
    size_t i=0,j=0;
    for(;i<W.size();i++){
      int ci=W[i]; vector<int>&c=cls[ci];
      if(c[0]==fl) swap(c[0],c[1]);
      if(lv(c[0])==1){W[j++]=ci;continue;}
      bool found=false;
      for(size_t k=2;k<c.size();k++) if(lv(c[k])!=0){swap(c[1],c[k]); watch[c[1]].push_back(ci); found=true; break;}
      if(found) continue;
      W[j++]=ci;
      if(lv(c[0])==0){ for(i++;i<W.size();i++) W[j++]=W[i]; W.resize(j); return false;}
      assign_lit(c[0]);
    }
    W.resize(j);
  }
  return true;
}
void undo(size_t to){while(trail.size()>to){val[trail.back()>>1]=-1;trail.pop_back();}}
bool checkfull(){ // verify complete matrix has no mono K5 (direct brute force)
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++){
    char e=M[a][b]; if(M[a][c]!=e||M[b][c]!=e) continue;
    for(int d=c+1;d<n;d++){ if(M[a][d]!=e||M[b][d]!=e||M[c][d]!=e) continue;
      for(int f=d+1;f<n;f++) if(M[a][f]==e&&M[b][f]==e&&M[c][f]==e&&M[d][f]==e) return false;}}
  return true;
}
string solve(const string&tag){
  vid.assign(n,vector<int>(n,-1)); nv=0;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++) if(M[i][j]=='?'){vid[i][j]=vid[j][i]=nv++;}
  cls.clear(); val.assign(nv,-1); trail.clear(); watch.assign(2*nv,{});
  vector<int> units; bool fixedbad=false;
  int p[5]; int e[10][2];
  for(p[0]=0;p[0]<n;p[0]++)for(p[1]=p[0]+1;p[1]<n;p[1]++)for(p[2]=p[1]+1;p[2]<n;p[2]++)
  for(p[3]=p[2]+1;p[3]<n;p[3]++){ char a01=M[p[0]][p[1]],a02=M[p[0]][p[2]],a12=M[p[1]][p[2]]; (void)a01;(void)a02;(void)a12; for(p[4]=p[3]+1;p[4]<n;p[4]++){
    int r=0,b=0; int uv[10]; int nu=0;
    for(int x=0;x<5;x++)for(int y=x+1;y<5;y++){char ch=M[p[x]][p[y]]; if(ch=='1')r++; else if(ch=='0')b++; else uv[nu++]=vid[p[x]][p[y]];}
    if(r&&b) continue;
    for(int col=0;col<2;col++){
      if(col==0&&b) continue; if(col==1&&r) continue;
      // forbid all-colour col: clause OR over unknown of (var != col)
      if(nu==0){fixedbad=true;continue;}
      vector<int> c(nu); for(int k=0;k<nu;k++) c[k]=2*uv[k]+(col==0?1:0);
      if(c.size()==1) units.push_back(c[0]);
      else cls.push_back(c);
    }
  }}
  if(fixedbad) return "FIXED";
  bool noprop=getenv("NOPROP")!=nullptr;
  if(noprop){ for(int l:units) cls.push_back({l}); }
  else {
  for(size_t i=0;i<cls.size();i++){watch[cls[i][0]].push_back(i);watch[cls[i][1]].push_back(i);}
  for(int l:units) if(!assign_lit(l)) return "UP";
  if(!propagate(0)) return "UP";
  // failed-literal probing to fixpoint
  bool changed=true;
  while(changed){changed=false;
    for(int x=0;x<nv;x++){ if(val[x]>=0) continue;
      for(int s=0;s<2;s++){ if(val[x]>=0) break;
        size_t t=trail.size(); assign_lit(2*x+s); bool ok=propagate(t); undo(t);
        if(!ok){ size_t t2=trail.size(); assign_lit(2*x+(s^1)); if(!propagate(t2)) return "PROBE"; changed=true; }
      }}
  }
  }
  // cadical on residual
  string f="/tmp/indep_"+to_string(getpid())+".cnf";
  {FILE*o=fopen(f.c_str(),"w"); vector<string> lines; int cnt=0;
   string body;
   for(int x=0;x<nv;x++) if(val[x]>=0){body+=(val[x]==1?"":"-")+to_string(x+1)+" 0\n";cnt++;}
   for(auto&c:cls){bool sat=false; string s; for(int l:c){int q=lv(l); if(q==1){sat=true;break;} if(q==0) continue; s+=((l&1)?"-":"")+to_string((l>>1)+1)+" ";} if(sat) continue; body+=s+"0\n"; cnt++;}
   fprintf(o,"p cnf %d %d\n%s",max(nv,1),cnt,body.c_str()); fclose(o);}
  string cmd="cadical -q "+f+" 2>/dev/null";
  FILE*pp=popen(cmd.c_str(),"r"); char buf[1<<16]; string out; while(fgets(buf,sizeof buf,pp)) out+=buf; pclose(pp); remove(f.c_str());
  if(out.find("s UNSATISFIABLE")!=string::npos) return "CAD_UNSAT";
  if(out.find("s SATISFIABLE")==string::npos) return "CAD_ERR";
  vector<int> mdl(nv+1,0); {istringstream is(out); string tok; while(is>>tok){ if(tok=="v"||tok=="s"||tok=="SATISFIABLE") continue; int z; try{z=stoi(tok);}catch(...){continue;} if(z>0)mdl[z]=1;}}
  for(int i=0;i<n;i++)for(int j=0;j<n;j++) if(i!=j&&M[i][j]=='?') M[i][j]=mdl[vid[i][j]+1]?'1':'0';
  string fn="sat_"+tag+".txt"; FILE*o=fopen(fn.c_str(),"w"); for(auto&s:M) fprintf(o,"%s\n",s.c_str()); fclose(o);
  return checkfull()?"CAD_SAT_OK":"CAD_SAT_BAD";
}
int main(){ string tag; while(cin>>n>>tag){ M.assign(n,""); for(int i=0;i<n;i++) cin>>M[i];
  auto t0=chrono::steady_clock::now(); string r=solve(tag);
  double dt=chrono::duration<double>(chrono::steady_clock::now()-t0).count();
  printf("%s %s %.3f\n",tag.c_str(),r.c_str(),dt); fflush(stdout);} }
