import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, curve_fit
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr

#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -----------------------------------------  analyze  -----------------------------------------  #

def fitfunc(x,a,b,c):
    #return (a*np.exp(-b*x) + c) * ( 1 + d/x )
    return (a*np.exp(-b*x) + 0.38629) * ( 1 + c/x )


def fitfuncp(x,a,b,c,d):
    return (a*b*np.exp(-b*x)) * ( 1 + d/x ) - (a*np.exp(-b*x) + c) * d/x**2 

xmin = 6
deg = 5

rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
fs = []

cols = cm.get_cmap('cmr.ember', 9)

c = 0
for N in range(18,38,2): 
    which = (data[0]==N) & (data[1]>=xmin)
    x = data[1,which]
    y = data[2,which]
    
    # interpolation
    #f = interp1d(x, y, kind='cubic')
    
    # polynomial fit
    fit = np.polyfit(x, y, deg)
    f1 = lambda x: np.dot( x**np.arange(deg+1), fit[::-1] )
    f = np.vectorize(f1)
    
    """
    # exp fit
    #bds = ((0,2,0),(np.inf,2.2,np.inf))
    #guess = (0.2,0.2,0.3,0.01)
    guess = (0.2,0.2,0.01)
    fit, cov = curve_fit(fitfunc, x, y, p0=guess) #, bounds=bds)
    f = lambda x: fitfunc(x, *fit)
    """
    # plot
    """
    plt.plot(x, y, '.', c=cols(c), label=N)
    x2 = np.linspace(min(x),max(x),100)
    plt.plot(x2, f(x2), '--', c=cols(c))
    plt.title(N)
    plt.show()
    """
    # store the results
    Ns.append(N)
    fs.append(fit)
    
    c += 1

Ns = np.array(Ns)

def f1(iN,x):
    #return fitfunc(x, *fs[iN])
    return np.dot( x**np.arange(deg+1), fs[iN][::-1] )

f = np.vectorize(f1)

crosses = np.zeros(len(Ns))
crosses[0] = 8

for iN in range(1,len(Ns)):
    temp = lambda x: f(iN,x)-f(iN-1,x)
    
    # plot
    which = (data[0]==Ns[iN-1]) & (data[1]>=xmin)
    plt.plot(data[1,which], data[2,which], 'o', ms=4, c=cols(0))
    which = (data[0]==Ns[iN-1]) & (data[1]<xmin)
    plt.plot(data[1,which], data[2,which], 'x', ms=4, c=cols(0))
    which = (data[0]==Ns[iN]) & (data[1]>=xmin)
    plt.plot(data[1,which], data[2,which], 'o', ms=4, c=cols(5))
    which = (data[0]==Ns[iN]) & (data[1]<xmin)
    plt.plot(data[1,which], data[2,which], 'x', ms=4, c=cols(5))
    
    x2 = np.linspace(1,18,100)
    plt.plot(x2, f(iN-1,x2), '-', c=cols(0))
    plt.plot(x2, f(iN,x2), '-', c=cols(5))
    
    plt.title(Ns[iN])
    plt.ylim((0.38, 0.5))
    #plt.yscale("log")
    plt.show()
    
    crosses[iN] = fsolve(temp, crosses[iN-1])
    
    #print(Ns[iN], fitfuncp(crosses[iN],*fs[iN]) - fitfuncp(crosses[iN],*fs[iN-1]))
    
    
crosses = np.array(crosses)

np.savetxt("Plots/r_cross.txt", np.stack((Ns[1:], crosses[1:])).T, header="N crossing", fmt="%d %f")

#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.plot(Ns[1:], crosses[1:], '.', c='black', label="data")

# fit
fit = np.polyfit(Ns[:], crosses[:], 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(Ns[:], f(Ns[:]), '--', c='gray', label="fit")

ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\varepsilon^*$")

ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*,N) = r(\varepsilon^*,N-2)$")

ax.legend()
plt.show()

exit(0)
"""

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 12)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')




x = np.linspace(xmin,17,100)
for iN in range(1,len(Ns)):
    ax.plot(x, f(iN,x)-f(iN-1,x), '-', marker=dots[c%len(dots)], ms=4, c=cols(iN), label=r"$%d-%d$"%(Ns[iN],Ns[iN-1]))

ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"$r$")

#ax.set_title(r"disorder realizations: 1000 ($N$=12) to 200 ($N$=26)")

ax.legend()
plt.show()
"""


