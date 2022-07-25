
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
#plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

#ax.axhline(0.5307, ls='--', color='black', label="GOE")

c = 0
for N in range(18,38,2): 
    which = data[0]==N
    x = 2*data[1,which]
    y = data[2,which]
    
    # low
    ax.plot((x-0.25*N-11)*N**0.5, y, '-', marker=dots[c], ms=4, c=cols(c), label=r"$N = %d$" % N)
    
    # high
    #ax.plot(x/N**0.5, y, '-', marker=dots[c], ms=4, c=cols(c), label=r"$N = %d$" % N)
    c += 1


#ax.axhline(0.3863, ls=':', color='black', label="Poisson")


ax.set_xlabel(r"$(W-0.25N - 11) N^{1/2}$")     # low
#ax.set_xlabel(r"$W/N^{1/2}$")                  # high
ax.set_ylabel(r"$r$")

#ax.set_xlim((1,37))
#ax.set_ylim((0.38,0.54))

#ax.set_xticks(np.arange(5,40,5))
#ax.set_yticks(np.linspace(0.39,0.53,6))
#ax.tick_params(axis='x', which='minor', bottom=False)

#ax.set_title(r"scaling for $r$ small: ")
ax.set_title(r"scaling for $r$ big")

ax.legend(labelspacing=0.3, fontsize="small")
#plt.savefig("Plots/r.pdf", bbox_inches='tight')
plt.show()











