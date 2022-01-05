#import sys
#sys.path.append('../Numerics-dis')

import numpy as np
#from partitions import *
from matplotlib import pyplot as plt
from matplotlib import cm
import cmasher as cmr


N = 30
dis_num = 1920

#  ---------------------------------------  load & plot  ---------------------------------------  #

fig, ax = plt.subplots()
#cols = cm.get_cmap('cmr.ember', 10)
cols = cm.get_cmap('viridis', 10)
dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')


c = 0
for eps in range(1,19,2): 
    filename = "Analysis/sHisto_N%d_e%.4f_d%d.txt" % (N,eps,dis_num)
    data = np.loadtxt(filename).T
    
    # compute average spacing
    av_s = 0.5 * data[1,0]*data[0,0] * (data[0,1]-data[0,0])
    for x in range(1,len(data[0])-1):
        av_s += data[1,x]*data[0,x] * (data[0,x+1]-data[0,x])
    av_s += 0.5 * data[1,-1]*data[0,-1] * (data[0,-2]-data[0,-1])
        
    ax.plot(data[0]/av_s, data[1]*av_s, '-', c=cols(c), label=eps)
    #ax.plot(data[0]/av_s, data[1]*av_s, '-', c=cols(c), label=eps, marker=dots[c], ms=4)
    c += 1


s = np.linspace(0,10,100)
ax.plot(s, np.exp(-s), '--', label='Poisson', c='black')
ax.plot(s, 0.5*s*np.pi * np.exp(-0.25*np.pi*s**2), ':', label='GOE', c='black')

ax.set_xlim((0,6))

ax.set_xlabel(r"$s$")
ax.set_ylabel(r"$P(s)$")

#ax.set_yscale('log')

ax.set_title(r"$N = %d$; %d disorder realizations" % (N,dis_num))

ax.legend(title=r"$\varepsilon$")
plt.show()











