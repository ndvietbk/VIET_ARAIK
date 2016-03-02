import pandas as pd
import numpy as np
from gg1_function import simulate_gg1, qexp_rate, rand_qexp

def main():
    #Import file from system, this file contains inter-arrival time and size of request file
    infile ='saskatchewan.txt'
    data = pd.read_csv(infile,delim_whitespace = True, header=None, na_filter = True)      #Read file without header and using space ' ' to seperate between columns
    data.columns = ['Time','IP','numcon','size']   # Sign names for columns
    data = data[data.time >=0]                                               #Drop negative time variable
    time = np.asarray(data['time'])                                            #Variable x contain values of variable
    ssize = np.asarray(data['size'])
    ssize = np.nan_to_num(ssize)                                                   #Replace nan size variable to 0


    ssize = 8*ssize/1024**2
    time_ave = time.mean()
    ssize_ave = ssize.mean()


    q1 = 1.30
    q2 = 1.32
    rate1= qexp_rate(q1, time_ave)
    rate2=qexp_rate(q2, ssize_ave)

    n = 1000
    timet=rand_qexp(n,q1,rate1)
    ssizet=rand_qexp(n,q2,rate2)
    timet = timet.flatten()
    ssizet = ssizet.flatten()


    c=np.logspace(np.log10(0.005), np.log10(0.056), 5);

    a1 = []
    a2 = []
    for i in range(len(c)):
        a1.append(simulate_gg1(n,time,ssize/c[i]))
        d1 = pd.DataFrame(a1)
        a2.append(simulate_gg1(n,timet,ssizet/c[i]))
        d2 = pd.DataFrame(a2)
    print('\nParameters of queueing system using empirical data')
    print(d1)
    print('\nParameters of queueing system using q exponential distribution series')
    print(d2)

    print("column 0: Utilization     Column 1: W     Column 2:    L")
if __name__ == '__main__':
    main()
