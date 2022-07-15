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


Ns = np.array((20,22,24,26,28,30))

eps = np.array( (1.0,2.5,4.5))
Tfin = np.array((1e2,1e3,1e4,1e5))

dis_nums = np.array((400,800,1000,1200,1600,3000))


plt.rcParams["figure.figsize"] = [12.8,4]

fig = plt.figure()
gs = fig.add_gridspec(1, 3, wspace=0)
ax = gs.subplots(sharex=False, sharey=True)
#ax_in = []


cols = cm.get_cmap("inferno", len(Ns)+1)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']
alpha = 0.1

#  -------------------------------------------  load  ------------------------------------------  #

for ie in range(len(eps)):
    e = eps[ie]
    
    if ie==2:
        left, bottom, width, height = 0.2, 0.45, 0.7, 0.5
        ax_in = ax[ie].inset_axes([left, bottom, width, height])
    
    for iN in range(len(Ns)):
        N = Ns[iN]
        
                
        for T in Tfin[::-1]:
            
            found = False
            
            for dis_num in dis_nums[::-1]:
                
                try:
                    filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_av%d.txt" % (N,e,0,T,dis_num)
                    av = np.loadtxt(filename).T  # t lat vert area EE
                    ts = av[0]
                    av = av[1:]
                
                    filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_std%d.txt" % (N,e,0,T,dis_num)
                    std = np.sqrt(np.loadtxt(filename)[:,1:]).T  # t lat vert area EE
                    
                    found = True
                    break
                
                except:
                    None
              
            if found:
                break
            
#  -------------------------------------------  plot  ------------------------------------------  #
                        
        lab = r"$N=%d$" % N
        
        ax[ie].plot(ts, av[2], '-', label=lab, c=cols(iN))
        ax[ie].fill_between(ts, av[2]+std[2], av[2]-std[2], color=cols(iN), alpha=alpha)         
        

#  ------------------------------------------  inset  ------------------------------------------  #
        
        if ie==2:
            logt = np.log(ts[1:])
            av2 = np.maximum(av[2,1:], np.ones(len(av[2,1:]))*1e-10)
            logN = np.log(av2)
            ax_in.plot(0.5*(ts[1:-1]+ts[2:]), np.diff(logN)/np.diff(logt), '-', c=cols(iN))

#  ----------------------------------------  parameters  ---------------------------------------  #

    ax[ie].set_xlabel(r"$t$")
        
    ax[ie].set_title(r"$W$ = %.2f" %(2*e))

    ax[ie].set_xscale("log")
    #ax.set_yscale("log")
    
    if ie==0:
        ax[ie].legend(frameon=False, loc="lower right")




ax[0].xaxis.set_ticks([1e-1,1e0,1e1])
ax[0].set_xlim((1e-1,1e2))

ax[1].xaxis.set_ticks([1e0,1e1,1e2,1e3])
ax[1].set_xlim((1e-1,1e4))

ax[2].xaxis.set_ticks([1e0,1e1,1e2,1e3,1e4,1e5])
ax[2].set_xlim((1e-1,1e5))

ax_in.set_xlabel(r"$t$")
ax_in.set_ylabel(r"$\frac{d \log(N)}{d \log(t)}$")
ax_in.set_xscale("log")

ax[0].set_ylabel(r"$N(t)$")

ax[0].yaxis.set_minor_locator(AutoMinorLocator())
ax[0].set_ylim((0,24))

plt.savefig("Plots/ev.pdf", bbox_inches='tight')
plt.show()














