Nmin=10
Nmax=10
dN=2

epsMin=2
epsMax=2
dEps=1

Tfin=10
dt=0.5
save_dt=0.5

eig_frac=20

dis_num_in=0
dis_num_fin=1

overwrite=1
nProc=8

for N in $(seq $Nmin $dN $Nmax);
do    
    #(
    echo $N $dis_num_in $dis_num_fin | python3 buildDiagHam.py 1>>log 2>>err
  
    for eps in $(seq $epsMin $dEps $epsMax);
    do
        if [[ ! -f stop ]];
        then
            #python3 spectrum.py $N $eps $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            #python3 spectrum_sparse.py $N $eps $eig_frac $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
        
            python3 tEv.py $N $eps $Tfin $dt $save_dt $dis_num_in $dis_num_fin #1>>log.txt 2>>err.txt
        
        fi
    done
    #)&
done


