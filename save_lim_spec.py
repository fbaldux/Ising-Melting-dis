#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the minimum, center and maximum of the spectrum. 
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



#  ---------------------------------------  load & save  ---------------------------------------  #

min_av = 0.
min_std = 0.
mid_av = 0.
mid_std = 0.
max_av = 0.
max_std = 0.

dis_num_true = dis_num

for dis in range(dis_num):
    
    try:
        #filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,eps,dis)
        filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        data = np.loadtxt(filename)[:,0] 
    
        min_av += data[0]
        min_std += data[0]**2
        
        mid_av += data[len(data)//2]
        mid_std += data[len(data)//2]**2
        
        max_av += data[-1]
        max_std += data[-1]**2
    
    except:
        sys.stderr.write("Error at " + filename + "\n")
        dis_num_true -= 1
        
min_av /= dis_num_true
min_std /= dis_num_true
mid_av /= dis_num_true
mid_std /= dis_num_true
max_av /= dis_num_true
max_std /= dis_num_true

min_std = np.sqrt(min_std - min_av**2)
mid_std = np.sqrt(mid_std - mid_av**2)
max_std = np.sqrt(max_std - max_av**2)

fOut = open("Analysis/lim_spec.txt", 'a')
fOut.write("%d %f %e %e %e %e %e %e %d\n" % (N,eps, min_av,min_std, mid_av,mid_std, max_av,max_std, dis_num_true))
fOut.close()

print("END", ' '.join(sys.argv))   
   

