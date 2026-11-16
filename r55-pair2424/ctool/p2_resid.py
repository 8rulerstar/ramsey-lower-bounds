# cadical (60 s) on 50 evenly spaced c=12 probe residuals; SAT -> verify; out p2_resid50.txt
import subprocess,time
out=open('p2_resid50.txt','w'); L=open('p2_res_c12.txt').read().splitlines(); st=len(L)//50
for i in range(0,st*50,st):
    line=L[i].split(' ',1)[1]
    open('p2_cnf/r.cnf','w').write(subprocess.run(['./p2_pair2','dimacs'],input=line+'\n',capture_output=True,text=True).stdout)
    t=time.time()
    try: o=subprocess.run(['cadical','-q','p2_cnf/r.cnf'],capture_output=True,text=True,timeout=60).stdout; r=o.split('\n')[0]
    except subprocess.TimeoutExpired: r='TIMEOUT'
    if 'SATISFIABLE'==r.split()[-1]:
        open(f'p2_sat_{i}.line','w').write(line+'\n'); open(f'p2_sat_{i}.out','w').write(o)
        r+=' '+subprocess.run(['./p2_pair2','verify',f'p2_sat_{i}.line',f'p2_sat_{i}.out'],capture_output=True,text=True).stdout.split('\n')[0]
    out.write(f'{i} {r} {time.time()-t:.3f}\n'); out.flush()
