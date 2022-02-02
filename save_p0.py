#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the typical p0 parameter.
#   It loads the Results/p0\_{...} files, and saves to Analysis/
#
#  ---------------------------------------------------------------------------------------------  #

import sys
import numpy as np
np.seterr(all='raise')

# system size
N = int( sys.argv[1] )

# disorder
eps = float( sys.argv[2] )


#  ---------------------------------------  load & save  ---------------------------------------  #

filename = "Results/p0_N%d_e%.4f.txt" % (N,eps)
#filename = "Results_N%d_e%.0f/p0_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
data = np.loadtxt(filename).T 

E_av = np.average(data[0])
E_std = np.sqrt( np.average(data[0]**2) )

N_av = np.average(data[1])

p0_typ = np.exp( np.average(np.log(data[2])) )

fOut = open("Analysis/p0_typ.txt", 'a')
fOut.write("%d %f %e %e %e %e %d\n" % (N, eps, E_av, E_std, N_av, p0_typ, len(data)))
fOut.close()

print(' '.join(sys.argv))   
   

