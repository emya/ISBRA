#!/usr/bin/env python
import sys
import os
import time
import commands
import numpy as np
import math
import insert_noise_exclusive as ins
#from mcmc import makej
import transfer_concretedata as tc
import scipy.misc as scm
from decimal import *
import random
import poiss_binomial as poi
import fisher_test2_exclusive

argvs = sys.argv

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n -r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] +1
        yield tuple(pool[i] for i in indices)

def make_freq(mat):
    n_p = len(mat)
    n_s = len(mat[0])
    f_p = [0 for i in range(n_p)]
    f_s = [0 for i in range(n_s)]
    for i in range(n_p):
        f_p[i] = sum(mat[i])/float(n_s)
    for i in range(n_p):
        for j in range(n_s):
            f_s[j] += mat[i][j]
    f_s = [x/float(n_p) for x in f_s]
    return f_p, f_s

def prplot(fisher, proposed, existing, poisson_p, poisson_s, rn, leng, signal, variance, noise, num, roop_n):
    #pid = os.getpid()
    print "prplot starts!"
    sys.stdout.flush()

    fpos_fisher = "pos_"+fisher+"_"+str(rn)+".out"
    fneg_fisher = "neg_"+fisher+"_"+str(rn)+".out"

    pos_fisher = []
    neg_fisher = []

    fpos_poi_p = "pos_"+poisson_p+"_"+str(rn)+".out"
    fneg_poi_p = "neg_"+poisson_p+"_"+str(rn)+".out"

    pos_poi_p = []
    neg_poi_p = []

    fpos_poi_s = "pos_"+poisson_s+"_"+str(rn)+".out"
    fneg_poi_s = "neg_"+poisson_s+"_"+str(rn)+".out"

    pos_poi_s = []
    neg_poi_s = []

    for i in range(5):
        print "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii=%d", i
        sys.stdout.flush()

        m = ins.normal_dist(leng,leng,signal, 0.0, variance, noise, 1, "b")
        datafile = "data"+proposed+".out"
        bm = tc.read_and_writedata_sim_withoutfile(m, 0.5, datafile)
        ft = fisher_test2_exclusive.fisher_test(m)

        poi_pmat_p, poi_pmat_s = poi.poisson_p(m)
        #poi_pmat_p = [[0 for i in range(50)] for j in range(50)]
        #poi_pmat_s = [[0 for i in range(50)] for j in range(50)]

        inproposed1 = proposed+"_num"+str(num*5)
        print "file1", inproposed1
        sys.stdout.flush()

        cmd="sh child_poissonandproposed_exclusive.sh "+str(leng)+" "+str(num)+" "+datafile+" "+inproposed1+""
        os.system(cmd)
        print "inproposed1"

        inproposed2= proposed+"_num"+str(num*5*10)
        print "file2", inproposed2
        sys.stdout.flush()

        cmd="sh child_poissonandproposed_exclusive.sh "+str(leng)+" "+str(num*10)+" "+datafile+" "+inproposed2+""
        os.system(cmd)
        print "inproposed2"

        inexisting1 = existing+"_num"+str(num*5)
        print "inexisting1", inexisting1
        cmd="sh child_poissonandexisting_exclusive.sh "+str(leng)+" "+str(num)+" "+datafile+" "+inexisting1+""
        os.system(cmd)

        inexisting2 = existing+"_num"+str(num*5*10)
        print "inexisting2", inexisting2
        cmd="sh child_poissonandexisting_exclusive.sh "+str(leng)+" "+str(num*10)+" "+datafile+" "+inexisting2+""
        os.system(cmd)

        """
        tmp = 1
        while tmp >0:
            time.sleep(10)
            tmp = int(commands.getoutput("qstat| grep "+"ch_"+str(pid)+" |wc").split()[0])
        """

        for k in range(leng):
            for l in range(k+1, leng):
                if(k == 0 and l == 1) or (k == 3 and l == 4):
                    pos_fisher.append(str(ft[k][l])+" ")
                    pos_poi_p.append(str(poi_pmat_p[k][l])+" ")
                    pos_poi_s.append(str(poi_pmat_s[k][l])+" ")
                else:
                    neg_fisher.append(str(ft[k][l])+" ")
                    neg_poi_p.append(str(poi_pmat_p[k][l])+" ")
                    neg_poi_s.append(str(poi_pmat_s[k][l])+" ")

    ffp = open(fpos_fisher, "w")
    ffn = open(fneg_fisher, "w")
    ffp.writelines(pos_fisher)
    ffn.writelines(neg_fisher)
    ffp.close()
    ffn.close()

    ffp = open(fpos_poi_p, "w")
    ffn = open(fneg_poi_p, "w")
    ffp.writelines(pos_poi_p)
    ffn.writelines(neg_poi_p)
    ffp.close()
    ffn.close()

    ffp = open(fpos_poi_s, "w")
    ffn = open(fneg_poi_s, "w")
    ffp.writelines(pos_poi_s)
    ffn.writelines(neg_poi_s)
    ffp.close()
    ffn.close()
    return 0

fisher = argvs[1]
proposed = argvs[2]
existing = argvs[3]
poisson_p = argvs[4]
poisson_s = argvs[5]
rn = int(argvs[6])
leng = int(argvs[7])
signal = int(argvs[8])
variance = float(argvs[9])
noise = float(argvs[10])
num = int(argvs[11])
roop_n = str(argvs[12])
prplot(fisher, proposed, existing, poisson_p, poisson_s, rn, leng, signal, variance, noise, num, roop_n)
