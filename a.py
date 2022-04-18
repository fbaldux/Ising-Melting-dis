#!/usr/local/bin/python3
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
import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from partitions import *
import numba as nb


# system size
N = 60




#  ------------------------------------  x  -----------------------------------  #

toSave = np.zeros((N+1,3), dtype=np.int_)
toSave[:,0] = np.arange(N+1)

toSave[0,1] = 0
toSave[0,2] = 1

toSave[1,1] = 1
toSave[1,2] = 1 + dim[1]



for n in range(2,N+1):

    print(n)
    
    # MANCA CUMSUM
    filename = "Hamiltonians/clean_N%d.txt" % n
    temp = np.loadtxt(filename).T
    
    toSave[n,1] = len(temp[0])*2
    toSave[n,2] = toSave[n,1] + dim[n]
    
np.savetxt("ham_lengths.txt", toSave, fmt="%d")
    





