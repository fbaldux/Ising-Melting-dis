DIS_IN=0
DIS_FIN=100

for N in $(seq 24 2 26);
do
    
    for eps in $(seq 13 14);
    do
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g;s/DIS_IN/$DIS_IN/g;s/DIS_FIN/$DIS_FIN/g;" runUlysses.sh > temp.sh        
                
        sbatch temp.sh
        
        sleep 1
    done
done

rm temp.sh

