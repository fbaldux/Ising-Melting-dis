import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data1000 = np.loadtxt("Analysis/rAv_1000.txt").T
data200 = np.loadtxt("Analysis/rAv_200.txt").T


#  -----------------------------------------  analyze  -----------------------------------------  #
"""
rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
fs = []

for N in range(12,22,2): 
    which = data1000[0]==N
    f = interp1d(data1000[1,which], data1000[2,which], kind='cubic')
    
    Ns.append(N)
    fs.append(f)
    
for N in range(24,28,2): 
    which = data200[0]==N
    f = interp1d(data200[1,which], data200[2,which], kind='cubic')
    
    Ns.append(N)
    fs.append(f)


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

Ns = []
xs = []
ys = []

c = 0
for N in range(12,22,2): 
    which = data1000[0]==N
    xs.append(data1000[1,which])
    ys.append(data1000[2,which])
    Ns.append(N)

for N in range(24,28,2): 
    which = data200[0]==N
    xs.append(data200[1,which])
    ys.append(data200[2,which])
    Ns.append(N)
    

for iN in range(1,len(Ns)):
    ax.plot(xs[0], ys[iN]-ys[iN-1], '-', marker=dots[c], ms=4, c=cols(iN), label=r"$%d-%d$"%(Ns[iN],Ns[iN-1]))

ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"$r$")

#ax.set_title(r"disorder realizations: 1000 ($N$=12) to 200 ($N$=26)")

ax.legend()
plt.show()









