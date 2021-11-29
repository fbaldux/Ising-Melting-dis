
Tfin=200
dt=0.1
save_dt=2

eig_frac=1846

dis_num_in=0
dis_num_fin=1

overwrite=1
nProc=7

for N in $(seq 49 2 49);
do    
    #(
    #python3 buildDiagHam.py $N $dis_num_in $dis_num_fin 1>>log 2>>err
  
    for eps in $(seq 6 1 6);
    do
        if [[ ! -f stop ]];
        then
            #python3 spectrum.py $N $eps $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            #python3 spectrum_sparse.py $N $eps $eig_frac $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            
            python3 tEv.py $N $eps $Tfin $dt $save_dt $dis_num_in $dis_num_fin $nProc #1>>log 2>>err
            #python3 tEv_sparse.py $N $eps $Tfin $dt $save_dt $dis_num_in $dis_num_fin $nProc #1>>log #2>>err
                        
        fi
        
        #python3 plot_ev.py $N $eps $dis_num_fin &
    done
    #)&
done



