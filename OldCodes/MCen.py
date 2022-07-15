
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Averages/MCen_N10000_d10000.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #


#plt.rcParams["figure.figsize"] = [5,5]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.plot(np.arange(len(data[0])), data[0], '-', c='black', label=r"$\langle E(t) \rangle$")
ax.plot(np.arange(len(data[0])), data[1], '--', c='blue', label=r"$\langle E^2(t) \rangle^{1/2}$")


ax.set_xlabel(r"MC time")
ax.set_ylabel(r"$E$")


#ax.set_xticks(np.arange(5,40,5))
#ax.set_yticks(np.linspace(0.39,0.53,6))
#ax.tick_params(axis='x', which='minor', bottom=False)

#ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend(labelspacing=0.3, fontsize=15)
plt.savefig("Plots/MCen.pdf", bbox_inches='tight')
plt.show()











