
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

N = 10
eps = np.arange(1,12,2)
dis_num = 100

fig, ax = plt.subplots()


for ie in range(len(eps)):
    e = eps[ie]

    data = np.loadtxt("Results/spec_N%d_e%.4f_d%d.txt" % (N,e,0))[:,1:]
    
    for d in range(1,dis_num):
        data += np.loadtxt("Results/spec_N%d_e%.4f_d%d.txt" % (N,e,1))[:,1:]

    data /= dis_num
    
    data = np.average(data, axis=0)
    
    ax.plot(e, data[0], '.', c='black')
    ax.plot(e, data[1], 'x', c='red')
    ax.plot(e, data[2], '+', c='green')

#  -------------------------------------------  plot  ------------------------------------------  #



ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"params")

#ax.set_title(r"disorder realizations: 10000 ($N$=12...22) to 2000 ($N$=24...26)")

#ax.legend(title=r"$N$")
plt.show()











