#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state on the Young diagram lattice.
#
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds sparse Hamiltonian from the entries.
#   - It evolves an initial state via full exponentiation or sparse Krylov (expm_multiply).
#   - It saves to Results/ the linear dimensions of the state and the area.
#   - It saves to States/ the final state reached.
#   - It is suited for time evolution in log scale (the dt is progressively increased).
#
#  ---------------------------------------------------------------------------------------------  #

import sys, os

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# time evolution parameters
Tfin = float( sys.argv[3] )
ts_per_decade = int( sys.argv[4] )

# number of disorder instances
dis_num_in = int( sys.argv[5] )
dis_num_fin = int( sys.argv[6] )

# whether to overwrite existing files
overwrite = int( sys.argv[7] )

# number of processors to use
nProc = int( sys.argv[8] )


os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy.linalg import expm
from scipy import sparse
from scipy.sparse.linalg import expm_multiply
import numba as nb
from partitions import *
from time import time


save_steps = int( (np.log10(Tfin)+1)*ts_per_decade )

startTime = time()


#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )

levels = tuple(levels)


#  ------------------------------------  load hopping terms  -----------------------------------  #

# from partitions.py
H0 = load_adjacency(N)


#  ------------------------  operators for quantifying the removed area  -----------------------  #

# from partitions.py
vh_op = vertical_height(N,levels)
sl1_op = side1_length(N,levels)
sl2_op = side2_length(N,levels)
area_op = area(N)


#  ---------------------------  store stuff in the array of results  ---------------------------  #

def store(t,i,v2):
    toSave[i,0] = t
    
    toSave[i,1] = np.dot(v2, sl1_op)
    toSave[i,2] = np.dot(v2, vh_op)
    toSave[i,3] = np.dot(v2, sl2_op)
    toSave[i,4] = np.dot(v2, area_op)


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):
    
    done = False
    if not overwrite and os.path.isfile("Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,epsilon,Tfin,dis)):
        done = True
    
    if not done:
    
        # load the disorder
        if epsilon != 0:
            filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
            diag = np.loadtxt(filename)
            Him = -1j*( H0 + epsilon * sparse.diags(diag) )
        else:
            Him = -1j * H0
 
 
        # array to store the observables
        toSave = np.zeros((save_steps+1,5)) # t lateral1 vertical lateral2 area
 
 
        # initial state
        v = np.zeros(dim[N])
        v[0] = 1
        store(0, 0, np.abs(v)**2)
        
 
        # time evolution
        # first step
        v = expm_multiply(Him, v, start=0, stop=0.1, num=2, endpoint=True)[-1]
        store(0.1, 1, np.abs(v)**2)
        
        # bulk
        c = 2
        for p in range(-1,int(np.log10(Tfin))):
    
            start = 10**p
            stop = 10**(p+1)
            dt = (stop-start) / (ts_per_decade-1)
            vt = expm_multiply(Him, v, start=0, stop=stop-start, num=ts_per_decade, endpoint=True)
    
            for it in range(ts_per_decade-1):
                store(start+it*dt, c, np.abs(vt[it])**2)
                c += 1
    
            v = vt[-1]
        
        # last step
        store(Tfin, c, np.abs(v)**2)
        
        
        # save to file
        filename = "Results/tEv_N%d_e%.4f_T%.2e_d%d.txt" % (N,epsilon,Tfin,dis)
        head = "t lat1 vert lat2 area"
        np.savetxt(filename, toSave, header=head)
        
        filename = "States/N%d_e%.4f_T%.2e_d%d.npy" % (N,epsilon,Tfin,dis)
        np.save(filename, v)

    
print(sys.argv[0] + " N %d Tfin %d time %f" % (N, Tfin, time()-startTime))










