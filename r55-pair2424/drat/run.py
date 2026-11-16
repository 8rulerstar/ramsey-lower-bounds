# usage: python3 run.py LISTFILE OUT.tsv ; per batch line: CNF -> cadical DRAT -> drat-trim; proof deleted, sha256+size kept
import subprocess,time,hashlib,os,sys
from concurrent.futures import ThreadPoolExecutor
C='../ctool'; DT=os.environ.get('DRAT_TRIM', os.path.expanduser('~/tools/drat-trim/drat-trim'))  # set DRAT_TRIM to your drat-trim binary
L=[l for l in open(sys.argv[1]).read().splitlines() if l.strip()]
def one(i):
    bid,rest=L[i].split(' ',1); cnf=f'w/{i}.cnf'; prf=f'w/{i}.drat'
    open(cnf,'w').write(subprocess.run([C+'/p2_pair2','dimacs'],input=rest+'\n',capture_output=True,text=True).stdout)
    t=time.time(); r=subprocess.run(['cadical','-q',cnf,prf],capture_output=True,text=True).stdout.split('\n')[0]; tc=time.time()-t
    sz=os.path.getsize(prf); h=hashlib.sha256(open(prf,'rb').read()).hexdigest()
    t=time.time(); o=subprocess.run([DT,cnf,prf],capture_output=True,text=True).stdout; td=time.time()-t
    v='VERIFIED' if 's VERIFIED' in o else 'FAIL'
    os.remove(prf); os.remove(cnf)
    return f'{bid}\t{r}\t{tc:.3f}\t{sz}\t{h}\t{v}\t{td:.3f}'
os.makedirs('w',exist_ok=True)
with open(sys.argv[2],'w') as f, ThreadPoolExecutor(3) as ex:
    f.write('batch\tcadical\tcad_s\tdrat_bytes\tdrat_sha256\tdrat_trim\tdt_s\n')
    for s in ex.map(one,range(len(L))): f.write(s+'\n'); f.flush()
