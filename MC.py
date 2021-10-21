#  ---------------------------------------------------------------------------------------------  #
#
#   The program samples Young diagrams by successively adding/removing boxes. The probability
#   of adding a box is pForw, therefore of removing one is 1-pForw.
#
#  ---------------------------------------------------------------------------------------------  #

import numpy as np
import numba as nb

instring = input("").split(' ')

# system size
N = int( float(instring[0]) )

# probability to add a box
pForw = float( instring[1] )

# average over disorder
rep_num = int( instring[2] )


#  -----------------------------------  MonteCarlo procedure  ----------------------------------  #

@nb.njit
def MC(N,p):
    shape = np.zeros(N, dtype=np.int_)
    shape[0] = 1
    
    c = 1
    max_row = 2
    while c<N:
        #coin = rng.random()
        coin = np.random.random()
        
        # add a box
        if coin < pForw:
            row = np.random.randint(max_row)
            #row = rng.integers(max_row)
        
            if row==0 or shape[row-1]>shape[row]:
                shape[row] += 1
                c += 1
            
                if row == max_row-1:
                    max_row += 1
        
        # remove a box
        else:
            row = np.random.randint(max_row)
            #row = rng.integers(max_row)
            
            if shape[row+1]<shape[row]:
                shape[row] -= 1
                c += 1
            
                if shape[row] == 0:
                    max_row -= 1
    
    return shape


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

from matplotlib import pyplot as plt

av_V_shape = np.zeros(2*N+1)

for rep in range(rep_num):
    corner_shape = MC(N,pForw)
    corner_shape = reshape(corner_shape,N)
    
    # 45 deg rotation
    av_V_shape += (corner_shape[0] + corner_shape[1]) / np.sqrt(2)
    
av_V_shape /= rep_num 


#  -------------------------------------------  save  ------------------------------------------  #

x = np.arange(-N,N+1) / np.sqrt(2*N)
y = av_V_shape / np.sqrt(N)

filename = "Results/MC_N%d_p%.4f_av%d.txt" % (N,pForw,rep_num)
np.savetxt(filename, np.stack((x,y)).T, header="x y")














