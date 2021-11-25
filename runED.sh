Nmin=18
Nmax=18
dN=2

epsMin=2
epsMax=2
dEps=1

Tfin=10
dt=0.5
save_dt=0.5

eig_frac=1846

dis_num_in=0
dis_num_fin=1

overwrite=1
nProc=7

for N in $(seq $Nmin $dN $Nmax);
do    
    #(
    python3 buildDiagHam.py $N $dis_num_in $dis_num_fin 1>>log 2>>err
  
    for eps in $(seq $epsMin $dEps $epsMax);
    do
        if [[ ! -f stop ]];
        then
            python3 spectrum.py $N $eps $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            #python3 spectrum_sparse.py $N $eps $eig_frac $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            
            #python3 tEv.py $N $eps $Tfin $dt $save_dt $dis_num_in $dis_num_fin #1>>log.txt 2>>err.txt
        
            echo
        fi
    done
    #)&
done


