#!/usr/bin/env python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pylab import *
import sys
#import re

def read_and_writedata(file, interval):
    dic = {1:279000000,
           2:251000000,
           3:221000000,
           4:197000000,
           5:198000000,
           6:176000000,
           7:163000000,
           8:148000000,
           9:140000000,
           10:143000000,
           11:148000000,
           12:142000000,
           13:118000000,
           14:107000000,
           15:100000000,
           16:104000000,
           17:88000000,
           18:86000000,
           19:72000000,
           20:66000000,
           21:45000000,
           22:48000000,
           23:163000000,
           24:51000000}
    #23 == x, 24 == y
    title = ["name"]
    data = []
    ch = 1
    while ch != 25:
        le_c = dic[ch]
        for i in range(le_c/interval):
            if ch == 23:
                ch_name="ch_x:"+str(i*interval)
                title.append(ch_name)
            elif ch == 24:
                ch_name="ch_y:"+str(i*interval)
                title.append(ch_name)
            else:
                ch_name="ch_"+str(ch)+":"+str(i*interval)
                title.append(ch_name)
        ch += 1
    #print title
    print len(title)

    f = open(file, "r")
    line = f.readline()

    while line:
        l = line.split()
        print "l", l
        exist = -1
        for i in range(len(data)):
            if l[0] in data[i]:
                exist = i
        print "exist", exist
        if exist == -1:
            newl = ["n" for i in range(len(title))]
            newl[0] = l[0]
            data.append(newl)
            exist = len(data)-1
            prel = []
        for i in range(1, len(title)):
            bar = title[i].index("_")
            col = title[i].index(":")
            if l[1]==title[i][bar+1:col] and int(l[2])<=int(title[i][col+1:])<=int(l[3]):
                print "ch", title[i][bar+1:col]
                print "value", title[i][col+1:]
                print "data", l[5]
                data[exist][i]=float(l[5])
        if len(prel)!=0 and prel[1]==l[1] and int(l[2])-int(prel[3]) >= 1:
            print "if"
            for i in range(1, len(title)):
                bar = title[i].index("_")
                col = title[i].index(":")
                if l[1]==title[i][bar+1:col] and int(prel[3])<int(title[i][col+1:])<int(l[2]):
                    if int(title[i][col+1])-int(prel[3]) < int(l[2])-int(title[i][col+1:]):
                        data[exist][i] = float(prel[5])
                    else:data[exist][i] = float(l[5])
        elif len(prel)==0 and l[3] > interval:
            for i in range(1, len(title)):
                bar = title[i].index("_")
                col = title[i].index(":")
                if l[1]==title[i][bar+1:col] and int(title[i][col+1:])<int(l[2]):
                    data[exist][i] = float(l[5])
        elif len(prel)!=0 and l[1] != prel[1]:
            for i in range(1, len(title)):
                bar = title[i].index("_")
                col = title[i].index(":")
                if prel[1]==title[i][bar+1:col] and int(title[i][col+1:])>int(prel[3]):
                    data[exist][i] = float(prel[5])
                if l[1]==title[i][bar+1:col] and int(title[i][col+1:])<int(l[2]):
                    data[exist][i] = float(l[5])

        prel = l
        line = f.readline()

    f.close()
    for i in range(2):
        print data[i][0]


def read_and_writedata_withinterval(file, thres, out):
    f = open(file, "r")
    line = f.readline()
    order = []
    wc = 0
    data = []
    while line:
        l = line.split()
        if wc == 0:
            title = l
        else:
            order.append(l[0])
            del l[0]
            data.append(l)
        wc += 1
        line = f.readline()

    f.close()
    print "data", data
    h = []
    for i in range(wc-1):
        d = [float(x) for x in data[i]]
        h += d
        #print data[i][0],
    for i in range(wc-1):
        for j in range(len(title)):
            if float(data[i][j]) < thres:
                data[i][j] = 0
            else:data[i][j] = 1

    f = open(out, "w")
    for i in range(wc-1):
        f.writelines(str(data[i])+"\n")
    f.close()
    print "order", order
    return order
    """
    fig = plt.figure(0)
    name = "histvalue.png"
    plt.hist(h, bins=40, log=True, alpha = 0.5)
    savefig(name)

    print ""
    print "title", len(title)
    print "lendata", len(data[0])
    print "lendata", len(data[5])
    print "len wc-1", wc-1
    print "order", order
    """

def read_and_writedata_withinterval_loss(file, thres, out):
    f = open(file, "r")
    line = f.readline()
    order = []
    wc = 0
    data = []
    while line:
        l = line.split()
        if wc == 0:
            title = l
        else:
            order.append(l[0])
            del l[0]
            data.append(l)
        wc += 1
        line = f.readline()

    f.close()
    print "data", data
    h = []
    for i in range(wc-1):
        d = [float(x) for x in data[i]]
        h += d
        #print data[i][0],
    for i in range(wc-1):
        for j in range(len(title)):
            if float(data[i][j]) < thres:
                data[i][j] = 1
            else:data[i][j] = 0

    f = open(out, "w")
    for i in range(wc-1):
        f.writelines(str(data[i])+"\n")
    f.close()
    print "order", order
    return order

def read_and_writedata_sim_interval(file, thres, out):
    f = open(file, "r")
    line = f.readline()
    data = []
    while line:
        ll = line.strip(" \n")
        l = ll.split(" ")
        data.append(l)
        line = f.readline()

    f.close()
    print "data", data
    h = []
    for i in range(len(data)):
        d = [float(x) for x in data[i]]
        h += d
        #print data[i][0],
    for i in range(len(data)):
        for j in range(len(data[0])):
            if float(data[i][j]) < thres:
                data[i][j] = 0
            else:data[i][j] = 1

    f = open(out, "w")
    for i in range(len(data)):
        for j in range(len(data[0])):
            f.write(str(data[i][j])+" ")
        f.write("\n")
    f.close()
    return 0

def read_and_writedata_sim_withoutfile(data, thres, out):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if float(data[i][j]) < thres:
                data[i][j] = 0
            else:data[i][j] = 1
    f = open(out, "w")
    for i in range(len(data)):
        f.write(" ".join([str(x) for x in data[i]])+"\n")
    f.close()
    return data



#read_and_writedata_sim_interval("simdata_len10sig5.txt", 1, "bi_simdata_len10sig5.txt")
#read_and_writedata("shortCCLE_NCIH889.txt", 100000)
