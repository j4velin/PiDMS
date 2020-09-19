# PiDMS
Some scripts and configs for my Raspberry Pi based document managament system (DMS) and personal finance manager setup

## Setup
The Pi runs docker containers for [paperless](https://github.com/the-paperless-project/paperless) and [Firefly III](https://github.com/firefly-iii/firefly-iii)

## Scripts
- backup.sh -> used to trigger a backup of the paperless and Firefly data / database
- fan_control.py -> enables the fan to cool the Pi, when reaching a certain temperature range
- ocr.sh -> runs [OCRmyPDF](https://github.com/jbarlow83/OCRmyPDF) on new pdf files and moves the ocr'ed version to the paperless input directory (better results than using paperless' OCR feature directly)
- scan.sh -> calls [scanimage](https://linux.die.net/man/1/scanimage) to batch scan multiple pages and converts them into a pdf (and moves it to the ocr.sh input directory)
- scanserver.py -> allows executing the scan.sh script with a HTTP GET request

## Crontabs
@reboot /home/pi/ocr.sh &
@reboot /home/pi/fan_control.py &
@reboot /home/pi/scanserver.py &
