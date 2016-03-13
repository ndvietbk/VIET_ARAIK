import pandas as pd
import numpy as np
import math


def DFA(indata,q,m):
    scale = np.logspace(np.log10(10**1),np.log10(10**3),10)
    scale = scale.astype(int)
    y = np.cumsum(indata-indata.mean())             #Equation 1 in paper
    RMSt = []                                       #Temporary RMS variable: contain F(s,v) value
    F = []                                          #F: Fluctuation function
    for i in range(len(scale)):
        ns = int(np.floor(len(y)/scale[i]))         #number of segments: Ns = int(N/s)
        for v in range(ns):
            index_start = v*scale[i]
            index_end = (v+1)*scale[i]
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
    return(H)

def correlate(x,b):
    N = len(x)
    #FFT
    xft = np.fft.fft(x)
    #Modify power spectrum
    xft[0]=0
    ind1 = np.linspace(2, N/2, N/2-2)
    f = (0.5*np.divide(ind1,N))**(-b/2.0)
    xft[2:N/2]= np.multiply(xft[2:N/2], f)
    xft[N/2+1:N-1]= np.multiply(xft[N/2+1:N-1], f)
  #  xft[N] = xft[N]*0.5**(-b/2)
    #inverse FFT
    x1 = np.fft.ifft(xft).real
    #Result normaliztion
    y = x1*((N/np.sum(x1**2))**0.5)
    return(y)

def schriber(x, H, Htol, Hstep, maxiter):
    iter = 0
    Hcor = H
    He = 0
    N = len(x)
    x = np.sort(x)
    y1 = np.random.normal(size =N)
    while((He < H-Htol)|(He>H+Htol))&(iter<maxiter):
        y = y1
        y = correlate(y,Hcor)
        z = np.sort(y)
        p = sorted(range(len(y)),key=lambda x:y[x])
        y[p] = x
        He = DFA(y,2,2)
        print He
        Hcor = 2*(Hcor + Hstep)
        iter = iter +1
    return y,iter


def main():
    infile = 'norm_1.txt'
    data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)
    data.columns = ['T']
    time = np.asarray(data.T)
    time = time.flatten()
    y = correlate(time, 0.7)
    #y,iter = schriber(time, 0.8, 0.1, 0.01,1000)
    #print iter
    Hy = DFA(y,2,2)
    print Hy


if __name__ == '__main__':
    main()