#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Araik Tamazian, Viet Duc Nguyen
import pandas as pd
import numpy as np
import math
import scipy.special as sp
import cmath as cm
import matplotlib.pyplot as plt

#Function for simulating QE/QE/1
def qexp_rate(q, ave):
    rate = 1/(ave*(3-2*q))
    return rate

def ts_qlog(x,q):
    if q==1:
        y=np.log(x)
    else:
        y = (x**(1-q)-1)/(1-q)
    return y
def rand_qexp(N,q,rate):
    q1 = 1/(2-q)
    u = np.random.uniform(0,1,size=(1,N))
    y = -q1*ts_qlog(u,q1)/rate
    return y
#----------------------------------------------------------------------------


def DFA(indata,q,m):
    scale = np.logspace(np.log10(10**1),np.log10(10**5),10)
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

def fgnoise(n, H):
    w = np.linspace(2*np.pi/n, np.pi, n/2-1)
    Aw = 2*np.sin(np.pi*H)*sp.gamma(2*H+1)*(1-np.cos(w))
    d = -2*H-1
    d1 = -2*H

    a1 = 2*np.pi+w
    a2 = 4*np.pi+w
    a3 = 6*np.pi+w
    a4 = 8*np.pi+w

    b1 = 2*np.pi-w
    b2 = 4*np.pi-w
    b3 = 6*np.pi-w
    b4 = 8*np.pi-w

    Bw1 = (a3**d1 + b3**d1 + a4**d1 + b4**d1)/(8*H*np.pi)
    Bw = a1**d + b1**d + a2**d + b2**d + a3**d + b3**d +Bw1
    Sw = Aw*(np.abs(w)**(-2*H-1) + Bw)

    Z = np.zeros(n/2, dtype=complex)
    Zph = np.random.uniform(0, 2*np.pi, n/2-1)
    #Z = cm.rect(Sw**0.5, Zph)
    Z = np.vectorize(cm.rect)(Sw**0.5, Zph)

    Z1 = np.zeros(n, dtype=complex)
    Z1[0] = 0
    Z1[1:n/2] = Z
    Z1[n/2+1:n] = np.conj(Z)

    x = np.fft.ifft(Z1).real
    return(x)


def schriber(x, H, Htol, maxiter):
    iter = 0
    Hcor = H
    He = 0
    N = len(x)
    x = np.sort(x)
    while((He < H-Htol)|(He>H+Htol))&(iter<maxiter):
        y = fgnoise(N,Hcor)
        z = np.sort(y)
        p = sorted(range(len(y)),key=lambda x:y[x])
        y[p] = x
        He = DFA(y,2,2)
        print He
        Hcor = Hcor + (Hcor-He)
        iter = iter +1
    return y,iter


def main():
    infile = 'ses_20081013.txt'
    data1 = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
    data1.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
    data1 = data1[data1.time >= 0]                    #Drop negative time variable
    data =data1[0:10**6]
    size = np.asarray(data['size'])



    Hsas = DFA(size,2,2)
    print 'Hurst parameter of inter-arrival size of ses_20081013: ', Hsas
    np.savetxt('size.txt',size,header='none')

    size_ave = size.mean()
    q=1.24
    rate= qexp_rate(q, size_ave)
    a = len(size)
    sizet = rand_qexp(a,q,rate)
    sizet = sizet.flatten()
    np.savetxt('qexp_sizet.txt',sizet,header='none')
    Hq = DFA(sizet,2,2)
    print 'Hurst parameter of surrogate size series: ', Hq

    y,itr = schriber(sizet, Hsas, 0.02, 1000)
    print 'iteration: ',itr
    Hy = DFA(y,2,2)
    print 'Hurst parameter of surrogate size series with s-s method: ', Hy
    np.savetxt('sssize.txt',y,header='none')
if __name__ == '__main__':
    main()



# def main():
#     infile = 'ses_20081013.txt'
#     data1 = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
#     data1.columns = ['time','ip', 'numcon', 'size']   # Sign names for columns
#     data1 = data1[data1.time >= 0]                    #Drop negative time variable
#     data =data1[0:10**6]
#     time1 = np.asarray(data['time'])
#     time1 = np.diff(time1)
#     time = np.insert(time1,0,0.0)
#
#
#     Hsas = DFA(time,2,2)
#     print 'Hurst parameter of inter-arrival time of ses_20081013: ', Hsas
#     np.savetxt('time.txt',time,header='none')
#
#     time_ave = time.mean()
#     q1=1.07
#     rate1= qexp_rate(q1, time_ave)
#     a = len(time)
#     timet = rand_qexp(a,q1,rate1)
#     timet = timet.flatten()
#     np.savetxt('qexp_timet.txt',timet,header='none')
#     Hq = DFA(timet,2,2)
#     print 'Hurst parameter of surrogate time series: ', Hq
#
#     y,itr = schriber(timet, Hsas, 0.02, 1000)
#     print 'iteration: ',itr
#     Hy = DFA(y,2,2)
#     print 'Hurst parameter of surrogate time series with s-s method: ', Hy
#     np.savetxt('sstime.txt',y,header='none')
# if __name__ == '__main__':
#     main()
