#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the average r parameter around the center of the spectrum. 
#   It loads the Results/spec\_{...} files, and saves to Analysis/
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
np.seterr(all='raise')

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
dis_num_true = dis_num

for dis in range(dis_num):
    
    try:
        #filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,eps,dis)
        filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        data = np.loadtxt(filename)[:,0] 
    
        eig_num = len(data)
    
        if frac != 1:
            start = eig_num//2 - int(0.5*frac*eig_num)
            stop = eig_num//2 + int(0.5*frac*eig_num)        
            data = data[start:stop]
                    
        diff = np.diff(data)
        rs = np.minimum(diff[:-1], diff[1:]) / np.maximum(diff[:-1], diff[1:])
    
        r_av += np.average(rs)
    
    except:
        sys.stderr.write("Error at " + filename + "\n")
        dis_num_true -= 1
        
r_av /= dis_num_true

fOut = open("Analysis/rAv.txt", 'a')
fOut.write("%d %f %e %d\n" % (N, eps, r_av, dis_num_true))
fOut.close()

print("END", ' '.join(sys.argv))   
   

