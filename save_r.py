import numpy as np

Ns = np.arange(12,22,2)
#Ns = np.array((12,))

epsilon = np.arange(1,15,1)
#epsilon = np.array((1.0,))

dis_num = 5000

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
                
                if sparse:
                    r_av += np.average(data)
                else:
                    r_av += np.average(data[3*len(data)//10:7*len(data)//10])
            
            r_av /= dis_num
            
            fOut = open("Analysis/rAv_d%d.txt" % dis_num, 'a')
            fOut.write("%d %e %e\n" % (Ns[iN], epsilon[ie], r_av[iN,ie]))
            fOut.close()
        
        except:
            print("Error at N%d e%f" % (Ns[iN], epsilon[ie]))   

