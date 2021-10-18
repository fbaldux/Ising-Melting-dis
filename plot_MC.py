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


Ns = np.array( (1e3,1e4,1e5), dtype=np.int_ )
#Ns = np.array( (1000, ) )
rep_num = 1000

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
    
   
    plt.plot(x, y-Okounkov(x), '-', c=cols(iN), label=r"$N=10^{%d}$"%np.log10(N))

"""    
xO = np.linspace(-3,3,100)
yO = Okounkov(xO)
plt.plot(xO, yO, '--', c='darkgreen', label="Okounkov")

plt.plot((-2,2), (2,2), '.', c='darkgreen')
"""

#plt.xlim((-3,3))
#plt.ylim((1,3))

plt.xlabel(r"$x$")
plt.ylabel(r"$y - y_{Okounkov}$")

plt.legend(loc="lower left")
plt.show()
















