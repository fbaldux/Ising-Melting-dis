#  ---------------------------------------------------------------------------------------------  #
#
#   The program ...
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from matplotlib import pyplot as plt

instring = input("").split(' ')

N = int( instring[0] )
rep_num = int( instring[1] )


#  ---------------------------------------  MC sampling  ---------------------------------------  #
"""
@nb.njit
def MC():
    shape = np.zeros(N, dtype=np.int_)
    shape[0] = 1
    
    c = 1
    max_row = 2
    while c<N:
        row = np.random.randint(max_row)
        
        if row==0 or shape[row-1]>shape[row]:
            shape[row] += 1
            c += 1
            
            if row == max_row-1:
                max_row += 1

    return shape
"""

cache = {}

def count_partitions(n, limit):
    if n == 0:
        return 1
    if (n, limit) in cache:
        return cache[n, limit]
    x = cache[n, limit] = sum(count_partitions(n-k, k) for k in range(1, min(limit, n) + 1))
    return x

def random_partition(n):
    a = []
    limit = n
    total = count_partitions(n, limit)
    which = np.random.randint(total)
    while n:
        for k in range(1, min(limit, n) + 1):
            count = count_partitions(n-k, k)
            if which < count:
                break
            which -= count
        a.append(k)
        limit = k
        n -= k
    return a

#  -------------------------------------------  main  ------------------------------------------  #

shape = np.zeros(N)
for rep in range(rep_num):
    
    s = np.array(random_partition(N))
    shape[:len(s)] += np.log(s)
    
    #plt.plot(N-shape, N-np.arange(N), '-')
  

shape /= rep_num
shape = np.exp(shape)

plt.plot(N-shape, N-np.arange(N), '-')
plt.show()
    