#!/usr/bin/env python
import math

def factorial(n):
    num = 1
    while n >= 1:
        num = num*n
        n = n -1
    return num
def fisher_test(mat):
    n_p = len(mat)
    n_s = len(mat[0])
    p_mat = [[0 for i in range(n_p)]for j in range(n_p)]
    for i in range(n_p):
        for j in range(i+1, n_p):
            a = 0 #and
            b = 0 # i and n-j
            c = 0 # n-i and j
            d = 0 #n-i and n-j
            for k in range(n_s):
                if (mat[i][k] == 1 and mat[j][k] ==1):
                    a += 1
                elif (mat[i][k] == 1 and mat[j][k] == 0):
                    b += 1
                elif (mat[i][k] == 0 and mat[j][k] == 1):
                    c += 1
                elif (mat[i][k] == 0 and mat[j][k] == 0):
                    d += 1
            #print "a=",a," b=",b," c=",c," d=",d
            #if (d == 0):
            #    fisher = 1.0
            #else:
            fisher =factorial(a+b)*factorial(c+d)*factorial(a+c)*factorial(b+d)/float(factorial(a)*factorial(b)*factorial(c)*factorial(d)*factorial(n_s))
            p_mat[i][j] = -math.log10(fisher)
            p_mat[j][i] = -math.log10(fisher)
    return p_mat

"""
mat = [[0,1,0,0,1,1,1],[0,0,1,1,0,1,0]]
p = fisher_test(mat)
print p
"""
