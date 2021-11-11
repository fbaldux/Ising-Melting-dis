
import numpy as np


Ns = np.arange(12,20,2)
#Ns = np.array((12,))

epsilon = np.arange(1,6.5,1)
#epsilon = np.array((1.0,))


dis_num = 1000

p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))

dim = np.cumsum(p)


#  -------------------------------------------  load  ------------------------------------------  #


fOut = open("Analysis/rAv_%d.txt" % dis_num, 'a')

r_av = np.zeros((len(Ns),len(epsilon)))

for iN in range(len(Ns)):
    N = Ns[iN]
    
    for ie in range(len(epsilon)):
        e = epsilon[ie]
        
        try:
            # load all the r parameters
            filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,e,0)
            data = np.loadtxt(filename)[:-2,2]
            rs = np.zeros((dis_num,len(data)))
            del data
            
            for dis in range(dis_num):
                filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,e,dis)
                rs[dis] = np.loadtxt(filename)[:-2,2] 
    
            # take only the center of the spectrum?
            r_av[iN,ie] = np.average(rs)
            
            fOut.write("%d %e %e\n" % (Ns[iN], epsilon[ie], r_av[iN,ie]))
        
        except:
            print("Error at N%d e%f" % (Ns[iN], epsilon[ie]))
            #None


#  -------------------------------------------  save  ------------------------------------------  #

"""

for iN in range(len(Ns)):
    for ie in range(len(epsilon)):
        if r_av[iN,ie] > 0:
"""         

fOut.close()









