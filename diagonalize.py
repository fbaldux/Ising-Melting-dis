import numpy as np
rng = np.random.default_rng()
import numba as nb
from scipy import sparse
from scipy.linalg import eigh,expm
from scipy.sparse.linalg import eigsh
from matplotlib import pyplot as plt
from matplotlib import cm


plt.rcParams["figure.figsize"] = [6,6]

fig, ax = plt.subplots()


instring = input("").split(' ')

# system size
N = int( instring[0] )

# number of disorder instances
dis_num = int( instring[1] )

epsilon = float( instring[2] )


p = np.array((1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77, 101, 135, 176, 231, 297, 385, 490, 627, \
     792, 1002, 1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842, 8349, 10143, 12310, 14883, 17977,\
     21637, 26015, 31185, 37338, 44583, 53174, 63261, 75175, 89134, 105558, 124754, 147273, 173525))


dim = np.cumsum(p)
Ham_lens = np.loadtxt("ham_lengths.txt", dtype=np.int_).T
try:
    my_len = Ham_lens[1,Ham_lens[0]==N][0]
except:
    print("\nError! Hamiltonian for N=%d not built\n" % N)
    exit(0)

filename = "Hamiltonians/clean_N33.txt"
row_ind, col_ind = np.loadtxt(filename)[:my_len].T

# load the adjacency matrix

H0 = sparse.csr_matrix((np.ones(len(row_ind)), (row_ind, col_ind)), shape=(dim[N], dim[N]))
H0 += H0.T

Eps=np.zeros(len(np.arange(0.5, epsilon, 0.5)))
RPar=np.zeros(len(np.arange(0.5, epsilon, 0.5)))
j=0

# cicle over value of disorder and disorder realizations

for eps in np.arange(0.5, epsilon, 0.5):
    R = np.zeros(dis_num)
    for dis in range(dis_num):


        # load the disorder hamiltonian
        filename = "Hamiltonians/rand_N%d_d%d.txt" % (N,dis)
        diag = np.loadtxt(filename)
        H = H0 + eps * sparse.diags(diag)
        H= H.todense()
        #N = 1000

        # diagonalize the matrix
        #H = rng.normal(0,1,size=(N,N))
        eigvals, eigvecs = eigh(H)
        eigvecs = eigvecs.T
        # compute the IPR
        IPRs = np.sum(eigvecs**4, axis=1)

        # compute the r parameter
        diff = np.diff(eigvals)
        """
        r = np.zeros(len(diff)-1)
        for k in range(len(r)):
            r[k] = min(diff[k], diff[k+1]) / max(diff[k], diff[k+1])
        """
        i=0
        r = np.zeros(2*len(diff)//10)
        
        for k in range(4*len(diff)//10, 6*len(diff)//10-1):
            r[i] = min(diff[k], diff[k+1]) / max(diff[k], diff[k+1])
            i += 1

        R[dis] = np.average(r)

    Eps[j]=eps
    RPar[j]=np.average(R)
    j += 1

points_r=np.zeros((2,len(Eps)))
"""
ax.plot(Eps, RPar, '-', lw=0.5, c='black')
ax.set_xlabel("Epsilon")
ax.set_ylabel("r-param")

ax.set_title("n=%d" %(N))

ax.legend()
plt.show()
"""
#  save to file
filename = "Results/points_N%d.txt" % (N)
toSave = np.array((Eps, RPar)).T
head = "eps rpar"
np.savetxt(filename, toSave, header=head)

