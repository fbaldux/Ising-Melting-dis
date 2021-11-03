# Ising-Melting

Melting of "solid" initial condition in 2d quantum Ising model.


---
### buildAdj.py

The program builds the adjacency matrix of the partitions graph as follows:

1. It generates all partitions of n and n+1 w/ the accelerated ruleAsc algorithm 
2. It runs through both arrays and finds what couples are linked by a "hook move"
3. It saves the sparse adjacency matrix entry by entry (i.e. row indices and column indices that are non-zero).
4. In the meanwhile, it saves how many matrix elements are needed at each level n<N: in this way, all the Hamiltonians for smaller N can be loaded from the same file. 

- The program uses Numba to speed up calculations.
- The row indices and column indices are saved to a .txt file.


---
### buildDiagHam.py

The program builds the diagonal part of the Hamiltonian for the partitions graph. It proceeds as follows:

1. It generates all partitions of n w/ the accelerated ruleAsc algorithm 
2. It extracts a NxN grid of disordered on-site energies for the 2d model
3. For each partition, it sums the disordered energies contained in the shape

- The program uses Numba to speed up calculations.
- The matrix elements are saved to a .txt file.



---
### ham_lengths.txt

The file containing the number of non-zero entries of the sparse adjacency matrix, up to each level N. 


---
### LanczosRoutines.py

Program nicely given us from Vittorio Vitale & Alessadro Santini. It contains the Lanczos algorithm for matrix exponentiation with Krylov subspaces.


---
### MC.py

The program samples Young diagrams by successively adding/removing boxes. The probability of adding a box is pForw, therefore of removing one is 1-pForw.


---
### partitions.py

Various trials on the partition adjacency matrix


---
### plot\_{...}.py

Just to plot results.


---
### tEv.py

The program evolves a state on the Young diagram lattice.

- It loads the non-zero entries of the adjacency matrix from the biggest Hamiltonian/clean_N#.txt file.
- It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
- It builds sparse Hamiltonian from the entries.
- It evolves an initial state via Krylov (from LanczosRoutines.py).



---
### time_fit.py

Just to estimate how long computing times become.


---
### run??.sh

One shell to rule them all!