
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data1 = np.loadtxt("Analysis/rAv_d10000.txt").T
data2 = np.loadtxt("Analysis/rAv_d2000.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

c = 0
for N in range(12,24,2): 
    which = data1[0]==N
    ax.plot(data1[1,which], data1[2,which], '-', marker=dots[c], ms=4, c=cols(c), label=N)
    c += 1


for N in range(24,28,2): 
    which = data2[0]==N
    ax.plot(data2[1,which], data2[2,which], '-', marker=dots[c], ms=4, c=cols(c), label=N)
    c += 1

ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"$r$")

ax.set_title(r"disorder realizations: 10000 ($N$=12...22) to 2000 ($N$=24...26)")

ax.legend(title=r"$N$")
plt.show()











