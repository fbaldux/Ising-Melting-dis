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

import sys, os

# system size
N = 30

import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from partitions import *
import numba as nb
from matplotlib import pyplot as plt

np.seterr(divide='ignore')

#  ------------------------------------  load hopping terms  -----------------------------------  #




#  ------------------------------------  ...  -----------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )

levels = tuple(levels)


# "magnetization" in the 2d plane: how much of the corner is removed
@nb.njit
def build_mag2d():
    
    M = np.zeros((N,N,dim[N]), dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # iterate over the rows of the Young diagrams
            r = 0
            while r<n and levels[n][i,r]>0:
                M[r,:levels[n][i,r],k] = 1
                r += 1
            
    return M

mag2d_op = build_mag2d()


"""
triang = np.cumsum(np.arange(N+1))

def build_mag2d_2():
    
    M = np.zeros((triang[N],dim[N]), dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # iterate over the rows of the Young diagrams
            r = 0
            while r<n and levels[n][i,r]>0:
                M[triang[r]:triang[r]+levels[n][i,r],k] = 1
                r += 1
            
    return M

mag2d_op2 = build_mag2d_2()
"""

"""
for k in range(dim[N]):
    print(mag2d_op[:,:,k])
exit(0)
"""
"""
for n in range(1,N+1):
    for i in range(p[n]):
        k = dim[n-1]+i
        print(levels[n][i])
        print(mag2d_op[:,:,k])
        print(mag2d_op2[:,k])
        print("-------------------------------\n")
exit(0)
"""



"""
n = 10
i = 12
k = dim[n-1]+i
print(levels[n][i])

v = np.zeros(dim[N])
v[k] = 1

M = np.einsum("abc,c->ab", mag2d_op,v)

M[1,1] = 100

plt.imshow(M)

plt.show()
"""


M = np.einsum("xyi,i->xy", mag2d_op, np.ones(dim[N]))

M[M!=0] = 1
plt.imshow(M)
"""
M = M.flatten()
mag2d_op = mag2d_op.reshape(N*N,dim[N])
mag2d_op = mag2d_op[M!=0]
for k in range(dim[N]):
    print(mag2d_op[:,k])
"""
plt.show()








