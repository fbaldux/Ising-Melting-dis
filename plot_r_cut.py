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

rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
cuts = []


for N in range(12,24,2): 
    if N!=20:
        which = data10000[0]==N
        f = interp1d(data10000[1,which], data10000[2,which], kind='cubic')
        f2 = lambda x: f(x) - cut
    
        Ns.append(N)
        cuts.append( fsolve(f2, 4) )
    
for N in range(24,28,2): 
    which = data1100[0]==N
    f = interp1d(data1100[1,which], data1100[2,which], kind='cubic')
    f2 = lambda x: f(x) - cut
    
    Ns.append(N)
    cuts.append( fsolve(f2, 4) )


Ns = np.array(Ns)
cuts = np.array(cuts)


#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


ax.plot(Ns, cuts, '.', c='black', label="data")

# fit
fit = np.polyfit(Ns, cuts, 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(Ns, f(Ns), '--', c='gray', label="fit")



ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\varepsilon^*$")

ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

ax.legend()
plt.show()











