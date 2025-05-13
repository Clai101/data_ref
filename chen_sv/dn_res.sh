#!/bin/bash

filelist=$(ssh matrk@login.cc.kek.jp "find ~/work/chan_siev/hbk_data -name '?.hist' -size +0c | sort")


for i in ${filelist}
do
    scp matrk@login.cc.kek.jp:/gpfs/$i . &
    time 3
done

wait