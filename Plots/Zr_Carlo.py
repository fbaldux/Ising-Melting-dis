#  ---------------------------------------------------------------------------------------------  #
#
#
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy import sparse
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr
from matplotlib.ticker import *


#  ------------------------------------  program constants  ------------------------------------  #

N = 45
h = 10
dis_num = 3015

init_state=0

N_bins = 50


#  -------------------------------------------  main  ------------------------------------------  #

plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})
#plt.rcParams["figure.figsize"] = [7,5]

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 7)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


data = np.loadtxt("Analysis/FSA_L%d_h%.3f_in%d_r%d.txt" % (N,h,init_state,dis_num))
data += np.log(h)


r = np.arange(0,N+1)
ax.plot(r[3:], data[3:], 'o', ms=4, label="FA", c='black')



def fitfunc(x,a,b):
    return a*np.log(x)+b

"""
# log fit
start = 30
r2 = np.linspace(r[start], r[-1], 100)
fit, err = curve_fit(fitfunc, r[start:], data[start:])
print("log", fit)
ax.plot(r[start:], fitfunc(r[start:], *fit), '-', label=r"log fit", c=cols(6))
"""


# log-log fit
start = 13
r2 = np.linspace(r[start], r[-1], 100)
fit = np.polyfit(np.log(r[start:]), np.log(data[start:]), 1)
print("log-log", fit)
f = lambda x: np.exp(fit[1]) * x**fit[0]
ax.plot(r2, f(r2), '--', label=r"fit", c=cols(2))


# sqrt guide
r2 = np.linspace(10, 50, 10)
f = lambda x: np.exp(-0.6) * x**0.5
ax.plot(r2, f(r2), '--', label=r"$\sim r^{1/2}$", c=cols(4))

# log guide
r2 = np.linspace(15, 45, 10)
f = lambda x: 1.7*np.log(x)-2.1
ax.plot(r2, f(r2), ':', label=r"$\sim \ln r$", c=cols(2))


ax.set_xlabel(r"$r$")
ax.set_ylabel(r"$\langle Z_r \rangle - \ln |g/W|$")

ax.set_xlim((2.5,51))

ax.set_xscale("log")
ax.set_yscale("log")

ax.yaxis.set_ticks([2,3,4])  
ax.yaxis.set_ticklabels([2,3,4])  

ax.legend(frameon=False, loc="lower right")


#  ------------------------------------------  inset  ------------------------------------------  #


left, bottom, width, height = 0.06, 0.5, 0.45, 0.48
ax2 = ax.inset_axes([left, bottom, width, height])   


ax2.plot(r[3:], data[3:], 'o', ms=2, c='black')
#ax2.plot(r2, f(r2), '--', c=cols(2))

#ax2.set_xlabel(r"$r$")
#ax2.set_ylabel(r"$\langle Z_r \rangle - \log |g/W|$")

ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())


plt.savefig("Plots/Zr.pdf", bbox_inches='tight')
plt.show()




