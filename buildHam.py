#  ---------------------------------------------------------------------------------------------  #
#
#   The program builds the adjacency matrix of the partitions graph as follows:
#   - It generates all partitions of n and n+1 w/ the accelerated ruleAsc algorithm 
#   - It runs through both arrays and finds what couples are linked by a "hook move"
#   - It saves the sparse adjacency matrix entry by entry (i.e. row indices and column indices
#     that are non-zero) 
#
#   The program uses Numba to speed up calculations.
#   The data, row indices and column indices are saved to txt file.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
#from time import time as now

instring = input("").split(' ')

N = int( instring[0] )

#start = now()

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
        

#  ----------------------------------  build adjacency matrix  ---------------------------------  #

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

# the first box
row_ind = [0]
col_ind = [1]  

# file of sparse Hamiltonians sizes
flen = open("ham_lengths.txt", "w")
flen.write("# N nonzero_elements\n")
flen.close()

next_level = np.array( [x for x in generate_partitions(1)] )
levels = [next_level]
for n in range(1,N):

    # reshape level n to make the strings long n+1
    level = np.append(next_level, np.zeros((p[n],1), dtype=np.int_), 1)
    
    # generate level n+1
    next_level = np.array( [x for x in generate_partitions(n+1)] )
        
    # store all the levels
    levels.append( next_level )
    
    # update the adjacencies
    temp = update_adj(level,next_level,n)
    row_ind += temp[0]
    col_ind += temp[1]
    
    # save the lengths
    flen = open("ham_lengths.txt", "a")
    flen.write("%d %d\n" % (n+1,len(row_ind)))
    flen.close()
    
#  ---------------------------------------  save to file  --------------------------------------  #

filename = "Hamiltonians/clean_N%d.txt" % N
toSave = np.array((row_ind,col_ind)).T
head = "row col"
np.savetxt(filename, toSave, header=head, fmt='%d')

#print("A built", now()-start)
#print(n, now()-start)

















