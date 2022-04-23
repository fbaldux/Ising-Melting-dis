
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

Ns = np.array((20,))
eps = np.arange(2,19,2)
dis_num = 10000

fig, ax = plt.subplots()
#cols = cm.get_cmap("inferno", len(Ns)+1)
cols = cm.get_cmap("inferno", len(eps)+1)

#P = np.zeros((len(eps), nbins))
for iN in range(len(Ns)):
    N = Ns[iN]
    
    for ie in range(len(eps)):
        e = eps[ie]

        data = np.loadtxt("Analysis/DOS_N%d_e%.4f_av%d.txt" % (N,e,dis_num)).T
        
        lab = r"$\varepsilon=%.1f$"%e
        ax.plot(data[0], data[1], '-', label=lab, c=cols(ie))
        
        

#  -------------------------------------------  plot  ------------------------------------------  #



#ax.set_xlabel(r"$\varepsilon$")
#ax.set_ylabel(r"area")

ax.set_xlabel(r"$\tilde{E}$")
ax.set_ylabel(r"DOS")

#ax.set_xscale("log")

#ax.set_title(r"disorder realizations: 10000 ($N$=12...22) to 2000 ($N$=24...26)")

ax.legend()
plt.show()











