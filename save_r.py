import numpy as np

Ns = np.arange(22,24,2)
#Ns = np.array((12,))

epsilon = np.arange(1,4,1)
#epsilon = np.array((1.0,))

dis_num = 1000


#  ---------------------------------------  load & save  ---------------------------------------  #

# full
#fOut = open("Analysis/rAv_%d_full.txt" % dis_num, 'a')
# center
fOut = open("Analysis/rAv_%d.txt" % dis_num, 'a')

r_av = np.zeros((len(Ns),len(epsilon)))

for iN in range(len(Ns)):
    N = Ns[iN]
    
    for ie in range(len(epsilon)):
        e = epsilon[ie]
        
        try:
            # load all the r parameters
            filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,e,0)
            data = np.loadtxt(filename)[:-2,2]
            
            # full
            #rs = np.zeros((dis_num,len(data)))
            # center
            frac = len(data)//5
            rs = np.zeros((dis_num,frac))     

            del data
            

            for dis in range(dis_num):
                filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,e,dis)
                
                # full
                #rs[dis] = np.loadtxt(filename)[:-2,2]
                # center
                data = np.loadtxt(filename)[:-2,2] 
                rs[dis] = data[3*len(data)//10:3*len(data)//10+frac]

            r_av[iN,ie] = np.average(rs)
            
            fOut.write("%d %e %e\n" % (Ns[iN], epsilon[ie], r_av[iN,ie]))
        
        except:
            print("Error at N%d e%f" % (Ns[iN], epsilon[ie]))
            #None   

fOut.close()