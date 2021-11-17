import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr

#  -------------------------------------------  load  ------------------------------------------  #

data10000 = np.loadtxt("Analysis/rAv_d10000.txt").T
data1100 = np.loadtxt("Analysis/rAv_d1100.txt").T


#  -----------------------------------------  analyze  -----------------------------------------  #

xmin = 6
deg = 4

rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
fs = []

cols = cm.get_cmap('cmr.ember', 9)

c = 0
for N in range(12,24,2): 
    if N!=20:
        which = (data10000[0]==N) & (data10000[1]>=xmin)
        x = data10000[1,which]
        y = data10000[2,which]
        
        # interpolation
        #f = interp1d(x, y, kind='cubic')
        # fit
        fit = np.polyfit(x, y, deg)
        f1 = lambda x: np.dot( x**np.arange(deg+1), fit[::-1] )
        f = np.vectorize(f1)
        
        # plot
        """
        plt.plot(x, y, '.', c=cols(c), label=N)
        x2 = np.linspace(min(x),max(x),100)
        plt.plot(x2, f(x2), '--', c=cols(c))
        """
        
        # store the results
        Ns.append(N)
        fs.append(fit)
        
        c += 1


for N in range(24,28,2): 
    which = (data1100[0]==N) & (data1100[1]>=xmin)
    x = data1100[1,which]
    y = data1100[2,which]
    
    # interpolation
    #f = interp1d(x, y, kind='cubic')
    # fit
    fit = np.polyfit(x, y, deg)
    f1 = lambda x: np.dot( x**np.arange(deg+1), fit[::-1] )
    f = np.vectorize(f1)
    
    # plot
    """
    plt.plot(x, y, '.', c=cols(c), label=N)
    x2 = np.linspace(min(x),max(x),100)
    plt.plot(x2, f(x2), '--', c=cols(c))
    """
    
    # store the results
    Ns.append(N)
    fs.append(fit)
    
    c += 1
        
"""
Ns = np.array(Ns)

crosses = np.zeros(len(Ns))
crosses[0] = 8

for iN in range(1,len(Ns)):
    f = lambda x: fs[iN](x) - fs[iN-1](x)
    
    crosses[iN] = fsolve(f, crosses[iN-1])
    
crosses = np.array(crosses)

#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.plot(Ns[1:], crosses[1:], '.', c='black')

ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\varepsilon^*$")

ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

#ax.legend(title=r"$N$")
plt.show()
"""



fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


def f1(iN,x):
    return np.dot( x**np.arange(deg+1), fs[iN][::-1] )

f = np.vectorize(f1)

x = np.linspace(xmin,14,100)
for iN in range(1,len(Ns)):
    ax.plot(x, f(iN,x)-f(iN-1,x), '-', marker=dots[c], ms=4, c=cols(iN), label=r"$%d-%d$"%(Ns[iN],Ns[iN-1]))

ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"$r$")

#ax.set_title(r"disorder realizations: 1000 ($N$=12) to 200 ($N$=26)")

ax.legend()
plt.show()



