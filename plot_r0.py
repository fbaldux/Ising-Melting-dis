
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data1 = np.loadtxt("Analysis/rAv_d10000.txt").T
data10 = np.loadtxt("Analysis/rAv_d10000.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 3)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

which = data1[0]==20
ax.plot(data1[1,which], data1[2,which], '-', marker=dots[0], ms=4, c=cols(0), label="center")


which = data10[0]==20
ax.plot(data10[1,which], data10[2,which], '-', marker=dots[1], ms=4, c=cols(1), label="zero")

ax.set_xlabel(r"$\varepsilon$")
ax.set_ylabel(r"$r$")

#ax.set_title(r"disorder realizations: 10000 ($N$=12...22) to 2000 ($N$=24...26)")

ax.legend(title=r"$N$")
plt.show()











