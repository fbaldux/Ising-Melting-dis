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


#  -----------------------------------  compute height at 0  -----------------------------------  #

# build (diagonal) operator that gives the height at 0 of the tilted Young diagram
@nb.njit
def height0(levels):
    h0 = np.zeros(dim[N], dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(N):
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
















