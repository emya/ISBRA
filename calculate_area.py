#!/usr/bin/env python

import sys
from math import fabs

argvs = sys.argv
argc = len(argvs)

"""
f_x = open(argvs[1], "r")
f_y = open(argvs[2], "r")

line_x = f_x.readline()
line_y = f_y.readline()
line_x = line_x.split()
line_y = line_y.split()
"""

def area(list_x, list_y):
    len_x = len(list_x)
    len_y = len(list_y)
    if (len_x != len_y):
        print "defferent length!\n"
        quit()
    total = 0
    print total
    for i in range(1,len_x):
        total += fabs( float(list_x[i])-float(list_x[i-1]) )*( (
            float(list_y[i])+float(list_y[i-1]))/2 )
    return total
