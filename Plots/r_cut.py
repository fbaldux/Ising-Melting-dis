import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, brentq
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -----------------------------------------  analyze  -----------------------------------------  #

rGOE = 0.5307
dr = 0.02
cut = 0.52

deg = 4
eps_max = 100

Ns = []
cuts = []


for N in range(22,36,2): 
    which = (data[0]==N) & (data[1]<eps_max)
    x = data[1,which]
    y = data[2,which]
    
    
    # interpolate
    f = interp1d(x, y, kind='cubic')
    f1 = np.vectorize(f)
    
    """
    # fit
    fit = np.polyfit(x, y, deg)
    f = lambda x: np.dot( x**np.arange(deg+1), fit[::-1] )
    f1 = np.vectorize(f)
    
    # plot
    x1 = np.linspace(np.min(x), np.max(x), 100)
    plt.plot(x, y, '.')
    plt.plot(x1, f1(x1), '-')
    plt.title("N = %d" % N)
    plt.show()
    """
    f2 = lambda x: f1(x) - cut
    
    Ns.append(N)
    cuts.append( 2*fsolve(f2, 4) )
    #cuts.append( brentq(f2, 1, eps_max) )
    

Ns = np.array(Ns)
cuts = np.array(cuts)[:,0]

np.savetxt("Plots/r_cut.txt", np.stack((Ns,cuts)).T, header="N cut", fmt="%d %e")
exit(0)

#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [5.2,4.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 9)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


ax.plot(Ns, cuts, '.', c='black', label="data")

# fit
fit = np.polyfit(Ns, cuts, 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(Ns, f(Ns), '--', c='gray', label="fit")


ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$W^*$")

#ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

ax.legend(labelspacing=0.3)
plt.savefig("Plots/r_cut.pdf", bbox_inches='tight')
plt.show()











