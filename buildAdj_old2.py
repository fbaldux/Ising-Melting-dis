#  ---------------------------------------------------------------------------------------------  #
#
#   The program builds the adjacency matrix of the partitions graph as follows:
#   - It generates all partitions of n and n+1 w/ the accelerated ruleAsc algorithm 
#   - It runs through both arrays and finds what couples are linked by a "hook move"
#   - It saves the sparse adjacency matrix entry by entry (i.e. row indices and column indices
#     that are non-zero) 
#
#   The program uses Numba to speed up calculations.
#   The row indices and column indices are saved to a .txt file for each level.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
import numba as nb
from partitions import *
from time import time

start = time()


Nin = int( sys.argv[1] )
Nfin = int( sys.argv[2] )

# Nin should be > 0
if Nin == 0:
    Nin = 1


#  ------------------------  build adjacency matrix between two levels  ------------------------  #

@nb.njit
def update_adj(l1,l2,n):
    row_ind = [np.int_(1) for i in range(0)]
    col_ind = [np.int_(1) for i in range(0)]
    
    # check what are the partitions differing just by 1
    for i in range(p[n+1]):
        for j in range(p[n]):
            if np.sum((l2[i]-l1[j])**2) == 1:
                row_ind.append(dim[n]+i)
                col_ind.append(dim[n-1]+j)
    
    return row_ind, col_ind


#  ---------------------------------------  save to file  --------------------------------------  #

def save_adj(n,row_ind,col_ind):
    
    filename = "Hamiltonians2/clean_N%d.txt" % n
    toSave = np.array((row_ind,col_ind)).T
    head = "row col"
    np.savetxt(filename, toSave, header=head, fmt='%d')


#  -------------------------------------------  main  ------------------------------------------  #


next_level = np.array( [x for x in generate_partitions(Nin)] )
levels = [next_level]
for n in range(Nin,Nfin):

    # reshape level n to make the strings long n+1
    level = np.append(next_level, np.zeros((p[n],1), dtype=np.int_), 1)
    
    # generate level n+1
    next_level = np.array( [x for x in generate_partitions(n+1)] )
    
    # update the adjacencies
    row_ind, col_ind = update_adj(level,next_level,n)
    
    # save the adjacency matrices
    save_adj(n+1, row_ind, col_ind)
    
    #print("built adj. for N = %d" % (n+1))
    print(n+1, time()-start)

















