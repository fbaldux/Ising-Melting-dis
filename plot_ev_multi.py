#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.special import jv
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm


#Ns = np.arange(30,34,2)
Ns = np.array((22,24,26))
#eps = np.arange(0.5,3.5,0.5)
eps = np.array((1,2,3,4,5))
init_states = np.array((0,24,121,))
Tfin = np.array((1e4,1e4,1e4,1e5,1e5))
dis_num = 1500


#plt.rcParams["figure.figsize"] = [6,6]

#fig, ax = plt.subplots()

#cols = cm.get_cmap("inferno", len(Ns)*len(eps)+1)
cols = cm.get_cmap("inferno", len(init_states)+1)
#cmaps = ["Greys", "Purples", "Blues", "Oranges", "Reds"]
#cmaps = ["viridis", "plasma", "cividis", "Greys", "Purples", "Blues", "Oranges", "Reds"]

dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']

#  -------------------------------------------  load  ------------------------------------------  #

c = 0
for ie in range(len(eps)):
    e = eps[ie]
    
    #cols = cm.get_cmap(cmaps[ie], len(Ns)+1)
    fig, ax = plt.subplots()
    
    for iN in range(len(Ns)):
        N = Ns[iN]
           
        c = 0
        
        for iS in range(len(init_states)):
            in_st = init_states[iS]
        
            filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_av%d.txt" % (N,e,in_st,Tfin[ie],dis_num)
            av = np.loadtxt(filename).T  # t lat vert area
            ts = av[0]
            av = av[1:]
            
            filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_std%d.txt" % (N,e,in_st,Tfin[ie],dis_num)
            std = np.sqrt(np.loadtxt(filename)[:,1:])  # t lat vert area EE

#  -------------------------------------------  plot  ------------------------------------------  #
                        
            #lab = r"$N=%d$" % N
            #lab = r"$\varepsilon=%.2f$" % e
            #lab = r"$N=%d$, $\varepsilon=%.2f$" % (N,e)
            lab = r"$N$=%d, in.st.=%d" % (N,in_st)
            
            #ax.plot(ts, 0.5*(data[1]+data[3]), '-', label="lateral", c='black')
    
            #ax.plot(data[0], data[2], '-', label=lab, c=cols(c))
            #ax.plot(data[0], np.sqrt(data[4]), '-', label=lab, c=cols(c))
            
            #ax.plot(ts[::], av[2,::], '-', marker=dots[iN], ms=3, label=lab, c=cols(iS))
            ax.plot(ts, av[3], ls[iN], label=lab, c=cols(iS))
            #ax.fill_between(ts[::10], av[2,::10]+std[2,::10], av[2,::10]-std[2,::10], alpha=0.5, lw=0, color=cols(iS))

            c += 1

#  ----------------------------------------  parameters  ---------------------------------------  #

    ax.set_xlabel(r"$t$")
    #ax.set_ylabel(r"$\ell$")
    #ax.set_ylabel(r"$N(t)$")
    ax.set_ylabel(r"$S_E(t)$")

    #plt.clim((0,1))

    #ax.set_title(r"$N$=%d, $W$ = %.2f" %(N,2*e))
    ax.set_title(r"$W$ = %.2f" %(2*e))

    ax.set_xscale("log")
    #ax.set_yscale("log")

    ax.legend(fontsize="small")
    plt.savefig("temp/p_e%.2f.pdf" % (e), bbox_inches='tight')
    #plt.show()
    plt.clf()















