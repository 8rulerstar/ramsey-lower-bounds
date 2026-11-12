# Independent structure check of F1053 (own code). Reads F, maps, H204.txt.
import sys
def load(f):
    r=[l.strip() for l in open(f) if l.strip()]; n=int(r[0]); M=r[1:]; assert len(M)==n and all(len(x)==n for x in M); return n,M
N,F=load('R8_18_1053.txt'); nH,H=load('H204.txt'); nC,Cf=load('C133.txt')
xG,xC=[list(map(int,l.split())) for l in open('maps_R8_18_1053.txt')]
m=len(xG); nG=4*nH; assert N==nG+nC+m, (N,nG,nC,m)
a=lambda i,j: F[i][j]=='1'
h=lambda i,j: H[i][j]=='1'
bad={}
def B(k): bad[k]=bad.get(k,0)+1
for i in range(N):
    if a(i,i): B('loop')
    for j in range(i):
        if a(i,j)!=a(j,i): B('asym')
def gam(p,q):
    i1,j1=divmod(p,nH); i2,j2=divmod(q,nH)
    if p==q: return False
    if i1==i2: return h(j1,j2)
    if {i1,i2} in ({0,1},{2,3}): return j1==j2
    return j1!=j2 and h(j1,j2)
for p in range(nG):
    for q in range(nG):
        if a(p,q)!=gam(p,q): B('G!=Gamma(H204)')
for p in range(nC):
    for q in range(nC):
        if a(nG+p,nG+q)!=(Cf[p][q]=='1'): B('C!=Cfile')
assert len(set(xG))==m and len(set(xC))==m
mt=dict(zip(xG,xC))
for p in range(nG):
    for q in range(nC):
        if a(p,nG+q)!=(mt.get(p)==q): B('G-C edges not matching')
Wb=nG+nC
for i in range(m):
    w=Wb+i
    if a(w,xG[i]) or a(w,nG+xC[i]): B('w adj own')
    for y in range(nG):
        if y!=xG[i] and a(w,y)!=a(xG[i],y): B('w not twin G')
    for y in range(nC):
        if y!=xC[i] and a(w,nG+y)!=a(nG+xC[i],nG+y): B('w not twin C')
    for j in range(m):
        if j!=i and not (a(w,Wb+j)==a(xG[i],xG[j])==a(nG+xC[i],nG+xC[j])): B('M not common induced')
print('N',N,'nG',nG,'nC',nC,'m',m,'violations',bad or 0)
