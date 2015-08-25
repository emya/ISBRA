#!/usr/bin/env python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import insert_noise3 as ins
import numpy as np
import pylab as pl
from pylab import *
import random

def data_to_txt(len_p, len_s, signal, noise, fname, pid):
    pmat = ins.normal_dist(len_s, len_p, signal, 0.5, 2.5, noise, 1, "b")

    f = open(fname, "w")
    for i in range(len_p):
        st = ""
        for j in range(len_s):
            st = str(pmat[i][j])+" "
            f.write(st)
        f.write("\n")
    f.close()

    return 0

def random_weight_choice(L):
    choice = None
    total = 0

    for item, p in L:
        total += p
        if random.random()*total < p:
            choice = item

    print "choice=",choice, type(choice)
    return choice

def read_file(fname):
    f = open(fname, "r")
    line = f.readline()
    l = []
    while line:
        print "line[0]=", line[0]
        li = line.split()
        l.append(li)
        line = f.readline()
    f.close
    print l

def pick(whole_n, p_n):
    l = []
    while len(l) != p_n:
        r = random.randrange(whole_n)
        if r not in l:
            l.append(r) 
    return l
