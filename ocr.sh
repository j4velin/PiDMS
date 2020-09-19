#!/bin/bash

workdir=/home/pi/ocr.work
scaninput=/home/pi/scaninput
outdir=/home/pi/paperless.consume

inotifywait -m -e close_write -e moved_to $scaninput |
    while read -r path action file; do
        echo "Waiting for $file..."
        sleep 10
        echo "Processing $file..."

        out="${file%%.*}.pdf"

        ocrmypdf -l deu "$scaninput/$file" "$workdir/$out" 2>&1 | tee /tmp/paperless.ocr.log
        echo "File $file processed"
	mv -n "$workdir/$out" "$outdir/$out" && rm "$path/$file"
    done
