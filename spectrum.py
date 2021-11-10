#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt
#     file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It saves to file the eigenvalues, IPR and r parameters (or the eigenvectors, but it takes
#     a lot of space).
#
#  ---------------------------------------------------------------------------------------------  #

import os
os.environ["MKL_NUM_THREADS"] = "8"
os.environ["NUMEXPR_NUM_THREADS"] = "8"
os.environ["OMP_NUM_THREADS"] = "8"

import numpy as np
from scipy import sparse
from scipy.linalg import eigh,expm
from scipy.sparse.linalg import eigsh

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
    
    done = False
    if not overwrite and os.path.isfile("Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)):
        done = True
    
    if not done:
        # load the disorder
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        diag = np.loadtxt(filename)
        H = H0 + epsilon * sparse.diags(diag)
 
        # dense
        #H = H.todense()
        #eigvals, eigvecs = eigh(H)
        #eigvecs = eigvecs.T
    
        # sparse
        eigvals, eigvecs = eigsh(H, k=dim[N]//eig_frac, which='SM')
        eigvecs = eigvecs.T
    
        # compute the IPR
        IPRs = np.sum(eigvecs**4, axis=1)

        # compute the r parameter
        diff = np.diff(eigvals)
        r = np.minimum(diff[:-1], diff[1:]) / np.maximum(diff[:-1], diff[1:])
        r = np.append(r, (0,0))
        
        # save to file
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "eigenvalue IPR r"
        np.savetxt(filename, np.stack((eigvals, IPRs, r)).T, header=head)
        """
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "eigval eigvec[0] eigvec[1] ..." 
        np.savetxt( filename, np.vstack((eigvals, eigvecs)).T, header=head )
        """








