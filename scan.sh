#!/bin/bash
count=$1
resolution=150

cd /home/pi/scans

if [ $count -gt 1 ]; then
	scanimage --batch=scan_%d.tiff --batch-count=$count --format=tiff --resolution $resolution --mode Gray
	resultcode=$?
	if [ $resultcode -eq 0 ]; then
		tiffcp scan_* scan.tiff
		rm scan_*
	fi
else
	scanimage --format=tiff --resolution $resolution --mode Gray >scan.tiff
	resultcode=$?
fi

if [ $resultcode -eq 0 ]; then
	tiff2pdf -p A4 scan.tiff > scan.pdf
	rm scan.tiff
	mv scan.pdf ../scaninput/scan_$(date +'%d_%m_%y_%H_%M_%S').pdf
fi
exit $resultcode
