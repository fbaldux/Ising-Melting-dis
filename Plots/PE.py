import sys
sys.path.append('../Numerics-dis')

import numpy as np
from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/PE.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [5.2,4.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 8)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

c = 0
for N in range(22,36,2): 
    which = data[0]==N
    #ax.plot(data[1,which], data[2,which], '-', marker=dots[c], ms=4, c=cols(c), label=N)
    ax.plot(2*data[1,which], data[2,which]/np.log(dim[N]), '-', marker=dots[c], ms=4, c=cols(c), label=N)
    c += 1



ax.set_xlabel(r"$W$")
ax.set_ylabel(r"$S_{\mathrm{P}} / \ln d_N$")

ax.set_xlim((1,37))
ax.set_ylim((0.1,1))

ax.set_xticks(np.arange(5,40,5))
ax.set_yticks(np.linspace(0.1,1,10)[::2])

#ax.set_yscale('log')

#ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend(title=r"$N$", labelspacing=0.3)
plt.savefig("Plots/PE.pdf", bbox_inches='tight')
plt.show()











