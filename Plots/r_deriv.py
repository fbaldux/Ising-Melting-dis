
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

high = np.loadtxt("Plots/r_cut_high.txt").T
cross = np.loadtxt("Plots/r_cross.txt").T

high_d = np.diff(high[1])/2
cross_d = np.diff(cross[1])/2

print(high_d)
print(high_d.shape)

#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
#plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.plot(high[0,1:], high_d, '.', label="U")
ax.plot(cross[0,1:], cross_d, '.', label="*")

ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$\partial W / \partial N$")

#ax.set_xlim((1,37))
#ax.set_ylim((0.38,0.54))



ax.legend()
#plt.savefig("Plots/r.pdf", bbox_inches='tight')
plt.show()




















