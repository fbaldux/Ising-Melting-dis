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

instring = input("").split(' ')

N = int( instring[0] )
dis_num = int( instring[1] )


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

for dis in range(dis_num):
    
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



















