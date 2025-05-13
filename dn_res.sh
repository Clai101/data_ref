#!/bin/bash

if [ -n "$1" ]; then
    type=$1
else
    echo "No type provided. Exiting."
    exit 1
fi

for i in {0..9}
do
    scp matrk@login.cc.kek.jp:~/work/skim_mc/hbk_${type}/${i}\*.hist end_${type}/. &
    time 3
done

wait
