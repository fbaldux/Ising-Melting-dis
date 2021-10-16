#  ---------------------------------------------------------------------------------------------  #
#
#   The program ...
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy import sparse
from scipy.linalg import eigh,expm
from scipy.sparse.linalg import eigsh
#from LanczosRoutines import *
from matplotlib import pyplot as plt
from matplotlib import cm

instring = input("").split(' ')

# system size
N = int( instring[0] )

# time evolution parameters
Tfin = float( instring[1] )
dt = float( instring[2] )
t_steps = int( Tfin/dt )
save_step = int( instring[3] )

p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)


#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()
cols = cm.get_cmap('viridis', t_steps+1)
    
#  -------------------------------------  load Hamiltonian  ------------------------------------  #

filename = "Hamiltonians/clean_N30.txt"
row_ind, col_ind = np.loadtxt(filename)[:dim[N]].T

H = sparse.csr_matrix((np.ones(len(row_ind)), (row_ind, col_ind)), shape=(dim[N], dim[N]))
H += H.T


#  -------------------------------  time evolve the Hamiltonian  -------------------------------  #

H = H.todense()
"""
def applyH(v):
    return 1j * H.dot(v)
"""

# initial state
v = np.zeros(dim[N])
v[0] = 1
U = expm(-1j*H*dt)

top = 0

for it in range(1,t_steps):
    v = U.dot(v)
    #v = expm_krylov_lanczos(applyH, v, dt, numiter=20)
    
    if it%save_step == 0:
        ax.plot(np.arange(dim[N]), np.abs(v)**2, '.', c=cols(it), label=it*dt)
        top = max(top, np.max(np.abs(v)**2))
        
for n in range(N):
    ax.plot(np.ones(2)*dim[n], np.linspace(0,top,2), '-', lw=0.75, c='black')


ax.set_title("n=%d (dim=%d)" %(N,dim[N]))

#ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend()
plt.show()


















