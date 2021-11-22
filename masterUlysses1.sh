# NB: dis_per_thread deve essere divisibile per il numero di core etc.
dis_num_in=240
dis_num_fin=480
dis_per_thread=12

for ((d=$dis_num_in; d<$dis_num_fin; d+=$dis_per_thread));
do
    DIS_IN=$d 
    DIS_FIN=$(( $d+$dis_per_thread ))

    for N in $(seq 28 2 28);
    do
    
        for eps in $(seq 1 17);
        do
            sed "s/ENNE/$N/g;s/EPSILON/$eps/g;s/DIS_IN/$DIS_IN/g;s/DIS_FIN/$DIS_FIN/g;" runUlysses1.sh > temp.sh        
                
            sbatch temp.sh
        
            sleep 1
        done
    done
done

rm temp.sh
