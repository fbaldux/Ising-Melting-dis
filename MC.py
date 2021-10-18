#  ---------------------------------------------------------------------------------------------  #
#
#   The program builds a Young diagram by successively adding boxes. It thus samples, through
#   a MonteCarlo procedure, the n-box Young diagrams with the measure given by the paths
#   in the graph.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import cm

#plt.rcParams["figure.figsize"] = [6,6]

"""
#Ns = np.array( (1e3,1e4,1e5), dtype=np.int_ )
Ns = np.array( (1e6,), dtype=np.int_ )
rep_num = 1000

cols = cm.get_cmap('magma', len(Ns)+1)
"""
instring = input("").split(' ')

# system size
N = int( instring[0] )
rep_num = int( instring[1] )


#  ---------------------------------------  corner plot  ---------------------------------------  #

def reshape(s,N):
    s2 = np.zeros(2*N+1)
    
    s2[0] = N
    s2[1::2] = s
    s2[2::2] = s
  
    return s2
        
"""
for iN in range(len(Ns)):
    N = Ns[iN]
    
    filename = "Results/MC_N%d_av%d.txt" % (N,rep_num)
    shape = np.loadtxt(filename)
    
    
    #  -----  real staircase  -----  #
    shape = reshape(shape,N)
    y = np.zeros(2*N+1)
    y[::2] = np.arange(N+1)
    y[1::2] = np.arange(N)
    
    plt.plot(-shape/np.sqrt(N), -y/np.sqrt(N), '-', c=cols(iN), label=r"$N=%d$"%N)
    
    #  -----  non-orthogonal staircase  -----  #
    #plt.plot(-shape/np.sqrt(N), -np.arange(N)/np.sqrt(N), '-', c=cols(iN), label=r"$N=%d$"%N)
    
    
    #  -----  only non-trivial part  -----  #
    #shape = shape[shape>0]
    #plt.plot(-shape/np.sqrt(N), -np.arange(len(shape))/np.sqrt(N), '-', c=cols(iN), label=r"$N=%d$"%N)


a = np.linspace(-2,2,100)
b = 2/np.pi * ( a*np.arcsin(0.5*a) + np.sqrt(4 - a**2) )

x = 0.5*(b+a)
y = 0.5*(b-a)

plt.plot(-x, -y, '--', c='darkgreen', label="Okounkov")


#plt.xlim((-2*np.sqrt(2),0))
#plt.ylim((-2*np.sqrt(2),0))

plt.xlabel(r"$x / \sqrt{N}$")
plt.ylabel(r"$y / \sqrt{N}$")

#plt.title(r"$10^{%d}$ boxes removed; $10^{%d}$ instances averaged" % (np.log10(N), np.log10(rep_num)) )

plt.legend(loc="lower left")
plt.show()

"""

#  -------------------------------------  horizontal plot  -------------------------------------  #


@nb.vectorize
def Okounkov(x):
    if x < -2:
        return -x
    elif x > 2:
        return x
    else:
        return 2/np.pi * ( x*np.arcsin(0.5*x) + np.sqrt(4 - x**2) )

@nb.njit
def MC(N):
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


for iN in range(len(Ns)):
    N = Ns[iN]
        
    #filename = "Results/MC_N%d_av%d.txt" % (N,rep_num)
    #shape = np.loadtxt(filename)
    
    x = np.linspace(-3,3,min(N,1000))
    shape = np.zeros(min(N,1000))
    
    a = np.zeros(2*N+1)
    a[::2] = np.arange(N+1)
    a[1::2] = np.arange(N)
    a /= np.sqrt(N)
        
    for rep in range(rep_num):
        temp = MC(N)
        
        temp = reshape(temp,N) / np.sqrt(N)
                
        f = interp1d(temp-a, temp+a)
        
        shape += f(x)
        
    shape /= rep_num 

    #yO = Okounkov(x)
    
    #plt.plot(x, shape, '-', c=cols(iN), label=r"$N=10^{%d}$"%np.log10(N))

    filename = "Results/MC_N%d_av%d.txt" % (N,rep_num)
    np.savetxt(filename, np.stack((x,shape)).T, header="x y")

"""
xO = np.linspace(-3,3,100)
yO = Okounkov(xO)
plt.plot(xO, yO, '--', c='darkgreen', label="Okounkov")

plt.plot((-2,2), (2,2), '.', c='darkgreen')

plt.xlim((-3,3))
plt.ylim((-1,4))
#plt.ylim((-1,1))

#plt.xlim((-10/np.sqrt(2),10/np.sqrt(2)))
#plt.ylim((0,20/np.sqrt(2)))

plt.legend(loc="lower left")
plt.show()

"""














