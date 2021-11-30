import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
#import numba as nb

fig, ax = plt.subplots()

##########################  ALL N  ##########################

"""
Ns = np.array((20,40,80,160,320))

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
"""

##########################  FIT DECAY  ##########################

data = np.loadtxt("Results/DW_N320.txt").T

which = (data[0]>10) & (data[0]<75)
t = data[0,which]
IPR = data[1,which]

ax.plot(data[0], data[1], '-', label="N=320")

fit = np.polyfit(np.log(t), np.log(IPR), 1)
print(fit)
f = lambda x: np.exp(fit[1]) * x**fit[0]
ax.plot(t, f(t), '--', label="fit")

plt.text(0.5, 0.6, r"slope=$%.2f$" %(fit[0]), transform=ax.transAxes, c='tab:orange')


ax.set_xlabel(r"$t$")
ax.set_ylabel(r"IPR")

ax.set_xscale('log')
ax.set_yscale('log')

ax.legend()
plt.show()










