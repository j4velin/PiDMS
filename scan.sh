#!/bin/bash
count=$1
resolution=150

cd /home/pi/scans

if [ $count -gt 1 ]
then
	scanimage --batch=scan_%d.tiff --batch-count=$count --format=tiff --resolution $resolution --mode Gray
	tiffcp scan_* scan.tiff
	rm scan_*
else
	scanimage --format=tiff --resolution $resolution --mode Gray >scan.tiff
fi
tiff2pdf -p A4 scan.tiff > scan.pdf
rm scan.tiff
mv scan.pdf ../scaninput/scan_$(date +'%d_%m_%y_%H_%M_%S').pdf
