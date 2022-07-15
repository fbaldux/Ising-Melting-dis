import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, brentq, curve_fit
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

low = np.loadtxt("Plots/r_cut_low.txt").T
high = np.loadtxt("Plots/r_cut_high.txt").T



#  -------------------------------------------  main  ------------------------------------------  #

plt.rcParams["figure.figsize"] = [6.4,4.6]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 8)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


# plot
ax.plot(1/low[0], low[1], 'o', ms=4, c='darkgreen', label=r"$W_L$")
ax.plot(1/high[0], high[1], 'o', ms=4, c='steelblue', label=r"$W_U$")


# fit low (~L)
start = 3
fit = np.polyfit(low[0,start:], low[1,start:], 1)
f = lambda x: fit[0]*x + fit[1]
#ax.plot(1/low[0,start:], f(low[0,start:]), '--',  c='black')
r = np.linspace(0.001,1/np.min(low[0,start:]))
ax.plot(r, f(1/r), '--',  c='darkgreen')


# fit high (~L)
fit = np.polyfit(high[0], high[1], 1)
f = lambda x: fit[0]*x + fit[1]
#ax.plot(1/high[0], f(high[0]), ':',  c='maroon')
r = np.linspace(0.001,1/np.min(high[0]))
ax.plot(r, f(1/r), '--',  c='steelblue')


# fit low (~1/L^2)
start = 2
fit = np.polyfit(1/low[0,start:], low[1,start:], 2)
f = lambda x: fit[0]*x**2 + fit[1]*x + fit[2]
r = np.linspace(0,1/np.min(low[0,start:]))
ax.plot(r, f(r), ':',  c='darkgreen')


# fit high (~1/L^2)
fit = np.polyfit(1/high[0], high[1], 2)
f = lambda x: fit[0]*x**2 + fit[1]*x + fit[2]
r = np.linspace(0,1/np.min(high[0]))
ax.plot(r, f(r), ':',  c='steelblue')


ax.set_xlabel(r"$1/N$")
ax.set_ylabel(r"$W$")

ax.set_xlim((0,0.06))
ax.set_ylim((6,50))

ax.text(0.01, 0.93, "(b)", c='black', transform=ax.transAxes)

#ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

ax.legend(labelspacing=0.3, handlelength=1, handletextpad=0.5, frameon=False, loc='lower left')


#  ------------------------------------------  inset  ------------------------------------------  #


left, bottom, width, height = 0.475, 0.45, 0.5, 0.5
ax2 = ax.inset_axes([left, bottom, width, height])   


# plot
ax2.plot(low[0], low[1], 'o', ms=3, c='darkgreen')
ax2.plot(high[0], high[1], 's', ms=3, c='steelblue')
#ax2.plot(cross[0], 2*cross[1], 'o', ms=3, c='darkgreen', label=r"$W^*$")
#ax2.errorbar(cross[0], 2*cross[1], yerr=2/(4*cross[1]**2*cross_err[1]), marker='o', ms=3, c='darkgreen', label=r"$W^*$")


# fit low
start = 3
fit = np.polyfit(low[0,start:], low[1,start:], 1)
print("low", fit)
f = lambda x: fit[0]*x + fit[1]
ax2.plot(low[0,start:], f(low[0,start:]), '--',  c='darkgreen')

# fit high
fit = np.polyfit(high[0], high[1], 1)
print("high", fit)
f = lambda x: fit[0]*x + fit[1]
ax2.plot(high[0], f(high[0]), '--',  c='steelblue')

"""
# fit cross
fit = np.polyfit(cross[0,-4:], 2*cross[1,-4:], 1)
print("cross", fit)
f = lambda x: fit[0]*x + fit[1]
ax2.plot(cross[0,-4:], f(cross[0,-4:]), '-.',  c='darkgreen')
"""

ax2.set_xlabel(r"$N$")
ax2.set_ylabel(r"$W$")

ax2.xaxis.set_label_coords(0.55, -0.15)
#ax2.yaxis.set_label_coords(-0.1, 0.4)

ax2.set_xticks(np.arange(20,40,5))
#ax.set_yticks(np.linspace(0.39,0.53,6))

#ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

#ax2.legend(labelspacing=0.3, handlelength=0.5, handletextpad=0.5, frameon=False, fontsize=15)


#  -------------------------------------------  plot  ------------------------------------------  #


plt.savefig("Plots/cuts.pdf", bbox_inches='tight')
plt.show()











