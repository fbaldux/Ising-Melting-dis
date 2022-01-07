
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

# 0   1    2      3       4      5       6      7         8
# N eps min_av min_std mid_av mid_std max_av max_std dis_num_true
data = np.loadtxt("Analysis/lim_spec.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [4,3.2]
#plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 8)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

"""
c = 0
for eps in range(5,6):
    which = data[1]==eps
    
    c += 1
"""

which = data[1]==5
ax.errorbar(data[0,which], data[2,which], yerr=data[3,which], fmt='--', marker='v', ms=4)
ax.errorbar(data[0,which], data[4,which], yerr=data[5,which], fmt='-',  marker='o', ms=4)
ax.errorbar(data[0,which], data[6,which], yerr=data[7,which], fmt=':',  marker='^', ms=4)

ax.set_xlabel(r"$N$")
ax.set_ylabel(r"spec")



#ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend()
plt.show()











