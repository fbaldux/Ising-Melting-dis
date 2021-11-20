for N in $(seq 28 2 28);
do
    for e in $(seq 1 14);
    do
        mv Results/spec_N${N}_e$e.00* Results_N${N}_e$e/ 
    done
done