#!/bin/bash

ftype=DNL
ftime=0000
for fdate in 20150419
do
	fyear=${fdate:0:4}	
	
	dir=${fyear}/${ftype}/${fdate}${ftime}/http
	
 	# Create folder for sum files if necessary 
	if [ ! -d "$dir" ]; then
  		mkdir "$dir"
	fi
	for i in {01..60}
	do
		echo -n "Processing dump for date $fdate...$i/60..."
		tshark -r $fyear/$ftype/${fdate}${ftime}/${fdate}${ftime}_${ftype}_p${i}.dump -T fields -e frame.time -e ip.src -e ip.dst -e ip.proto -e frame.len -E header=y -E separator=/t, -E quote=n -E occurrence=a > $dir/http_${fdate}${ftime}_${ftype}_p${i}.txt	
	done
	cat $fyear/$ftype/${fdate}${ftime}/http/*.txt > ~/data/dorm2/2015/DNL/http/http_${fdate}D.txt
	echo "Done"
done
