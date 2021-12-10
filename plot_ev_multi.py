#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.special import jv
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm


N = 34
eps = np.arange(0,9,2)
T = 100
dis_num = 1


#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()

#cols = cm.get_cmap("inferno", len(Ns)+1)
cols = cm.get_cmap("inferno", len(eps)+1)


#  -------------------------------------------  load  ------------------------------------------  #

c = 0

#for iN in range(len(Ns)):
#    N = Ns[iN]
for ie in range(len(eps)):
    e = eps[ie]
    
    filename = "Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,e,T,0)
    data = np.loadtxt(filename).T

    ts = data[0]
    data = data[1:]

    for dis in range(1,dis_num):

        #  load the results
        filename = "Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,e,T,dis)
        data += np.loadtxt(filename)[:,1:].T
    
    data /= dis_num


#  -------------------------------------------  plot  ------------------------------------------  #

    #lab = r"$N=%d$" % N
    lab = r"$\varepsilon=%.2f$" % e
    
    #ax.plot(ts, 0.5*(data[0]+data[2]), '-', label="lateral", c='black')
    
    #ax.plot(ts, data[1], '-', label=lab, c=cols(c))
    #ax.plot(ts, np.sqrt(data[3]), '-', label=lab, c=cols(c))
    ax.plot(ts, data[3], '-', label=lab, c=cols(c))
    

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

ax.set_xlabel(r"$t$")
#ax.set_ylabel(r"$\ell$")
ax.set_ylabel(r"$N(t)$")

#plt.clim((0,1))

#ax.set_title(r"$N=%d$, $\epsilon = %.2f$" %(N,epsilon))
ax.set_title(r"$N=%d$" %(N))

#ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend()
#plt.savefig("Plots/e%.2f_t%.2f.pdf"%(epsilon,ts[it]), bbox_inches='tight')
plt.show()
















