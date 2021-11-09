Nmin=12
Nmax=22
dN=2

epsMin=0.5
epsMax=6.0
dEps=0.5

Tfin=100
dt=0.5
save_dt=10

eig_frac=5

dis_num=5000

for N in $(seq $Nmin $dN $Nmax);
do
    for eps in $(seq $epsMin $dEps $epsMax);
    do
        echo $N $dis_num | python3 buildDiagHam.py
    
        echo $N $eps $eig_frac $dis_num | python3 spectrum.py
    done
done


#echo $N | python3 buildHam.py
#echo $N $eps $Tfin $dt $save_dt $dis_num | python3 tEv.py
#echo $N $eps $dis_num | python3 plot_mag_2d.py