
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

Ns = np.arange(14,15,2)
eps = np.arange(1,11,1)
dis_num = 50
nbins = 20

fig, ax = plt.subplots()
#cols = cm.get_cmap("inferno", len(Ns)+1)
cols = cm.get_cmap("inferno", len(eps)+1)

#P = np.zeros((len(eps), nbins))
for iN in range(len(Ns)):
    N = Ns[iN]
    
    av = np.zeros(len(eps))
    std = np.zeros(len(eps))
    
    for ie in range(len(eps)):
        e = eps[ie]

        data = [np.loadtxt("Results/spec_N%d_e%.4f_d%d.txt" % (N,e,0))[:-1,4]]
    
        for d in range(1,dis_num):
            data.append(np.loadtxt("Results/spec_N%d_e%.4f_d%d.txt" % (N,e,1))[:-1,4])

        data = np.array(data) #/ N**2
        """
        av[ie] = np.average(data)
        std[ie] = np.std(data)
    
    ax.errorbar(eps, av, yerr=std, fmt='s', c=cols(iN), label="N=%d"%N)
        """

        
        histo,bins = np.histogram(np.log(np.abs(data)), bins=nbins, density=True)
        bins = 0.5 * ( bins[1:] + bins[:-1] )
    
        ax.plot(bins, histo, '-', label=r"$\varepsilon=%.1f$"%e, c=cols(ie))


#  -------------------------------------------  plot  ------------------------------------------  #



#ax.set_xlabel(r"$\varepsilon$")
#ax.set_ylabel(r"area")

ax.set_xlabel(r"area")
ax.set_ylabel(r"P(area)")

#ax.set_xscale("log")

#ax.set_title(r"disorder realizations: 10000 ($N$=12...22) to 2000 ($N$=24...26)")

ax.legend()
plt.show()











