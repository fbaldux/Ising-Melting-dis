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
#from LanczosRoutines import *

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
dis_num_fin = int( instring[6   ] )


p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)


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


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):
    
    # load the disorder
    filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
    diag = np.loadtxt(filename)
    H = H0 + epsilon * sparse.diags(diag)
 
 
    # initial state
    v = np.zeros(dim[N])
    v[0] = 1
 
 
    # time evolve the Hamiltonian
    # sparse
    #applyH = lambda v: 1j * H.dot(v)
    # dense
    H = H.todense()
    U = expm(-1j*H*dt)
    
    # array to store the evolved array
    vStore = np.zeros((t_steps//save_step,dim[N]+1))

    for it in range(1,t_steps):
        # sparse
        #v = expm_krylov_lanczos(applyH, v, dt, numiter=20)
        # dense
        v = U.dot(v)
        
    
        if it%save_step == 0:
            vStore[it//save_step-1,0] = it*dt
            vStore[it//save_step-1,1:] = np.abs(v)**2
    
    vStore[t_steps//save_step-1,0] = Tfin
    vStore[t_steps//save_step-1,1:] = np.abs(v)**2


    # save to file
    filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
    head = "t |v[0]|^2 |v[1]|^2 ..."
    np.savetxt(filename, vStore, header=head)

    











