#  ---------------------------------------------------------------------------------------------  #
#
#   ...
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from scipy.special import erf
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import cm

plt.rcParams["figure.figsize"] = [8,4]


#Ns = np.array( (1e3,1e4,1e5,1e6), dtype=np.int_ )
Ns = np.array( (1e4, ), dtype=np.int_ )

pForw = .9
rep_num = 1

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


@nb.vectorize
def Dijkgraaf(x):
    return 2*np.log(2*np.cosh(0.5*x))

#@nb.vectorize
def diffusion(x):
    return np.exp(-x**2)/np.sqrt(np.pi) + x*erf(x)

def subdiff(x):
    x = np.abs(x)

    if x>=2:
        return x
    else:
        return x + 4 * (np.sqrt(1-x*x/4) - 0.5*x*np.arccos(0.5*x)) / np.pi

subdiff_v = np.vectorize(subdiff)

for iN in range(len(Ns)):
    N = Ns[iN]
    
    #try: 
    filename = "Results/MC_N%d_p%.4f_av%d.txt" % (N,pForw,rep_num)
    x,y = np.loadtxt(filename).T

    plt.plot(x, y, '-', c=cols(iN), label=r"$N=10^{%d}$"%np.log10(N))
   
        #plt.plot(x, y-Okounkov(x), '-', c=cols(iN), label=r"$N=10^{%d}$"%np.log10(N))

    #except:
    #    None

   
xO = np.linspace(-3,3,100)
#plt.plot(xO, Okounkov(xO), '--', c='darkgreen', label="Okounkov")
#plt.plot(xO, Dijkgraaf(xO), '--', c='royalblue', label="Dijkgraaf")
plt.plot(xO, subdiff_v(xO), '-.', c='royalblue', label="subdiff")

"""
fit = np.polyfit(x,y,2)
print(fit)

f = lambda t: fit[0]*t**2 + fit[1]*t + fit[2] 
plt.plot(xO, f(xO), '--', c='royalblue', label="parabola")


fit = np.polyfit(x,y,4)
print(fit)

#print(2**np.arange(4,-1,-1))
#exit(0)
f = lambda t: fit[0]*t**4 + fit[1]*t**3 + fit[2]*t**2 + fit[3]*t + fit[4]
plt.plot(xO, f(xO), '--', c='royalblue', label="4tic")
"""
#plt.plot(x, y-f(x), '-', c=cols(iN))


plt.xlim((-3,3))
plt.ylim((0,3))

plt.xlabel(r"$x$")
#plt.ylabel(r"$y - y_{Okounkov}$")
plt.ylabel(r"$y$")

plt.legend()
plt.show()
















