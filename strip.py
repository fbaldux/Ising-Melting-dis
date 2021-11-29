#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state in the Hilbert space of a strip of length L.
#   Needed for some checks.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.linalg import expm
from scipy import sparse
from LanczosRoutines import *
from time import time

#  ------------------------------------  program constants  ------------------------------------  #

Fibonacci = np.array((0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,\
             4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040,\
             1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986))

# system size
L = int( sys.argv[1] )
dim = Fibonacci[L]

# time evolution parameters
Tfin = float( sys.argv[2] )
dt = float( sys.argv[3] )
t_steps = int( Tfin/dt )
save_dt = float( sys.argv[4] )
save_step = int( save_dt/dt )

start = time()


#  ---------------------------------  find all flippable spins  --------------------------------  #

def find_000(state):
    
    l = []
    
    for i in range(1,L-1):        
        if state[i-1:i+2] == '000':
            l.append(i)
    
    return l


#  --------------------------------------  initial state  --------------------------------------  #

# construct the all down state
v0 = ''.join(['0' for i in range(L)])


#  --------------------------------  construct adjacency matrix  -------------------------------  #

intvec = np.vectorize(int)

states_dict = {v0:0}
states = [v0]
last = 0

row_ind = []
col_ind = []

# propagate through the graph
c = 1
while len(states)<dim:
    
    pivot = len(states)
    
    for i in range(last, len(states)):
        flip_sites = find_000(states[i])
        
        for f in flip_sites:
            temp = [x for x in states[i]]
            temp[f] = '1'
            temp = ''.join(temp)
            
            if temp in states_dict:
                row_ind.append(i)
                col_ind.append(states_dict[temp])
            else:
                states_dict[temp] = c
                states.append(temp)                
                
                row_ind.append(i)
                col_ind.append(c)
                c += 1

    last = pivot


#  ---------------------------------------  save to file  --------------------------------------  #
"""
# save dictionary
f = open("Hamiltonians/stripStates_L%d.txt" % L, 'w')
f.write("# state index\n")
for s in states_dict:
    f.write("%s %d\n" % (s, states_dict[s]))
f.close() 


# save adjacency matrix
f = open("Hamiltonians/stripAdj_L%d.txt" % L, 'w')
f.write("# row_ind col_ind\n")
for i in range(len(row_ind)):
    f.write("%d %d\n" % (row_ind[i], col_ind[i]))
f.close() 
"""

#  -----------------------------  construct magnetization matrices  ----------------------------  #

m = np.ones((L,dim))

for state in states:
    for i in range(L):
        if state[i] == '0':
            m[i,states_dict[state]] = -1.


#  ---------------------------------------  time evolve  ---------------------------------------  #

H = sparse.csr_matrix((np.ones(len(row_ind)), (row_ind, col_ind)), shape=(dim, dim))
H += H.T

# dense
#U = expm(-1j * H.todense() * dt)
# sparse
applyH = lambda v: 1j * H.dot(v)

# initial state
v = np.zeros(dim)
v[0] = 1.

# array to save observables
toSave = np.zeros((int(Tfin/save_dt)+1,L+1)) # t m[0] m[1] ... m[L-1]
toSave[0,1:] = np.einsum('ab,b->a', m, np.abs(v)**2)

c = 1
for it in range(1,t_steps+1):
    # dense
    #v = U.dot(v)
    # sparse
    v = expm_krylov_lanczos(applyH, v, dt, numiter=100)
    
    
    if it%save_step == 0:
        toSave[c,0] = it*dt
        toSave[c,1:] = np.einsum('ab,b->a', m, np.abs(v)**2)
        c += 1


# save to file
filename = "Results/stripEv_L%d.txt" % (L)
head = "t m[0] m[1] ... m[L-1]"
np.savetxt(filename, toSave, header=head)



from matplotlib import pyplot as plt

plt.plot(np.arange(L), toSave[0,1:], '-')
plt.plot(np.arange(L), toSave[-1,1:], '-')

plt.show()














