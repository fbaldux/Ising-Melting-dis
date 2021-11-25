#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
import numba as nb
from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm


N = int( sys.argv[1] )
epsilon = float( sys.argv[2] )
dis_num = int( sys.argv[3] )


plt.rcParams["figure.figsize"] = [6,6]

#fig, ax = plt.subplots()


#  ---------------------------------  build all the partitions  --------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )


#  ---------------------------------  compute the magnetization  --------------------------------  #

#@nb.njit
def mag2d(v):

    Mtemp = np.zeros((N,N))

    #
    for n in range(N):
        for i in range(p[n]):
            k = dim[n-1]+i

            r = 0
            while r<n and levels[n][i,r]>0:
                Mtemp[r,:levels[n][i,r]] += v[k]
                r += 1

    return Mtemp


#  --------------------------  load data  --------------------------  #

filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N,epsilon,0)
data = np.loadtxt(filename)
t_steps = len(data)

M = np.zeros((t_steps,N,N))

#  --------------------------  compute the 2d magnetization  --------------------------  #

for dis in range(dis_num):

    #  load the vectors
    filename = "Results/tEv_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
    data = np.loadtxt(filename)

    ts = data[:,0]
    v = data[:,1:]

    # compute the magnetization
    for it in range(t_steps):
        M[it] += mag2d(v[it])

M /= dis_num

#  --------------------------  determines the averge position along the line y=x  --------------------------  #

y = np.zeros(t_steps)
for it in range(t_steps):
    y_t=0
    n_t=0
    for x in range(N):
        y_t += x*M[it,x,x]
        n_t += M[it,x,x]

    y[it] = y_t/n_t

#  --------------------------  save data  --------------------------  #

filename = "Results/y%.4f.txt" % epsilon
toSave = np.array((np.arange(t_steps), y)).T
head = "time y"
np.savetxt(filename, toSave, header=head)

"""
ax.plot(np.arange(t_steps), y, '-', label="y")

ax.set_xlabel("t")
ax.set_ylabel("y")

#ax.set_title("n=%d (dim=%d)" %(N,dim[N]))
#ax.set_title(r"n=%d: $\epsilon = %.2f$" %(N,epsilon))

#ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend()
#plt.savefig("eps%.2f.pdf"%epsilon, bbox_inches='tight')
plt.show()

exit(0)
"""
#  --------------------------  plot  --------------------------  #
"""
for it in range(t_steps):
    fig, ax = plt.subplots()

    #tics = np.linspace(0, 1, 11)

    #im = ax.imshow(M[it], norm=LogNorm(vmin=1e-20, vmax=1))
    im = ax.imshow(M[it], vmin=0, vmax=1)
    cbar = ax.figure.colorbar(im, ax=ax) #boundaries=tics, ticks=tics)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    #plt.clim((0,1))

    ax.set_title(r"n=%d: $\epsilon = %.2f, t = %.2f$" %(N,epsilon,ts[it]))

    #ax.set_xscale("log")
    #ax.set_yscale("log")

    #ax.legend()
    #plt.savefig("Plots/e%.2f_t%.2f.pdf"%(epsilon,ts[it]), bbox_inches='tight')
    plt.savefig("Plots/e%.2f_t%.2f.png"%(epsilon,ts[it]), bbox_inches='tight')
    #plt.show()
    plt.clf()

"""
