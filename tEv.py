#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state on the Young diagram graph.
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt
#     file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It evolves an initial state via Krylov (from LanczosRoutines.py), or full exact diagonalization.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy import sparse
from scipy.linalg import eigh,expm
from scipy.sparse.linalg import eigsh
import numba as nb
from partitions import *
from LanczosRoutines import *

instring = input("").split(' ')

# system size
N = int( instring[0] )

# disorder
epsilon = float( instring[1] )

# time evolution parameters
Tfin = float( instring[2] )
dt = float( instring[3] )
t_steps = int( Tfin/dt )
save_dt = float( instring[4] )
save_step = int( save_dt/dt )

# number of disorder instances
dis_num_in = int( instring[5] )
dis_num_fin = int( instring[6] )


#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )

levels = tuple(levels)


#  ------------------------------------  load hopping terms  -----------------------------------  #

Ham_lens = np.loadtxt("ham_lengths.txt", dtype=np.int_).T
try:
    my_len = Ham_lens[1,Ham_lens[0]==N][0]
except:
    print("\nError! Hamiltonian for N=%d not built\n" % N)
    exit(0)
    
filename = "Hamiltonians/clean_N38.txt"
row_ind, col_ind = np.loadtxt(filename)[:my_len].T

H0 = sparse.csr_matrix((np.ones(len(row_ind)), (row_ind, col_ind)), shape=(dim[N], dim[N]))
H0 += H0.T


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
            sl[k] = np.where(levels[n][i]==0)[0][0]
     
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
 
 
    # evolutor from the Hamiltonian
    # sparse
    #applyH = lambda v: 1j * H.dot(v)
    # dense
    H = H.todense()
    U = expm(-1j*H*dt)
    
    
    # array to save observables
    toSave = np.zeros((int(Tfin/save_dt),5)) # t lateral1 vertical lateral2 area 
    store(0,v)

    for it in range(1,t_steps):
        # sparse
        #v = expm_krylov_lanczos(applyH, v, dt, numiter=20)
        # dense
        v = U.dot(v)
        
        if it%save_step == 0:
            store(it,v)
            

    # save to file
    filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
    head = "t lat1 vert lat2 area"
    np.savetxt(filename, toSave, header=head)

    











