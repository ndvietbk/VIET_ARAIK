#Program simulate queueing system in parallel
#Copyright (C) 2016 by Araik Tamazian, Viet Duc Nguyen
#Saint Petersburg  Electrotechnical University LETI

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import timeit
from datetime import datetime


#Extract time series needed for Hurst parameter analysis
infile = 'saskatchewan.txt'
data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)
data.columns = ['host','time','size']
data = data[data.time >= 0]
time = np.asarray(data.time)

# infile = 'ses_20081013.txt'
# data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True,usecols = [0])
# data.columns = ['time']
# data = data[data.time >= 0]                    #Drop negative time variable
# time1 = np.asarray(data['time'])
# time1 = np.diff(time1)
# time = np.insert(time1,0,0.0)
# time  = time/np.mean(time)
#-------------------------------------------------------------------------------------------------------------------

#----------Function for estimating Hurst by MF-DFA------------------------------------------------------------------------------------------
'''
    Function MF-DFA is used for estimating Hurst parameter of time series based on J.W. Kantelhardt's paper (2002)
        "Multifractal of detrended fluctuation analysis of non stationary time series"
    Input parameters:   1, indata: Time series
                        2, scale:  List or array variable define the sample sizes of the non-overlapping segments
                                for instance: scale = np.logspace(np.log10(10**1),np.log10(10**5),30)
                        3, q: order statistical moment
                        4, m: Polynomial trend (m=1: linear, m=2: quadratic, m=3: cubic)
                        Usually, q=2, m=1
    Output:             1, H: Hurst parameters. It is a float variable
                        2, scale: similar to input scale. It is a list (or array) variable
                        3, F: The fluctuation function. It is a list variable
'''

def DFA(indata,scale,q,m):
    y = np.cumsum(indata-indata.mean())             #Equation 1 in paper
    RMSt = []                                       #Temporary RMS variable: contain F(s,v) value
    F = []                                          #F: Fluctuation function
    N = len(indata)
    print 'len indata: ',N
    for i in range(len(scale)):
        ns = int(np.floor(len(y)/scale[i]))         #number of segments: Ns = int(N/s)
        for v in range(2*ns):
            if v < ns:
                index_start = v*scale[i]
                index_end = (v+1)*scale[i]
            else:
                index_start = N - (v-ns)*scale[i]-scale[i]
                index_end = N - (v-ns)*scale[i]
            index = range(index_start,index_end)    #calculate index for each segment
            yv = y[index_start:index_end]           #Extract values of time series for each segments
            c = np.polyfit(index,yv,m)
            fit = np.polyval(c,index)
            RMSt.append(math.sqrt(np.mean((yv-fit)**2))) #Equation 2. But calculating only F(v,s) not F(v,s)**2
        RMS = np.asarray(RMSt)                      #Convert RMSt to array
        qRMS = RMS**q
        F.append(np.mean(qRMS)**(1.0/q))              #Equation 4
        del RMSt[:]                                 #Reset RMSt[:]
    C = np.polyfit(np.log2(scale),np.log2(F),1)
    H = C[0]                                        #Hurst parameter
    return (H,scale,F)
#------------------- End DFA function -------------------------------------------------------------------------

if __name__ == '__main__':
    start_time = timeit.default_timer()                                         #Variale for calculate time of simulation
    print 'Time of beginning simulation: ', datetime.now()                      #Print current time


    scale = np.logspace(np.log10(10**1),np.log10(10**5),30)
    scale = scale.astype(int)
    H,scale,F = DFA(time,scale,2,2)

    C = np.polyfit(np.log2(scale),np.log2(F),1)
    regline = np.polyval(C,np.log2(scale))

    plt.loglog(scale,F,'>',color = 'black',markersize = 10)
    plt.plot(scale,2**regline,'r',linewidth = 2, label='Slope H = %0.2f'%C[0])

    plt.xlabel('Log10(Scale)',fontsize = 20,labelpad = 20)
    plt.ylabel('Log10(F fluct. func.)',fontsize = 20,labelpad = 20)

    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)

    plt.legend(loc = "upper left")
    plt.show()



