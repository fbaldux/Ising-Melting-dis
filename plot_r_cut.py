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

rGOE = 0.5307
dr = 0.02
cut = 0.52

Ns = []
cuts = []


for N in range(12,22,2): 
    which = data1000[0]==N
    f = interp1d(data1000[1,which], data1000[2,which], kind='cubic')
    f2 = lambda x: f(x) - cut
    
    Ns.append(N)
    cuts.append( fsolve(f2, 4) )
    
for N in range(24,28,2): 
    which = data200[0]==N
    f = interp1d(data200[1,which], data200[2,which], kind='cubic')
    f2 = lambda x: f(x) - cut
    
    Ns.append(N)
    cuts.append( fsolve(f2, 4) )


Ns = np.array(Ns)
cuts = np.array(cuts)


#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


ax.plot(Ns, cuts, '.', c='black')

ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\varepsilon^*$")

ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

#ax.legend(title=r"$N$")
plt.show()











