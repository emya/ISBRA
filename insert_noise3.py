#!/usr/bin/env python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import random
from create_sdata import somechoose

def normal_dist(sample, position, signal, mean, va, noise, weight, fix_data):
    if fix_data == "p":s_rate = [1 for i in range(sample)]
    else:
        s_rate = []
        for s in range(sample):
            r = -1
            while  0 > r or r > 1:
                r = random.normalvariate(mean, va)
            s_rate.append(r)

    if fix_data == "s":p_rate = [1 for i in range(position)]
    else:
        p_rate = []
        for p in range(position):
            r = -1
            while  0 > r or r > 1:
                r = random.normalvariate(mean, va)
            p_rate.append(r)
    mat = [[0 for i in range(sample)]for j in range(position)]
    total = 0
    for s in range(sample):
        for p in range(position):
            total += s_rate[s]*p_rate[p]
    mf = 0
    for i in range(position):
        for j in range(sample):
            #r = random.randrange(10)/10.0
            #print "r", r
            mat[i][j] = s_rate[j]*p_rate[i]*weight/total
            mf += s_rate[j]*p_rate[i]*weight/total
            #if r < s_rate[j]*p_rate[i]*weight/total:mat[i][j] = 1
    newmat, total = change_prob(mat, sample, position, fix_data)
    if fix_data == "b":
        """
        pmat = [[0 for i in range(sample)]for j in range(position)]
        s = somechoose(sample, signal)
        s.sort()
        print "somechoose, length", len(s), s
        for i in range(position):
            for j in range(sample):
                r = random.randrange(10)
                if r >= noise:pmat[i][j] = 1
            if i == m or i == n:
                for z in range(signal):
                    pmat[i][s[z]] = 1
        """
        L=[]
        for i in range(position):
            for j in range(sample):
                tuple=(i,j)
                L.append((tuple, newmat[i][j]))

        arr = np.array(newmat)
        elnum = position*sample
        mat = [[0 for i in range(sample)]for j in range(position)]
        """
        for i in range(10):
            for j in range(elnum/10):
                r = np.unravel_index(arr.argmin(), arr.shape)
                mat[r[0]][r[1]] = i*0.1 +0.05
                arr[r[0]][r[1]] = 2.0
        print "mat", mat
        """
        pmat = [[0 for i in range(sample)]for j in range(position)]
        s1 = somechoose(sample, signal)
        s2 = somechoose(sample, signal)
        c = []
        while (len(c) < sample*position*(10-noise)/10):
            choice = random_weight_choice(L)
            if choice not in c:
                c.append(choice)

        for k in range(len(c)):
            pmat[c[k][0]][c[k][1]] = 1

        for z in range(signal):
            pmat[0][s1[z]] = 1
            pmat[1][s1[z]] = 1
            pmat[3][s2[z]] = 1
            pmat[4][s2[z]] = 1
        """
        for i in range(position):
            for j in range(sample):
                #r = random.randrange(10)
                if mat[i][j] >= (noise)/10.0:pmat[i][j] = 1
            if i == m or i == n:
                print "signal", signal
                for z in range(signal):
                    print "s[z]", s[z]
                    pmat[i][s[z]] = 1
        """
    if fix_data == "p":pmat = position_fixmat(newmat, total, position, sample, signal, noise, m, n)
    elif fix_data == "s":pmat = sample_fixmat(newmat, total, position, sample, signal, noise, m, n)
    return pmat

def position_fixmat(newmat, total, position, sample, signal, noise, m, n):
    p_list = []
    for i in range(position):
        r = round( (newmat[i][0]/total)*((10.0-noise)/10)*(position*sample) )
        p_list.append(r/sample)
    #print "p_list", p_list
    mat = [[0 for i in range(sample)]for j in range(position)]
    s = somechoose(sample, signal)
    for i in range(position):
        for j in range(sample):
            r = (random.randrange(10)+1)/10.0
            if p_list[i] >= r:mat[i][j] = 1
        if i == m or i == n:
            for z in range(signal):
                mat[i][s[z]] = 1
    return mat

def sample_fixmat(newmat, total, position, sample, signal, noise, m, n):
    s_list = []
    for i in range(sample):
        r = round( (newmat[0][i]/total)*((10.0-noise)/10)*(position*sample) )
        s_list.append(r/position)
    #print "s_list", s_list
    mat = [[0 for i in range(sample)]for j in range(position)]
    s = somechoose(sample, signal)
    for i in range(position):
        for j in range(sample):
            r = (random.randrange(10)+1)/10.0
            if s_list[j] >= r:mat[i][j] = 1
        if i == m or i == n:
            for z in range(signal):
                mat[i][s[z]] = 1
    return mat

def change_prob(mat, sample, position, fix_data):
    newmat = [[0 for i in range(sample)]for j in range(position)]
    ma = 0.0
    mi = 1.0
    for i in range(position):
        if ma < max(mat[i]):
            #print "max", max(mat[i])
            ma = max(mat[i])
        if mi > min(mat[i]):
            #print "min", min(mat[i])
            mi = min(mat[i])
    #print "mi", mi
    #print "ma", ma
    interv = ma - mi
    changed_mi = mi/interv
    #print "changed_mi", changed_mi
    for i in range(position):
        for j in range(sample):
            newmat[i][j] = (mat[i][j]/interv) - changed_mi
    total = 0
    if fix_data == "p":
        for i in range(position):
            total += newmat[i][0]
            #print newmat[i]
    elif fix_data == "s":
        for i in range(sample):
            total += newmat[0][i]
            #print newmat[i]
    return newmat, total

def random_weight_choice(L):
    choice = None
    total = 0

    for item, p in L:
        total += p
        if random.random()*total < p:
            choice = item

    return choice

"""
m = normal_dist(10,10,5,2,3,0.5,0.01,8,1,"b")
total = 0
for i in range(10):
    total += sum(m[i])
    print m[i]
print "total", total
data = np.array(m)
plt.subplot(1,3,1)
plt.pcolor(data)
plt.colorbar()

m = normal_dist(10,10,5,2,3,0.5,0.01,8,1,"s")
total = 0
print "sssssssssssssssssssssssssssssssssssssss"
for i in range(10):
    total += sum(m[i])
    print m[i]
print "total", total
data = np.array(m)
plt.subplot(1,3,2)
plt.pcolor(data)
plt.colorbar()

m = normal_dist(10,10,5,2,3,0.5,0.01,8,1,"p")
total = 0
print "ppppppppppppppppppppppppppppppppppppppp"
for i in range(10):
    total += sum(m[i])
    print m[i]
print "total", total
data = np.array(m)
plt.subplot(1,3,3)
plt.pcolor(data)
plt.colorbar()
savefig("sample.png")
"""
