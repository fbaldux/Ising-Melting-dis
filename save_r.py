import numpy as np

instring = input("").split(' ')

# system size
N = int( instring[0] )

# disorder
epsilon = float( instring[1] )

# number of disorder instances
dis_num = int( instring[2] )

sparse = False

#  ---------------------------------------  load & save  ---------------------------------------  #


for iN in range(len(Ns)):
    N = Ns[iN]
    
    for ie in range(len(epsilon)):
        e = epsilon[ie]
        
        try:
            r_av = 0.
            
            for dis in range(dis_num):
                filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,e,dis)
                data = np.loadtxt(filename)[:-2,0] 
                
                # if full, take the center of the spectrum
                if not sparse:
                    data = data[3*len(data)//10:7*len(data)//10]
                                
                diff = np.diff(data)
                rs = np.minimum(diff[:-1], diff[1:]) / np.maximum(diff[:-1], diff[1:])
                
                r_av += np.average(rs)
                
            r_av /= dis_num
            
            fOut = open("Analysis/rAv_d%d.txt" % dis_num, 'a')
            fOut.write("%d %e %e\n" % (Ns[iN], epsilon[ie], r_av))
            fOut.close()
        
        except:
            print("Error at N%d e%f" % (Ns[iN], epsilon[ie]))   

