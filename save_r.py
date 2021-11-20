#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the average r parameter from the Results/spec\_{...} files,
#   saving it in Analysis/.
#
#  ---------------------------------------------------------------------------------------------  #


import numpy as np

instring = input("").split(' ')

# system size
N = int( instring[0] )

# disorder
eps = float( instring[1] )

# number of disorder instances
dis_num = int( instring[2] )

sparse = False

#  ---------------------------------------  load & save  ---------------------------------------  #



try:
    r_av = 0.
    
    for dis in range(dis_num):
        filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        data = np.loadtxt(filename)[:-2,0] 
        
        # if full, take the center of the spectrum
        if not sparse:
            data = data[3*len(data)//10:7*len(data)//10]
                        
        diff = np.diff(data)
        rs = np.minimum(diff[:-1], diff[1:]) / np.maximum(diff[:-1], diff[1:])
        
        r_av += np.average(rs)
        
    r_av /= dis_num
    
    fOut = open("Analysis/rAv_d%d.txt" % dis_num, 'a')
    fOut.write("%d %e %e\n" % (N, eps, r_av))
    fOut.close()
    
    print("Done N%d e%f" % (N, eps))   

except:
    print("Error at N%d e%f" % (N, eps))   

