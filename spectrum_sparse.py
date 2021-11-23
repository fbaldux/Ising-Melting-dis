#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian.
#
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It saves to file a fraction the eigenvalues and IPRs at the center of the spectrum (or also
#     the eigenvectors, but it takes a lot of space).
#
#  ---------------------------------------------------------------------------------------------  #

instring = input("").split(' ')

# system size
N = int( instring[0] )

# disorder
epsilon = float( instring[1] )

# number of eigenvalues (for sparse diagonalization)
eig_frac = int( instring[2] )

# number of disorder instances
dis_num_in = int( instring[3] )
dis_num_fin = int( instring[4] )

# whether to overwrite existing files
overwrite = int( instring[5] )

# number of processors to use
nProc = int( instring[6] )


import os
os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from partitions import *


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
    
    done = False
    if not overwrite and os.path.isfile("Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)):
        done = True
    
    if not done:
        # load the disorder
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        diag = np.loadtxt(filename)
        H = H0 + epsilon * sparse.diags(diag)
 
        # sparse
        eigvals, eigvecs = eigsh(H, k=dim[N]//eig_frac, which='SM')
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






