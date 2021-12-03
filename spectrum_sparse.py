#  ---------------------------------------------------------------------------------------------  #
#
#   The program diagonalizes the disordered, Young graph Hamiltonian.
#
#   - It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
#   - It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
#   - It builds the sparse Hamiltonian from the entries.
#   - It saves to Results/spec_{...} a fraction, at the center of the spectrum, of the
#       - eigenvalues
#       - IPR
#       - Kullback-Leibler divergence of neighbouring eigenstates
#       - participation entropy of the eigenstates (in the graph basis)
#   - It saves to Results/magDiff_{...} the magnetization difference of neighbouring eigenstates, 
#     for each site of the 2d Ising model.
#   - It optionally saves the eigenvectors, but it takes a HUGE amount of space.
#
#  ---------------------------------------------------------------------------------------------  #

import sys, os

# system size
N = int( sys.argv[1] )

# disorder
epsilon = float( sys.argv[2] )

# number of eigenvalues (for sparse diagonalization)
#eig_frac = int( sys.argv[3] )
eig_num = int( sys.argv[3] )

# number of disorder instances
dis_num_in = int( sys.argv[4] )
dis_num_fin = int( sys.argv[5] )

# whether to overwrite existing files
overwrite = int( sys.argv[6] )

# number of processors to use
nProc = int( sys.argv[7] )


os.environ["MKL_NUM_THREADS"] = str(nProc)
os.environ["NUMEXPR_NUM_THREADS"] = str(nProc)
os.environ["OMP_NUM_THREADS"] = str(nProc)

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from partitions import *
from time import time

np.seterr(divide='ignore')

#eig_num = dim[N]//eig_frac
start = time()

#  ------------------------------------  load hopping terms  -----------------------------------  #

# from partitions.py
H0 = load_adjacency(N)


#  -------------------------------  build magnetization operator  ------------------------------  #

levels = [np.array(((0,),))]
for n in range(1,N+1):
    levels.append( np.array( [x for x in generate_partitions(n)] ) )

levels = tuple(levels)


# "magnetization" in the 2d plane: how much of the corner is removed
@nb.njit
def build_mag2d():
    
    M = np.zeros((N,N,dim[N]), dtype=np.float_)
    
    # sum over all basis states (split in n and i)
    for n in range(1,N+1):
        for i in range(p[n]):
            k = dim[n-1]+i
            
            # iterate over the rows of the Young diagrams
            r = 0
            while r<n and levels[n][i,r]>0:
                M[r,:levels[n][i,r],k] = 1
                r += 1
            
    return M

mag2d_op = build_mag2d()

# get rid of inaccessible spins in the NxN grid
M = np.einsum("xyi,i->xy", mag2d_op, np.ones(dim[N])).flatten()
mag2d_op = mag2d_op.reshape(N*N,dim[N])
mag2d_op = mag2d_op[M!=0]


#  -------------------------------------------  main  ------------------------------------------  #

for dis in range(dis_num_in,dis_num_fin):
    
    done = False
    if not overwrite and os.path.isfile("Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)):
        done = True
    
    if not done:
        # load the disorder
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        H = H0 + epsilon * sparse.diags(np.loadtxt(filename))
                
        # sparse
        center = np.sum(H.diagonal())
        eigvals, eigvecs = eigsh(H, k=eig_num, which='LM', sigma=center)
        eigvecs = eigvecs.T
        eigvecs2 = eigvecs**2
        del eigvecs, H
    
        # compute the IPR
        IPRs = np.sum(eigvecs2**2, axis=1)
        
        
        # compute the KL divergence of neighbouring states [w/ regularization 0*log(0) -> 0]
        # NOTE: if argLog==0/0 -> np.inf, the KL is not defined and the data will be ignored later on
        np.seterr(divide='ignore',invalid='ignore')
        KL = np.zeros(eig_num)
        argLog = eigvecs2[:-1]/eigvecs2[1:]
        argLog[argLog==0] = 1.
        KL[:-1] = np.einsum( "ab,ab->a", eigvecs2[:-1], np.log(argLog) )
        KL[-1] = -1.
        np.seterr(all='warn')
        
        
        # compute the participaton entropies [w/ regularization 0*log(0) -> 0]
        argLog = np.copy(eigvecs2)
        argLog[argLog==0] = 1.
        PE = - np.einsum( "ab,ab->a", eigvecs2, np.log(argLog) )
        
        
        # compute the magnetization difference in every site, for neighbouring states
        # NOTE: magDiff2 has dimension (# squares)x(eig_num-1)
        magDiff = np.einsum("xk,ik->xi", mag2d_op, eigvecs2)
        magDiff = 2 * np.abs(magDiff[:,1:] - magDiff[:,:1])
        
       
        # save to file
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        toSave = np.stack((eigvals, IPRs, KL, PE)).T
        head = "eigenvalue IPR KL PE"
        np.savetxt(filename, toSave, header=head)
        
        filename = "Results/magDiff_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "magDiff[site 0] magDiff[site 1] etc."
        np.savetxt(filename, magDiff.T, header=head)
        
        """
        filename = "Results/spec_N%d_e%.4f_d%d.txt" % (N, epsilon, dis)
        head = "eigval eigvec[0] eigvec[1] ..." 
        np.savetxt( filename, np.vstack((eigvals, eigvecs)).T, header=head )
        """

print("End spec N%d e%.4f d%d-%d" % (N,epsilon,dis_num_in,dis_num_fin))
#print(N, time()-start)





