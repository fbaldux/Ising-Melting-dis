
# for ED
eig_num=10

# for tEv
Tin=0
Tfin=10000
dt=1
save_dt=1
sparse=0

ts_per_decade=20

dis_num_in=0
dis_num_fin=1

overwrite=1
nProc=7

for N in $(seq 24 2 24);
do    
    #(
    python3 buildDiagHam.py $N $dis_num_in $dis_num_fin 1>>log 2>>err
  
    for eps in $(seq 5 1 5);
    do
        if [[ ! -f stop ]];
        then
            #python3 spectrum.py $N $eps $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            #python3 spectrum_sparse.py $N $eps $eig_num $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            
            #python3 tEv.py $N $eps $Tin $Tfin $dt $save_dt $dis_num_in $dis_num_fin $sparse $overwrite $nProc 1>>log 2>>err
            python3 tEv_log.py $N $eps $Tfin $ts_per_decade $dis_num_in $dis_num_fin $sparse $overwrite $nProc #1>>log 2>>err
        fi
        
        #python3 plot_ev.py $N $eps $dis_num_fin &
    done
    #)&
done



