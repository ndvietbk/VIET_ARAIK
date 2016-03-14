#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Araik Tamazian, Viet Duc Nguyen


import argparse
import numpy as np
from schreiber import schriber
from qexp import rand_qexp


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser('Generate q-exponential random '
                                     'deviates with specified Hurst exponent.')
    parser.add_argument('output', help='an output file')
    parser.add_argument('-n', '--num', default=1e+5, type=int,
                        help='number of random deviates')
    parser.add_argument('-q', '--qshape', default=1.0, type=float,
                        help='q - shape parameter')
    parser.add_argument('-r', '--rate', default=1.0, type=float,
                        help='rate parameter')
    parser.add_argument('-u', '--hurst', default=0.6, type=float,
                        help='Hurst exponent')
    parser.add_argument('--htol', default=0.02, type=float,
                        help='Hurst exponent tolerance')
    parser.add_argument('--maxitr', default=100, type=int,
                        help='Maximum number of iterations allowed')
    return parser.parse_args()


def main(output, num, qshape, rate, hurst, htol, maxitr):
    print 'Generating random deviates...'
    x = rand_qexp(num, qshape, rate)
    print 'Introducing correlation to them...'
    y, he, itr = schriber(x, hurst, htol, maxitr)
    print ' Completed in ', itr, ' iteration(s)'
    print ' Hurst exponent is equal to ', np.round(he, 2)
    print 'Saving result to ', output
    np.savetxt(output, y, fmt='%.6e')


if __name__ == '__main__':
    args = parse_args()
    main(args.output, args.num, args.qshape, args.rate, args.hurst, args.htol, args.maxitr)
