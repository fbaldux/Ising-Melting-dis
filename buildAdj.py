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


#  ------------------------------------  create dictionary  ------------------------------------  #

def create_dict(l):
    l_string = [','.join([str(num) for num in x]) for x in l]
    
    d = {l_string[i]:i for i in range(len(l_string))}

    return d

#  -------------------------------  generate nearest neighbours  -------------------------------  #

# generate partitions on the next level that come from C
# the routine tries to add a box to each row
#@nb.njit
def nearest_neigh(C):
    # I can always add to the 0-th row
    temp = np.copy(C)
    temp[0] += 1
    yield temp
    
    # in the bulk, check if allowed
    for row in range(1,len(C)):
        
        if C[row-1]>C[row]:
            temp = np.copy(C) 
            temp[row] += 1
            yield temp


#  ------------------------  build adjacency matrix between two levels  ------------------------  #

#@nb.njit
def update_adj(l, d_next, n):
    row_ind = [np.int_(1) for i in range(0)]
    col_ind = [np.int_(1) for i in range(0)]
        
    for i in range(p[n]):
        
        # generate the partitions coming from l[i]
        NN = [x for x in nearest_neigh(l[i])]
        
        # convert NN into strings for hashing
        NN_string = [','.join([str(y) for y in x]) for x in NN]
        
        for s in NN_string:
            row_ind.append(dim[n-1]+i)
            col_ind.append(dim[n]+d_next[s])
    
    return row_ind, col_ind


#  ---------------------------------------  save to file  --------------------------------------  #

def save_adj(n,row_ind,col_ind):
    
    filename = "Hamiltonians/clean_N%d.txt" % n
    toSave = np.array((row_ind,col_ind)).T
    head = "row col"
    np.savetxt(filename, toSave, header=head, fmt='%d')


#  -------------------------------------------  main  ------------------------------------------  #


next_level = np.array( [x for x in generate_partitions(Nin)] )

for n in range(Nin,Nfin):

    # reshape level n to make the strings long n+1
    level = np.append(next_level, np.zeros((p[n],1), dtype=np.int_), 1)
    
    # generate level n+1
    next_level = np.array( [x for x in generate_partitions(n+1)] )
    dict_nl = create_dict(next_level)
    
    # update the adjacencies
    row_ind, col_ind = update_adj(level, dict_nl, n)
    
    # save the adjacency matrices
    save_adj(n+1, row_ind, col_ind)
        
    #print("built adj. for N = %d" % (n+1))
    print(n+1, time()-start)
    

















