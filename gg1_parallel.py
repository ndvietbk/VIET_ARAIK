import pandas as pd
import numpy as np
from gg1_function import simulate_gg1, qexp_rate, rand_qexp, simulate_mm1
import matplotlib.pyplot as plt
import timeit
import multiprocessing
from joblib import Parallel, delayed

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
print 'len time:', len(time)
print 'len size: ', len(ssize)
timess = pd.read_csv('sur_time_20081013_8.txt')
timess = np.asarray(timess)
timess = timess.flatten()
ssizess = pd.read_csv('sur_size_20081013_8.txt')
ssizess = np.asarray(ssizess)
ssizess = ssizess.flatten()
print 'len timess:',len(timess)
print 'len ssizess: ',len(ssizess)
n = 10**6
c=np.logspace(np.log10(1.2), np.log10(10),10)
inputs = range(len(c))


def processInput(i):
    return simulate_gg1(n,time,ssize/c[i])
def processInputs(i):
    return simulate_gg1(n,timess,ssizess/c[i])
if __name__ == '__main__':
    start_time = timeit.default_timer()


    num_cores = multiprocessing.cpu_count()
    results1  = Parallel(n_jobs=5)(delayed(processInput)(i) for i in inputs)
    print 'empirical data:', results1
    results2  = Parallel(n_jobs=5)(delayed(processInputs)(i) for i in inputs)
    print 'Surrogate data:', results2
    stop_time = timeit.default_timer()
    time_simulation = stop_time - start_time
    print 'simulation time: ', time_simulation

