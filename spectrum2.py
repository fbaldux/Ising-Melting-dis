#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian.
#
#   - It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries, and converts it to a full matrix.
#   - It saves to Results/spec_{...} the
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
Nmax = 26

# disorder
epsilon = 6



import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm

cols = cm.get_cmap("turbo", 10)


#  -------------------------------------------  main  ------------------------------------------  #

c = 0
for N in range(12,22,2):
    
    H0 = load_adjacency(N)
    
    # load the disorder
    filename = "Hamiltonians/rand_N%d_d%d.txt" % (Nmax,0)
    D = np.loadtxt(filename)[:dim[N]]
    H = H0 + epsilon * sparse.diags(D)

    # dense
    eigvals, eigvecs = eigh(H.todense())
    eigvecs = eigvecs.T
    #eigvecs2 = eigvecs**2
    #del eigvecs, H

    #plt.plot(np.arange(-dim[N]//2,dim[N]//2)/dim[N], eigvals, 'o', ms=2, label=N, c=cols(c))
    #plt.plot(np.arange(-dim[N]//2,dim[N]//2), np.abs(eigvecs[:,0])**2, 'o', ms=2, label=N, c=cols(c))
    """
    ii = np.argsort(np.abs(eigvals))[:10]
    for i in ii:
        plt.plot(i-dim[N]//2, np.abs(eigvecs[i,0])**2, 's', ms=5, c=cols(c))
    """
    
    #i = np.argmax(np.abs(eigvecs[:,0])**2)
    #plt.plot(np.arange(dim[N]), np.abs(eigvecs[i])**2, 'o', ms=2, label=N, c=cols(c))
    
    
    j = np.random.randint(dim[N//2], dim[N//2+1])
    plt.plot(np.arange(-dim[N]//2,dim[N]//2), np.abs(eigvecs[:,j])**2, 'o', ms=2, label=N, c=cols(c))
    
    
    c += 1
    
plt.yscale('log')

plt.legend()
plt.show()







