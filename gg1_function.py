#Simulate queuing system G/G/1
#@Author: Nguyen Duc Viet
import random as rd
import numpy as np
import simpy


#Function for epirical data --------------------------------------------------------------------------------------------
data_wt = []
def arrival(env, number,counter,interval,time_service):
    for i in range(number):
        t = interval[i]
        yield env.timeout(t)
        c = service(env,'Customer %02d'%i,counter,i,time_service[i])
        env.process(c)


def service(env,name, counter,i, time_service):
    arrive = env.now
    with counter.request() as req:
        yield req
        wait = env.now - arrive
        #print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        data_wt.append(wait)
        ts = time_service
        yield env.timeout(ts)
        #print('%7.4f %s: Finished' % (env.now, name))


def simulate_gg1(n,interval_time,time_service):
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=1)
    t = env.now
    env.process(arrival(env,n,counter,interval_time,time_service))
    env.run()
    t = env.now - t
    #print("\nTotal simulation time: %f"% t)
    tw = np.array(data_wt)
    ts = np.array(time_service)
    del data_wt[:]                              #reset list variable containing waiting time
    b=0   #busy time of server
    for i in range(n):
        b = b+ts[i]
    t_in_system =  tw.sum() + b         #     Total time spent in system of all packet = total waiting time + total service time
    #print("Total waiting time of %i packets: %f" %(n,tw.sum()))
    #print("Total time spent in system of %i packets: %f\n" %(n,t_in_system))

    #Caculate output parameters: Utilization; mean time spent in system; mean number of clients
    u = b/t
    w = t_in_system/n                           #Mean time spent in system
    l = t_in_system/t                           #Mean number of clients in the system
    return (u,w,l)
#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
#function for simulating M/M/1
def simulate_MM1(lamb_da,mu):
    u = lamb_da/mu
    if u>1:
        u=1
    W =1/(mu-lamb_da)
    Wq = W - 1/mu
    L = lamb_da*W
    return (u,W,L)
#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
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
