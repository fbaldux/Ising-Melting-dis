#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian.
#
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries, and converts it to a full matrix.
#   - It saves to file the eigenvalues and IPRs (or the eigenvectors, but it takes a lot of space).
#
#  ---------------------------------------------------------------------------------------------  #

import sys

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# number of disorder instances
dis_num_in = int( sys.argv[3] )
dis_num_fin = int( sys.argv[4] )

# whether to overwrite existing files
overwrite = int( sys.argv[5] )

# number of processors to use
nProc = int( sys.argv[6] )


import os
os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from partitions import *


#  ------------------------------------  load hopping terms  -----------------------------------  #

# from partitions.py
H0 = load_adjacency(N)


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):
    
    done = False
    if not overwrite and os.path.isfile("Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)):
        done = True
    
    if not done:
        # load the disorder
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        diag = np.loadtxt(filename)
        H = H0 + epsilon * sparse.diags(diag)
 
        # dense
        H = H.todense()
        eigvals, eigvecs = eigh(H)
        eigvecs = eigvecs.T
    
        # compute the IPR
        IPRs = np.sum(eigvecs**4, axis=1)
        
        # save to file
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "eigenvalue IPR"
        np.savetxt(filename, np.stack((eigvals, IPRs)).T, header=head)
        
        """
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "eigval eigvec[0] eigvec[1] ..." 
        np.savetxt( filename, np.vstack((eigvals, eigvecs)).T, header=head )
        """

print("End spec N%d e%.4f d%d-%d" % (N,epsilon,dis_num_in,dis_num_fin))






