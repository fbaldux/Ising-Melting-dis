N=£N

eps=£E

dis_num_in=£Di
dis_num_fin=£Df
dis_threads=4


count=0
for ((d=$dis_num_in; $count<$dis_threads && d<$dis_num_fin; d++));
do
    if [[ ! -f Results_N${N}_e${eps}/spec_N${N}_e${eps}.0000_d$d.txt ]];
    then
        count=$(( $count+1 ))
        echo -n "$d "
    fi
done
echo $d > final
echo "final=$d"

