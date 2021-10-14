#  ---------------------------------------------------------------------------------------------  #
#
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy import sparse
import numba as nb


n_fin = 7

p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)

#  ----------------------------  generate the partitions at level n  ---------------------------  #

# accelerated ruleAsc algorithm: https://jeromekelleher.net/category/combinatorics.html
@nb.jit
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
            yield np.concatenate(( a[:k+2], np.zeros(n-k-2,dtype=np.int_) ))
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield np.concatenate(( a[:k+1], np.zeros(n-k-1,dtype=np.int_) ))
        

#  ----------------------------  ...  ---------------------------  #

A = sparse.csr_matrix((dim[n_fin],dim[n_fin]))

next_level = np.array( [x for x in generate_partitions(1)] )
for n in range(1,n_fin):

    level = np.append(next_level, np.zeros((p[n],1), dtype=np.int_), 1)
    next_level = np.array( [x for x in generate_partitions(n+1)] )
    
    print("\n", level.shape)
    print(level)
    
    for i in range(len(next_level)):
        for j in range(len(level)):
            if np.sum(next_level[i]-level[j]) == 1:
                A[dim[n]+i, dim[n-1]+j] = 1
                A[dim[n-1]+j, dim[n]+i] = 1
    
print("\n", A)































