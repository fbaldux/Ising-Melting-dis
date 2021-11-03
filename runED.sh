
#  ----------------  DYNAMICS  ---------------  #
 
N=5
eps=1.

Tfin=10
dt=0.1
save_step=10

dis_num=10

#echo $N | python3 buildHam.py
echo $N $eps $dis_num | python3 buildDiagHam.py

#echo $N $Tfin $dt $save_step | python3 tEv.py