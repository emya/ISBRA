#!/usr/bin/env python

# mcmc in only fixed position
"""
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pylab as pl
from pylab import*
"""
import sys
import numpy as np
import random
import types
import copy
#import mojcdcoscale as cd
#from mojcdcoscale import cdco
from copy import deepcopy
import math
import create_sdata as cre

def bingain(a):
    if a > 0:
       k = 1
    else:
       k = 0
    return k

def binloss(a):
    if a < 0:
       k = 1
    else:
       k = 0
    return k
"""
def maked(Mat): #make binary table(pos*sample)
    len(Mat) = pos
    len(Mat[0]) = sam
    newMat = [[0 for j in range(self.pos)] for i in range(self.sam)]
    for i in range(self.sam):
        for j in range(self.pos):
            a = float(Mat[i][j+1])
            k = self.bingain(a)
            newMat[i][j] = k
    return newMat
"""
def marginal(Mat):
    newMat = deepcopy(Mat)
    len_s = len(Mat[0])
    len_p = len(Mat)
    sam = [0 for i in range(len_s)]
    pos = [0 for j in range(len_p)]
    """
    for i in range(self.sam):
        sam[i] = sum(newMat[i])
    for j in range(self.pos):
        p = 0
        for i in range(self.sam):
            p += int(newMat[i][j])
        pos[j] = p
    """
    for i in range(len_p):
        pos[i] = sum(newMat[i])
    for j in range(len_s):
        p = 0
        for i in range(len_p):
            p += int(newMat[i][j])
        sam[j] = p
    return sam, pos
def decident(t): #co-occurunce i,j  t is matrix wiz position * sample
    len_p = len(t)
    len_s = len(t[0])
    i, j = choosent(len_p, len_s)
   # print "i, j=", i, j
   # print "len(t)", len(t)
   # print "len(t[0])", len(t[0])
  # print "t =", t
    if t[i][j] == 1:
       return i, j
    else:
       return decident(t)

def chooseor(t, i, j): #i=position,j=sample
    len_p = len(t)
    len_s = len(t[0])
    k, l = choosent(len_p, len_s)
    if t[k][l] == 1 or (k == i and l ==j):
       return k, l
    else:
       return chooseor(t, i, j)

def choosent(len_p, len_s):
   # print "self.pos=", self.pos
   # print "self.sam=", self.sam
    i = random.randrange(len_p)
    j = random.randrange(len_s)
    return i, j
def perfect(l1, l2): #judge perfect or not
    if l1 == l2:
       return 1
    else:
       return 0
def rai(T, bn, an, fix):
    len_p = len(T)
    len_s = len(T[0])
    originals, originalp = marginal(T)
    jac = makej(T)
    print "originaljac jac"
    for i in range(len_p):
        print jac[i]
    print "jac jac jac"
    for i in range(len_p):
        print jac[i]
    cmat = [[0 for j in range(len_p)] for i in range(len_p)]
    pmat = [[0 for j in range(len_p)] for i in range(len_p)]
    x = None
    y = None
    p = 0
    if fix == "s": f = follow_fixedsample
    elif fix == "p": f = follow_fixedposition
    elif fix == "b": f = follow
    print "function ", type(f)
    #originT = T
    for m in range(an):
        #T, x, y, p = f(originT, originals, originalp, x, y, p)
        beforeT, x, y, p = f(T, originals, originalp, x, y, p)
        #beforeT = deepcopy(T)
        print "beforeT"
        for i in range(len_p):#
            print beforeT[i]
        newjac = makej(beforeT)
        print "newjac="
        for i in range(len_p):
            print newjac[i]
        #pn, sn = marg(T)#
        T = np.copy(beforeT)
        #print "TTTTTTTTTTTTTTTT", T
        if m >= bn:
            for i in range(len_p):
                for j in range(i+1, len_p):
                    if newjac[i][j] >= jac[i][j]:
                        cmat[i][j] += 1
                    elif jac[i][j] == 0:
                        pass
    for i in range(len_p):
        for j in range(i+1, len_p):
            if cmat[i][j] > 0:
                c = cmat[i][j]/float(an-bn)
                print "////////////////////"
                print "cmat, cmat/total", cmat[i][j], cmat[i][j]/float(an-bn)
                t = -math.log10(c)
                #if t < 0: t = t*(-1)
                pmat[i][j] = t
                if t >= 1: print "i,j,cmat,jac,marginal, t", i, j, cmat[i][j], jac[i][j], originalp[i], originalp[j], t
            elif cmat[i][j] == 0 and jac[i][j] != 0:
                c = 0.5/float(an-bn)
                t = -math.log10(c)
                pmat[i][j] = t
            else:
                pmat[i][j] = None
    return pmat, cmat

