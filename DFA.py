import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def main():
    #infile = 'ses_20081013.txt'
    infile = 'saskatchewan.txt'
    data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)
    #data.columns = ['time','ip', 'numcon', 'size']
    data.columns = ['host','time','size']
    data = data[data.time >= 0]
    #data.time = np.diff(data.time)
    time = np.asarray(data.time)
    x = np.cumsum(time-time.mean())
    scale = np.logspace(np.log10(10**1),np.log10(10**5),30)
    scale = scale.astype(int)
    q=2
    m=1
    RMSt = []
    Fq = []
    for i in range(len(scale)):
        ns = int(np.floor(len(x)/scale[i]))
        for v in range(ns):
            index_start = v*scale[i]
            index_end = (v+1)*scale[i]
            index = range(index_start,index_end)
            xv = x[index_start:index_end]
            c = np.polyfit(index,xv,m)
            fit = np.polyval(c,index)
            RMSt.append(math.sqrt(np.mean((xv-fit)**2)))
        RMS = np.asarray(RMSt)
        qRMS = RMS**q
        Fq.append(np.mean(qRMS)**(1/q))
        del RMSt[:]
    print(Fq)
    C = np.polyfit(np.log2(scale),np.log2(Fq),m)
    regline = np.polyval(C,np.log2(scale))
    plt.loglog(scale,Fq,'>',color = 'black',markersize = 10)
    plt.plot(scale,2**regline,'r',linewidth = 2, label='Slope H = %0.2f'%C[0])
    plt.legend(loc = "upper left")
    plt.show()
if __name__ == '__main__':
    main()

