#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state on the Young diagram graph.
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt
#     file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It evolves an initial state via Krylov (from LanczosRoutines.py).
#
#  ---------------------------------------------------------------------------------------------  #

import sys, os

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# time evolution parameters
Tfin = float( sys.argv[3] )
dt = float( sys.argv[4] )
t_steps = int( Tfin/dt )
save_dt = float( sys.argv[5] )
save_step = int( save_dt/dt )

# number of disorder instances
dis_num_in = int( sys.argv[6] )
dis_num_fin = int( sys.argv[7] )

# number of processors to use
nProc = int( sys.argv[8] )

os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy import sparse
import numba as nb
from partitions import *
from LanczosRoutines import *
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

# (diagonal) operator that gives the height on the vertical line for the tilted Young diagrams
@nb.njit
def vertical_height():
    vh = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # check how many rows are longer than their index (i.e. one can fit in a square)
            r = 0
            while r<n and levels[n][i,r]>r:
                r += 1
            
            vh[k] = r
            
    return vh

vh_op = vertical_height()


# (diagonal) operator that gives the length on the left side for the tilted Young diagrams
@nb.njit
def side1_length():
    sl = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # the lateral length is the 0th entry of the level
            sl[k] = levels[n][i,0]
            
    return sl

sl1_op = side1_length()


# (diagonal) operator that gives the length on the right side for the tilted Young diagrams
@nb.njit
def side2_length():
    sl = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # the lateral length is the first 0 entry
            temp = np.where(levels[n][i]==0)[0]
            if len(temp)>0:
                sl[k] = temp[0]
            else:
                sl[k] = n
     
    return sl

sl2_op = side2_length()


# (diagonal) operator that gives the area of the Young diagrams
area_op = np.zeros(dim[N], dtype=np.float_)
for n in range(1,N+1):
    area_op[dim[n-1]:dim[n]] = n


#  ---------------------------  store stuff in the array of results  ---------------------------  #

def store(it,v):
    toSave[it//save_step,0] = it*dt
    
    v2 = np.abs(v)**2
    toSave[it//save_step,1] = np.dot(v2, sl1_op)
    toSave[it//save_step,2] = np.dot(v2, vh_op)
    toSave[it//save_step,3] = np.dot(v2, sl2_op)
    toSave[it//save_step,4] = np.dot(v2, area_op)


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):
    
    # load the disorder
    filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
    diag = np.loadtxt(filename)
    H = H0 + epsilon * sparse.diags(diag)
 
 
    # initial state
    v = np.zeros(dim[N])
    v[0] = 1
 
 
    # to evolve the Hamiltonian we need the abstract function that applies H to a vector
    applyH = lambda v: 1j * H.dot(v)
    
    
    # array to save observables
    toSave = np.zeros((int(Tfin/save_dt),5)) # t lateral1 vertical lateral2 area 
    store(0,v)

    for it in range(1,t_steps):
        v = expm_krylov_lanczos(applyH, v, dt, numiter=100)
      
        if it%save_step == 0:
            store(it,v)
            

    # save to file
    filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
    head = "t lat1 vert lat2 area"
    np.savetxt(filename, toSave, header=head)

    
#print("N %d t_steps %d time %f" % (N, t_steps, time()-start))
print(N, t_steps, time()-start)









