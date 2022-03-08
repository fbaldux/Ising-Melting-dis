#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.special import jv
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm


N = int( sys.argv[1] )
epsilon = float( sys.argv[2] )
init_state = int( sys.argv[3] )
T = float( sys.argv[4] )
dis_num = int( sys.argv[5] )


#  -------------------------------------------  load  ------------------------------------------  #

filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,T,0)
data = np.loadtxt(filename).T

ts = data[0]
data = data[1:]

for dis in range(1,dis_num):

    #  load the results
    filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,T,dis)
    data += np.loadtxt(filename)[:,1:].T
    
data /= dis_num


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()

ax.plot(ts, data[0], '.', label="lateral", c='black')
ax.plot(ts, data[1], '.', label="central", c='firebrick')
ax.plot(ts, np.sqrt(data[2]), '.', label="sqrt(area)", c='darkblue')
ax.plot(ts, data[3], '.', label="EE", c='darkgreen')

# clean case
#ax.plot(ts, np.sqrt(2)*ts, '--', c='black')
#ax.plot(ts, 2*ts/np.pi, '--', c='firebrick')

"""
lat_clean = lambda t: sum([2 * (t-k) * jv(k, 2*t)**2 for k in range(-50,int(t))]) - t
lat_clean2 = np.vectorize(lat_clean)

ts2 = np.linspace(0,15,100)
#ax.plot(ts2, lat_clean2(ts2), '--', c='black')
"""

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$\ell$")

#plt.clim((0,1))

ax.set_title(r"$N$=%d, $\epsilon$=%.2f, init.state=%d" %(N,epsilon,init_state))

ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend()
#plt.savefig("Plots/e%.2f_t%.2f.pdf"%(epsilon,ts[it]), bbox_inches='tight')
plt.show()
















