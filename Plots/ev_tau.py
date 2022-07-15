#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.special import jv
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import cmasher as cmr


N = 30

eps = np.array((2.0,2.5,3.0,3.5,4.0,4.5))
Tfin = np.array((1e2,1e3,1e4,1e5))

dis_nums = np.array((400,800,1000,1200,1600,3000))


#plt.rcParams["figure.figsize"] = [12.8,4]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.tropical', len(eps))
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']

# inset
left, bottom, width, height = 0.54, 0.15, 0.45, 0.48
ax2 = ax.inset_axes([left, bottom, width, height])   

threshold = 0.05


#  -------------------------------------------  load  ------------------------------------------  #

for ie in range(len(eps)):
    e = eps[ie]
            
    for T in Tfin[::-1]:
    
        found = False
    
        for dis_num in dis_nums[::-1]:
        
            try:
                filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_av%d.txt" % (N,e,0,T,dis_num)
                av = np.loadtxt(filename).T  # t lat vert area EE
                ts = av[0]
                av = av[1:]
    
                found = True
                break
        
            except:
                None
      
        if found:
            break
            
#  -------------------------------------------  plot  ------------------------------------------  #
    
    # main            
    lab = r"$W=%d$" % (2*e)
    ax.plot(ts, av[2], '-', label=lab, c=cols(ie))
    
    
    # inset
    tau = np.where( np.abs(np.log(ts[1:]**2/av[2,1:])) > threshold )[0][0]
    tau = ts[tau+1]
    ax2.plot(2*e, tau, 'x', c='black', ms=4)
    
    
    
ts = np.linspace(0.1,10,100)
ax.plot(ts, ts**2, '--', c='black', label=r"$t^2$")


#  ----------------------------------------  parameters  ---------------------------------------  #

# main
ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$N(t)$")

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlim((1e-1,1e5))
ax.set_ylim((1e-2,30))

ax.legend(labelspacing=0.3, fontsize=14, loc="lower center", bbox_to_anchor=(0.27,0), frameon=False)


# inset
ax2.set_xlabel(r"$W$", fontsize=15)
ax2.set_ylabel(r"$\tau(W)$", fontsize=15)

#ax2.set_xscale("log")
#ax2.set_yscale("log")


# save
plt.savefig("Plots/ev_tau.pdf", bbox_inches='tight')
plt.show()












