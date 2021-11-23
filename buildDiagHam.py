#  ---------------------------------------------------------------------------------------------  #
#
#   The program builds the diagonal part of the Hamiltonian for the partitions graph. It proceeds as follows:
#   - It generates all partitions of n w/ the accelerated ruleAsc algorithm 
#   - It extracts a NxN grid of disordered on-site energies for the 2d model. The energies are
#     uniformly distributed in [-1,1], then the disorder strength can be easily increased by
#     rescaling with an overall factor.
#   - For each partition, it sums the disordered energies contained in the shape
#
#   The program uses Numba to speed up calculations.
#   The row indices, column indices and matrix elements are saved to a .txt file.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
rng = np.random.default_rng()
from partitions import *

instring = input("").split(' ')

N = int( instring[0] )
dis_num_in = int( instring[1] )
dis_num_fin = int( instring[2] )


#  -------------------------------  compute the matrix elements  -------------------------------  #

@nb.njit
def update_diag(l,square_dis,n):
    matr_el = [np.float_(1) for i in range(0)]
    
    # sum the squares in the Young diagram
    for i in range(p[n]):
        r = 0
        tot = 0.
        while r<n and l[i,r]>0:
            tot += np.sum(square_dis[r,:l[i,r]])
            r += 1

        matr_el.append(tot)        
    
    return matr_el


#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )


#  --------------------------  build the diagonal of the Hamiltonian  --------------------------  #

for dis in range(dis_num_in, dis_num_fin):
    
    # extract the disorder
    square_dis = rng.uniform(-1,1,size=(N,N))

    # arrays for the sparse Hamiltonian
    matr_el = [0.]  

    for n in range(1,N+1):
        matr_el += update_diag(levels[n],square_dis,n)
    
    
    #  save to file
    filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
    head = "element [column and row given by index]"
    np.savetxt(filename, matr_el, header=head)



















