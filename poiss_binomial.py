#!/usr/bin/env python
import sys
import os
import numpy as np
import math
from mcmc import makej
import scipy.misc as scm
from decimal import *
import random

argvs = sys.argv

def poisson_p(mat):
    f_p, f_s = make_freq(mat)
    p_mat_p = pois_fixposition(mat)
    print "done p_mat_p"
    sys.stdout.flush()
    #p_mat_s = pois_fixsample(mat)
    p_mat_s = pois_fixsample_bylessR(mat)
    print "done p_mat_s"
    sys.stdout.flush()
    return p_mat_p, p_mat_s

"""
def poisson_p(mat, fix_mc, R, roop_n):
    f_p, f_s = make_freq(mat)
    if R == "R":
        if fix_mc == "p":p_mat = pois_fixposition_byR(mat, roop_n)
        elif fix_mc == "s":p_mat = pois_fixsample_byR(mat)
    else:
        if fix_mc == "p":p_mat = pois_fixposition(mat)
        elif fix_mc == "s":p_mat = pois_fixsample(mat)
    return p_mat
"""

def pois_fixposition_byR(mat, roop_n):
    origina_j = makej(mat)
    n_p = len(mat)
    n_s = len(mat[0])
    p_mat = [[0 for i in range(n_p)]for i in range(n_p)]
    f_p, f_s = make_freq(mat)
    print "f_p", f_p
    print "f_s", f_s
    #print "jmat", origina_j
    for i in range(n_p):
        for j in range(i+1, n_p):
            #a = f_p[i]*f_p[j]
            f = open("a.txt", "w")
            a = str(f_p[i]*f_p[j])
            print "a", a
            f.writelines(a)
            f.close()
            print "a" , a
            test_s = origina_j[i][j]
            print "test_s" , test_s
            cmd = "R --vanilla --args "+str(test_s)+" "+str(a)+" "+str(n_s)+" "+roop_n+" < /home/ayada/cell/fixposition_poison.R"
            os.system(cmd)
            fname = "p"+roop_n+".txt"
            f1 = open(fname, "r")
            l = f1.readline()
            print "l", l
            total = float(l)
            print "total", total
            if 1.0-(0.1)**15 <= total <= 1.0+(0.1)**15:
                p_mat[i][j] = 1
                p_mat[j][i] = 1
            else:
                ta = float(1.0 - total)
                p_mat[i][j] = -math.log10(ta)
                p_mat[j][i] = -math.log10(ta)
    return p_mat

def pois_fixposition(mat):
    origina_j = makej(mat)
    n_p = len(mat)
    n_s = len(mat[0])
    p_mat = [[0 for i in range(n_p)]for i in range(n_p)]
    f_p, f_s = make_freq(mat)
    print "f_p", f_p
    #print "f_s", f_s
    #print "jmat", origina_j
    for i in range(n_p):
        for j in range(i+1, n_p):
            test_s = origina_j[i][j]
            rate_c = f_p[i]*f_p[j]
            #print "test_s", test_s
            #print "rate_c", rate_c
            total = 0
            #total = (1- rate_c)**n_s
            for t in range(test_s+1):#change!
                #print "t, test_s, scm.comb", t, test_s, scm.comb(n_s, t)
                total += scm.comb(n_s, t) * (rate_c**t) * ((1-rate_c)**(n_s -t))
            #print "i, j, total", i, j, total
            #print "decimal", Decimal(str(total))
            #print "1 minus", 1-total
            #print "multiple", total*1.0
            if 1.0-(0.1)**8 <= total <= 1.0+(0.1)**8:
                p_mat[i][j] = 1
                p_mat[j][i] = 1
            else:
                ta = float(1.0 - total)
                #print "ta", ta
                #print "to", total
                p_mat[i][j] = -math.log10(ta)
                p_mat[j][i] = -math.log10(ta)
    return p_mat

