#!/usr/bin/env python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
#import mojscalbctmcmc as moj
from calculate_area import area
import os

def plot_pr(leng, out, pout, nout):
    print "out", out
    print "pout", pout
    print "nout", nout
    recall = []
    precision = []
    f = open(pout, "r")
    pos = f.readline()
    print "pos", pos
    f.close()
    lis = pos.split()
    pos = [float(x) for x in lis]
    f = open(nout, "r")
    neg = f.readline()
    f.close()
    lis = neg.split()
    neg = [float(x) for x in lis]

    mi = min(neg)-0.1
    ma = max(pos)+0.1
    print "mi", mi
    print "ma", ma
    interv = ma - mi
    inte = interv/100
    for th in range(100): #
        t = mi + inte*th
        print "th", th
        print "threshold", t
        tp = list_count(pos, t)
        fn = len(pos) - tp
        fp = list_count(neg, t)
        tn = len(neg) - fp
        print "tp", tp
        print "fn", fn
        print "tn", tn
        print "fp", fp
        if tp == 0:
            recall.append(0)
            precision.append(0)
        else:
            print "tp/(tp+fn)", tp/float(tp+fn)
            print "tp/(tp+fp)", tp/float(tp+fp)
            recall.append( tp/float(tp+fn) )
            precision.append( tp/float(tp+fp) )
    print "recall", recall
    print "precision", precision
    total = area(recall, precision)
    print "total=", total
    c = "prarea_"+out+".out"
    print "c =", c
    f = open(c, "w")
    f.write(str(total))
    f.close()
    fig = plt.figure(0)
    plt.plot(recall, precision)
    a = "prplot_"+out+".png"
    fig.savefig(a)
    close()

    hold(True)
    plt.hist(neg, log=True, alpha=0.5, facecolor='b')
    plt.hist(pos, log=True, alpha=0.5, facecolor='r')
    b = "pvalue_"+out+".png"
    savefig(b)

    close()
    return 0
def list_count(list, u):
    newlist = [x for x in list if x > u]
    return len(newlist)
def dist_pvalue(f, an, bn, sam, pos):
    c = np.loadtxt(f)
    name = "p-value_mcmc_"+str(an)+"burn"+str(bn)+"mat_"+str(sam)+"*"+str(pos)+".png"
    return 0
