#!/usr/bin/env python

import sys
import itertools
import random
#import reverse_array as rev

def creat(sa, po, m, n, la, noise): # size of matrix is i(samp)*j(posi), mth and nth row co-occurence and la is len of aberration
    #l = [[0 for y in range(po)]for x in range(sa)] # y is position and x is sample
    l = [[0 for y in range(sa)]for x in range(po)] # y is position and x is sample
#    a = [x for x in range(j)]
    s = somechoose(po, la)
    print "s=", s
#    print "a=", a
    for x in range(po):
        for y in range(sa):
            if random.randrange(10) > noise-1:#parameter of noise
               l[x][y] = 1
            if y == m or y == n:
                for z in range(la):
                    l[s[z]][y] = 1
    return l

def somechoose(i, j):#i is whole number and j is number chosen up
    a = []
    l=[0 for n in range(i)]
    while  sum(l) != j:
        n = random.randrange(i)
        if l[n] == 0:
            l[n] = 1
            a.append(n)
        else :
            pass
    return a

#c = creat(8, 10, 2, 5, 5, 7) #3 is sample, 10 is position
