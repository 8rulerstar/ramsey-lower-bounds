# cadical (60 s) on evenly spaced probe-UNSAT opens; out p2_val200.txt
import subprocess
out=open('p2_val200.txt','w')
for f,k in (('open_c8.txt',80),('open_c9.txt',60),('open_c10_sample.txt',40),('open_c11_sample.txt',20)):
    L=open(f).read().splitlines(); st=len(L)//k
    for i in range(0,st*k,st):
        cnf=subprocess.run(['./p2_pair2','dimacs'],input=L[i]+'\n',capture_output=True,text=True).stdout
        open('p2_cnf/t.cnf','w').write(cnf)
        try: r=subprocess.run(['cadical','-q','p2_cnf/t.cnf'],capture_output=True,text=True,timeout=60).stdout.split('\n')[0]
        except subprocess.TimeoutExpired: r='TIMEOUT'
        out.write(f'{f} {i} {r}\n'); out.flush()
