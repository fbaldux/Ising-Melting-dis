
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data1 = np.loadtxt("Analysis/rAv_d10000.txt")
data2 = np.loadtxt("Analysis/rAv_d2000.txt")
data3 = np.loadtxt("Analysis/rAv_d4800.txt")[:,:-1]
data4 = np.loadtxt("Analysis/rAv_d1440.txt")[:,:-1]
data5 = np.loadtxt("Analysis/rAv_d1800.txt")[:,:-1]
data6 = np.loadtxt("Analysis/rAv_d780.txt")[:,:-1]

data = np.vstack((data1,data2,data3,data4,data5,data6)).T


#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 11)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

c = 0
for N in range(18,36,2): 
    which = data[0]==N
    ax.plot(data[1,which], data[2,which], '-', marker=dots[c], ms=4, c=cols(c), label=N)
    c += 1



ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"$r$")

ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend(title=r"$N$")
plt.show()











