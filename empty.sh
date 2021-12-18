for N in $(seq 28 2 32);
do
    for e in $(seq 1 17);
    do
	for f in Results_N${N}_e$e/*;
	do
	    if [[ ! -s $f ]]
	    then
		rm $f
	    fi
	done
    done
done
