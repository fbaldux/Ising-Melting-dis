#  ---------------------------------------------------------------------------------------------  #
#
#   The program evolves a state in the Hilbert space of a strip of length L.
#   Needed for some checks.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
from scipy.linalg import expm
from scipy import sparse
from LanczosRoutines import *
from time import time
from matplotlib import pyplot as plt


#  ------------------------------------  program constants  ------------------------------------  #

Fibonacci = np.array((0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584,\
             4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040,\
             1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986))

# system size
L = 22
dim = Fibonacci[L]


#  ---------------------------------------  load & plot  ---------------------------------------  #

filename = "Results/stripEv_L%d.txt" % (L)
data = np.loadtxt(filename)


plt.plot(np.arange(L), data[-1,1:], '-', label="t=%.0f" % data[-1,0])
plt.plot(np.arange(L), data[-2,1:], '-', label="t=%.0f" % data[-2,0])
plt.plot(np.arange(L), data[-3,1:], '-', label="t=%.0f" % data[-3,0])

plt.xlabel("x")
plt.ylabel("m")

plt.legend()
plt.show()














