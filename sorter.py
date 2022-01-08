#  ---------------------------------------------------------------------------------------------  #
#
#   The program sorts the r parameter files in Analysis for later convenience.
#
#  ---------------------------------------------------------------------------------------------  #


import numpy as np

#  -------------------------------------------  load  ------------------------------------------  #

filename = "Analysis2/IPR.txt"

data = np.loadtxt(filename).T
data = np.flip(data, axis=0)

ordr = np.lexsort(data)
data_len = len(data)

f = open(filename, 'w')
for i in range(len(ordr)):
    temp =  "%d %f " % (data[-1,ordr[i]], data[-2,ordr[i]])
    temp += ("%e "*(data_len-3)) % tuple([data[k,ordr[i]] for k in range(data_len-3,0,-1)])
    temp += "%d\n" % data[0,ordr[i]]
    f.write(temp)
    
    #f.write("%d %f %e %d\n" % (data[3,ordr[i]], data[2,ordr[i]], data[1,ordr[i]], data[0,ordr[i]]))
    #print("%d %f %e" % (data[2,ordr[i]], data[1,ordr[i]], data[0,ordr[i]]))

f.close()
#data = np.take_along_axis(data, ordr, axis=0)









