#Program simulate queueing system in parallel
#Copyright (C) 2016 by Araik Tamazian, Viet Duc Nguyen

import pandas as pd
import numpy as np
from gg1_function import simulate_gg1, qexp_rate, rand_qexp, simulate_mm1
import matplotlib.pyplot as plt
import timeit
import multiprocessing
from joblib import Parallel, delayed

#Import external file containing empirical data (time and size)
infile = 'ses_20081013.txt'
data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
data.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
data = data[data.time >= 0]                    #Drop negative time variable
time1 = np.asarray(data['time'])
time1 = np.diff(time1)
time = np.insert(time1,0,0.0)
time  = time/np.mean(time)
ssize = data['size']
ssize = ssize/np.mean(ssize)
print 'len time:', len(time)
print 'len size: ', len(ssize)

#Import surrogate time
timess = pd.read_csv('sur_time_20081013_2.txt')
timess = np.asarray(timess)
timess = timess.flatten()
ssizess = pd.read_csv('sur_size_20081013_2.txt')
ssizess = np.asarray(ssizess)
ssizess = ssizess.flatten()
print 'len timess:',len(timess)
print 'len ssizess: ',len(ssizess)

#Declare variables
res_mm1 =[]                                                     #Variale gets results of simulating MM1
n = 10**6                                                       #Number of data samples (data lines) needed simulating
c=np.logspace(np.log10(1.2), np.log10(10),10)                   #Values of throughput
inputs = range(len(c))                                          #Variable for loop in parallel

#Function for simulating queueing system with empirical data in parallel via throughput
def processInput(i):
    return simulate_gg1(n,time,ssize/c[i])

#Function for simulating queueing system with surrogate data in parallel via throughput
def processInputs(i):
    return simulate_gg1(n,timess,ssizess/c[i])
if __name__ == '__main__':
    start_time = timeit.default_timer()                                         #Variale for calculate time of simulation

    #Simulate queueing system with empirical data, surrogate data and MM1
    res_real  = Parallel(n_jobs=3)(delayed(processInput)(i) for i in inputs)    #With empirical data
    print 'empirical data:', res_real

    res_sur  = Parallel(n_jobs=3)(delayed(processInputs)(i) for i in inputs)    #With surrogate data
    print 'Surrogate data:', res_sur

    for i in range(len(c)):                                                     #Queueing system MM1
        res_mm1.append(simulate_mm1(1/np.mean(time), 1/np.mean(ssize/c[i])))

    #Convert results from array into data.frame using thoughput like index and save into txt files
    res_real = pd.DataFrame(data = res_real,index=c, columns=['Ur','Wr','Lr'])
    res_sur = pd.DataFrame(data = res_sur,index=c, columns=['Us','Ws','Ls'])
    res_mm1 = pd.DataFrame(data = res_mm1,index=c, columns=['Um','Wm','Lm'])

    res_real.to_csv("simres_real.txt", sep=" ", header=False)
    res_sur.to_csv("simres_sim.txt", sep=" ", header=False)
    res_mm1.to_csv("simres_mm1.txt", sep=" ", header=False)



    #------Plot multigraphs in one panel (subplot)-------
    #Plot Utilization versus throughput
    plt.subplot(1,3,1)                                              #plt.subplot(row,column, position)
    plt.plot(c,res_real['Ur'], color = 'black',linewidth = 2)
    plt.plot(c,res_sur['Us'], color = 'red',linewidth = 2)
    plt.plot(c,res_mm1['Um'], color = 'green',linewidth = 2)
    plt.xlabel('Channel throughput, C', size = 15)
    plt.ylabel('Utilization, U', size = 15)
    plt.yscale('log')
    plt.xscale('log')
    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)
    plt.legend(loc = "upper right")

    #Plot Average sojourn time in system versus throughput
    plt.subplot(1,3,2)
    plt.plot(c,res_real['Wr'], color = 'black',linewidth = 2)
    plt.plot(c,res_sur['Ws'], color = 'red',linewidth = 2)
    plt.plot(c,res_mm1['Wm'], color = 'green',linewidth = 2)
    plt.xlabel('Channel throughput, C', size = 15)
    plt.ylabel('Average soujourn time,W', size = 15)
    plt.yscale('log')
    plt.xscale('log')
    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)
    plt.legend(loc = "upper right")

    #Plot Average number of requests in system versus throughput
    plt.subplot(1,3,3)
    plt.loglog(c,res_real['Lr'], color = 'black',linewidth = 2)
    plt.loglog(c,res_sur['Ls'], color = 'red',linewidth = 2)
    plt.loglog(c,res_mm1['Lm'], color = 'green',linewidth = 2)
    plt.xlabel('Channel throughput, C', size = 15)
    plt.ylabel('Average request in system, L', size = 15)
    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)
    plt.yscale('log')
    plt.xscale('log')
    plt.legend(loc = "upper right")

    stop_time = timeit.default_timer()
    time_simulation = stop_time - start_time
    print 'simulation time: ', time_simulation

    plt.savefig('n206.png')
    plt.show()


#---------------end-----------------------------------------------------------------------------------------------------
