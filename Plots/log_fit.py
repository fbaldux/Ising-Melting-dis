#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import cmasher as cmr




#plt.rcParams["figure.figsize"] = [12.8,4]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 6)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']

# inset
#left, bottom, width, height = 0.54, 0.15, 0.45, 0.48
#ax2 = ax.inset_axes([left, bottom, width, height])   



#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Plots/fit_ev_log.txt").T
dataEE = np.loadtxt("Plots/fit_evEE_log.txt").T

            
#  -------------------------------------------  plot  ------------------------------------------  #

ax.plot(data[0], data[1], 'o', ms=3, c=cols(0), label=r"$\eta_N$")
ax.plot(dataEE[0], dataEE[1], 's', ms=3, c=cols(3), label=r"$\eta_E$")


#  -------------------------------------------  fit  -------------------------------------------  #

fit = np.polyfit(data[0], np.log(data[1]), 1)
print("N", fit[0], fit[1])
f = lambda t: np.exp(fit[0]*t + fit[1])
ax.plot(data[0], f(data[0]), '--', c=cols(0))


fit = np.polyfit(dataEE[0], np.log(dataEE[1]), 1)
print("EE", fit[0], fit[1])
f = lambda t: np.exp(fit[0]*t + fit[1])
ax.plot(dataEE[0], f(dataEE[0]), '--', c=cols(3))

#  ----------------------------------------  parameters  ---------------------------------------  #

# main
ax.set_xlabel(r"$W$")
ax.set_ylabel(r"$\eta$")

#ax.set_xscale("log")
ax.set_yscale("log")

#ax.set_xlim((1e-1,1e5))
#ax.set_ylim((1e-2,40))

ax.legend(labelspacing=0.3, handlelength=1, handletextpad=0.5, loc="lower left", frameon=False)

#ax.set_title(r"$N(t) = a \ln t + b$")

# save
plt.savefig("Plots/log_fit.pdf", bbox_inches='tight')
plt.show()












