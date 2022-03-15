#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state on the Young diagram lattice.
#
#   - It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It evolves an initial state via full exponentiation.
#   - It saves to Results/ the linear dimensions of the state and the area.
#   - It saves to States/ the final state reached.
#   - It is suited for time evolution in log scale (the dt is progressively increased).
#   - It evolves several initial states, but diagonalizing the Hamiltonian only once.
#
#  ---------------------------------------------------------------------------------------------  #

import sys, os

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# initial state
init_states = (0,24,121)

# time evolution parameters
Tin = float( sys.argv[4] )
Tfin = float( sys.argv[5] )
ts_per_pow2 = int( sys.argv[6] )
Tin_cutoff = 1e-1

# number of disorder instances
dis_num_in = int( sys.argv[7] )
dis_num_fin = int( sys.argv[8] )

# whether to overwrite existing files
overwrite = int( sys.argv[9] )

# whether to use sparse exponentiation
use_sparse = False

# number of processors to use
nProc = int( sys.argv[11] )


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


#  ----------------------------  stuff for the entanglement entropy  ---------------------------  #

# integer representation in the language of the fermions
int_rep = build_integer_repr(N,levels)     # int_rep[0]=left, int_rep[1]=right
new_states = np.unique(int_rep[:,0])


#  ---------------------------  store stuff in the array of results  ---------------------------  #

def store(t,it,v):
    temp = [t]
    
    v2 = np.abs(v)**2
    temp.append( np.dot(v2, sl_op) )
    temp.append( np.dot(v2, vh_op) )
    temp.append( np.dot(v2, area_op) )

    temp.append( entanglement_entropy(reduced_density_matrix(N, v, int_rep, new_states)) )

    return temp


#  ----------------------------------------  file names  ---------------------------------------  #

def filename_obs(iS,T,d):
    return "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,iS,T,d)

def filename_state(iS,T,d):
    return "States/N%d_e%.4f_s%d_T%.1f_d%d.npy" % (N,epsilon,iS,T,d)


#  -------------------------------------------  main  ------------------------------------------  #

# handling Tin=0
if Tin == 0:
    Tin_true = Tin_cutoff
else:
    Tin_true = Tin

for dis in range(dis_num_in,dis_num_fin):
    
    do_this = False
    for iS in init_states:
        if overwrite or ( not os.path.isfile(filename_obs(iS,Tfin,dis)) ):
            do_this = True
    
    if do_this:
    
        # load the disorder
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        diag = np.loadtxt(filename)
        H = H0 + epsilon * sparse.diags(diag)
        
        save_steps = int( (np.log2(Tfin/Tin_true))*ts_per_pow2 )
        ts = np.exp( np.linspace(np.log(Tin_true), np.log(Tfin), save_steps) )
    
        # it holds H = U @ Hdiag @ U.H
        Hdiag, U = eigh(H.todense())
        
        for iS in init_states:
        
            # array to store the observables
            toSave = [] # t lateral vertical area EE

            # initial state
            if Tin == 0:
                v = np.zeros(dim[N])
                v[iS] = 1
                toSave.append( store(0,0,v) )
            else:
                v = np.load(filename_state(iS,Tin,dis))
    
    
            vrot = np.dot(np.conj(U.T), v)
    
            for it in range(save_steps):
                vt = np.einsum("ab,b,b", U, np.exp(-1j*Hdiag*ts[it]), vrot)
                toSave.append( store(ts[it], it+1, vt) )
    
            v = vt
        
            toSave = np.array(toSave)
    
            if Tin > 0:
                temp = np.loadtxt(filename_obs(iS,Tin,dis))
                print(temp.shape, toSave.shape)
                toSave = np.vstack((temp,toSave))
        
            # save to file
            head = "t lat vert area EE"
            np.savetxt(filename_obs(iS,Tfin,dis), toSave, header=head)
    
            np.save(filename_state(iS,Tfin,dis), v)
        
            if Tin > 0:
                os.system("rm " + filename_obs(iS,Tin,dis))
                os.system("rm " + filename_state(iS,Tin,dis))

print("END", ' '.join(sys.argv), "time", time()-startTime)










