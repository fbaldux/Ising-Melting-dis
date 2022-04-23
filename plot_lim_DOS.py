
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

Ns = np.array((20,22,24,26))
eps = np.array((5,))
#eps = np.arange(2,19,2)
dis_nums = np.array((10000,5000,))

fig, ax = plt.subplots()
cols = cm.get_cmap("inferno", len(Ns)+1)
#cols = cm.get_cmap("inferno", len(eps)+1)

#P = np.zeros((len(eps), nbins))
for iN in range(len(Ns)):
    N = Ns[iN]
    
    for ie in range(len(eps)):
        e = eps[ie]
        
        for dis_num in dis_nums:
            try:
                """
                data = np.loadtxt("Analysis/histoMin_N%d_e%.4f_av%d.txt" % (N,e,dis_num)).T        
                lab = r"$N$=%d, $\varepsilon$=%.1f" % (N,e)
                ax.plot(-data[0], data[1], '-', label=lab, c=cols(ie))
        
        
                data = np.loadtxt("Analysis/histoMax_N%d_e%.4f_av%d.txt" % (N,e,dis_num)).T
                ax.plot(data[0], data[1], '--', c=cols(ie))
                """
        
                data = np.loadtxt("Analysis/histoRatios_N%d_e%.4f_av%d.txt" % (N,e,dis_num)).T
                lab = r"$N$=%d, $\varepsilon$=%.1f" % (N,e)
                ax.plot(data[0], data[1], '-', label=lab, c=cols(iN))
        
            except:
                None
        
        

#  -------------------------------------------  plot  ------------------------------------------  #



#ax.set_xlabel(r"$\varepsilon$")
#ax.set_ylabel(r"area")

#ax.set_xlabel(r"$-E_{\min}, \, E_{\max}$")
#ax.set_ylabel(r"prob")

ax.set_xlabel(r"$\dfrac{|E_\max|}{|E_\max| + |E_\min|}$")
ax.set_ylabel(r"prob")

#ax.set_xscale("log")

#ax.set_title(r"$-$=min, --=max; dis.realiz.=%d" % dis_num)

ax.legend()
plt.savefig("plot.pdf", bbox_inches='tight')
plt.show()











