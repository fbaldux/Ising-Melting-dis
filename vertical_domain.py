#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state in the Hilbert space of domain walls with a single defect.
#   Needed for some checks.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy.linalg import eigh,expm
from matplotlib import pyplot as plt
from matplotlib import cm
#import numba as nb


N = 40
dim = N*(N-1)//2

Tfin = 100.
dt = 0.5
t_steps = int( Tfin/dt ) + 1

#save_dt = 2
#save_step = int( save_dt/dt )

fig, ax = plt.subplots()
#cols = cm.get_cmap('magma', 10)


#  ------------------------------------  build Hamiltonian  ------------------------------------  #

# real space representation of states
states = []
for a in range(N-1):
    for b in range(a+1,N):
        states += [(a,b)]
    
states = np.array(states)


# build the adjacency matrix
H = np.zeros((dim,dim))
for k in range(dim):
    for l in range(k):
        if np.sum(np.abs(states[k]-states[l])) == 1:
            H[k,l] = 1.
            H[l,k] = 1.

U = expm(-1j*H*dt)

"""
ax.imshow(H, cmap='magma_r')
plt.show()
exit(0)
"""

#  ---------------------------------------  time evolve  ---------------------------------------  #


v = np.zeros(dim)
v[1] = 1

IPR = np.zeros(t_steps)
IPR[0] = 1.

c = 0
for it in range(1,t_steps):
    v = U.dot(v)
    
    IPR[it] = np.sum(np.abs(v)**4)
    
    #if it%save_step == 0:
        #ax.plot(np.arange(dim), np.abs(v)**2, '.', c=cols(c), label=it*dt)
    #    c += 1

# final time
#ax.plot(np.arange(dim), np.abs(v)**2, '.', c=cols(c), label=it*dt)

np.savetxt("Results/DW_N%d.txt" % (N), np.stack((np.arange(t_steps)*dt,IPR)).T, header="t IPR")

"""
ax.plot(np.arange(t_steps)*dt, IPR, '-', c='black')

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"IPR")

ax.set_xscale('log')
ax.set_yscale('log')

ax.legend()
plt.show()

"""












