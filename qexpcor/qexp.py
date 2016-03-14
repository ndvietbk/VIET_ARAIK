#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Araik Tamazian, Viet Duc Nguyen

import numpy as np

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
    u = np.random.uniform(0,1,size=(1,N))[0]
    y = -q1*ts_qlog(u,q1)/rate
    return y