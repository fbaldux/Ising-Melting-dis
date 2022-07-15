
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MultipleLocator
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Averages/MCshape_N10000_d10000.txt").T


#  -------------------------------------------  plot  ------------------------------------------  #

def Okounkov(x):
    if x < -2:
        return -x
    elif x > 2:
        return x
    else:
        return 2/np.pi * ( x*np.arcsin(0.5*x) + np.sqrt(4 - x**2) )



plt.rcParams["figure.figsize"] = [5,5]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember_r', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')

ax.plot(data[0]*np.sqrt(2), data[1]*np.sqrt(2), '-', c='black', label=r"Monte Carlo")

xO = np.linspace(-10,10,100)
plt.plot(xO, np.vectorize(Okounkov)(xO), '--', c='red', label="Okounkov")


ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")

ax.set_xlim((-10,10))
ax.set_ylim((0,10))

#ax.set_xticks(np.arange(5,40,5))
#ax.set_yticks(np.linspace(0.39,0.53,6))
#ax.tick_params(axis='x', which='minor', bottom=False)

#ax.set_title(r"disorder realizations: 10000 ($N$=12) to 700 ($N$=34)")

ax.legend(labelspacing=0.3, fontsize=15)
plt.savefig("Plots/MCshape.pdf", bbox_inches='tight')
plt.show()











