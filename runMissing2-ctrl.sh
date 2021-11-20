N=ENNE

eps=EPSILON

eig_frac=10

dis_num_in=DIS_IN
dis_num_fin=DIS_FIN
dis_threads=8

overwrite=0

count=0
for ((d=$dis_num_in; $count<$dis_threads && d<$dis_num_fin; d++));
do
    if [[ ! -f Results_N${N}_e${eps}/spec_N${N}_e${eps}.0000_d$d.txt ]];
    then
        count=$(( $count+1 ))
        echo $d
    fi
done
echo $d > final
echo "$d -> final"

