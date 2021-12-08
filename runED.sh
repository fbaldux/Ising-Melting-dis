
# for ED
eig_num=10

# for tEv
Tfin=1000
dt=10
save_dt=50
sparse=1


dis_num_in=0
dis_num_fin=1

overwrite=1
nProc=1

for N in $(seq 24 2 24);
do    
    #(
    #python3 buildDiagHam.py $N $dis_num_in $dis_num_fin 1>>log 2>>err
  
    for eps in $(seq 8 1 8);
    do
        if [[ ! -f stop ]];
        then
            #python3 spectrum.py $N $eps $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            #python3 spectrum_sparse.py $N $eps $eig_num $dis_num_in $dis_num_fin $overwrite $nProc 1>>log 2>>err
            
            python3 tEv.py $N $eps $Tfin $dt $save_dt $d $dis_num_in $dis_num_fin $sparse $overwrite $nProc #1>>log 2>>err
                        
        fi
        
        #python3 plot_ev.py $N $eps $dis_num_fin &
    done
    #)&
done



