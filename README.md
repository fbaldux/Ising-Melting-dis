# Ising-Melting

Melting of "solid" initial condition in 2d disordered quantum Ising model.


## average\_ev.py

The program averages the output of `tEv.py` from Results/ to Averages/


## buildAdj.py

The program builds the adjacency matrix of the partitions graph as follows:

- It generates all partitions of n and n+1 w/ the accelerated ruleAsc algorithm 
- It runs through both arrays and finds what couples are at a "single square" distance
- It saves the sparse adjacency matrix entry by entry (i.e. row indices and column indices that are non-zero).

The program uses Numba to speed up calculations.  
The row indices and column indices are saved to a .txt file for each level.


## buildDiagHam.py

The program builds the diagonal part of the Hamiltonian for the partitions graph. It proceeds as follows:

- It generates all partitions of n w/ the accelerated ruleAsc algorithm 
- It extracts a NxN grid of disordered on-site energies for the 2d model
- For each partition, it sums the disordered energies contained in the shape

The program uses Numba to speed up calculations.  
The matrix elements are saved to a .txt file.


## empty.sh

The shell removes empty files (coming from failed jobs).


## ground\_state.py

The program computes the average and standard deviation for the GS energy. It loads the files from the Results/spec\_{...} and saves to Analysis/.


## LanczosRoutines.py

Program nicely given us from Vittorio Vitale & Alessadro Santini. It contains the Lanczos algorithm for matrix exponentiation with Krylov subspaces.
NOTE: performs worse than scipy.sparse!


## masterMissing{1,2}.sh

Shell to send multiple jobs on Ulysses, on partition regular {1,2}, to fill voids (i.e. jobs that haven't delivered the final output). It modifies and executes `runMissing{1,2}.py` and `runMissing{1,2}-ctrl.py`.


## masterUlysses{1,2}.sh

Shell to send multiple jobs on Ulysses, on partition regular {1,2}. It modifies and executes `runUlysses{1,2}.py`.


## min\_potential.sh

The program computes the average and standard deviation for the minimum of the potential. 
It loads the files from the Results/spec\_{...} and saves to Analysis/.


## mover.sh

Shell to reorganize folders of results.


## partitions.py

The program contains routines for building the Young diagrams.


## plot\_{...}.py

Just to plot results.


## runED.sh

Shell to run jobs on workstations.


## runSave.sh

Shell to run `save_r.py` or `average_ev.py` on Ulysses.


## runMissing{1,2}.sh

Shell to run the single job on Ulysses, partition regular {1,2}, to fill voids (i.e. jobs that haven't delivered the final output).


## runMissing{1,2}-ctrl.sh

Shell to help the correct functioning of `runMissing{1,2}.sh`.


## runUlysses{1,2}.sh

Shell to run the single job on Ulysses, partition regular {1,2}.


## save\_r.py

The program computes the average r parameter around the center of the spectrum.  
It loads the Results/spec\_{...} files, and saves to Analysis/


## save\_r0.py

The program computes the average r parameter around the energy E=0.  
It loads the Results/spec\_{...} files, and saves to Analysis/


## sorter.py

The program sorts the r parameter files in Analysis for later convenience.


## spectrum.py

The program diagonalizes the disordered, Young graph Hamiltonian.

- It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
- It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
- It builds the sparse Hamiltonian from the entries, and converts it to a full matrix.
- It saves to Results/spec_{...} the
    - eigenvalues
    - IPR
    - Kullback-Leibler divergence of neighbouring eigenstates
    - participation entropy of the eigenstates (in the graph basis)
- It saves to Results/magDiff_{...} the magnetization difference of neighbouring eigenstates, for each site of the 2d Ising model.
- It optionally saves the eigenvectors, but it takes a HUGE amount of space.


## spectrum\_sparse.py

The program diagonalizes the disordered, Young graph Hamiltonian.

- It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
- It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
- It builds the sparse Hamiltonian from the entries.
- It saves to Results/spec_{...} a fraction, at the center of the spectrum, of the
    - eigenvalues
    - IPR
    - Kullback-Leibler divergence of neighbouring eigenstates
    - participation entropy of the eigenstates (in the graph basis)
- It saves to Results/magDiff_{...} the magnetization difference of neighbouring eigenstates, for each site of the 2d Ising model.
- It optionally saves the eigenvectors, but it takes a HUGE amount of space.


## tEv.py

The program evolves a state on the Young diagram lattice.

- It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
- It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
- It builds the sparse Hamiltonian from the entries.
- It evolves an initial state via full exponentiation or sparse Pade' (expm_multiply).
- It saves to Results/ the linear dimensions of the state and the area.
- It saves to States/ the final state reached.


## tEv\_log.py

The program evolves a state on the Young diagram lattice.

- It loads the non-zero entries of the adjacency matrix from the Hamiltonian/clean_N#.txt files.
- It loads the diagonal entries of the Hamiltonian matrix from the files Hamiltonian/rand...
- It builds the sparse Hamiltonian from the entries.
- It evolves an initial state via full exponentiation or sparse Pade' (expm_multiply).
- It saves to Results/ the linear dimensions of the state and the area.
- It saves to States/ the final state reached.
- It is suited for time evolution in log scale (the dt is progressively increased).


## time_fit.py

Just to estimate how long computing times become.

