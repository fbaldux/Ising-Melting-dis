#  ---------------------------------------------------------------------------------------------  #
#
#   The program ...
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
from scipy import sparse
from scipy.linalg import eigh
from scipy.sparse.linalg import eigsh
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()


N = 12
epsilon = 2

    
#  -------------------------------------  load Hamiltonian  ------------------------------------  #

filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, 0)
eigvals, IPR = np.loadtxt(filename).T

histo, bins = np.histogram(eigvals, bins=20)


#ax.plot(np.arange(len(eigvals)), eigvals, '.', c='red', ms=2)

ax.plot(bins[:-1], histo, '.', c='red', ms=2)

#ax.set_xlim((0,dim[N]))
#ax.set_ylim((0,dim[N]))



#ax.set_title("n=%d (dim=%d)" %(N,dim[N]))

#ax.set_xscale("log")
#ax.set_yscale("log")

ax.legend()
plt.show()


















