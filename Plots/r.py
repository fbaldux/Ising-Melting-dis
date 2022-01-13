
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.axhline(0.53, ls='--', color='black', label="GOE")

c = 0
for N in range(18,38,2): 
    which = data[0]==N
    ax.plot(2*data[1,which], data[2,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$N = %d$" % N)
    c += 1


ax.axhline(0.39, ls=':', color='black', label="Poisson")

ax.set_xlabel(r"$W$")
ax.set_ylabel(r"$r$")

ax.set_xlim((1,37))
ax.set_ylim((0.38,0.54))

ax.set_xticks(np.arange(5,40,5))
ax.set_yticks(np.linspace(0.39,0.53,6))
#ax.tick_params(axis='x', which='minor', bottom=False)

#ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend(labelspacing=0.3, fontsize=15)
plt.savefig("Plots/r.pdf", bbox_inches='tight')
plt.show()











