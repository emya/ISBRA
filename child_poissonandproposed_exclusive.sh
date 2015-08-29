#!/bin/bash
leng=$1
an=$2
input=$3
out=$4

python mcmc_perf.py ${leng} ${an} ${input} ${out} 
# ${MPI_HOME}/bin/mpirun -np ${NSLOTS} -machinefile ${TMPDIR}/machines ./mmse ${leng} ${leng} ${an} ${input} ${out}
