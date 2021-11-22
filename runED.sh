Nmin=22
Nmax=22
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
    $(
    echo $N $dis_num_in $dis_num_fin | python3 buildDiagHam.py 1>>log 2>>err
  
    for eps in $(seq $epsMin $dEps $epsMax);
    do
        if [[ ! -f stop ]];
        then
            #echo $N $eps $dis_num_in $dis_num_fin $overwrite $nProc | python3 spectrum.py 1>>log 2>>err
            echo $N $eps $eig_frac $dis_num_in $dis_num_fin $overwrite $nProc | python3 spectrum_sparse.py 1>>log 2>>err
        
            #echo $N $eps $Tfin $dt $save_dt $dis_num_in $dis_num_fin | python3 tEv.py #1>>log.txt 2>>err.txt
        
            #echo $N $eps $dis_num_fin | python3 plot_y0.py
        fi
    done
    )&
done


#echo $N $eps $dis_num | python3 plot_mag_2d.py