def follow_fixedsample(givenT, originals, originalp, x, y, z):
    pos = len(givenT)
    sam = len(givenT[0])
    #T = [[0 for i in range(sam)] for i in range(pos)]
    T = np.transpose(givenT)
    for i in range(sam):
        random.shuffle(T[i])
    """
    print "len(oris)=", len(originals)
    print originals
    for i in range(len(originals)):
        l = []
        p = 0
        while p < originals[i]:
            r = random.randrange(pos)
            if r not in l:
                l.append(r)
                p += 1
        for j in range(len(l)):
            T[l[j]][i] = 1
    print "T="
    """
    givenT = np.transpose(T)
    print "Matrics"
    for i in range(pos):
        print givenT[i]
    return givenT, x, y, z
def follow_fixedposition(givenT, originals, originalp, x, y, z):
    pos = len(givenT)
    print "pos", pos
    sam = len(givenT[0])
    print "sam", sam
    T = [[0 for i in range(sam)] for i in range(pos)]
    for i in range(pos):
        random.shuffle(givenT[i])
    """
        rate = sum(givenT[i])
        print "rate", rate
        for j in range(sam):
            r = random.randrange(sam)
            #print r/float(sam)
            if r < rate:T[i][j] = 1
    #old permutation
    T = [[0 for i in range(sam)] for i in range(pos)]
    for i in range(len(originalp)):
        l = []
        p = 0
        while p < originalp[i]:
            r = random.randrange(sam)
            if r not in l:
                l.append(r)
                p += 1
        print "l", l
        for j in range(len(l)):
            T[i][l[j]] = 1
    print "T", T
    """
    return givenT, x, y, z

def follow(givenT, originals, originalp, i, j, p): # return binary table maybe new
    # i = position, j = sample
    if i is None and j is None:
       g = decident(givenT)
       i = copy.copy(g[0]) #i is position
       j = copy.copy(g[1]) #j is sample
    givens, givenp = marginal(givenT)    #list
    ps = perfect(originals, givens)
    pp = perfect(originalp, givenp)
    if pp*ps == 1:  # when perfect
       givenT[i][j] = 0
       p = p+1
       return np.array(givenT), i, j, p
    else: # when near-perfect
       k, l = chooseor(givenT, i, j)
       if k == i and l == j:
          givenT[i][j] = 1
          return np.array(givenT), i, j, p
       else:
          if random.randrange(10) >= 5: # preserve position margin
            if givenT[k][j] == 0:
               givenT[k][j] = 1
               givenT[k][l] = 0
               j = l
            return np.array(givenT), i, j, p
          else: # preserve sample marginal
             if givenT[i][l] == 0:
                givenT[i][l] = 1
                givenT[k][l] = 0
                i = k
             return np.array(givenT), i, j, p
def marg(Matrics):
    sam = len(Matrics[0])
    pos = len(Matrics)
    mp = []
    ms = []
    for i in range(pos):
        mp.append(sum(Matrics[i]))
    for j in range(sam):
        t = 0
        for i in range(pos):
            t += Matrics[i][j]
        ms.append(t)
    return mp, ms
def checkmarg(orig, new):
    if len(orig) != len(new):
        return False
    if orig == new:
        return True
    l = []
    for i in range(len(orig)):
        l.append(abs(orig[i]-new[i]))
    return l
def makej(Mat):
    n_p = len(Mat)
    n_s = len(Mat[0])
    jac = [[0 for i in range(n_p)]for j in range(n_p)]
    for i in range(n_p):
        for j in range(i+1, n_p):
            s = [Mat[i][k]*Mat[j][k] for k in range(n_s)]
            """
            print "s", s
            s = 0
            for k in range(n_s):
                if Mat[i][k]*Mat[j][k] == 1: s += 1
            """
            jac[i][j] = sum(s)
            jac[j][i] = sum(s)
    return jac
