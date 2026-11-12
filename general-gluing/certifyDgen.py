"""Certificate for the independent side of theorem DG on a concrete graph file F (read from file, not rebuilt).
python3 certifyDgen.py spec.json F.txt s_0 s_1 .. s_{t-1} [family graph files, one per colour]
Uses the vertex layout of gluegen.py (Gamma-vertex j on its positions pos(j)) and the colouring named in the spec (colourings.json).
Checks
 0. the colouring is valid for the pattern (|C(L)| >= |L|, separated labels get disjoint colour sets), re-checked here from the definition;
 1. for every fibre j: every non-empty L inside pos(j) with {(j,c): c in L} independent IN THE FILE is a label, and gets C(L);
 2. for all states (j,L), (l,M), j != l, with no edge of the file between them: if C(L), C(M) share a colour then j, l are not adjacent in Gamma;
 3. W_i = {j : some state of j has colour i}; Gamma[W_i] is, vertex by vertex, the graph file given for colour i (so alpha(Gamma[W_i]) <= s_i - 1
    once `verify k s_i file` has been run on that file).
Then every independent set I of F has |I| <= sum_i |T_i| <= sum_i (s_i - 1), T_i = {j : i in C(I_j)} independent in Gamma[W_i]."""
import sys, json, itertools, os
from dgen import labels_of, sep
from gluegen import layout, read_graph
spec,N,typ,A,pos,part,Gs,gid=layout(sys.argv[1])
tok=open(sys.argv[2]).read().split(); nF=int(tok[0]); F=[int(r[::-1],2) for r in tok[1:1+nF]]      # bit b of F[a] = adjacency a,b
ent=json.load(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),"colourings.json")))[spec["colouring"]]
t=ent["t"]; assert ent["N"]==N
C={tuple(int(x) for x in k.split(",")):frozenset(v) for k,v in ent["col"].items()}
svals=[int(x) for x in sys.argv[3:3+t]]; famfiles=sys.argv[3+t:3+2*t]
# 0
labs=labels_of(N,typ); assert set(labs)==set(C)
assert all(len(C[L])>=len(L) and C[L]<=set(range(t)) for L in labs)
nsep=0
for L in labs:
    for M in labs:
        if L<M and sep(typ,L,M): nsep+=1; assert not C[L]&C[M]
print(f"0 ok: colouring valid ({len(labs)} labels, {nsep} separated pairs)")
# layout
n=len(A); off=[0]*(n+1)
for j in range(n): off[j+1]=off[j]+len(pos[j])
assert off[n]==nF, "file size does not match the spec"
vid=lambda j,c: off[j]+pos[j].index(c)
# 1
states=[]; W=[set() for _ in range(t)]; bad=0
for j in range(n):
    st=[]
    for k in range(1,len(pos[j])+1):
        for L in itertools.combinations(pos[j],k):
            vs=[vid(j,c) for c in L]
            if any(F[a]>>b&1 for a in vs for b in vs): continue
            if L not in C: bad+=1; continue
            vm=0; nm=0
            for a in vs: vm|=1<<a; nm|=F[a]
            cm=sum(1<<i for i in C[L]); st.append((vm,nm,cm))
            for i in C[L]: W[i].add(j)
    states.append(st)
nel=sum(map(len,states))
# 2
pairs=0; viol=0
for j in range(n):
    Aj=A[j]; sj=states[j]
    for l in range(j):
        adjG=Aj[l]
        for vm,nm,cm in sj:
            for vm2,nm2,cm2 in states[l]:
                if nm&vm2: continue
                pairs+=1
                if adjG and cm&cm2: viol+=1
print(f"1,2: fibres {n}, elements {nel}, independent position sets that are not labels {bad}, admissible pairs {pairs}, violations {viol}")
# 3
ok3=True
for i in range(t):
    Wi=sorted(W[i]); msg=f"colour {i}: |W_i| = {len(Wi)}"
    if famfiles:
        G=read_graph(famfiles[i])
        # which part graph is it: find a part (or M) whose Gamma-vertex set equals W_i and compare adjacency through gid
        found=False
        for pi,d in enumerate(gid):
            if set(d.values())==set(Wi) and len(G)==len(Gs[pi]):
                same=(G==Gs[pi]) and all(A[d[a]][d[b]]==G[a][b] for a in range(len(G)) for b in range(len(G)))
                found=found or same
        msg+=f", equals {famfiles[i]} (no independent {svals[i]} by verify): {found}"; ok3&=found
    print("3",msg)
print(f"conclusion if all checks pass: alpha(F) <= {sum(s-1 for s in svals)}, i.e. no independent set of size {sum(s-1 for s in svals)+1}")
sys.exit(0 if (viol==0 and bad==0 and ok3) else 1)
