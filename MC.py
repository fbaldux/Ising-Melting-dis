#  ---------------------------------------------------------------------------------------------  #
#
#   The program builds a Young diagram by successively adding boxes. It thus samples, through
#   a MonteCarlo procedure, the n-box Young diagrams with the measure given by the paths
#   in the graph.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from matplotlib import pyplot as plt
from matplotlib import cm

plt.rcParams["figure.figsize"] = [6,6]
cols = cm.get_cmap('magma', 6)


instring = input("").split(' ')

N = int( float(instring[0]) )
rep_num = int( instring[1] )


#  ---------------------------------------  MC sampling  ---------------------------------------  #

@nb.njit
def MC():
    shape = np.zeros(N, dtype=np.int_)
    shape[0] = 1
    
    c = 1
    max_row = 2
    while c<N:
        row = np.random.randint(max_row)
        
        if row==0 or shape[row-1]>shape[row]:
            shape[row] += 1
            c += 1
            
            if row == max_row-1:
                max_row += 1

    return shape


#  -------------------------------------------  main  ------------------------------------------  #

shape = np.zeros(N)

for rep in range(rep_num): 
    shape += MC()
    

shape /= rep_num


filename = "Results/MC_N%d_av%d.txt" % (N,rep_num)
np.savetxt(filename, shape)
"""


plt.plot(-shape/np.sqrt(N), -np.arange(N)/np.sqrt(N), '-', c='black', label=r"MonteCarlo")

mesh = 100

a = np.linspace(-2,2,mesh)
b = 2/np.pi * ( a*np.arcsin(0.5*a) + np.sqrt(4 - a**2) )

x = 0.5*(b+a)
y = 0.5*(b-a)

plt.plot(-x, -y, '--', c='red', label="Okounkov")


plt.xlim((-2*np.sqrt(2),0))
plt.ylim((-2*np.sqrt(2),0))

plt.xlabel(r"$x / \sqrt{N}$")
plt.ylabel(r"$y / \sqrt{N}$")

plt.title(r"$10^{%d}$ boxes removed; $10^{%d}$ instances averaged" % (np.log10(N), np.log10(rep_num)) )

plt.legend(loc="lower left")
plt.show()
"""