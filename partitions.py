#  ---------------------------------------------------------------------------------------------  #
#
#   The program contains routines for building the Young diagrams.
#
#  ---------------------------------------------------------------------------------------------  #

import os
import numpy as np
from scipy import sparse
import numba as nb

#  -----------------------  dimensions of the Young graph level by level  ----------------------  #

p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)


#  ----------------------------  generate the partitions at level n  ---------------------------  #

# accelerated ruleAsc algorithm: https://jeromekelleher.net/category/combinatorics.html
@nb.njit
def generate_partitions(n):
    a = np.zeros(n+1, dtype=np.int_)
    k = 1
    y = n - 1
    while k!=0:
        x = a[k-1] + 1
        k -= 1
        while 2*x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield np.concatenate(( np.flip(a[:k+2]), np.zeros(n-k-2,dtype=np.int_) ))
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield np.concatenate(( np.flip(a[:k+1]), np.zeros(n-k-1,dtype=np.int_) ))


#  -------------------------------  load hopping terms from file  ------------------------------  #

def load_adjacency(N):
    H0 = sparse.lil_matrix((dim[N],dim[N]))
    H0[0,1] = 1
    H0 = sparse.csr_matrix(H0)

    for n in range(2,N+1):
    
        filename = "Hamiltonians/clean_N%d.txt" % n
        if os.path.isfile(filename):
            row_ind, col_ind = np.loadtxt(filename).T
        else:
            print("\nError! Hamiltonian for N=%d not built!\n" % n)
            exit(0)

        H0 += sparse.csr_matrix((np.ones(len(row_ind)), (row_ind, col_ind)), shape=(dim[N], dim[N]))

    H0 += H0.T
    
    return H0





