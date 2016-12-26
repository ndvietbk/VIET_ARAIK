#!/bin/bash

set -e -u -o pipefail

proto=6
maxtime=1
ipnum=1000
fdate=$1
ftime=$2
fyear=${fdate:0:4}

if [ ! -d "ses/" ]; then
    mkdir "ses/"
fi

outdir="ses/${fyear}"
if [ ! -d "$outdir" ]; then
    mkdir "$outdir"
fi

./ses_extract.py log/${fyear}/log_${fdate}${ftime}.txt.gz ${outdir}/ses_${fdate}${ftime}.txt -p ${proto} -t ${maxtime} -n ${ipnum}
#gzip ${outdir}/ses_${fdate}${ftime}.txt



