for N in $(seq 24 2 30)
do
    for e in $(seq 1 5)
    do
        for iS in 0 24 121
        do
            echo $N $e $iS $(ls Results/tEv_N${N}_e${e}.0000_s${iS}_* | wc -l) >> count_ev
            echo $N $e $iS
        done
    done
done
