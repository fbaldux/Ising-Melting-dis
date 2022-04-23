#  ---------------------------------------------------------------------------------------------  #
#
#   The program computes the histogram of the average DOS (normalized from -1 to 1), and the 
#   histogram of the positions of the max and min eigenvalue.
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

# number of bins for the histogram
N_bins = int( sys.argv[4] )


#  -------------------------------------------  load  ------------------------------------------  #

allmins = []
allmaxs = []
allratios = []
allspecs = []
dis_num_true = dis_num

for dis in range(dis_num):
    
    try:
        #filename = "OldGood/Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        filename = "Results_N%d_e%.0f/spec_N%d_e%.4f_d%d.txt" % (N,eps,N,eps,dis)
        #filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N,eps,dis)
        
        spec = np.loadtxt(filename)[:,0] 
        
        # save max and min
        allmins.append(spec[0])
        allmaxs.append(spec[-1])
        allratios.append( np.abs(spec[-1])/(np.abs(spec[-1])+np.abs(spec[0])) )

        # save normalized spectrum
        spec = (spec - spec[0]) / (spec[-1] - spec[0]) * 2 - 1
        allspecs.append(spec)

    except:
        dis_num_true -= 1
    


#  -----------------------------------------  save DOS  ----------------------------------------  #

histo,bins = np.histogram(np.array(allspecs), bins=N_bins, density=True)
bins = 0.5 * ( bins[1:] + bins[:-1] )

filename = "Analysis/DOS_N%d_e%.4f_av%d.txt" % (N,eps,dis_num)
head = "dis.true=%d\nbins histo" % dis_num_true
np.savetxt(filename, np.stack((bins,histo)).T, header=head)


#  -----------------------------------------  save min  ----------------------------------------  #

histo,bins = np.histogram(np.array(allmins), bins=N_bins, density=True)
bins = 0.5 * ( bins[1:] + bins[:-1] )

filename = "Analysis/histoMin_N%d_e%.4f_av%d.txt" % (N,eps,dis_num)
head = "dis.true=%d\nbins histo" % dis_num_true
np.savetxt(filename, np.stack((bins,histo)).T, header=head)


#  -----------------------------------------  save max  ----------------------------------------  #

histo,bins = np.histogram(np.array(allmaxs), bins=N_bins, density=True)
bins = 0.5 * ( bins[1:] + bins[:-1] )

filename = "Analysis/histoMax_N%d_e%.4f_av%d.txt" % (N,eps,dis_num)
head = "dis.true=%d\nbins histo" % dis_num_true
np.savetxt(filename, np.stack((bins,histo)).T, header=head)


#  ---------------------------------------  save ratios  ---------------------------------------  #

#allratios = np.array(allratios)
#allratios = allratios[allratios>0]
#histo,bins = np.histogram(np.log(allratios), bins=N_bins, density=True)
histo,bins = np.histogram(allratios, bins=N_bins, density=True)
bins = 0.5 * ( bins[1:] + bins[:-1] )

filename = "Analysis/histoRatios_N%d_e%.4f_av%d.txt" % (N,eps,dis_num)
head = "dis.true=%d\nbins histo" % dis_num_true
np.savetxt(filename, np.stack((bins,histo)).T, header=head)

print("END", ' '.join(sys.argv))

















