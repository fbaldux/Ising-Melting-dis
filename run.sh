rep_num=1000

for N in 100 400 1000 4000 10000 40000 100000 ;
do
    #echo $N | python3 buildHam.py
    
    echo $N $rep_num | python3 MC.py &
done

#for n in $(seq 2 30);
#do
#    echo $n $(( $( wc -l < Hamiltonians/clean_N$n.txt ) - 1)) >> lengths.txt
#done

N=33
Tfin=10
dt=0.1
save_step=10

#echo $N | python3 buildHam.py

#echo $N $Tfin $dt $save_step | python3 tEv.py