# Positive controls (known SAT): subsets of the (5,5)-good 41-vertex coloring found_R5_5_n41.txt,
# keep prob p in {1.0,0.95,0.8,0.5,0.3}, 20 each; slots 41..44 unused (run with NV=41). out: ctl.txt
import random
L=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','data','found_R5_5_n41.txt')).read().split()[1:]
n=45; random.seed(1); out=open('ctl.txt','w')
for p in (1.0,0.95,0.8,0.5,0.3):
    for _ in range(20):
        F=[['.']*n for _ in range(n)]
        for i in range(n): F[i][i]='0'
        for i in range(41):
            for j in range(i+1,41):
                if random.random()<p: F[i][j]=F[j][i]=L[i][j]
        out.write(''.join(''.join(r) for r in F)+'\n')
