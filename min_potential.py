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

# number of disorder instances
dis_num = int( sys.argv[2] )


#  ---------------------------------------  load & save  ---------------------------------------  #

try:
    
    minV_av = 0.
    minV2_av = 0.
    
    for dis in range(dis_num):
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        minV = np.min(np.loadtxt(filename))
        
        minV_av += minV
        minV2_av += minV**2

    minV_av /= dis_num
    minV2_av /= dis_num
    
    
    fOut = open("Analysis/minV_d%d.txt" % dis_num, 'a')
    fOut.write("%d %e %e\n" % (N, minV_av, np.sqrt(minV2_av-minV_av**2)))
    fOut.close()
    
    print("Done N%d" % (N))   

except:
    print("Error at N%d" % N)   

