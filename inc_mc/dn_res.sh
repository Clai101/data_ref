#!/bin/bash

filelist=$(ssh matrk@login.cc.kek.jp "find ~/basf2/mc_skim/root -name '?.csv' -size +0c | sort")

for i in ${filelist}
do
    scp matrk@login.cc.kek.jp:/gpfs/$i . &
    time 3
done

wait