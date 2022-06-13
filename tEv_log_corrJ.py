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
Tin = 0
Tfin = float( sys.argv[5] )
ts_per_pow2 = int( sys.argv[6] )
Tin_cutoff = 1e-1

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
from scipy.linalg import eigh,expm
from scipy import sparse
from scipy.sparse.linalg import expm_multiply
import numba as nb
import partitions as pt
from time import time

startTime = time()

#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in pt.generate_partitions(n)] ) )

levels = tuple(levels)


#  ------------------------------------  load hopping terms  -----------------------------------  #

# from partitions.py
H0 = pt.load_adjacency(N)


#  ------------------------  operators for quantifying the removed area  -----------------------  #

# from partitions.py
vh_op = pt.vertical_height(N,levels)
sl_op = 0.5 * (pt.side1_length(N,levels) + pt.side2_length(N,levels))
area_op = pt.area(N)


#  ----------------------------  stuff for the entanglement entropy  ---------------------------  #

# integer representation in the language of the fermions
int_rep = pt.build_integer_repr(N,levels)     # int_rep[0]=left, int_rep[1]=right
new_states = np.unique(int_rep[:,0])


#  -------------------------------------  current operator  ------------------------------------  #

J_op = pt.current_center(N,levels)


#  ---------------------------  store stuff in the array of results  ---------------------------  #

def store(t,v0,v1,J):
    temp = [t]
    
    temp.append( np.dot(np.abs(v0)**2, area_op) )
    temp2 = np.dot(np.conj(v0), J.dot(v1))
    temp.append( temp2.real )
    temp.append( temp2.imag )

    return temp


#  ----------------------------------------  file names  ---------------------------------------  #

def filename_obs(T,d):
    return "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,T,d)

def filename_state(T,d):
    return "States/N%d_e%.4f_s%d_T%.1f_d%d.npy" % (N,epsilon,init_state,T,d)


#  -------------------------------------------  main  ------------------------------------------  #

# handling Tin=0
if Tin == 0:
    Tin_true = Tin_cutoff
else:
    Tin_true = Tin

for dis in range(dis_num_in,dis_num_fin):
    
    if overwrite or ( not os.path.isfile(filename_obs(Tfin,dis)) ):
        
        # load the disorder
        if epsilon != 0:
            filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
            diag = np.loadtxt(filename)
            H = H0 + epsilon * sparse.diags(diag)
        else:
            H = H0


        # array to store the observables
        toSave = [] # t area <J(t)J(0)>


        # initial state
        v0 = np.zeros(pt.dim[N], dtype=np.complex_); v0[0] = 1
        v1 = np.zeros(pt.dim[N], dtype=np.complex_); v1[1] = 1j

        # time evolution
        if use_sparse:
            
            Him = -1j*H
            del H
        
            # first step
            if Tin == 0:
                v0_running = expm_multiply(Him, v0, start=0, stop=Tin_true, num=2, endpoint=True)[-1]
                v1_running = expm_multiply(Him, v1, start=0, stop=Tin_true, num=2, endpoint=True)[-1]
                toSave.append( store(Tin_true, v0_running, v1_running, J_op) )
                # for <J(t)>
                #toSave.append( store(Tin_true, v0_running, v0_running, J_op) )
    
            # bulk
            t_pivots = np.concatenate(( 2**np.arange( 0, np.log2(Tfin/Tin_true) )*Tin_true, (Tfin,) ))

            for p in range(len(t_pivots)-1):
                v0t = expm_multiply(Him, v0_running, start=0, stop=t_pivots[p+1]-t_pivots[p], num=ts_per_pow2, endpoint=True)
                v1t = expm_multiply(Him, v1_running, start=0, stop=t_pivots[p+1]-t_pivots[p], num=ts_per_pow2, endpoint=True)
            
                ts = np.linspace(t_pivots[p],t_pivots[p+1],ts_per_pow2)
                for it in range(1,ts_per_pow2):
                    toSave.append( store(ts[it], v0t[it], v1t[it], J_op) )
                    # for <J(t)>
                    #toSave.append( store(ts[it], v0t[it], v0t[it], J_op) )

                v0_running = v0t[-1]
                v1_running = v1t[-1]
            
        else:
        
            save_steps = int( (np.log2(Tfin/Tin_true))*ts_per_pow2 )
            ts = np.exp( np.linspace(np.log(Tin_true), np.log(Tfin), save_steps) )
            
            # it holds H = U @ Hdiag @ U.H
            Hdiag, U = eigh(H.todense())
        
            v0rot = np.dot(np.conj(U.T), v0)
            v1rot = np.dot(np.conj(U.T), v1)
            Jrot = np.einsum("ab,bc,cd->ad", np.conj(U.T), J_op.todense(), U)
        
            for it in range(save_steps):
                v0t = np.einsum("ab,b,b", U, np.exp(-1j*Hdiag*ts[it]), v0rot)
                v1t = np.einsum("ab,b,b", U, np.exp(-1j*Hdiag*ts[it]), v1rot)
                toSave.append( store(ts[it], v0t, v1t, Jrot) )
        
        
        toSave = np.array(toSave)
    
        
        # save to file
        head = "t area <J(t)J(0)>"
        np.savetxt(filename_obs(Tfin,dis), toSave, header=head)
    

print("END", ' '.join(sys.argv), "time", time()-startTime)










