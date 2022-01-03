for N in $(seq 28 2 28);
do
    for e in $(seq 1 17);
    do
        #mv Results/{spec,magDiff}_N${N}_e$e.00* Results_N${N}_e$e/
        echo $N	$e $(ls Results_N${N}_e$e/spec_N${N}_e$e.0* | wc -l) >>	count
        echo $N $e
    done
done
