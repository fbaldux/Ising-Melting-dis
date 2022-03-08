#  ---------------------------------------------------------------------------------------------  #
#
#   The program performs a walk on the Young diagram lattice, by trying to stay in resonance
#   with the energy of the initial state.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
import numba as nb
from matplotlib import pyplot as plt

# system size
N = int( float(sys.argv[1]) )

# number of disorder instances
dis_num = int( sys.argv[2] )


#  -----------------------------------  MonteCarlo procedure  ----------------------------------  #

@nb.njit
def MC(RF):
    shape = np.zeros(N, dtype=np.int_)
    Et = np.zeros(N)
    
    # initial state
    shape[0] = 1
    Et[0] = RF[0]
    
    c = 1
    max_row = 2
    while c<N:        
        # check which box is better to add
        best_row = 0
        best_E = Et[c-1] + RF[0]
        for row in range(1,max_row):
            if shape[row-1]>shape[row]:
                trial_E = Et[c-1] + RF[row]
            
                if np.abs(trial_E) < np.abs(best_E):
                    best_row = row
                    best_E = trial_E
    
        shape[best_row] += 1
        Et[c] = best_E
        RF[best_row] = np.random.uniform(-1,1)
        c += 1

        if best_row == max_row-1:
            max_row += 1
    
    return shape, Et


#  ---------------------------------  fill in continuous line  ---------------------------------  #

@nb.njit
def reshape(shape,N):
    box_num = np.sum(shape)
    
    shape_x = np.zeros(2*N+1)
    shape_y = np.zeros(2*N+1)
    
    x = N
    y = 0
    
    c = 0
    while y < box_num:
        shape_x[c] = x
        shape_y[c] = y
        
        # go down
        if shape[y] == x:
            y += 1
        # go right
        else:
            x -= 1
        
        c += 1
    
    shape_y[2*N] = N
    
    return shape_x, shape_y


#  -------------------------------------------  main  ------------------------------------------  #

av_V_shape = np.zeros(2*N+1)
av_Et = np.zeros(N)
av_Et2 = np.zeros(N)

for dis in range(dis_num):
    # extract the random fields
    RF = np.random.uniform(-1, 1, size=N)
    
    # perform the Monte Carlo
    corner_shape, Et = MC(RF)
    
    """
    plt.plot(np.arange(N), Et, '-', c='black')
    plt.xlabel("N")
    plt.ylabel("E")
    plt.show()
    exit(0)
    """
        
    corner_shape = reshape(corner_shape,N)                          # convert to a continuous line
    av_V_shape += (corner_shape[0] + corner_shape[1]) / np.sqrt(2)  # 45 deg rotation
    
    av_Et += Et
    av_Et2 += Et**2
    
    
av_V_shape /= dis_num 
av_Et /= dis_num
av_Et2 = np.sqrt(av_Et2 / dis_num)


#  ----------------------------------------  plot shape  ---------------------------------------  #

x = np.arange(-N,N+1) / np.sqrt(2*N)
y = av_V_shape / np.sqrt(N)

"""
@nb.vectorize
def Okounkov(x):
    if x < -2:
        return -x
    elif x > 2:
        return x
    else:
        return 2/np.pi * ( x*np.arcsin(0.5*x) + np.sqrt(4 - x**2) )


plt.rcParams["figure.figsize"] = [8,4]

plt.plot(np.sqrt(2)*x, np.sqrt(2)*y, '-', c='black', label="MC")

xO = np.linspace(-10,10,100)
plt.plot(xO, Okounkov(xO), '--', c='darkgreen', label="Okounkov")

plt.xlabel("x")
plt.ylabel("y")

plt.xlim((-10,10))
plt.ylim((0,10))

plt.legend()
plt.show()
"""

filename = "Averages/MCshape_N%d_d%d.txt" % (N,dis_num)
np.savetxt(filename, np.stack((x,y)).T, header="x y")


#  --------------------------------------  plot energies  --------------------------------------  #

"""
plt.plot(np.arange(N), av_Et, '-', c='blue', label=r"$\langle E(t) \rangle$")
plt.plot(np.arange(N), av_Et2, '--', c='blue', label=r"$\langle E^2(t) \rangle^{1/2}$")

plt.axhline(0, ls=":", c="black")

plt.xlabel(r"MC time")
plt.ylabel(r"energy")

plt.title(r"$N = %d$, dis.samp. = %d" % (N, dis_num))

plt.legend()
plt.show()
"""

filename = "Averages/MCen_N%d_d%d.txt" % (N,dis_num)
np.savetxt(filename, np.stack((av_Et,av_Et2)).T, header="<E> sqrt<E^2>")







