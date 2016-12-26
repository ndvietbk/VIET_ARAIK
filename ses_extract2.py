#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 by Araik Tamazian

import argparse
import pandas as pd
import numpy as np
from tqdm import trange


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser('Extract user sessions from log.')
    parser.add_argument('input', help='an input file')
    parser.add_argument('output', help='an output file')
    parser.add_argument('-p', '--protocol', default='6', type=str,
                        help='extract sessions with a specified protocol')
    parser.add_argument('-t', '--maxtime', default=0.01, type=float,
                        help='largest time within a session allowed')
    parser.add_argument('-d', '--duration', default=0.01, type=float,
                        help='maximum session duration allowed')
    parser.add_argument('-n', '--ipnum', default=0, type=int,
                        help='number of destination IPs for which sessions will be extracted')
    return parser.parse_args()


def split(arr, cond):
  return [arr[cond], arr[~cond]]


def extract_session(input_file, output_file, protocol, maxtime, duration, ipnum):
    """
    Given handles of input and output files, read the connection
    statistics from the input file and output the connections grouped
    by their destination to the output handle.

    :param input_file: an input handle where connection statistics
        are read from
    :param output_file: an output handle where grouped statistics
        are written to
    :param protocol: a protocol which connections are to be considered
    :type protocol: str
    :return: the tuple of two numbers: the number of connection
        records processed and the number of grouped records written
        to the specified output file
    :rtype: tuple
    """

    # Read data from log
    print('Reading data from file ...')
    data = pd.read_csv(input_file, sep='\t', header=None, encoding='utf-8',
                names=['ptime', 'ipsrc', 'ipdst', 'proto', 'psize'],
                dtype={'ptime': float, 'ipsrc': str, 'ipdst': str, 'proto': str, 'psize': int},
                compression='gzip')

    data = data[data.proto == protocol]
    data = data[np.isfinite(data['psize'])]

    print('Ranking destination IPs ...')
    all_ipdst = pd.Series.value_counts(data.ipdst)
    all_ipdst = all_ipdst[all_ipdst > 1]

    if ipnum == 0:
        ipnum = len(all_ipdst)
        all_ipdst = all_ipdst.index
    else:
        if len(all_ipdst) > ipnum:
            all_ipdst = all_ipdst.index[0:ipnum]
        else:
            all_ipdst = all_ipdst.index

    for i in trange(ipnum, desc='Extracting user sessions:'):
        data1 = data[data.ipdst == all_ipdst[i]]
        data1 = data1.set_index(np.arange(len(data1.ptime)))

        dtime = np.diff(np.asarray(data1.ptime))
        dtime = np.insert(dtime, 0, 0.0)
        ptime1 = data1.iloc[1::]['ptime']
        ncon2 = np.ones(len(data1.ptime), dtype=np.int64)

        ind = np.asarray(np.where(dtime > maxtime))
        ind22 = []
        dtime_tmp = 0

        for j in range(len(dtime)):
            if j in ind:
                dtime_tmp = 0
            if dtime_tmp > duration:
                ind22.append(j-1)
                dtime_tmp = dtime[j]
            else:
                dtime_tmp += dtime[j]

        ind22 = np.asarray(ind22)
        ind = np.unique(np.sort(np.hstack((ind[0], ind22))))
        ind = ind.astype(int)
        stime = ptime1[ind]
        stime = np.hstack([data1.iloc[0]['ptime'], stime])

        if len(ind) != len(data1.ptime)-1:
            ptime2 = np.asarray(np.array_split(data1.ptime, ind))
            dtime1 = [np.diff(a) for a in ptime2]
        else:
            dtime1 = np.diff(np.asarray(data1.ptime))

        dtime2 = [np.sum(a) for a in dtime1]
        ssize2 = np.array(data1.psize)
        if len(ind) != len(data1.ptime) - 1:
            ssize1 = np.asarray(np.array_split(ssize2, ind))
            ssize = [np.sum(a) for a in ssize1]
        else:
            ssize = ssize2
        if ssize[0] == 0:
            ssize[0] = ssize2[0]
        ncon1 = np.asarray(np.array_split(ncon2, ind))
        ncon = [np.sum(a) for a in ncon1]
        if ncon[0] == 0:
            ncon[0] = ncon2[0]
        # else:
        #     dtime2 = np.sum(dtime)
        #     ssize = np.sum(data1.psize)
        #     ncon = np.sum(ncon2)

        # for j in range(len(dtime)):
        #     if dtime[j] < maxtime:
        #         ssize[l] += data1.iloc[j]['psize']
        #         ncon[l] += 1
        #     else:
        #         l += 1
        #         ssize[l] = data1.iloc[j]['psize']

        stime = pd.Series(stime, name='stime', dtype=np.float64)
        sip1 = np.repeat(all_ipdst[i], len(stime))
        sip = pd.Series(sip1, name='ipdst', dtype=str)
        ncons = pd.Series(ncon, name='ncon', dtype=np.int64)
        ssize = pd.Series(ssize, name='ssize', dtype=np.int64)
        dtime2 = pd.Series(dtime2, name='sdur', dtype=np.float64)
        if i == 0:
            out = pd.concat([stime, sip, ncons, ssize, dtime2], axis=1)
        else:
            out1 = pd.concat([stime, sip, ncons, ssize, dtime2], axis=1)
            out = out.append(out1)

    # Sort sessions by arrival time
    out = out.sort_values(by='stime')

    # Write sessions to file
    print('Writing results to file ...')
    out[['stime']] = out[['stime']].astype(np.float64)
    out[['stime']] = pd.Series(["{0:.6f}".format(val) for val in out['stime']], index=out.index)
    out[['ipdst']] = pd.Series(["{:15}".format(val) for val in out['ipdst']], index=out.index)
    out[['ncon']] = pd.Series(["{:6.0f}".format(val) for val in out['ncon']], index=out.index)
    out[['ssize']] = pd.Series(["{:9.0f}".format(val) for val in out['ssize']], index=out.index)
    out[['sdur']] = pd.Series(["{:.6f}".format(val) for val in out['sdur']], index=out.index)
    out.to_csv(output_file, header=False, index=False, sep='\t')

if __name__ == '__main__':
    args = parse_args()
    with open(args.input) as input_file:
        with open(args.output, 'w') as output_file:
            extract_session(input_file, output_file, args.protocol, args.maxtime, args.duration, args.ipnum)
