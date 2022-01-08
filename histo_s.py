#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the histogram of the level spacing `s = E[n] - E[n-1]`  
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

# number of bins
N_bins = int( sys.argv[5] )

# value to cut histogram
s_max = 10


#  -------------------------------------------  load  ------------------------------------------  #

s = []

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
        s.extend(list(diff))
        
    except:
        sys.stderr.write("Error at " + filename + "\n")

s = np.array(s)

#  --------------------------------------  make histogram  -------------------------------------  #

s /= np.average(s)
s = s[s<10]

histo,bins = np.histogram(s, bins=N_bins, density=True)
bins = 0.5 * ( bins[1:] + bins[:-1] )


#  -------------------------------------------  save  ------------------------------------------  #
     
filename = "Analysis/sHisto_N%d_e%.4f_d%d.txt" % (N,eps,dis_num)
head = "bins histo"
np.savetxt(filename, np.stack((bins,histo)).T, header=head)

print(' '.join(sys.argv))   
   



