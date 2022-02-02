import sys
sys.path.append('../Numerics-dis')

import numpy as np
from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/PE.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

#ax.axhline(0.53, ls='--', color='black', label="GOE")
#ax.axhline(0.53, ls='--', color='black')

c = 0
for N in range(18,36,4): 
    which = data[0]==N
    ax.plot(2*data[1,which], data[2,which]/np.log(dim[N]), '-', marker=dots[c], ms=4, c=cols(c), label=r"$%d$" % N)
    #ax.plot(2*data[1,which], data[2,which], '-', marker=dots[c], ms=4, c=cols(c))
    c += 2


#ax.axhline(0.39, ls=':', color='black', label="Poisson")
#ax.axhline(0.39, ls=':', color='black')

ax.plot((5,14), (0.8,0.8), '--', c="steelblue")
#ax.text(12.6, 0.512, "U", c="steelblue")

#ax.plot((14,22), (0.41,0.41), '-.cd ', c="darkgreen")
#ax.text(14.4, 0.4, "L", c="darkgreen")

ax.set_xlabel(r"$W$")
ax.set_ylabel(r"$S_{\mathrm{P}} / \ln d_N$")

#ax.set_xlim((1,37))
#ax.set_ylim((0.38,0.54))

#ax.set_xticks(np.arange(5,40,5))
#ax.set_yticks(np.linspace(0.39,0.53,6))
#ax.tick_params(axis='x', which='minor', bottom=False)


ax.legend(labelspacing=0.3, fontsize=15, title_fontsize=15, loc="lower left", title=r"$N$")


#  ------------------------------------------  inset  ------------------------------------------  #


left, bottom, width, height = 0.475, 0.45, 0.5, 0.5
ax2 = ax.inset_axes([left, bottom, width, height])   


# load
cut = np.loadtxt("Plots/PE_cut.txt").T


# plot
ax2.plot(cut[0], cut[1], 's', ms=3, c='steelblue')

"""
# fit low
start = 5
fit = np.polyfit(low[0,start:], low[1,start:], 1)
print("low", fit)
f = lambda x: fit[0]*x + fit[1]
ax2.plot(low[0,start:], f(low[0,start:]), '-.',  c='darkgreen')
"""


"""
# fit cross
fit = np.polyfit(cross[0,-4:], cross[1,-4:], 1)
print("cross", fit)
f = lambda x: fit[0]*x + fit[1]
ax2.plot(cross[0,-4:], f(cross[0,-4:]), '-.',  c='darkgreen')

"""
ax2.set_xlabel(r"$N$")
#ax2.set_ylabel(r"$W$")

ax2.xaxis.set_label_coords(0.55, -0.15)
#ax2.yaxis.set_label_coords(-0.1, 0.4)

ax2.set_xticks(np.arange(20,40,5))
#ax.set_yticks(np.linspace(0.39,0.53,6))

#ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

ax2.legend(labelspacing=0.3, handlelength=0.5, handletextpad=0.5, frameon=False, fontsize=15)

plt.savefig("Plots/PE.pdf", bbox_inches='tight')
plt.show()




















