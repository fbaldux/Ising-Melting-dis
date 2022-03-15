#  ---------------------------------------------------------------------------------------------  #
#   ...
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np

N = int( sys.argv[1] )
epsilon = float( sys.argv[2] )
init_state = int( sys.argv[3] )
Tfin = float( sys.argv[4] )
dis_num = int( sys.argv[5] )


#  -------------------------------------------  load  ------------------------------------------  #

filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,Tfin,0)
data = np.loadtxt(filename).T
data2 = np.copy(data)
data2[1:] = data2[1:]**2

fIn = open(filename, 'r')
head = fIn.readline()[2:-1]
fIn.close()

dis_num_true = dis_num
for dis in range(1,dis_num):

    # load the results
    try:
        filename = "Results/tEv_N%d_e%.4f_s%d_T%.1f_d%d.txt" % (N,epsilon,init_state,Tfin,dis)
        new = np.loadtxt(filename)[:,1:].T
        data[1:] += new
        data2[1:] += new**2
    
    except:
        sys.stderr.write("Error at " + filename + "\n")
        dis_num_true -= 1


data[1:] /= dis_num_true
data2[1:] /= dis_num_true
data2[1:] = np.sqrt( data2[1:] - data[1:]**2 ) 

#  -------------------------------------------  plot  ------------------------------------------  #


head += "; dis_true = %d" % dis_num_true

filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_av%d.txt" % (N,epsilon,init_state,Tfin,dis_num)
np.savetxt(filename, data.T, header=head)

filename = "Averages/tEv_N%d_e%.4f_s%d_T%.1f_std%d.txt" % (N,epsilon,init_state,Tfin,dis_num)
np.savetxt(filename, data2.T, header=head)

print("END " + ' '.join(sys.argv))
