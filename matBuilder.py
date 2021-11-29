#  ---------------------------------------------------------------------------------------------  #
#
#   This program builds the sparse matrices Sx[i],Sy[i],etc. of a spin chain of length L,
#   acting only on site i.
#
#  ---------------------------------------------------------------------------------------------  #


# program constants are defined already in the main


#  -------------------------------  construct the basic matrices  ------------------------------  #

sx = np.array( [[0,1],[1,0]], dtype=np.complex_ ) 
sy = np.array( [[0,-1j],[1j, 0]], dtype=np.complex_ ) 
sz = np.array( [[1,0],[0,-1]] ) 
sp = np.array( [[0,1],[0,0]] )
sm = np.array( [[0,0],[1,0]] )

sx_list = []; sy_list = []
sz_list = []
sp_list = []; sm_list = []

for i in range(L):

    if i==0:
        full_sx = sx; full_sy = sy
        full_sz = sz
        full_sp = sp; full_sm = sm
    else:
        full_sx = sparse.kron(sparse.identity(2**i), sx); full_sy = sparse.kron(sparse.identity(2**i), sy)
        full_sz = sparse.kron(sparse.identity(2**i), sz)
        full_sp = sparse.kron(sparse.identity(2**i), sp); full_sm = sparse.kron(sparse.identity(2**i), sm)

    if i!=L-1:
        full_sx = sparse.kron(full_sx, sparse.identity(2**(L-i-1))); full_sy = sparse.kron(full_sy, sparse.identity(2**(L-i-1)))
        full_sz = sparse.kron(full_sz, sparse.identity(2**(L-i-1)))
        full_sp = sparse.kron(full_sp, sparse.identity(2**(L-i-1))); full_sm = sparse.kron(full_sm, sparse.identity(2**(L-i-1)))

    sx_list.append( sparse.csr_matrix(full_sx) ); sy_list.append( sparse.csr_matrix(full_sy) )  
    sz_list.append( sparse.csr_matrix(full_sz) )  
    sp_list.append( sparse.csr_matrix(full_sp) ); sm_list.append( sparse.csr_matrix(full_sm) )

del full_sx, full_sy, full_sz, full_sp, full_sm






