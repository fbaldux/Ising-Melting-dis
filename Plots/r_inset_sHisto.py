
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.hlines(0.5307, 1, 30, ls='--', color='black', label="GOE")
#ax.axhline(0.53, ls='--', color='black')

c = 0
for N in range(20,38,4): 
    which = data[0]==N
    ax.plot(2*data[1,which], data[2,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$N = %d$" % N)
    #ax.plot(2*data[1,which], data[2,which], '-', marker=dots[c], ms=4, c=cols(c))
    c += 2


ax.axhline(0.3863, ls=':', color='black', label="Poisson")
#ax.axhline(0.39, ls=':', color='black')

ax.plot((6,13), (0.51,0.51), '-.', c="steelblue")
ax.text(11.6, 0.512, "U", c="steelblue")

ax.plot((15,22), (0.41,0.41), '-.', c="darkgreen")
ax.text(15.4, 0.4, "L", c="darkgreen")


#ax.text(1.5, 0.515, "(a)", c="black")


ax.set_xlabel(r"$W$")
ax.set_ylabel(r"$r$")

ax.set_xlim((1,37))
ax.set_ylim((0.38,0.54))

ax.set_xticks(np.arange(5,40,5))
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.set_yticks(np.linspace(0.4,0.52,4))
ax.yaxis.set_minor_locator(AutoMinorLocator())


#ax.legend(labelspacing=0.3, fontsize=15, title_fontsize=15, loc="lower left", title=r"$N$")
ax.legend(labelspacing=0.3, fontsize=14, loc="lower left", frameon=False)


#  ------------------------------------------  inset  ------------------------------------------  #


left, bottom, width, height = 0.505, 0.515, 0.48, 0.48
ax2 = ax.inset_axes([left, bottom, width, height])   

N = 32
dis_num = 3000

cols = cm.get_cmap('cmr.tropical', 5)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

s = np.linspace(0,10,100)
#ax2.plot(s, 0.5*s*np.pi * np.exp(-0.25*np.pi*s**2), '--', label='GOE', c='black')
ax2.plot(s, 0.5*s*np.pi * np.exp(-0.25*np.pi*s**2), '--', c='black')

c = 0
for eps in range(1,19,4): 
    filename = "Analysis/sHisto_N%d_e%.4f_d%d.txt" % (N,eps,dis_num)
    data = np.loadtxt(filename).T
    
    ax2.plot(data[0], data[1], '-', c=cols(c), label=r"$W = %d$" % (2*eps))
    
    c += 1


#ax2.plot(s, np.exp(-s), ':', label='Poisson', c='black')
ax2.plot(s, np.exp(-s), ':', c='black')

ax2.set_xlim((0,6))


ax2.set_xlabel(r"$s$", fontsize=16)
ax2.set_ylabel(r"$P(s)$", fontsize=16)

ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())


ax2.legend(labelspacing=0.3, handlelength=1, handletextpad=0.5, frameon=False, fontsize=14)

plt.savefig("Plots/r.pdf", bbox_inches='tight')
plt.show()




















