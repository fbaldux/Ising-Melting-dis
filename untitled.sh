for e in $(seq 1 14);
do
    for r in $(seq 0 199);
    do
        f="Results/spec_N24_e${e}.0000_d${r}.txt"
        l=($(wc $f))
        if [ ${a[0]} == ];
        then
            rm $f
        fi
    done
done