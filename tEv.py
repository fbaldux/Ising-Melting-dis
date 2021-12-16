#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state on the Young diagram lattice.
#
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds sparse Hamiltonian from the entries.
#   - It evolves an initial state via full exponentiation or sparse Krylov (expm_multiply).
#   - It saves to file the linear dimensions of the state and the area.
#
#  ---------------------------------------------------------------------------------------------  #

import sys, os

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# time evolution parameters
Tin = float( sys.argv[3] )
Tfin = float( sys.argv[4] )
dt = float( sys.argv[5] )
t_steps = int( (Tfin-Tin)/dt )
save_dt = float( sys.argv[6] )
save_step = int( save_dt/dt )
save_steps = int( (Tfin-Tin)/save_dt )

# number of disorder instances
dis_num_in = int( sys.argv[7] )
dis_num_fin = int( sys.argv[8] )

# whether to use sparse exponentiation
use_sparse = int( sys.argv[9] )

# whether to overwrite existing files
overwrite = int( sys.argv[10] )

# number of processors to use
nProc = int( sys.argv[11] )


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

start = time()


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

def store(it,v2):
    toSave[it,0] = it*save_dt + Tin
    
    toSave[it,1] = np.dot(v2, sl1_op)
    toSave[it,2] = np.dot(v2, vh_op)
    toSave[it,3] = np.dot(v2, sl2_op)
    toSave[it,4] = np.dot(v2, area_op)


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
            H = H0 + epsilon * sparse.diags(diag)
        else:
            H = np.copy(H0)
 
        # array to store the observables
        toSave = np.zeros((save_steps+1,5)) # t lateral1 vertical lateral2 area
 
        # initial state
        if Tin == 0:
            v = np.zeros(dim[N])
            v[0] = 1
            store(0,np.abs(v)**2)
        else:
            v = np.load("States/N%d_e%.4f_T%.1f_d%d.npy" % (N,epsilon,Tin,dis))
 
        if use_sparse:
            vt = expm_multiply(-1j*H*dt, v, start=0, stop=t_steps, num=save_steps+1)
    
            for it in range(1,save_steps+1):
                store(it,np.abs(vt[it])**2)
            
            # to save the final state
            v = vt[-1]
                
        else:
            # evolutor from the Hamiltonian
            U = expm(-1j * H.todense() * dt)
            
            for it in range(1,t_steps+1):
                v = U.dot(v)
        
                if it%save_step == 0:
                    store(it//save_step,np.abs(v)**2)
        
        # save to file
        filename = "Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,epsilon,Tfin,dis)
        head = "t lat1 vert lat2 area"
        np.savetxt(filename, toSave, header=head)
        
        filename = "States/N%d_e%.4f_T%.1f_d%d.npy" % (N,epsilon,Tfin,dis)
        #np.savetxt(filename, np.stack((v.real,v.imag)), header="Re Im")
        np.save(filename, v)

    
print(' '.join(sys.argv), "time", time()-start)










