#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.special import jv
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm


Ns = np.arange(18,32,2)
#Ns = np.array((34,))
#eps = np.arange(0.5,3.5,0.5)
eps = np.arange(2,5.5,0.5)
T = 10000
dis_num = 10


#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()

#cols = cm.get_cmap("inferno", len(Ns)+1)
cols = cm.get_cmap("inferno", len(eps)+1)
#cmaps = ["Greys", "Purples", "Blues", "Oranges", "Reds"]
#cmaps = ["viridis", "plasma", "cividis", "Greys", "Purples", "Blues", "Oranges", "Reds"]

#  -------------------------------------------  load  ------------------------------------------  #

final = np.zeros((len(Ns),len(eps)))
c=0
for ie in range(len(eps)):
    e = eps[ie]
    
    for iN in range(len(Ns)):
        N = Ns[iN]
            
        #filename = "Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,e,T,0)
        #filename = "Averages/tEv_N%d_e%.4f_T%.1f_av%d.txt" % (N,e,T,dis_num)
        filename = "Averages/tEv_N%d_e%.4f_T%.2e_av%d.txt" % (N,e,T,dis_num)
        data = np.loadtxt(filename).T  # t lat1 vert lat2 area
        
        final[iN,ie] = np.average(data[4,-10:])

#  -------------------------------------------  plot  ------------------------------------------  #

    #lab = r"$N=%d$" % N
    lab = r"$\varepsilon=%.2f$" % e
    #lab = r"$N=%d$, $\varepsilon=%.2f$" % (N,e)

    ax.plot(Ns, final[:,ie], '.', label=lab, c=cols(c))


    c += 1

#  -------------------------------------------  clean  ------------------------------------------  #
"""
# clean case
#ax.plot(ts, np.sqrt(2)*ts, '--', c='black')
ax.plot(ts, 2*ts/np.pi, '--', c='firebrick')


lat_clean = lambda t: sum([2 * (t-k) * jv(k, 2*t)**2 for k in range(-50,int(t))]) - t
lat_clean2 = np.vectorize(lat_clean)

ts2 = np.linspace(0,15,100)
ax.plot(ts2, lat_clean2(ts2), '--', c='black')

"""
#  ----------------------------------------  parameters  ---------------------------------------  #

ax.set_xlabel(r"$N$")
#ax.set_ylabel(r"$\ell$")
ax.set_ylabel(r"$N(t_{fin})$")
#ax.set_ylabel(r"$\ell$")

#plt.clim((0,1))

#ax.set_title(r"$N=%d$, $\epsilon = %.2f$" %(N,epsilon))
#ax.set_title(r"$N=%d$" %(N))

#ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend()
#plt.savefig("plot.pdf", bbox_inches='tight')
plt.show()
















