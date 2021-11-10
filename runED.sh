Nmin=24
Nmax=30
dN=2

epsMin=1
epsMax=1
dEps=1

Tfin=10
dt=0.5
save_dt=0.5

eig_frac=10

dis_num_in=0
dis_num_fin=200

overwrite=1

for N in $(seq $Nmin $dN $Nmax);
do
    $(
    for eps in $(seq $epsMin $dEps $epsMax);
    do
        echo $N $dis_num_in $dis_num_fin | python3 buildDiagHam.py #1>>log.txt 2>>err.txt
    
        #echo $N $eps $eig_frac $dis_num_in $dis_num_fin $overwrite | python3 spectrum.py #1>>log.txt 2>>err.txt
        
        #echo $N $eps $Tfin $dt $save_dt $dis_num_in $dis_num_fin | python3 tEv.py #1>>log.txt 2>>err.txt
        
        #echo $N $eps $dis_num_fin | python3 plot_y0.py
    done
    )&
done


#echo $N | python3 buildHam.py
#echo $N $eps $dis_num | python3 plot_mag_2d.py