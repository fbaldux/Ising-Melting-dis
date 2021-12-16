#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the average r parameter from the Results/spec\_{...} files,
#   saving it in Analysis/.
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np

# system size
N = int( sys.argv[1] )

# disorder
eps = float( sys.argv[2] )

# number of disorder instances
dis_num = int( sys.argv[3] )

# fraction of the spectrum to consider
frac = float( sys.argv[4] )


#  ---------------------------------------  load & save  ---------------------------------------  #

r_av = 0.

for dis in range(dis_num):
    #filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,eps,dis)
    filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
    data = np.loadtxt(filename)[:,0] 
    
    eig_num = len(data)
    pos0 = np.where(data>0)[0][0]
    
    start = max(pos0 - int(0.5*frac*eig_num), 0)
    stop = pos0 + int(0.5*frac*eig_num)
    data = data[start:stop]
                    
    diff = np.diff(data)
    rs = np.minimum(diff[:-1], diff[1:]) / np.maximum(diff[:-1], diff[1:])
    
    r_av += np.average(rs)
    
r_av /= dis_num

fOut = open("Analysis/rAv0_d%d.txt" % dis_num, 'a')
fOut.write("%d %f %e\n" % (N, eps, r_av))
fOut.close()

print("Done N%d e%f" % (N, eps))   



