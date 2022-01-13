#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian.
#
#   - It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries, and converts it to a full matrix.
#   - It saves to Results/p0_{...} the max 
#       - eigenvalues
#       - IPR
#       - Kullback-Leibler divergence of neighbouring eigenstates
#       - participation entropy of the eigenstates (in the graph basis)
#   - It saves to Results/magDiff_{...} the magnetization difference of neighbouring eigenstates, 
#     for each site of the 2d Ising model.
#   - It optionally saves the eigenvectors, but it takes a HUGE amount of space.
#
#  ---------------------------------------------------------------------------------------------  #

import sys, os

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# number of disorder instances
dis_num_in = int( sys.argv[3] )
dis_num_fin = int( sys.argv[4] )

# number of processors to use
nProc = int( sys.argv[5] )


os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from partitions import *
import numba as nb
from time import time

start = time()

#  ------------------------------------  load hopping terms  -----------------------------------  #

# from partitions.py
H0 = load_adjacency(N)


#  ------------------------  operator for quantifying the removed area  ------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )

levels = tuple(levels)

area_op = area(N)


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):
    
    # load the disorder
    filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
    H = H0 + epsilon * sparse.diags(np.loadtxt(filename))

    # dense
    eigvals, eigvecs = eigh(H.todense())
    eigvecs = np.abs(eigvecs.T)**2
    
    k = np.argmax(eigvecs[:,0])
        
    f = open("Results/p0_N%d_e%.4f.txt" % (N,epsilon), 'a')
    f.write("%e %e %e\n" % (eigvals[k], np.dot(area_op, eigvecs[k]), eigvecs[k,0]))
    f.close()
    
print(' '.join(sys.argv), "time", time()-start)






