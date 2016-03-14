import pandas as pd
import numpy as np
from gg1_function import simulate_gg1, qexp_rate, rand_qexp, simulate_mm1
import matplotlib.pyplot as plt
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
    data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
    data.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
    data = data[data.time >= 0]                    #Drop negative time variable
    time1 = np.asarray(data['time'])
    time1 = np.diff(time1)
    time = np.insert(time1,0,0.0)
    time  = time/np.mean(time)
    ssize = data['size']
    ssize = ssize/np.mean(ssize)

    timess = pd.read_csv('sur_time_20081013.txt')
    timess = np.asarray(timess)
    timess = timess.flatten()

    ssizess = pd.read_csv('sur_size_20081013.txt')
    ssizess = np.asarray(ssizess)
    ssizess = ssizess.flatten()

    c=np.logspace(np.log10(2), np.log10(10),10)
    a1 = []
    a2 = []
    am = []
    n = 10**5
    for i in range(len(c)):
        a1.append(simulate_gg1(n,time,ssize/c[i]))
        a2.append(simulate_gg1(n,timess,ssizess/c[i]))
        am.append(simulate_mm1(1/np.mean(time), 1/np.mean(ssize/c[i])))
    d1 = pd.DataFrame(data = a1,index=c, columns=['Ur','Wr','Lr'])
    d2 = pd.DataFrame(data = a2,index=c, columns=['Us','Ws','Ls'])
    dm = pd.DataFrame(data = am,index=c, columns=['Um','Wm','Lm'])
    print('\nParameters of queueing system using empirical data')
    print(d1)
    print('\nParameters of queueing system using q exponential distribution series with s-s method')
    print(d2)
    print('\nParameters of queueing system mm1')
    print(dm)
    print("column 0: Utilization     Column 1: W     Column 2:    L")

    plt.subplot(1,3,1)                                  #plt.subplot(row,column, position)
    plt.plot(c,d1['Ur'], color = 'black',linewidth = 2)
    plt.plot(c,d2['Us'], color = 'red',linewidth = 2)
    plt.plot(c,dm['Um'], color = 'green',linewidth = 2)
    plt.xlabel('Channel throughput, C', size = 15)
    plt.ylabel('Utilization, U', size = 15)
    plt.yscale('log')
    plt.xscale('log')
    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)
    plt.legend(loc = "upper right")


    plt.subplot(1,3,2)
    plt.plot(c,d1['Wr'], color = 'black',linewidth = 2)
    plt.plot(c,d2['Ws'], color = 'red',linewidth = 2)
    plt.plot(c,dm['Wm'], color = 'green',linewidth = 2)
    plt.xlabel('Channel throughput, C', size = 15)
    plt.ylabel('Average soujourn time,W', size = 15)
    plt.yscale('log')
    plt.xscale('log')
    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)
    plt.legend(loc = "upper right")

    plt.subplot(1,3,3)
    plt.loglog(c,d1['Lr'], color = 'black',linewidth = 2)
    plt.loglog(c,d2['Ls'], color = 'red',linewidth = 2)
    plt.loglog(c,dm['Lm'], color = 'green',linewidth = 2)
    plt.xlabel('Channel throughput, C', size = 15)
    plt.ylabel('Average request in system, L', size = 15)
    plt.xticks(color='black', size=15)
    plt.yticks(color='black', size=15)
    plt.yscale('log')
    plt.xscale('log')
    plt.legend(loc = "upper right")

    plt.show()

if __name__ == '__main__':
    main()
