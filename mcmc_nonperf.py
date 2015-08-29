from random import randint
import sys

argvs = sys.argv

#${leng} ${leng} ${an} ${input} ${out}

num_steps = int(argvs[2])

datafile = argvs[3]

outfile = argvs[4]

leng = 50

sum_mat = [[0 for i in range(leng)] for j in range(leng)]
#mat[len_p][len_s]

def check_mat(mat, b_mat):#check whether new mat == before mat 
    return mat == b_mat

def decident(mat):
    match = False 

    while match is False:
        i = randint(0, leng-1)
        j = randint(0, leng-1)
        if mat[i][j] == 1:
           match = True 

    return i, j

def m_c(mat, original_s, original_p, ith, jth, p):
    marginal_p = [sum(mat[i]) for i in range(leng)]
    marginal_s = [0 for i in range(leng)]
    for i in range(leng):
        s = 0
        for j in range(leng):
            s += mat[j][i]
        marginal_s[i] = s

    if marginal_p == original_p and marginal_s == original_s:
        i, j = decident(mat)
        mat[i][j] = 0
        p = 0
        return mat, i, j, p
        #return mat, ith, jth, p
    else:
        if mat[ith][jth] == 0:
            mat[ith][jth] = 1
            p = 1
            return mat, ith, jth, p
        else:
            match = False
            while match is False:
                k = randint(0, leng-1)
                l = randint(0, leng-1)
                if mat[k][l] == 1:
                    match = True

            if k == ith and l == jth:
                if mat[ith][jth] == 0:
                    mat[ith][jth] = 1
                    p = 1
                return mat, ith, jth, p
            else:
                if randint(0, 9) < 5:
                    if mat[k][jth] == 0:
                        mat[k][jth] = 1
                        mat[k][l] = 0
                        jth = l
                        p = 0
                    return mat, ith, jth, p
               
                else:
                    if mat[ith][l] == 0:
                        mat[ith][l] = 1
                        mat[k][l] = 0
                        ith = k
                        p = 0
                    return mat, ith, jth, p
    return mat

def jaccade(mat):
    jmat = [[0 for i in range(leng)] for j in range(leng)]
    for i in range(leng):
        for j in range(i+1, leng):
            c = 0
            for k in range(leng): 
                if mat[i][k]*mat[j][k] == 1: 
                    c += 1 
            jmat[i][j] = c
            jmat[j][i] = c
    return jmat


def mcmc(num, d_file, o_file):
    original_data = []
    f = open(d_file, "r")
    for line in f:
        l = line.replace('\n', '').split(' ')
        #print "l", l
        original_data.append([int(x) for x in l])
    f.close()

    original_p = [sum(original_data[i]) for i in range(leng)]
    original_s = [0 for i in range(leng)]
    for i in range(leng):
        s = 0
        for j in range(leng):
            s += original_data[j][i]
        original_s[i] = s

    original_jmat = jaccade(original_data)
    count_n = 0

    mat = original_data

    cmat = [[0 for i in range(leng)] for j in range(leng)]
    
    p = 1
    mi = -1
    mj = -1

    while count_n < num:
        mat, mi, mj, p = m_c(mat, original_s, original_p, mi, mj, p)
        jmat = jaccade(mat)

        for i in range(leng):
            for j in range(i+1, leng):
                if jmat[i][j] > original_jmat[i][j]:
                    cmat[i][j] += 1
                    cmat[j][i] += 1
        count_n += 1

    tru = []
    fal = []

    pmat = [[0 for i in range(leng)] for j in range(leng)]
    for i in range(leng):
        for j in range(i+1, leng):
            if cmat[i][j] == 0:
                c = 0.5/num
            else: 
                c = cmat[i][j]/float(num)

            if (i == 0 and j == 1) or (i == 3 and j == 4):
                tru.append(c) 
            else: fal.append(c)

    fp = open('pos_'+o_file+'.out', 'a')
    fp.write(' '.join([str(x) for x in tru])+' ')
    fp.close()
    fn = open('neg_'+o_file+'.out', 'a')
    fn.write(' '.join([str(x) for x in fal])+' ')
    fn.close()

mcmc(num_steps, datafile, outfile)
