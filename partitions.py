#  ---------------------------------------------------------------------------------------------  #
#
#   The program contains routines for building the Young diagrams.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
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
        
