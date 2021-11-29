#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state in the Hilbert space of a strip of length L.
#   Needed for some checks.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy import sparse
from time import time

#  ------------------------------------  program constants  ------------------------------------  #


# system size
L = int( sys.argv[1] )
# Hilbert space size
dimH = 2**L

start = time()

#  -------------------------------  construct the basic matrices  ------------------------------  #

exec(open("matBuilder.py").read())


#  -------------------------------------  adjacency matrix  ------------------------------------  #

T = sparse.csr_matrix((dimH,dimH))
# for the whole Hilbert space
for i in range(1,L-1):
    T += 0.25 * (sparse.identity(2**L)-sz_list[i-1]) @ sp_list[i] @ (sparse.identity(2**L)-sz_list[i+1])


#  --------------------------------------  initial state  --------------------------------------  #

# construct the all up state
v0 = 1.
for i in range(L):
    v0 = np.kron(v0, np.array((0.,1.)))


def print_spins(v):
    print("\n\nVettore:")
    print(v)
    print("Configurazioni:")
    
    for k in np.nonzero(v)[0]:
        v2 = np.zeros(dimH_red)
        v2[k] = 1.
        
        s = np.zeros(L)
        for i in range(L):
            s[i] = np.dot(v2, Psz_list[i].dot(v2))
        print(s*2)

#  -------------------------------------------  main  ------------------------------------------  #

intvec = np.vectorize(int)

        
# load the initial state
v = np.copy(v0)
# keep track of the already visited states
visited = np.copy(v0)

# propagate through the graph
for r in range(L):        
    v = T.dot(v)
    v[visited!=0] = 0.

    # put a 1 on the visited sites
    visited += intvec(v!=0)

print(2**L, np.sum(visited))

"""
# check adiacenza
print_spins(v)
for r in range(L//2+1):        
    v = T0.dot(v)   
    #v[visited!=0] = 0.
    #visited += intvec(v!=0)
    print_spins(v)
"""








