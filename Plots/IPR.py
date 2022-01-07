import sys
sys.path.append('../Numerics-dis')

import numpy as np
from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/IPR.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

plt.rcParams["figure.figsize"] = [5.2,4.2]
fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 8)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

c = 0
for N in range(22,36,2): 
    which = data[0]==N
    ax.plot(data[1,which], 1/(data[2,which]), '-', marker=dots[c], ms=4, c=cols(c), label=N)
    c += 1



ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"IPR")

ax.set_yscale('log')

#ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend(title=r"$N$")
plt.savefig("Plots/IPR.pdf", bbox_inches='tight')
plt.show()











