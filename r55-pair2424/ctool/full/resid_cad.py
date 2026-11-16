# cadical (300 s) on all probe residuals of the full (24,24) run; SAT -> verify. out full/resid_cad.txt
import subprocess,time,sys,os
k,K=int(sys.argv[1]),int(sys.argv[2])
L=open('full/resid_all.txt').read().splitlines()
out=open(f'full/resid_cad_{k}.txt','w')
for i in range(k,len(L),K):
    line=L[i].split(' ',1)[1]
    cnf=f'full/r{k}.cnf'
    open(cnf,'w').write(subprocess.run(['./p2_pair2','dimacs'],input=line+'\n',capture_output=True,text=True).stdout)
    t=time.time()
    try: o=subprocess.run(['cadical','-q',cnf],capture_output=True,text=True,timeout=300).stdout; r=o.split('\n')[0]
    except subprocess.TimeoutExpired: r='TIMEOUT'
    if r.split() and r.split()[-1]=='SATISFIABLE':
        open(f'full/sat_{i}.line','w').write(line+'\n'); open(f'full/sat_{i}.out','w').write(o)
        r+=' '+subprocess.run(['./p2_pair2','verify',f'full/sat_{i}.line',f'full/sat_{i}.out'],capture_output=True,text=True).stdout.split('\n')[0]
    out.write(f'{i} {r} {time.time()-t:.3f}\n'); out.flush()
