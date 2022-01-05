#  ---------------------------------------------------------------------------------------------  #
#
#   The program sorts the r parameter files in Analysis for later convenience.
#
#  ---------------------------------------------------------------------------------------------  #


import numpy as np

#  -------------------------------------------  load  ------------------------------------------  #

filename = "Analysis/KL.txt"

data = np.loadtxt(filename).T
data = np.flip(data, axis=0)

ordr = np.lexsort(data)

f = open(filename, 'w')
for i in range(len(ordr)):
    f.write("%d %f %e %d\n" % (data[3,ordr[i]], data[2,ordr[i]], data[1,ordr[i]], data[0,ordr[i]]))
    #print("%d %f %e" % (data[2,ordr[i]], data[1,ordr[i]], data[0,ordr[i]]))

f.close()
#data = np.take_along_axis(data, ordr, axis=0)









