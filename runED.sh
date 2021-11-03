
#  ----------------  DYNAMICS  ---------------  #
 
N=20
eps=4.

Tfin=1000
dt=0.5
save_dt=100

dis_num=1

#echo $N | python3 buildHam.py
#echo $N $eps $dis_num | python3 buildDiagHam.py

echo $N $eps $Tfin $dt $save_dt $dis_num | python3 tEv.py