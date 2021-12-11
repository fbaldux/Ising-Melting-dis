#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the average and standard deviation for the GS energy. It loads the files
#   from the Results/spec\_{...} and saves to Analysis/.
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


#  ---------------------------------------  load & save  ---------------------------------------  #

try:
    GS_av = 0.
    GS2_av = 0.

    for dis in range(dis_num):
        filename = "OldGood/Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        #filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        #filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,eps,dis)
        
        f = open(filename, 'r')
        l = f.readline()
        l = f.readline().split(' ')
        f.close()

        E = float(l[0])
        #E = np.loadtxt(filename)[0,0] 

        GS_av += E
        GS2_av += E**2

    GS_av /= dis_num
    GS2_av /= dis_num
    
    
    fOut = open("Analysis/GS_d%d.txt" % dis_num, 'a')
    fOut.write("%d %e %e %e\n" % (N, eps, GS_av, np.sqrt(GS2_av-GS_av**2)))
    fOut.close()
    
    print("Done N%d e%f" % (N, eps))   

except:
    print("Error at N%d e%f" % (N, eps))   

