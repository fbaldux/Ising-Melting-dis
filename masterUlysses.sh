for N in $(seq 28 2 28);
do
    
    for eps in $(seq 1 12);
    do
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g" runUlysses.sh > temp.sh        
                
        sbatch temp.sh
        
        sleep 1
    done
done

rm temp.sh

