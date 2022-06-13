#  ---------------------------------------------------------------------------------------------  #
#
#   ...
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
import numba as nb
from matplotlib import pyplot as plt

# system size
N = int( float(sys.argv[1]) )

# power-law decay of waiting time distribution
a = float( sys.argv[2] )

# number of disorder instances
dis_num = int( sys.argv[3] )


plt.rcParams["figure.figsize"] = [8,4]


@nb.vectorize
def Okounkov(x):
    if x < -2:
        return -x
    elif x > 2:
        return x
    else:
        return 2/np.pi * ( x*np.arcsin(0.5*x) + np.sqrt(4 - x**2) )


@nb.vectorize
def CGM(x):
    if x < -1/np.sqrt(2):
        return -x
    elif x > 1/np.sqrt(2):
        return x
    else:
        return (1+2*x*x) / np.sqrt(8)

# corner growth model, aka TASEP
@nb.vectorize
def TASEP(x,c):
    x = np.abs(x)

    if x >= np.sqrt(2*c):
        return x
    else:
        return (2*np.sqrt(2)*x**2 + np.sqrt(2)*c**2)/(4*c)

#  -------------------------------------------  load  ------------------------------------------  #

#filename = "Averages/TASEP_shape_exp_N%d_d%d.txt" % (N,dis_num)
filename = "Averages/TASEP_shape_pow_N%d_a%.4f_d%d.txt" % (N,a,dis_num)
x,y = np.loadtxt(filename).T


#  -------------------------------------------  plot  ------------------------------------------  #

plt.plot(np.sqrt(2)*x, np.sqrt(2)*y, '-', c='black', label="MC")

xO = np.linspace(-10,10,100)
plt.plot(xO, Okounkov(xO), '--', c='darkgreen', label="Okounkov")
#plt.plot(xO, CGM(xO), '--', c='darkred', label="standard TASEP")
plt.plot(xO, TASEP(xO,np.sqrt(12)), '-.', c='royalblue', label="standard TASEP")

plt.xlabel("x")
plt.ylabel("y")

plt.xlim((-10,10))
plt.ylim((0,10))

plt.legend()
plt.show()







