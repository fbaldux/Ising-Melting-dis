#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian.
#
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It saves to Results/spec_{...} a fraction, at the center of the spectrum, of the
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

# number of eigenvalues (for sparse diagonalization)
#eig_frac = int( sys.argv[3] )
eig_num = int( sys.argv[3] )

# number of disorder instances
dis_num_in = int( sys.argv[4] )
dis_num_fin = int( sys.argv[5] )

# whether to overwrite existing files
overwrite = int( sys.argv[6] )

# number of processors to use
nProc = int( sys.argv[7] )


os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from partitions import *
from time import time

np.seterr(divide='ignore')

#eig_num = dim[N]//eig_frac
start = time()

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
        H = H0 + epsilon * sparse.diags(np.loadtxt(filename))
                
        # sparse
        center = np.sum(H.diagonal())
        eigvals, eigvecs = eigsh(H, k=eig_num, which='LM', sigma=center)
        eigvecs = eigvecs.T
        eigvecs2 = eigvecs**2
        del eigvecs, H
            
        # compute the IPR
        IPRs = np.sum(eigvecs2**2, axis=1)
        
        # compute the KL divergence of neighbouring states
        KL = np.zeros(eig_num)
        KL[:-1] = np.einsum( "ab,ab->a", eigvecs2[:-1], np.log(eigvecs2[:-1]/eigvecs2[1:]) )
        
        # compute the participaton entropies
        PE = - np.einsum( "ab,ab->a", eigvecs2, np.log(eigvecs2) )
        
        # compute the magnetization difference in the corner of neighbouring states
        magDiff = np.zeros(eig_num)
        magDiff[:-1] = 2 * (eigvecs2[1:,0] - eigvecs2[:1,0])
        
        
        # save to file
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        toSave = np.stack((eigvals, IPRs, KL, PE, magDiff)).T
        head = "eigenvalue IPR KL PE magDiff"
        np.savetxt(filename, toSave, header=head)
        
        """
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "eigval eigvec[0] eigvec[1] ..." 
        np.savetxt( filename, np.vstack((eigvals, eigvecs)).T, header=head )
        """

print("End spec N%d e%.4f d%d-%d" % (N,epsilon,dis_num_in,dis_num_fin))
#print(N, time()-start)