def pois_fixsample(mat):
    original_j = makej(mat)
    n_p = len(mat)
    n_s = len(mat[0])
    p_mat = [[0 for i in range(n_p)]for i in range(n_p)]
    f_p, f_s = make_freq(mat)
    print "f_s", f_s
    sys.stdout.flush()
    for i in range(n_p):
        print "n_p", n_p
        sys.stdout.flush()
        for j in range(i+1, n_p):
            #print "*******************************************"
            test_s = original_j[i][j]
            #print "test_s", test_s
            s_list = [x for x in range(n_s)]
            total = 1
            for t in range(n_s):
                total *= (1 - (f_s[t])**2)#when 0
            #print "first total", total
            for t in range(1, test_s+1):#change test_s
                mi_total = 0
                #print "s_list", s_list
                #print "i,j,t", i,j,t
                for c in combinations(s_list, t):
                    c = list(c)
                    remain_l = list(set(s_list) - set(c))
                    #print "c", c
                    #print "remain",remain_l
                    subtotal = 1
                    for s in range(t):
                        subtotal *= (f_s[c[s]]**2)
                    for s in range(n_s -t):
                        subtotal *= (1- (f_s[remain_l[s]])**2)
                    mi_total += subtotal
                #print "middle", t, mi_total
                total += mi_total
                #print "total", total
                #print "1-total", 1-total
            #print "*******************************************"
            #print "total", total
            if 1.0-(0.1)**15 <= total <= 1.0+(0.1)**15:
                p_mat[i][j] = 1
                p_mat[j][i] = 1
            else:
                p_mat[i][j] = -math.log10(1-total)
                p_mat[j][i] = -math.log10(1-total)
    return p_mat

def pois_fixsample_byR(mat):
    original_j = makej(mat)
    n_p = len(mat)
    n_s = len(mat[0])
    p_mat = [[0 for i in range(n_p)]for i in range(n_p)]
    f_p, f_s = make_freq(mat)
    #print "f_s", f_s
    list_rate = [x**2 for x in f_s]
    f = open("b.txt", "w")
    b = [str(x)+" " for x in list_rate]
    b.append("\n")
    #print "b", b
    f.writelines(b)
    f.close()
    for i in range(n_p):
        for j in range(i+1, n_p):
            #print "*******************************************"
            test_s = original_j[i][j]
            cmd = "R --vanilla --args "+str(test_s)+" < ./fixsample_poisson.R"
            os.system(cmd)
            f1 = open("s.txt", "r")
            l = f1.readline()
            #print "l", l
            total = float(l)
            #print "test_s", test_s
            #print "*******************************************"
            #print "total", total
            if 1.0-(0.1)**15 <= total <= 1.0+(0.1)**15:
                p_mat[i][j] = 1
                p_mat[j][i] = 1
            else:
                p_mat[i][j] = -math.log10(1-total)
                p_mat[j][i] = -math.log10(1-total)
    return p_mat

def pois_fixsample_bylessR(mat):
    original_j = makej(mat)
    n_p = len(mat)
    n_s = len(mat[0])
    p_mat = [[0 for i in range(n_p)]for i in range(n_p)]
    f_p, f_s = make_freq(mat)
    #print "f_s", f_s
    list_rate = [x**2 for x in f_s]
    f = open("b.txt", "w")
    b = [str(x)+" " for x in list_rate]
    b.append("\n")
    #print "b", b
    f.writelines(b)
    f.close()

    tests_s = []
    for i in range(n_p):
        for j in range(i+1, n_p):
            #print "*******************************************"
            test_s = original_j[i][j]
            tests_s.append(test_s)
    
    f = open("tests.txt", "w")
    f.write(" ".join([str(x) for x in tests_s]))
    f.close()
    
    cmd = "R --vanilla --args "+str(test_s)+" < ./fixsample_poisson_less.R"
    os.system(cmd)
    f1 = open("s.txt", "r")
    l = []
    for line in f1:
        l += line.replace('\n','').split(' ')
    f1.close()

    list_float = [float(x) for x in l]
            #print "l", l
            #total = float(l)
            #print "test_s", test_s
            #print "*******************************************"
            #print "total", total
    for i in range(n_p):
        for j in range(i+1, n_p):
            total = list_float.pop(0)
            if 1.0-(0.1)**15 <= total <= 1.0+(0.1)**15:
                p_mat[i][j] = 1
                p_mat[j][i] = 1
            else:
                p_mat[i][j] = -math.log10(1-total)
                p_mat[j][i] = -math.log10(1-total)
    return p_mat

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
