#  ---------------------------------------------------------------------------------------------  #
#
#   The program sorts the r parameter files in Analysis for later convenience.
#
#  ---------------------------------------------------------------------------------------------  #


import numpy as np

#  -------------------------------------------  load  ------------------------------------------  #

#filename = "Analysis/rAv_d960.txt"
#filename = "Analysis/GS_d2000.txt"
filename = "Analysis/a.txt"

data = np.loadtxt(filename).T
data = np.flip(data, axis=0)

ordr = np.lexsort(data)

for i in range(len(ordr)):
    print("%d %f %e %d" % (data[3,ordr[i]], data[2,ordr[i]], data[1,ordr[i]], data[0,ordr[i]]))
    #print("%d %f %e" % (data[2,ordr[i]], data[1,ordr[i]], data[0,ordr[i]]))

#data = np.take_along_axis(data, ordr, axis=0)









