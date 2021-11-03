#  ---------------------------------------------------------------------------------------------  #
#
#   The program builds the ... as follows:
#   - 
#
#   The program uses Numba to speed up calculations.
#   The row indices, column indices and matrix elements are saved to a .txt file.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
#from time import time as now

instring = input("").split(' ')

N = int( instring[0] )


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


#  -------------------------------  save the partitions to a file  -------------------------------  #

for n in range(N+1):
    
    # generate partitions
    partitions = np.array( [x for x in generate_partitions(n)] )
        
    # save to file
    filename = "Partitions/N%d.txt" % n
    np.savetxt(filename, partitions, fmt='%d')
















