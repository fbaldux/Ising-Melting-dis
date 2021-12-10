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

p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, \
            297, 385, 490, 627, 792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, \
            4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977, 21637, 26015, \
            31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, \
            147273, 173525, 204226, 239943, 281589, 329931, 386155, 451276, \
            526823, 614154, 715220, 831820, 966467, 1121505, 1300156, 1505499, \
            1741630, 2012558, 2323520, 2679689, 3087735, 3554345, 4087968, \
            4697205, 5392783, 6185689, 7089500, 8118264, 9289091, 10619863, \
            12132164, 13848650, 15796476))

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


#  ------------------------  operators for quantifying the removed area  -----------------------  #

# (diagonal) operator that gives the height on the vertical line for the tilted Young diagrams
@nb.njit
def vertical_height(N,levels):
    vh = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # check how many rows are longer than their index (i.e. one can fit in a square)
            r = 0
            while r<n and levels[n][i,r]>r:
                r += 1
            
            vh[k] = r
            
    return vh


# (diagonal) operator that gives the length on the left side for the tilted Young diagrams
@nb.njit
def side1_length(N,levels):
    sl = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # the lateral length is the 0th entry of the level
            sl[k] = levels[n][i,0]
            
    return sl


# (diagonal) operator that gives the length on the right side for the tilted Young diagrams
@nb.njit
def side2_length(N,levels):
    sl = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # the lateral length is the first 0 entry
            temp = np.where(levels[n][i]==0)[0]
            if len(temp)>0:
                sl[k] = temp[0]
            else:
                sl[k] = n
     
    return sl


# (diagonal) operator that gives the area of the Young diagrams
def area(N):
    area_op = np.zeros(dim[N], dtype=np.float_)
    
    for n in range(1,N+1):
        area_op[dim[n-1]:dim[n]] = n
    
    return area_op


