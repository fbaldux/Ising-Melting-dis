#  ---------------------------------------------------------------------------------------------  #
#
#   The program averages the data in the Results/spec\_{...} files, saving them to Analysis/
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


#  -------------------------------------------  load  ------------------------------------------  #

PE = 0
dis_num_true = dis_num

for dis in range(dis_num):
    
    try:
        #filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,eps,dis)
        filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        data = np.loadtxt(filename)[:,3]
    
        eig_num = len(data)
    
        if frac != 1:
            start = eig_num//2 - int(0.5*frac*eig_num)
            stop = eig_num//2 + int(0.5*frac*eig_num)        
            data = data[start:stop]
        
        data = data[(~np.isnan(data)) & (data<np.inf)]
        
        PE += np.average(data)
    
    except:
        sys.stderr.write("Error at " + filename + "\n")
        dis_num_true -= 1
        
PE /= dis_num_true


#  -------------------------------------------  save  ------------------------------------------  #

fOut = open("Analysis/PE.txt", 'a')
fOut.write("%d %f %e %d\n" % (N, eps, PE, dis_num_true))
fOut.close()

print("END", ' '.join(sys.argv))   
   

