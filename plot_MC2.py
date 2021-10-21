#  ---------------------------------------------------------------------------------------------  #
#
#   ...
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import cm

#plt.rcParams["figure.figsize"] = [6,6]


Ns = np.array( (1e3,1e4,1e5,1e6), dtype=np.int_ )
#Ns = np.array( (1000, ) )
rep_num = 10000

cols = cm.get_cmap('magma', len(Ns)+1)


#  -------------------------------------  horizontal plot  -------------------------------------  #


@nb.vectorize
def Okounkov(x):
    if x < -2:
        return -x
    elif x > 2:
        return x
    else:
        return 2/np.pi * ( x*np.arcsin(0.5*x) + np.sqrt(4 - x**2) )


for iN in range(len(Ns)):
    N = Ns[iN]
    
    filename = "Results/MC_N%d_av%d.txt" % (N,rep_num)
    x,y = np.loadtxt(filename).T
    
    plt.plot(N, y[len(x)//2], '.', c='black')
    #plt.plot(N, y[len(x)//3], '.', c='red')
    #plt.plot(N, y[len(x)//4], '.', c='blue')
   
    
plt.axhline(Okounkov(0), ls='--', lw=1, c='black')

 


#plt.xlim((-3,3))
plt.xscale('log')

plt.xlabel(r"$N$")
#plt.ylabel(r"$y - y_{Okounkov}$")
plt.ylabel(r"value at 0")

plt.legend()
plt.show()
















