#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.special import jv
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm


N = 30
eps = 1.
#Tfin = np.array((1e2,1e2,1e3,1e3,1e4,1e4,1e4,1e4,1e5,1e5))
Tfin = np.array((1e1,1e2,1e3,1e4,1e5))
#init_states = np.array((0,))
dis_nums = np.array((400,800,1000,1200,1600,3000))


#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']
alpha = 0.1

#  -------------------------------------------  load  ------------------------------------------  #


for T in Tfin[::-1]:
    
    found = False
    
    for dis_num in dis_nums[::-1]:
        
        #if 1:
        try:
            filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_av%d.txt" % (N,eps,0,T,dis_num)                    
            av = np.loadtxt(filename).T  # t lat vert area EE
            ts = av[0]
            av = av[1:]
            
            found = True       
            break
        
        except:
            None
    
    if found:
        break

    
#  -------------------------------------------  plot  ------------------------------------------  #
                        
lab = r"$W=%.2f$" % (2*eps)
ax.plot(ts, av[3], '.', label=lab, c='black')


#  -------------------------------------------  fit  -------------------------------------------  #

start = 4
stop = 12
which = (ts>start) & (ts<stop)

# log
x = np.log(ts[which])
y = av[3,which]
fit = np.polyfit(x, y, 1)
print("%.2f %f %f" % (2*eps,fit[0],fit[1]))
f = np.poly1d(fit)
ax.plot(np.exp(x), f(x), ':', c='steelblue')

"""
# power law
x = np.log(ts[which])
y = np.log(av[3,which])
fit = np.polyfit(x, y, 1)
print("%.2f %f %f" % (2*eps,np.exp(fit[1]),fit[0]))
f = lambda t: np.exp(fit[1]) * t**fit[0]
ax.plot(ts[which], f(ts[which]), ':', c='steelblue')
"""


#  ----------------------------------------  parameters  ---------------------------------------  #

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$N(t)$")


ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend(fontsize="small")
plt.show()















