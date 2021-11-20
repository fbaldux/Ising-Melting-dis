N=28

for eps in $(seq 1 14);
do
    echo "Starting eps $eps"
    DIS_IN=0
    DIS_FIN=240
    
    while (( DIS_IN<DIS_FIN ));
    do
    
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g;s/DIS_IN/$DIS_IN/g;s/DIS_FIN/$DIS_FIN/g;" runMissing2.sh > temp.sh        
        sbatch temp.sh
    
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g;s/DIS_IN/$DIS_IN/g;s/DIS_FIN/$DIS_FIN/g;" runMissing2-ctrl.sh > temp.sh        
        bash temp.sh
        
        sleep 1
        
        DIS_IN=$(more final) 
        
    done
done

rm temp.sh
rm final