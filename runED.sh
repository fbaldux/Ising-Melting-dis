
#  ----------------  DYNAMICS  ---------------  #
 
N=22
eps=0.5

Tfin=100
dt=0.5
save_dt=10

dis_num=1

#echo $N | python3 buildHam.py
#echo $N $dis_num | python3 buildDiagHam.py

#echo $N $eps $Tfin $dt $save_dt $dis_num | python3 tEv.py

echo $N $eps $dis_num | python3 plot_mag_2d.py
