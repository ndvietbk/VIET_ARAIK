import pandas as pd
import numpy as np
from gg1_function import simulate_gg1, qexp_rate, rand_qexp, simulate_MM1

def kingman_estimate(time,size):
    lamb_da = 1/np.mean(time)
    mu = 1/np.mean(size)
    ca = np.std(time)/np.mean(time)
    cs = np.std(size)/np.mean(size)
    p = lamb_da/mu
    #y = p*(ca**2 + cs**2)/((1-p)*2*mu)
    y = (p/(1-p))*0.5*(ca**2 + cs**2)/lamb_da+1/mu
    return y

def main():

    infile = 'ses_20081013.txt'
    data1 = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
    data1.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
    data1 = data1[data1.time >= 0]                    #Drop negative time variable
    data =data1[0:10**6]
    time1 = np.asarray(data['time'])
    time1 = np.diff(time1)
    time = np.insert(time1,0,0.0)
    ssize = data['size']

    timess = pd.read_csv('sstime.txt')
    timess = np.asarray(timess)
    timess = timess.flatten()

    ssizess = pd.read_csv('sssize.txt')
    ssizess = np.asarray(ssizess)
    ssizess = ssizess.flatten()

    c=np.logspace(np.log10(8*10**6.2), np.log10(8*10**8),10);
    a1 = []
    a2 = []
    am = []
    n = 10**5
    for i in range(len(c)):
        a1.append(simulate_gg1(n,time,ssize/c[i]))
        d1 = pd.DataFrame(a1)
        a2.append(simulate_gg1(n,timess,ssizess/c[i]))
        d2 = pd.DataFrame(a2)
        am.append(simulate_MM1(1/np.mean(time), 1/np.mean(ssize/c[i])))
        dm = pd.DataFrame(am)
    print('\nParameters of queueing system using empirical data')
    print(d1)
    print('\nParameters of queueing system using q exponential distribution series with s-s method')
    print(d2)
    #print('\nEstimate parameter W using Kingman formula')
    #print(dk)
    print('\nParameters of queueing system MM1')
    print(dm)

    print("column 0: Utilization     Column 1: W     Column 2:    L")


if __name__ == '__main__':
    main()
