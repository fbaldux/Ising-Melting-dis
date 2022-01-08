import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fsolve, brentq, curve_fit
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


#  -------------------------------------------  load  ------------------------------------------  #

data = np.loadtxt("Analysis/rAv.txt").T


#  -----------------------------------------  analyze  -----------------------------------------  #

def fitfunc(x,a,b):
    #return 0.53 - a * x**(-b)
    #return 0.53 - a * np.exp(b*(x-c))
    return 0.39 - 0.14 * np.tanh(a*x**3 + b*x )
    
rGOE = 0.5307
dr = 0.02
cut = 0.51

deg = 3
eps_min = 2
eps_max = 7

Ns = []
cuts = []


for N in range(18,36,2): 
    which = (data[0]==N) & (eps_min<=data[1]) & (data[1]<=eps_max)
    x = data[1,which]
    y = data[2,which]
    
    """"
    # interpolate
    f = interp1d(x, y, kind='cubic')
    """
    
    # fit
    fit = np.polyfit(x, y, deg)
    f = lambda x: np.dot( x**np.arange(deg+1), fit[::-1] )
    
    """
    # fit
    #bds = ((0,2,0),(np.inf,2.2,np.inf))
    guess = (1,1,)
    fit, cov = curve_fit(fitfunc, x, y, p0=guess) #, bounds=bds)
    f = lambda x: fitfunc(x, *fit)
    """
    
    f1 = np.vectorize(f)
    """
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
    #cuts.append( 2*brentq(f2, eps_min, eps_max) )
    

Ns = np.array(Ns)
cuts = np.array(cuts)[:,0]

np.savetxt("Plots/r_cut_high.txt", np.stack((Ns,cuts)).T, header="N cut", fmt="%d %e")
#exit(0)

#  -------------------------------------------  plot  ------------------------------------------  #

#plt.rcParams["figure.figsize"] = [5.2,4.2]
plt.rcParams.update({"text.usetex": True, "font.family": "serif", "font.size": 17})

fig, ax = plt.subplots()
cols = cm.get_cmap('cmr.ember', 8)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


ax.plot(Ns, cuts, '.', c='black', label="data")

# fit
fit = np.polyfit(Ns, cuts, 1)
f = lambda x: fit[0]*x + fit[1]
ax.plot(Ns, f(Ns), '--',  c='steelblue', label="linear fit")

"""
# fit 2
fit = np.polyfit(Ns, cuts, 2)
f = lambda x: fit[0]*x**2 + fit[1]*x + fit[2]
Ns2 = np.linspace(np.min(Ns), np.max(Ns), 100)
ax.plot(Ns2, f(Ns2), ':', c='maroon', label="quadratic fit")
"""

ax.set_xlabel(r"$N$")
ax.set_ylabel(r"$W^*$")

#ax.set_title(r"$\varepsilon^*$ s.t. $r(\varepsilon^*) = $%.3f" % cut)

ax.legend(labelspacing=0.3)
plt.savefig("Plots/r_cut_high.pdf", bbox_inches='tight')
plt.show()











