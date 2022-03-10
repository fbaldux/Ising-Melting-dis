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
dt = float( sys.argv[6] )
t_steps = int( (Tfin-Tin)/dt )
save_dt = float( sys.argv[7] )
save_step = int( save_dt/dt )
save_steps = int( (Tfin-Tin)/save_dt )

# number of disorder instances
dis_num_in = int( sys.argv[8] )
dis_num_fin = int( sys.argv[9] )

# whether to use sparse exponentiation
use_sparse = int( sys.argv[10] )

# whether to overwrite existing files
overwrite = int( sys.argv[11] )

# number of processors to use
nProc = int( sys.argv[12] )


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
sl_op = 0.5 * (side1_length(N,levels) + side2_length(N,levels))
area_op = area(N)


#  ----------------------------  stuff for the entanglement entropy  ---------------------------  #

# integer representation in the language of the fermions
int_rep = build_integer_repr(N,levels)     # int_rep[0]=left, int_rep[1]=right
new_states = np.unique(int_rep[:,0])



#  ---------------------------  store stuff in the array of results  ---------------------------  #

def store(it,v):
    toSave[it,0] = it*save_dt + Tin
    
    v2 = np.abs(v)**2
    toSave[it,1] = np.dot(v2, sl_op)
    toSave[it,2] = np.dot(v2, vh_op)
    toSave[it,3] = np.dot(v2, area_op)

    toSave[it,4] = entanglement_entropy(reduced_density_matrix(N, v, int_rep, new_states))


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):

    if overwrite or ( not os.path.isfile("Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)) ):

        # load the disorder
        if epsilon != 0:
            filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
            diag = np.loadtxt(filename)
            H = H0 + epsilon * sparse.diags(diag)
        else:
            H = np.copy(H0)

        # array to store the observables
        toSave = np.zeros((save_steps+1,5)) # t lateral vertical area EE

        # initial state
        if Tin == 0:
            v = np.zeros(dim[N])
            v[init_state] = 1
            store(0,v)
        else:
            v = np.load("States/N%d_e%.4f_s%d_T%.1f_d%d.npy" % (N,epsilon,init_state,Tin,dis))

        if use_sparse:
            vt = expm_multiply(-1j*H*dt, v, start=0, stop=t_steps, num=save_steps+1)

            for it in range(1,save_steps+1):
                store(it,vt[it])
        
            # to save the final state
            v = vt[-1]
            
        else:
            # evolutor from the Hamiltonian
            U = expm(-1j * H.todense() * dt)
        
            for it in range(1,t_steps+1):
                v = U.dot(v)
    
                if it%save_step == 0:
                    store(it//save_step,v)
        
                
        if Tin > 0:
            filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,Tin,dis)
            temp = np.loadtxt(filename)
            toSave = np.vstack((temp,toSave))
        
        # save to file
        filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,Tfin,dis)
        head = "t lat vert area EE"
        np.savetxt(filename, toSave, header=head)
    
        filename = "States/N%d_e%.4f_s%d_T%.1f_d%d.npy" % (N,epsilon,init_state,Tfin,dis)
        #np.savetxt(filename, np.stack((v.real,v.imag)), header="Re Im")
        np.save(filename, v)
        
        if Tin > 0:
            filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,Tin,dis)
            os.system("rm " + filename)
    
print("END", ' '.join(sys.argv), "time", time()-start)










