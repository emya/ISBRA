#!/usr/bin/env python

import sys
import os
import time
import commands
import create_data as c_d
#from transfer_concretedata import read_and_writedata_sim_interval
#from showdata import color_data_simulate
from pr_plot_simulation import plot_pr

argvs = sys.argv

def pn_file(name):
    p_parent = "pos_"+name+".out"
    n_parent = "neg_"+name+".out"
    fp = open(p_parent, "w")
    fn = open(n_parent, "w")
    for i in range(5):
        file_p = "pos_"+name+"_"+str(i)+".out"
        file_n = "neg_"+name+"_"+str(i)+".out"
        f1 = open(file_p, "r")
        f2 = open(file_n, "r")
        line = f1.readlines()
        fp.writelines(line)
        f1.close()
        line = f2.readlines()
        fn.writelines(line)
        f2.close()
    fp.close()
    fn.close()


def line_process(leng, signal, variance, contrue, num):
    #pid = os.getpid()
    print "process starts!"

    out_fisher = "simulation-fisher_exclusive_"+"len"+str(leng)+"sig"+str(signal)+"vari"+str(variance)+"noise"+str(contrue)
    out_proposed = "simulationout-proposedmcmcp_exclusive_len"+str(leng)+"sig"+str(signal)+"vari"+str(variance)+"noise"+str(contrue)
    out_existing = "simulationout-proposedmcmcn_exclusive_len"+str(leng)+"sig"+str(signal)+"vari"+str(variance)+"noise"+str(contrue)
    out_poisson_p = "simulationout-poisson_pp_len"+str(leng)+"sig"+str(signal)+"vari"+str(variance)+"noise"+str(contrue)
    out_poisson_s = "simulationout-poisson_ss_len"+str(leng)+"sig"+str(signal)+"vari"+str(variance)+"noise"+str(contrue)

    inproposed1 = out_proposed+"_num"+str(num*5)
    inproposed2 = out_proposed+"_num"+str(num*5*10)

    inexisting1 = out_existing+"_num"+str(num*5)
    inexisting2 = out_existing+"_num"+str(num*5*10)

    cmd = ":> pos_"+out_fisher+".out"
    os.system(cmd)
    cmd = ":> neg_"+out_fisher+".out"
    os.system(cmd)
    cmd = ":> pos_"+inproposed1+".out"
    os.system(cmd)
    cmd = ":> pos_"+inproposed2+".out"
    os.system(cmd)
    cmd = ":> neg_"+inproposed1+".out"
    os.system(cmd)
    cmd = ":> neg_"+inproposed2+".out"
    os.system(cmd)

    cmd = ":> pos_"+inexisting1+".out"
    os.system(cmd)
    cmd = ":> pos_"+inexisting2+".out"
    os.system(cmd)
    cmd = ":> neg_"+inexisting1+".out"
    os.system(cmd)
    cmd = ":> neg_"+inexisting2+".out"
    os.system(cmd)

    cmd = ":> pos_"+out_poisson_p+".out"
    os.system(cmd)
    cmd = ":> neg_"+out_poisson_p+".out"
    os.system(cmd)

    cmd = ":> pos_"+out_poisson_s+".out"
    os.system(cmd)
    cmd = ":> neg_"+out_poisson_s+".out"
    os.system(cmd)

    for i in range(5):
        print "i=%d", i
        sys.stdout.flush()

        cmd = "sh throw_child_fisher_exclusive.sh "+out_fisher+" "+out_proposed+" "+out_existing+" "+out_poisson_p+" "+out_poisson_s+" "+str(i)+" "+str(leng)+" "+str(signal)+" "+str(variance)+" "+str(contrue)+" "+str(num)+" "+str(i)+""
        os.system(cmd)
    """
    tmp = 1
    while tmp > 0:
        time.sleep(10)
        tmp = int(commands.getoutput("qstat| grep "+"out_"+str(pid)+" |wc").split()[0])
    """

    p_fisher = "pos_"+out_fisher+".out"
    n_fisher = "neg_"+out_fisher+".out"
    p_poi_p = "pos_"+out_poisson_p+".out"
    n_poi_p = "neg_"+out_poisson_p+".out"
    p_poi_s = "pos_"+out_poisson_s+".out"
    n_poi_s = "neg_"+out_poisson_s+".out"

    pn_file(out_fisher)
    pn_file(out_poisson_p)
    pn_file(out_poisson_s)

    """
    p_fisher = "pos_"+out_fisher+".out"
    n_fisher = "neg_"+out_fisher+".out"
    fp = open(p_fisher, "w")
    fn = open(n_fisher, "w")
    for i in range(5):
        file_p = "pos_"+out_fisher+"_"+str(i)+".out"
        file_n = "neg_"+out_fisher+"_"+str(i)+".out"
        f1 = open(file_p, "r")
        f2 = open(file_n, "r")
        line = f1.readlines()
        fp.writelines(line)
        f1.close()
        line = f2.readlines()
        fn.writelines(line)
        f1.close()
    fp.close()
    fn.close()
    """

    p_proposed1="pos_"+inproposed1+".out"
    n_proposed1="neg_"+inproposed1+".out"
    p_existing1="pos_"+inexisting1+".out"
    n_existing1="neg_"+inexisting1+".out"
    p_proposed2="pos_"+inproposed2+".out"
    n_proposed2="neg_"+inproposed2+".out"
    p_existing2="pos_"+inexisting2+".out"
    n_existing2="neg_"+inexisting2+".out"

    plot_pr(leng, out_fisher, p_fisher, n_fisher)
    plot_pr(leng, out_poisson_p, p_poi_p, n_poi_p)
    plot_pr(leng, out_poisson_s, p_poi_s, n_poi_s)
    plot_pr(leng, inproposed1, p_proposed1, n_proposed1)
    plot_pr(leng, inexisting1, p_existing1, n_existing1)

    print "inproposed2", inproposed2, "p_proposed2", p_proposed2

    plot_pr(leng, inproposed2, p_proposed2, n_proposed2)
    plot_pr(leng, inexisting2, p_existing2, n_existing2)
    return 0

leng = int(argvs[1])
signal = int(argvs[2])
variance = float(argvs[3])
contrue = float(argvs[4])
num = int(argvs[5])
line_process(leng, signal, variance, contrue, num)
