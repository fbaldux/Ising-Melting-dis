N=30

for eps in $(seq 1 17);
do
    echo "Starting eps $eps"
    DIS_IN=0
    DIS_FIN=480
    
    while (( DIS_IN<DIS_FIN ));
    do
        
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g;s/DIS_IN/$DIS_IN/g;s/DIS_FIN/$DIS_FIN/g;" runMissing-ctrl.sh > temp.sh        
        bash temp.sh
        
        sed "s/ENNE/$N/g;s/EPSILON/$eps/g;s/DIS_IN/$DIS_IN/g;s/DIS_FIN/$DIS_FIN/g;" runMissing.sh > temp.sh        
        sbatch temp.sh
        
        #sleep 1
        
        DIS_IN=$(more final) 
        
    done
done

rm temp.sh
rm final