
for N in $(seq 2 3)
do
    grep -v "#" Hamiltonians/clean_N$N.txt >> Hamiltonians/OFF_DIAG.txt
done