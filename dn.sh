if test $1
then
    type=$1
else

for i in 0 1 2 3 4 5 6 7 8 9
do
    scp matrk@login.cc.kek.jp:~/work/sieve/hbk_${type}/${i}.hist . &
done

wait