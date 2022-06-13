#      0   1   2   3   4   5   6   7   8   9   10 11 12 13 14 15 16 17 18 
eps=( 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 )
Tf=(  1e2 1e2 1e3 1e3 1e4 1e4 1e4 1e4 1e5 1e5 )

# NB: dis_per_run deve essere divisibile per il numero di core etc.
dis_num_in=0
dis_num_fin=1000
dis_per_run=250

for ((d=$dis_num_in; d<$dis_num_fin; d+=$dis_per_run))
do
    Di=$d 
    Df=$(( $d+$dis_per_run ))

    for N in $(seq 30 2 30)
    do
    
        #for ie in $(seq 0 9)
		for e in $(seq 9 18)
        do
            # spectrum
			sed "s/£N/$N/g;s/£E/$e/g;s/£Tf/0/g;s/£Di/$Di/g;s/£Df/$Df/g;" runUlysses.sh > temp.sh        
            
			# tEv
			#sed "s/£N/$N/g;s/£E/${eps[$ie]}/g;s/£Tf/${Tf[$ie]}/g;s/£Di/$Di/g;s/£Df/$Df/g;" runUlysses.sh > temp.sh        
                
            sbatch temp.sh
        
            #sleep 1
        done
    done
done

rm temp.sh
