#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np

N = int( sys.argv[1] )
epsilon = float( sys.argv[2] )
T = float( sys.argv[3] )
dis_num = int( sys.argv[4] )


#  -------------------------------------------  load  ------------------------------------------  #

filename = "Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,epsilon,T,0)
data = np.loadtxt(filename).T

for dis in range(1,dis_num):

    #  load the results
    filename = "Results/tEv_N%d_e%.4f_T%.1f_d%d.txt" % (N,epsilon,T,dis)
    data[1:] += np.loadtxt(filename)[:,1:].T
    
data[1:] /= dis_num


#  -------------------------------------------  plot  ------------------------------------------  #

fIn = open(filename, 'r')
head = fIn.readline()[2:-1]
fIn.close()


filename = "Averages/tEv_N%d_e%.4f_T%.1f_av%d.txt" % (N,epsilon,T,dis_num)
np.savetxt(filename, data.T, header=head)



