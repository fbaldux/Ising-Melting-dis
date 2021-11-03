#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm


instring = input("").split(' ')

N = int( instring[0] )
epsilon = float( instring[1] )
dis_num = int( instring[2] )


p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)

plt.rcParams["figure.figsize"] = [6,6]



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


#  --------------------------  main  --------------------------  #

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
        M[it] += mag2d(v[it])

M /= dis_num


#  --------------------------  plot  --------------------------  #

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
















