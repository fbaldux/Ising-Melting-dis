import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
import numba as nb
from time import time as now

N = 10

"""A = sparse.lil_matrix((10,10))

A[1,9] = 1
A[1,1] = 1

A[7,7] = 1"""

@nb.njit
def f():
    a = [[np.int_(1) for j in range(0)] for i in range(10)]
    return a
    
print(f())
"""
@nb.njit
def qwerty():
    
    rows.append(2)
    data.append(1.)
    
    return rows, data

rows = nb.typed.List([[1] for i in range(N)])
data = nb.typed.List([[1] for i in range(N)])
"""
#rows, data = qwerty()



#print(A.__dict__)
#print("\n", rows[0])
#print("\n", data[0])

#print("\n", A.todense())
