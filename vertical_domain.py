#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state in the Hilbert space of domain walls with a single defect.
#   Needed for some checks.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.linalg import eigh,expm
from scipy import sparse
from scipy.sparse.linalg import expm_multiply
from time import time


# system size
N = int( sys.argv[1] )
dim = np.arange(N+1)
dim = dim*(dim-1)//2

# time evolution parameters
Tfin = float( sys.argv[2] )
dt = float( sys.argv[3] )
t_steps = int( Tfin/dt )
save_dt = float( sys.argv[4] )
save_step = int( save_dt/dt )
save_steps = int( Tfin/save_dt )


#  ---------------------------  real space representation of states  ---------------------------  #

# The states are represented as couples (a,b) indicating the left and right boundaries of the
# impurity. They are accessed in time~O(1) using their link to the triangular numbers.

def state_from_index(k):
    if k > 2:
        d = np.where(k < dim[1:])[0][0]
        return (k%dim[d],d)
    elif k == 0:
        return (0,1)
    elif k == 1:
        return (0,2)
    elif k == 2:
        return (1,2)

def index_from_state(s):
    return dim[s[1]] + s[0]
 
"""
# to check
states = []
for b in range(1,N):
    for a in range(b):
        states.append( (a,b) )

states = np.array(states, dtype=np.int_)

for k in range(dim[N]):
    print(k, states[k], index_from_state(states[k]), state_from_index(k))
exit(0)
"""


#  --------------------------------  build the adjacency matrix  -------------------------------  #

"""
# to check
H2 = np.zeros((dim[N],dim[N]))
for k in range(dim[N]):
    for l in range(k):
        if np.sum(np.abs(states[k]-states[l])) == 1:
            H2[k,l] = 1.
            H2[l,k] = 1.
"""

H = sparse.lil_matrix((dim[N],dim[N]))
for k in range(dim[N]):
    s = state_from_index(k)
    
    # move the left boundary to the left
    if s[0] > 0:
        s2 = (s[0]-1,s[1])
        H[k,index_from_state(s2)] = 1.
        
    # move the right boundary to the right
    if s[1] < N-1:
        s2 = (s[0],s[1]+1)
        H[k,index_from_state(s2)] = 1.

    # if there is space between the two boundaries
    if s[1]-s[0] > 1:
        
        # move the left boundary to the right
        s2 = (s[0]+1,s[1])
        H[k,index_from_state(s2)] = 1.
        
        # move the right boundary to the left
        s2 = (s[0],s[1]-1)
        H[k,index_from_state(s2)] = 1.
    

H = sparse.csr_matrix(H)


#  ---------------------------------------  time evolve  ---------------------------------------  #


v = np.zeros(dim[N])
v[index_from_state((N//2,N//2+1))] = 1

IPR = np.zeros(save_steps+1)
IPR[0] = 1.

"""
# dense
U = expm(-1j*H.todense()*dt)
c = 1
for it in range(1,t_steps):
    v = U.dot(v)
        
    if it%save_step == 0:
        IPR[c] = np.sum(np.abs(v)**4)
        
        c += 1
"""

# sparse
vt = expm_multiply(-1j*H*dt, v, start=0, stop=t_steps, num=save_steps+1)

for it in range(save_steps+1):
    IPR[it] = np.sum( np.abs(vt[it])**4 )


#  ---------------------------------------  save to file  --------------------------------------  #

filename = "Results/DW_N%d.txt" % N
toSave = np.stack( (np.arange(save_steps+1)*save_dt, IPR) ).T
head = "t IPR"
np.savetxt(filename, toSave, header=head)


#  -------------------------------------------  plot  ------------------------------------------  #
"""
from matplotlib import pyplot as plt
from matplotlib import cm

fig, ax = plt.subplots()
#cols = cm.get_cmap('magma', 10)

ax.plot(np.arange(save_steps+1)*save_dt, IPR, '-', c='black')

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"IPR")

ax.set_xscale('log')
ax.set_yscale('log')

ax.legend()
plt.show()
"""











