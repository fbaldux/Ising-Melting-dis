
# for ED
eig_num=100

# for tEv
initState=0
Tin=0
Tfin=1e4
dt=0.1
save_dt=0.1
sparse=0

ts_per_pow2=5

dis_num_in=0
dis_num_fin=3

overwrite=1
nProc=1

for N in $(seq 36 2 36)
do    
    python3 buildDiagHam.py $N $dis_num_in $dis_num_fin 1>>log 2>>err
    
    python3 save_H.py $N $dis_num_in $dis_num_fin
    
    for eps in $(seq 1 2 1)
    do
        for initState in 0 #24 121
            do
            
            if [[ ! -f stop ]];
            then
                #python3 spectrum.py $N $eps $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
                #python3 spectrum_sparse.py $N $eps $eig_num $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            
                #python3 spectrum_p0.py $N $eps $dis_num_in $dis_num_fin $nProc #1>>log 2>>err
                #python3 save_p0.py $N $eps
            
                #python3 spectrum2.py $N $eps $dis_num_in $dis_num_fin
            
                #python3 tEv.py $N $eps $initState $Tin $Tfin $dt $save_dt $dis_num_in $dis_num_fin $sparse $overwrite $nProc #1>>log 2>>err
                #python3 tEv_log.py $N $eps $initState $Tin $Tfin $ts_per_pow2 $dis_num_in $dis_num_fin $sparse $overwrite $nProc 1>>log 2>>err
                :
            fi            
            #python3 average_ev.py $N $eps $initState $Tfin $dis_num_fin
            #python3 plot_ev.py $N $eps $initState $Tfin $dis_num_fin &
        done
        
        #python3 tEv_log_multiState.py $N $eps 0 $Tin $Tfin $ts_per_pow2 $dis_num_in $dis_num_fin 0 $overwrite $nProc
    
    done
    #wait
done



