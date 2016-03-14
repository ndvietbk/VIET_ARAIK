import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gg1_function import simulate_gg1, simulate_mm1, qexp_rate, rand_qexp


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

    #Import file from system, this file contains inter-arrival time and size of request file
    infile ='~/Dropbox/Rproj/beck_check/data/ses_20081013.txt'
    #infile = 'ses_20081013.txt'

    # Read file without header and using space delimiter
    data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)
    data.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
    data = data[data.time >= 0]                # Omit negative time variable
    time = np.asarray(data['time'])
    time = np.diff(time)

    ssize = np.asarray(data['size'])

    time_ave = np.mean(time)
    ssize_ave = np.mean(ssize)

    time = np.divide(time, time_ave)
    ssize = np.divide(ssize, ssize_ave)

    #Import file from system, this file contains inter-arrival time and size of request file
    infilet ='sur_time_20081013.txt'
    data = pd.read_csv(infilet,header=None, na_filter = True)
    timet = np.asarray(data.T[0])

    infilet2 ='sur_size_20081013.txt'
    data = pd.read_csv(infilet2,header=None, na_filter = True)
    ssizet = np.asarray(data.T[0])

    n = len(timet)
    c=np.logspace(np.log10(2), np.log10(10), 10)
    a1 = []
    a2 = []
    #ak = []    #estimate w by kingman formula
    am = []
    for i in range(len(c)):
        a1.append(simulate_gg1(n, time, ssize/c[i]))
        a2.append(simulate_gg1(n, timet, ssizet/c[i]))
        am.append(simulate_mm1(1, c[i]))
        #ak.append(kingman_estimate(timet,ssizet/c[i]))
        #dk = pd.DataFrame(ak)
    colnames=['Util', 'Av.soj.time', 'Av.users']
    d1 = pd.DataFrame(data = a2, index=c, columns=colnames)
    d2 = pd.DataFrame(data = a2, index=c, columns=colnames)
    dm = pd.DataFrame(data = am, index=c, columns=colnames)
    d1.to_csv("simres_real.txt", sep=" ", header=False)
    d2.to_csv("simres_sim.txt", sep=" ", header=False)
    dm.to_csv("simres_mm1.txt", sep=" ", header=False)

    print('\nParameters of queueing system using empirical data')
    print(d1)
    print('\nParameters of queueing system using q exponential distribution series')
    print(d2)
    print('\nParameters of queueing system M/M/1')
    print(dm)
    #print('\nEstimate parameter W using Kingman formula')
    #print(dk)


if __name__ == '__main__':
    main()
