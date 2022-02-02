#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state on the Young diagram lattice.
#
#   - It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It evolves an initial state via full exponentiation or sparse Pade' (expm_multiply).
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

# initial state
init_state = int( sys.argv[3] )

# time evolution parameters
Tin = float( sys.argv[4] )
Tfin = float( sys.argv[5] )
ts_per_decade = int( sys.argv[6] )

# number of disorder instances
dis_num_in = int( sys.argv[7] )
dis_num_fin = int( sys.argv[8] )

# whether to use sparse exponentiation
use_sparse = int( sys.argv[9] )

# number of processors to use
nProc = int( sys.argv[10] )


os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy.linalg import eigh,expm
from scipy import sparse
from scipy.sparse.linalg import expm_multiply
import numba as nb
from partitions import *
from time import time


save_steps = int( (np.log10(Tfin/Tin))*ts_per_decade )

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
sl_op = 0.5 * (side1_length(N,levels) + side2_length(N,levels))
area_op = area(N)


#  ---------------------------  store stuff in the array of results  ---------------------------  #

def store(t,i,v2):
    toSave[i,0] = t
    
    toSave[i,1] = np.dot(v2, sl_op)
    toSave[i,2] = np.dot(v2, vh_op)
    toSave[i,3] = np.dot(v2, area_op)


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):

    # load the disorder
    if epsilon != 0:
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        diag = np.loadtxt(filename)
        H = H0 + epsilon * sparse.diags(diag)
    else:
        H = H0


    # array to store the observables
    toSave = np.zeros((save_steps+1,4)) # t lateral vertical area


    # initial state
    v = np.zeros(dim[N])
    v[init_state] = 1
    store(0, 0, np.abs(v)**2)
    

    # time evolution
    if use_sparse:
        Him = -1j*H
        del H
        
        # first step
        v = expm_multiply(Him, v, start=0, stop=Tin, num=2, endpoint=True)[-1]
        store(Tin, 1, np.abs(v)**2)
    
        # bulk
        c = 2
        for p in range( int(np.log10(Tin)), int(np.log10(Tfin)) ):

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
        toSave = toSave[:c+1]
    
    else:
        ts = np.exp( np.linspace(np.log(Tin), np.log(Tfin), save_steps) )
        
        # it holds H = U @ Hdiag @ U.H
        Hdiag, U = eigh(H.todense())
        
        vrot = np.dot(np.conj(U.T), v)
        
        for it in range(save_steps):
            vt = np.einsum("ab,b,b", U, np.exp(-1j*Hdiag*ts[it]), vrot)
            store(ts[it], it+1, np.abs(vt)**2)
        
        v = vt
        
    
    # save to file
    filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,Tfin,dis)
    head = "t lat vert area"
    np.savetxt(filename, toSave, header=head)
    
    filename = "States/N%d_e%.4f_s%d_T%.1f_d%d.npy" % (N,epsilon,init_state,Tfin,dis)
    np.save(filename, v)

print(' '.join(sys.argv), "time", time()-startTime)










