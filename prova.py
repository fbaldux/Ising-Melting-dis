import numpy as np
from scipy.linalg import expm
from scipy import sparse
from scipy.sparse.linalg import expm_multiply

N = 4
Tfin = 1000
ts_per_decade = 10
save_steps = int( (np.log10(Tfin)+1)*ts_per_decade )


H = sparse.identity(N, format='csr') * np.log(2)
v = np.zeros(N)
v[0] = 1


v = expm_multiply(H, v, start=0, stop=0.1, num=2, endpoint=True)[-1]

# time evolution
for p in range(-1,int(np.log10(Tfin))):
    
    start = 10**p
    stop = 10**(p+1)
    dt = (stop-start) / (ts_per_decade-1)
    vt = expm_multiply(H, v, start=0, stop=stop-start, num=ts_per_decade, endpoint=True)
    #vt = expm_multiply(H, v, start=start, stop=stop, num=ts_per_decade, endpoint=True)
    
    for it in range(ts_per_decade-1):
        print(start + it*dt, np.log2(vt[it,0]))
    
    v = vt[-1]