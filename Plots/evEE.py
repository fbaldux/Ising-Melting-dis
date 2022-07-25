#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import cmasher as cmr


Ns = np.array((20,22,24,26,28,30))

eps = np.array( (1.0,2.5,4.5))
Tfin = np.array((1e2,1e3,1e4,1e5))

dis_nums = np.array((400,800,1000,1200,1600,3000))


plt.rcParams["figure.figsize"] = [12.8,4]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})

fig = plt.figure()
gs = fig.add_gridspec(1, 3, wspace=0)
ax = gs.subplots(sharex=False, sharey=True)
plot_label = ["(a)","(b)","(c)"] 


cols = cm.get_cmap('cmr.ember_r', len(Ns)+1)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']
alpha = 0.1

#  -------------------------------------------  load  ------------------------------------------  #

# exact
data = np.loadtxt("Plots/EE_exact.txt").T
#data2 = np.loadtxt("Plots/a.txt")
for ie in range(3):
    temp = np.logspace(1,5,100)
    ts = np.append(data[0], temp)
    EE = np.append(data[1], np.log(2*temp)/6+0.475)
    ax[ie].plot(ts, EE, '--', c='black')

    

for ie in range(len(eps)):
    e = eps[ie]
    """
    if ie==2:
        left, bottom, width, height = 0.2, 0.45, 0.7, 0.5
        ax_in = ax[ie].inset_axes([left, bottom, width, height])
    """
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
                    """
                    filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_std%d.txt" % (N,e,0,T,dis_num)
                    #std = np.sqrt(np.loadtxt(filename)[:,1:]).T  # t lat vert area EE
                    std = np.loadtxt(filename)[:,1:].T  # t lat vert area EE
                    """
                    found = True
                    break
                
                except:
                    None
              
            if found:
                break
            
#  -------------------------------------------  plot  ------------------------------------------  #
                        
        lab = r"$N=%d$" % N
        
        ax[ie].plot(ts, av[3], '-', label=lab, c=cols(iN))
        #ax[ie].fill_between(ts, av[3]+std[3], av[3]-std[3], color=cols(iN), alpha=alpha)

#  -------------------------------------------  fit  -------------------------------------------  #

        if ie>0 and N==30:
            
            if ie==1:
                which = (ts>1.7) & (ts<46)
            if ie==2:
                which = (ts>4) & (ts<2300)
            x = np.log(ts[which])
            y = av[3,which]
            fit = np.polyfit(x, y, 1)
            print(fit)
            f = np.poly1d(fit)
            if ie==1:
                ax[ie].plot(np.exp(x), f(x)+0.2, ':', c='steelblue')
            if ie==2:
                ax[ie].plot(np.exp(x), f(x)-0.2, ':', c='steelblue')
            
        
            """
            if ie==1:
                t = np.logspace(np.log10(2), np.log10(80),20)
            if ie==2:
                t = np.logspace(np.log10(2), np.log10(1900),20)
            """
            
            
            #ax[ie].plot(t, 3.57*np.log(t)+0.5, ':', c='green')

#  ------------------------------------------  inset  ------------------------------------------  #
        """
        if ie==2:
            logt = np.log(ts[1:])
            av2 = np.maximum(av[2,1:], np.ones(len(av[2,1:]))*1e-10)
            logN = np.log(av2)
            ax_in.plot(0.5*(ts[1:-1]+ts[2:]), np.diff(logN)/np.diff(logt), '-', c=cols(iN))
        """
#  ----------------------------------------  parameters  ---------------------------------------  #

    ax[ie].set_xlabel(r"$t$")
        
    ax[ie].set_title(r"$W$ = %d" %(2*e), fontsize=16)

    ax[ie].set_xscale("log")
    #ax.set_yscale("log")
    
    if ie==0:
        ax[ie].legend(labelspacing=0.3, fontsize=14, loc="upper left", frameon=False, bbox_to_anchor=(0.01, 0.9))

    ax[ie].text(0.02, 0.93, plot_label[ie], c='black', transform=ax[ie].transAxes)
    


ax[0].xaxis.set_ticks([1e-1,1e0,1e1])
ax[0].set_xlim((1e-1,1e2))

ax[1].xaxis.set_ticks([1e0,1e1,1e2,1e3])
ax[1].set_xlim((1e-1,1e4))

ax[2].xaxis.set_ticks([1e0,1e1,1e2,1e3,1e4,1e5])
ax[2].set_xlim((1e-1,1e5))
"""
ax_in.set_xlabel(r"$t$")
ax_in.set_ylabel(r"$\frac{d \log(N)}{d \log(t)}$")
ax_in.set_xscale("log")
"""
ax[0].set_ylabel(r"$S_E(t)$")

ax[0].yaxis.set_minor_locator(AutoMinorLocator())
ax[0].set_ylim((0,5))

plt.savefig("Plots/evEE.pdf", bbox_inches='tight')
plt.show()














