#!/usr/bin/env python

import transfer_concretedata as tc
import poiss_binomial as poi

datafile = "datasimulationout-proposedmcmcp_exclusive_len50sig15vari1.5noise8.0.out"

m = []

f = open(datafile, 'r')

for line in f:
    list = line.replace('\n', '').split(' ')
    m.append([int(x) for x in list])

f.close()

poi_pmat_p, poi_pmat_s = poi.poisson_p(m)
