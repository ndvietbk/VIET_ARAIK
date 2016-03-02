import pandas as pd
import numpy as np
from gg1_function import simulate_gg1, qexp_rate, rand_qexp

def kingman_estimate(time,size):
    lamb_da = 1/np.mean(time)
    mu = 1/np.mean(size)
    ca = np.std(time)/np.mean(time)
    cs = np.std(size)/np.mean(size)
    p = lamb_da/mu
    y = p*(ca**2 + cs**2)/((1-p)*2*mu)
    return y

def main():
    #Import file from system, this file contains inter-arrival time and size of request file
    infile ='~/Dropbox/Rproj/beck_check/data/ses_20081013.txt'
    data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
    data.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
    data = data[data.time >= 0]                                               #Drop negative time variable
    time = np.asarray(data['time'])
    time = np.diff(time)
    ssize = np.asarray(data['size'])

    time_ave = time.mean()
    ssize_ave = ssize.mean()


    q1 = 1.30
    q2 = 1.32
    rate1= qexp_rate(q1, time_ave)
    rate2=qexp_rate(q2, ssize_ave)

    n = 10000
    timet = rand_qexp(n,q1,rate1)
    ssizet = rand_qexp(n,q2,rate2)
    timet = timet.flatten()
    ssizet = ssizet.flatten()

    c=np.logspace(np.log10(8*10**8), np.log10(8*10**9), 5);

    a1 = []
    a2 = []
    ak = []    #estimate w by kingman formula
    for i in range(len(c)):
        a1.append(simulate_gg1(n,time,ssize/c[i]))
        d1 = pd.DataFrame(a1)
        a2.append(simulate_gg1(n,timet,ssizet/c[i]))
        d2 = pd.DataFrame(a2)
        ak.append(kingman_estimate(timet,ssizet/c[i]))
        dk = pd.DataFrame(ak)
    print('\nParameters of queueing system using empirical data')
    print(d1)
    print('\nParameters of queueing system using q exponential distribution series')
    print(d2)
    print('\nEstimate parameter W using Kingman formula')
    print(dk)


    print("column 0: Utilization     Column 1: W     Column 2:    L")
    
    
if __name__ == '__main__':
    main()
