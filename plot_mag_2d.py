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

plt.rcParams["figure.figsize"] = [6,6]


#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )


#  ---------------------------------  compute the magnetization  --------------------------------  #

# "magnetization" in the 2d plane: how much of the corner is removed
@nb.njit
def mag2d(v, levels):
    
    Mtemp = np.zeros((N,N), dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(N):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # iterate over the rows of the Young diagrams
            r = 0
            while r<n and levels[n][i,r]>0:
                Mtemp[r,:levels[n][i,r]] += v[k]
                r += 1
            
    return Mtemp


#  -------------------------------------------  main  ------------------------------------------  #

filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N,epsilon,0)
data = np.loadtxt(filename)
t_steps = len(data)

M = np.zeros((t_steps,N,N))

for dis in range(dis_num):

    #  load the vectors
    filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
    data = np.loadtxt(filename)
    
    ts = data[:,0]
    v = data[:,1:]
    
    # compute the magnetization
    for it in range(t_steps):
        M[it] += mag2d(v[it], levels)

M /= dis_num


#  -------------------------------------------  plot  ------------------------------------------  #

for it in range(t_steps):
    fig, ax = plt.subplots()
    
    #tics = np.linspace(0, 1, 11)
    
    im = ax.imshow(M[it], vmin=0, vmax=1)
    cbar = ax.figure.colorbar(im, ax=ax) #boundaries=tics, ticks=tics)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    
    #plt.clim((0,1))

    ax.set_title(r"n=%d: $\epsilon = %.2f, t = %.2f$" %(N,epsilon,ts[it]))

    #ax.set_xscale("log")
    #ax.set_yscale("log")

    #ax.legend()
    plt.savefig("Plots/e%.2f_t%.2f.pdf"%(epsilon,ts[it]), bbox_inches='tight')
    #plt.show()
    plt.clf()
















