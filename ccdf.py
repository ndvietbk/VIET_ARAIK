# Calculates ccdf of variable from input text file with given step and write it to output text file

#!/usr/bin/python

import pandas as pd
import numpy as np
import sys
import getopt


def main(argv):
    infile = ''            #Input file contains variable of which we need calculate cdf
    outfile = ''           #Output cdf file
    num = ''               #Number of needed step
    s = ''                 #Difference between steps
    cmp = False            #Logic variable for complementary CDF
    try:
        opts, args = getopt.getopt(argv, "hi:o:n:c", ["ifile=", "ofile=", "numpts", "cmpl"])
    except getopt.GetoptError:
        print('ccdf.py -i <input file> -o <output file> -n <number of pts> -c <complementary CDF>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ccdf.py -i <input file> -o <output file> -n <number of pts> -c <complementary CDF>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt in ("-o", "--ofile"):
            outfile = arg
        elif opt in ("-n", "--numpts"):
            num = arg
        elif opt in ("-c", "--cmpl"):
            cmp = True

    data = pd.read_table(infile)                #Read input file
    data = np.asarray(data)                     #Convert input variable to array
    data_sort = np.sort(data, axis=None)        #Sort array
    n = data_sort.size                          #Calculate length (size) of array
    ind = np.linspace(1, n, n)
    p = np.divide(ind, n)                       #determine CDF of variable at position ind
    if (cmp == True):                           # If cmp==true, it's CCDF
        data_sort = data_sort[::-1]
        p = p[::-1]
    if num != '':
        s = n/float(num)
    else:
        s = 1

    f = open(outfile, 'w')
    for i in np.arange(n, step=s):
        f.write('{0:f} {1:f}\n'.format(data_sort[i], p[i]))
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])



