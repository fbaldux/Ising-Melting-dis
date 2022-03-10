
# for ED
eig_num=100

#      0   1   2   3   4  5 6 7 8  9 10 11 12 13 14 15 16 17 18 
eps=(  1   2   3   4   5  6 7 8 9 10 11 12 13 14 15 16 17 18 )
Tfin=( 1e2 1e3 1e4 1e5 1e5 )


# for tEv
Tin=0
#Tfin=1e1
dt=5
save_dt=5
sparse=0

ts_per_pow2=10

dis_num_in=0
dis_num_fin=1000

overwrite=1
nProc=5

for N in $(seq 18 2 20)
do
    for ie in $(seq 0 4)
    do
        for initState in 0 5 121
        do
            (
            if [[ ! -f stop ]]
            then
                
                python3 tEv_log.py $N ${eps[$ie]} $initState $Tin ${Tfin[$ie]} $ts_per_pow2 $dis_num_in $dis_num_fin $sparse $overwrite $nProc 1>>log 2>>err
                :
            fi            
            
            python3 average_ev.py $N ${eps[$ie]} $initState ${Tfin[$ie]} $dis_num_fin
            #python3 plot_ev.py $N $eps $initState $Tfin $dis_num_fin &
            )&
        done  
        wait  
    done
done



