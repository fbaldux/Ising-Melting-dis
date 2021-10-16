# Thanks to Alessandro Santini: https://github.com/alessandro-santini/DMRG/blob/main/LanczosRoutines.py

import numpy as np
from scipy.linalg import eigh_tridiagonal
import warnings


def lanczos_iteration(Afunc, vstart, numiter):
    """Perform a "matrix free" Lanczos iteration.
    Args:
        Afunc:      "matrix free" linear transformation of a given vector
        vstart:     starting vector for iteration
        numiter:    number of iterations (should be much smaller than dimension of vstart)
    Returns:
        tuple: tuple containing
          - alpha:      diagonal real entries of Hessenberg matrix
          - beta:       off-diagonal real entries of Hessenberg matrix
          - V:          len(vstart) x numiter matrix containing the orthonormal Lanczos vectors
    """

    # normalize starting vector
    nrmv = np.linalg.norm(vstart)
    assert nrmv > 0
    vstart = vstart / nrmv

    alpha = np.zeros(numiter)
    beta  = np.zeros(numiter-1)

    V = np.zeros((numiter, len(vstart)), dtype=complex)
    V[0] = vstart

    for j in range(numiter-1):
        w = Afunc(V[j])
        alpha[j] = np.vdot(w, V[j]).real
        w -= alpha[j]*V[j] + (beta[j-1]*V[j-1] if j > 0 else 0)
        beta[j] = np.linalg.norm(w)
        
        if beta[j] < 100*len(vstart)*np.finfo(float).eps:
            warnings.warn(
                'beta[{}] ~= 0 encountered during Lanczos iteration.'.format(j),
                RuntimeWarning)
            # premature end of iteration
            numiter = j + 1
            return (alpha[:numiter], beta[:numiter-1], V[:numiter, :].T)
        V[j+1] = w / beta[j]
        
    j = numiter-1
    w = Afunc(V[j])
    alpha[j] = np.vdot(w, V[j]).real

    # complete final iteration
    return (alpha, beta, V.T)

def expm_krylov_lanczos(Afunc, v, dt, numiter=10): 
    """
    Compute Krylov subspace approximation of the matrix exponential
    applied to input vector: expm(dt*A)*v.
    Reference:
        M. Hochbruck and C. Lubich
        On Krylov subspace approximations to the matrix exponential operator
        SIAM J. Numer. Anal. 34, 1911 (1997)
    """

    alpha, beta, V = lanczos_iteration(Afunc, v, numiter)

    # diagonalize Hessenberg matrix
    w_hess, u_hess = eigh_tridiagonal(alpha, beta)

    return np.dot(V, np.dot(u_hess, np.linalg.norm(v) * np.exp(dt*w_hess) * u_hess[0]))

def optimize_lanczos(Afunc,v,numiter):
    alpha, beta, V = lanczos_iteration(Afunc, v, numiter)
    eig, w = eigh_tridiagonal(alpha, beta)
    return V@w[:,0], eig[0]

