#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, brentq
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import *
import cmasher as cmr


N = 30

eps = np.array((0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5))
Tfin = np.array((1e1,1e2,1e3,1e4,1e5))

dis_nums = np.array((400,800,1000,1200,1600,3000))


#plt.rcParams["figure.figsize"] = [12.8,4]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 16})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.tropical', len(eps))
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']
alpha = 0.1

# inset
left, bottom, width, height = 0.54, 0.15, 0.45, 0.48
ax2 = ax.inset_axes([left, bottom, width, height])   

taus = np.zeros(len(eps))
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

    # main
    if ie%2 == 0:
        lab = r"$W=%d$" % (2*e)
        ax.plot(ts, av[2], '-', label=lab, c=cols(ie))
        #ax.fill_between(ts, av[2]+std[2], av[2]-std[2], color=cols(ie), alpha=alpha)         
        
    
    # -------------  inset  ------------- #
    
    # first entry of the array (no interpolation)
    """
    tau = np.where( np.abs(np.log(ts[1:]**2/av[2,1:])) > threshold )[0][0]
    taus[ie] = ts[tau+1]
    """
    
    # with interpolation
    f = interp1d(ts, av[2], kind='cubic')
    f2 = lambda t: np.abs(np.log(t**2/f(t))) - threshold 
    taus[ie] = fsolve(f2, 1)


    
# clean case
ts = np.linspace(0.1,10,100)
ax.plot(ts, ts**2, '--', c='black', label=r"$t^2$")

# inset plot
ax2.plot(np.log(2*eps), np.log(taus), 'd', c='black', ms=4)

# inset fit
x = np.log(2*eps)
y = np.log(taus)
fit = np.polyfit(x, y, 1)
print(fit)
f = lambda t: fit[1] + t*fit[0]
ax2.plot(x, f(x), ':', c='black')


#  ----------------------------------------  parameters  ---------------------------------------  #

# main
ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$\langle N(t) \rangle$")

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlim((1e-1,1e5))
ax.set_ylim((1e-2,40))

ax.legend(labelspacing=0.3, fontsize=14, loc="lower center", bbox_to_anchor=(0.27,0), frameon=False)


# inset
#ax2.set_xlabel(r"$W$", fontsize=15)
#ax2.set_ylabel(r"$\tau(W)$", fontsize=15)
ax2.set_xlabel(r"$\ln W$", fontsize=15)
ax2.set_ylabel(r"$\ln \tau(W)$", fontsize=15)

ax2.xaxis.labelpad = -2
ax2.yaxis.labelpad = -2

ax2.xaxis.set_minor_locator(AutoMinorLocator())
ax2.yaxis.set_minor_locator(AutoMinorLocator())

#ax2.set_xscale("log")
#ax2.set_yscale("log")


# save
plt.savefig("Plots/ev_tau.pdf", bbox_inches='tight')
plt.show()












