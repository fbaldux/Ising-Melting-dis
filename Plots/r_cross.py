import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr

#  -------------------------------------------  load  ------------------------------------------  #

data1 = np.loadtxt("Analysis/rAv_d10000.txt")
data2 = np.loadtxt("Analysis/rAv_d2000.txt")
data3 = np.loadtxt("Analysis/rAv_d3200.txt")[:,:-1]
data4 = np.loadtxt("Analysis/rAv_d960.txt")[:,:-1]
data5 = np.loadtxt("Analysis/rAv_d880.txt")[:,:-1]
data6 = np.loadtxt("Analysis/rAv_d600.txt")[:,:-1]

data = np.vstack((data1,data2,data3,data4,data5,data6)).T


#  -----------------------------------------  analyze  -----------------------------------------  #

xmin = 6
deg = 5

rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
fs = []

cols = cm.get_cmap('cmr.ember', 9)

c = 0
for N in range(12,36,2): 
    which = (data[0]==N) & (data[1]>=xmin)
    x = data[1,which]
    y = data[2,which]
    
    # interpolation
    #f = interp1d(x, y, kind='cubic')
    # fit
    fit = np.polyfit(x, y, deg)
    f1 = lambda x: np.dot( x**np.arange(deg+1), fit[::-1] )
    f = np.vectorize(f1)
    
    # plot
    
    plt.plot(x, y, '.', c=cols(c), label=N)
    x2 = np.linspace(min(x),max(x),100)
    plt.plot(x2, f(x2), '--', c=cols(c))
    plt.title(N)
    plt.show()
    
    # store the results
    Ns.append(N)
    fs.append(fit)
    
    c += 1

Ns = np.array(Ns)

def f1(iN,x):
    return np.dot( x**np.arange(deg+1), fs[iN][::-1] )

f = np.vectorize(f1)

crosses = np.zeros(len(Ns))
crosses[0] = 8

for iN in range(1,len(Ns)):
    temp = lambda x: f(iN,x)-f(iN-1,x)
    
    crosses[iN] = fsolve(temp, crosses[iN-1])
    
crosses = np.array(crosses)

#  -------------------------------------------  plot  ------------------------------------------  #
"""
fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.plot(Ns[1:], crosses[1:], '.', c='black', label="data")

# fit
fit = np.polyfit(Ns[1:], crosses[1:], 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(Ns[1:], f(Ns[1:]), '--', c='gray', label="fit")

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



