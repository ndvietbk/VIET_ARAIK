#Plot CCDF of variable from inputted file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
infile = 'saskatchewan_time_ccdf.txt'                                #Text file include 2 columns: variable, CCDF
data = pd.read_csv(infile,delim_whitespace = True, header=None)      #Read file without header and using space ' ' to seperate between columns
data.columns = ['a','b']                                             # Sign names for columns
data = data.drop_duplicates('a', keep='last')                        #Drop duplicate values keeping last value
x = np.asarray(data['a'])                                            # Variable x contain values of variable
y = np.asarray(data['b'])                                            # Variable y contain CCDFs of variable
plt.plot(x,y,'ro', color = 'r')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('X variable', fontsize=20)
plt.ylabel('Commulative distribution function', fontsize = 18)
plt.grid(False)
plt.show()
