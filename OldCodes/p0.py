
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/p0_typ.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
#plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


c = 0
#for eps in range(2,18,2): 
    #which = data[1]==eps
for N in range(14,24,2): 
    which = data[0]==N
    
    # E
    #ax.plot(data[0,which], data[3,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$W=%d$" % (2*eps))
    #ax.plot(data[1,which], data[3,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$N=%d$" % N)
    
    # N
    #ax.plot(data[0,which], data[4,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$W=%d$" % (2*eps))
    
    # p0
    #ax.plot(data[0,which], data[5,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$W=%d$" % (2*eps))
    ax.plot(data[1,which], data[5,which], '-', marker=dots[c], ms=4, c=cols(c), label=r"$N=%d$" % (N))
    c += 1


ax.set_xlabel(r"$W$")
#ax.set_xlabel(r"$N$")
#ax.set_ylabel(r"$\sqrt{ \langle E[\psi_0]^2 \rangle }$")
#ax.set_ylabel(r"$\langle N[\psi_0] \rangle$")
ax.set_ylabel(r"typ $|\langle \emptyset | \psi_0 \rangle|^2$")



ax.set_title(r"disorder realizations: 1000")

#ax.legend(labelspacing=0.3, fontsize=15)
ax.legend()
plt.savefig("Plots/p0.pdf", bbox_inches='tight')
plt.show()











