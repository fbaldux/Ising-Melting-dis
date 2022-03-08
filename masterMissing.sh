N=30

for eps in $(seq 1 17);
do
    echo "Starting eps $eps"
    Di=0
    Df=480
    
    while (( Di<Df ));
    do
        
        sed "s/£N/$N/g;s/£E/$eps/g;s/£Di/$Di/g;s/£Df/$Df/g;" runMissing-ctrl.sh > temp.sh        
        bash temp.sh
        
        sed "s/£N/$N/g;s/£E/$eps/g;s/£Di/$Di/g;s/£Df/$Df/g;" runMissing.sh > temp.sh        
        sbatch temp.sh
        
        #sleep 1
        
        Di=$(more final) 
        
    done
done

rm temp.sh
rm final