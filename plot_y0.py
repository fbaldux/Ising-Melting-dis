#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm


instring = input("").split(' ')

N = int( instring[0] )
epsilon = float( instring[1] )
dis_num = int( instring[2] )


#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )


#  -----------------------------------  compute height at 0  -----------------------------------  #

# build (diagonal) operator that gives the height at 0 of the tilted Young diagram
@nb.njit
def height0(levels):
    h0 = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # check how many rows are longer than their index (i.e. one can fit in a square)
            r = 0
            while r<n and levels[n][i,r]>r:
                r += 1
            
            h0[k] = r
            
    return h0


#  -------------------------------------------  main  ------------------------------------------  #

filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N,epsilon,0)
data = np.loadtxt(filename)
t_steps = len(data)

h = np.zeros(t_steps)

# build the height operator
h_op = height0(levels)

for dis in range(dis_num):

    #  load the vectors
    filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
    data = np.loadtxt(filename)
    
    ts = data[:,0]
    v = data[:,1:]
    
    # compute the height
    for it in range(len(ts)):
        h[it] += np.dot(v[it],h_op)

h /= dis_num


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()

ax.plot(ts, h, '-')

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"height")

#plt.clim((0,1))

#ax.set_title(r"n=%d: $\epsilon = %.2f, t = %.2f$" %(N,epsilon,ts[it]))

#ax.set_xscale("log")
#ax.set_yscale("log")

#ax.legend()
#plt.savefig("Plots/e%.2f_t%.2f.pdf"%(epsilon,ts[it]), bbox_inches='tight')
plt.show()
#plt.clf()
















