#  ---------------  MONTECARLO  --------------  #
run=1
plot=1

N=1e4
p=0.75
rep_num=100

if (( $run == 1 ))
then
    #for N in 1e4; #100 400 1000 4000 10000 40000 100000 ;
    #do    
    #    echo $N $p $rep_num | python3 MC.py &
    #done
    #wait
    
    echo $N $p $rep_num | python3 MC.py
fi

if (( $plot == 1 ))
then
    echo $N $p $rep_num | python3 plot_MC.py &
fi

#echo $N $p $rep_num | python3 plot_MC.py &

#  ----------------  DYNAMICS  ---------------  #
 
N=33
Tfin=10
dt=0.1
save_step=10

#echo $N | python3 buildHam.py

#echo $N $Tfin $dt $save_step | python3 tEv.py