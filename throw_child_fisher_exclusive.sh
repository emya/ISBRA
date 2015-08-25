#!/bin/sh

out_fisher=$1
out_proposed=$2
out_existing=$3
out_poisson_p=$4
out_poisson_s=$5
rn=$6
leng=$7
signal=$8
variance=$9
contrue=${10}
num=${11}
ith=${12}

python fisher_simulate_exclusive.py ${out_fisher} ${out_proposed} ${out_existing} ${out_poisson_p} ${out_poisson_s} ${rn} ${leng} ${signal} ${variance} ${contrue} ${num} ${ith} > co.out
