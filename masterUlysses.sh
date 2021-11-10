for N in $(seq 24 2 26);
do
    
    for eps in $(seq 1 12);
    do
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g" runUlysses.sh > temp.sh        
                
        sbatch temp.sh
        
        sleep 1
    done
done

rm temp.sh

