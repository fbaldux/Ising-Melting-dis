for N in $(seq 24 34):
do
    
    for eps in (0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0);
    do
        cp runUlysses.sh temp.sh
        
        sed -i "" "s/ENNE/$N/g" temp.sh        
        sed -i "" "s/EPSILON/$eps/g" temp.sh        
        
        sbatch temp.sh
        
        sleep 1
    done
done

rm temp.sh