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
Ns = np.array((20,22,24,26,28,30))
#eps = np.arange(0.5,3.5,0.5)
eps = np.array((1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5))#,5.0,5.5))
Tfin = np.array((1e2,1e2,1e3,1e3,1e4,1e4,1e4,1e4,1e5,1e5))
#init_states = np.array((0,))
dis_nums = np.array((400,800,1000,1200,1600,3000))


#plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()

#cols = cm.get_cmap("inferno", len(Ns)*len(eps)+1)
cols = cm.get_cmap("inferno", len(Ns)+1)
#cols = cm.get_cmap("inferno", len(eps)+1)
#cols = cm.get_cmap("inferno", len(init_states)+1)
#cmaps = ["Greys", "Purples", "Blues", "Oranges", "Reds"]
#cmaps = ["viridis", "plasma", "cividis", "Greys", "Purples", "Blues", "Oranges", "Reds"]

dots = ('o', 'v', '^', '>', '<', 's', 'P', 'h', 'X', 'D')
ls = ['-', '--', '-.', ':']
alpha = 0.1

#  -------------------------------------------  load  ------------------------------------------  #

c = 0
for ie in range(2,len(eps)):
    e = eps[ie]
    T = Tfin[ie]
    
    #cols = cm.get_cmap(cmaps[ie], len(Ns)+1)
    fig, ax = plt.subplots()
    
    for iN in range(len(Ns)):
        N = Ns[iN]
           
        c = 0
        
        for T in Tfin[::-1]:
            
            for dis_num in dis_nums[::-1]:
                
                #if 1:
                try:
                    filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_av%d.txt" % (N,e,0,T,dis_num)
                    av = np.loadtxt(filename).T  # t lat vert area EE
                    ts = av[0]
                    av = av[1:]
                
                    filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_std%d.txt" % (N,e,0,T,dis_num)
                    std = np.sqrt(np.loadtxt(filename)[:,1:]).T  # t lat vert area EE
                                
                    break
                
                except:
                    None
#  -------------------------------------------  plot  ------------------------------------------  #
                        
        lab = r"$N=%d$" % N
        #lab = r"$\varepsilon=%.2f$" % e
        #lab = r"$N=%d$, $\varepsilon=%.2f$" % (N,e)
        #lab = r"$N$=%d, in.st.=%d" % (N,in_st)
        
        #ax.plot(ts, 0.5*(data[1]+data[3]), '-', label="lateral", c='black')

        #ax.plot(av[2], av[3], '-', label=lab, c=cols(iN))
        #ax.plot(data[0], np.sqrt(data[4]), '-', label=lab, c=cols(c))
        
        # N(t)
        #ax.plot(ts, av[2], '-', label=lab, c=cols(iN))
        #ax.fill_between(ts, av[2]+std[2], av[2]-std[2], color=cols(iN), alpha=alpha)         
        
        # EE
        #ax.plot(ts, av[3], '-', label=lab, c=cols(iN))
        #ax.fill_between(ts, av[3]+std[3], av[3]-std[3], color=cols(iN), alpha=alpha)
        
        # log-derivative
        logt = np.log(ts)
        logN = np.log(av[2])
        ax.plot(0.5*(ts[:-1]+ts[1:]), np.diff(logN)/np.diff(logt), '-', label=lab, c=cols(iN))
        
        c += 1

#  ----------------------------------------  parameters  ---------------------------------------  #

    ax.set_xlabel(r"$t$")
    #ax.set_ylabel(r"$N(t)$")
    ax.set_ylabel(r"$\frac{d \log(N)}{d \log(t)}$")
    #ax.set_ylabel(r"$\frac{dN}{d \log(t)}$")
    #ax.set_ylabel(r"$S_E(t)$")

    #plt.xlim((0,1))

    #ax.set_title(r"$N$=%d" %(N))
    ax.set_title(r"$W$ = %.2f" %(2*e))

    ax.set_xscale("log")
    #ax.set_yscale("log")

    ax.legend(fontsize="small")
    plt.savefig("temp/p_e%.2f.pdf" % (e), bbox_inches='tight')
    #plt.show()
    plt.clf()















