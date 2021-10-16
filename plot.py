#  ---------------------------------------------------------------------------------------------  #
#
#   The program ...
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()

instring = input("").split(' ')

N = int( instring[0] )


p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)

    
#  -------------------------------------  load Hamiltonian  ------------------------------------  #

filename = "Hamiltonians/n%d.txt" % N
row_ind, col_ind = np.loadtxt(filename).T
"""
A = sparse.csr_matrix((np.ones(len(row_ind)), (row_ind, col_ind)), shape=(dim[N], dim[N]))
A += A.T


#  ---------------------------------  diagonalize Hamiltonian  ---------------------------------  #

A = A.todense()


eigvals, eigvecs = eigh(A)
eigvecs = eigvecs.T


#ax.plot(np.arange(dim[N]), eigvals, '.', c='black')

ax.set_xlabel("k")
#ax.set_ylabel(r"$E_k$")
ax.set_ylabel(r"$\psi_k$")

for k in range(-1,2):
    ax.plot(np.arange(dim[N]), eigvecs[dim[N]//2+k], '.', label="%.2e"%eigvals[dim[N]//2+k], ms=5)

ax.plot(dim[:N], np.zeros(N), '.', c='red')
"""

ax.plot(row_ind, col_ind, '.', c='red', ms=2)
ax.plot(col_ind, row_ind, '.', c='red', ms=2)

for n in range(N):
    ax.plot(np.ones(dim[N])*dim[n], np.arange(dim[N]), '-', lw=0.5, c='black')
    ax.plot(np.arange(dim[N]), np.ones(dim[N])*dim[n], '-', lw=0.5, c='black')

ax.set_xlim((0,dim[N]))
ax.set_ylim((0,dim[N]))

ax.set_title("n=%d (dim=%d)" %(N,dim[N]))

#ax.set_xscale("log")
#ax.set_yscale("log")

#ax.legend()
plt.show()


















