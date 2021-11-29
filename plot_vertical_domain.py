import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
#import numba as nb


Ns = np.array((20,40,80,160,320))

fig, ax = plt.subplots()
cols = cm.get_cmap('magma', len(Ns)+1)

for iN in range(len(Ns)):
    N = Ns[iN]
    
    data = np.loadtxt("Results/DW_N%d.txt" % (N)).T

    ax.plot(data[0], data[1], '-', c=cols(iN), label=r"$N=%d$"%N)
    

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"IPR")

ax.set_xscale('log')
ax.set_yscale('log')

ax.legend()
plt.show()














