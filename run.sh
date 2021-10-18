
#for N in $(seq 2 4);
#do
    #echo $N | python3 buildHam.py
    #done

#for n in $(seq 2 30);
#do
#    echo $n $(( $( wc -l < Hamiltonians/clean_N$n.txt ) - 1)) >> lengths.txt
#done

N=5
Tfin=10
dt=0.1
save_step=10

echo $N $Tfin $dt $save_step | python3 tEv.py