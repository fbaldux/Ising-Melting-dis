#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state in the Hilbert space of domain walls with a single defect.
#   Needed for some checks.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy.linalg import eigh,expm
from LanczosRoutines import *
from matplotlib import pyplot as plt
from matplotlib import cm
#import numba as nb


N = 320
dim = N*(N-1)//2

Tfin = 2.
dt = 0.2
t_steps = int( Tfin/dt ) + 1

save_dt = 0.2
save_step = int( save_dt/dt )


#  ------------------------------------  build Hamiltonian  ------------------------------------  #

# real space representation of states
states = []
for a in range(N-1):
    for b in range(a+1,N):
        states.append( (a,b) )

states = np.array(states, dtype=np.int_)


# build the adjacency matrix
H = np.zeros((dim,dim))
for k in range(dim):
    for l in range(k):
        if np.sum(np.abs(states[k]-states[l])) == 1:
            H[k,l] = 1.
            H[l,k] = 1.

applyH = lambda v: 1j * H.dot(v)
#U = expm(-1j*H*dt)


#  ---------------------------------------  time evolve  ---------------------------------------  #


v = np.zeros(dim)
k = 0
while k < dim:
    if states[k,0]==N//2 and states[k,1]==N//2+1:
        break
    else:
        k += 1
v[k] = 1

IPR = np.zeros(t_steps//save_step + 1)
IPR[0] = 1.

c = 1
for it in range(1,t_steps):
    #v = U.dot(v)
    v = expm_krylov_lanczos(applyH, v, dt, numiter=100)
        
    if it%save_step == 0:
        IPR[c] = np.sum(np.abs(v)**4)
        
        c += 1


np.savetxt("Results/DW_N%d.txt" % (N), np.stack((np.arange(len(IPR))*save_dt,IPR)).T, header="t IPR")

"""
fig, ax = plt.subplots()
#cols = cm.get_cmap('magma', 10)

ax.plot(np.arange(t_steps)*dt, IPR, '-', c='black')

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"IPR")

ax.set_xscale('log')
ax.set_yscale('log')

ax.legend()
plt.show()

"""











