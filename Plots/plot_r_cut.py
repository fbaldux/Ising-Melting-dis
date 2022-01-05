import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -----------------------------------------  analyze  -----------------------------------------  #

rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
cuts = []


for N in range(22,36,2): 
    which = data[0]==N
    f = interp1d(data[1,which], data[2,which], kind='cubic')
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











