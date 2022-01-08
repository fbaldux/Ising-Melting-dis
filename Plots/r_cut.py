import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, brentq, curve_fit
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

low = np.loadtxt("Plots/r_cut_low.txt").T
high = np.loadtxt("Plots/r_cut_high.txt").T



#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [5.2,4.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 8)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


# plot
ax.plot(low[0], low[1], '.', c='black', label=r"$W_L$")
ax.plot(high[0], high[1], '.', c='maroon', label=r"$W_U$")


# fit low
start = 5
fit = np.polyfit(low[0,start:], low[1,start:], 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(low[0,start:], f(low[0,start:]), '--',  c='black')


# fit high
fit = np.polyfit(high[0], high[1], 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(high[0], f(high[0]), ':',  c='maroon')



ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$W$")

#ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

ax.legend(labelspacing=0.3)
plt.savefig("Plots/r_cut.pdf", bbox_inches='tight')
plt.show()











