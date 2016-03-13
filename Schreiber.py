#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 by Araik Tamazian, Viet Duc Nguyen

#import pandas as pd
import numpy as np
import math
import scipy.special as sp
import cmath as cm

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
    #infile = 'norm_1.txt'
    #data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)
    #data.columns = ['T']
    #time = np.asarray(data.T)
    #time = time.flatten()
    y1 = np.random.exponential(1, size = 5e+5)
    y,itr = schriber(y1, 0.7, 0.02, 1000)
    print itr
    Hy = DFA(y,2,2)
    print Hy


if __name__ == '__main__':
    main()
