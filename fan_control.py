#! /usr/bin/python

import subprocess
import time
import re
from gpiozero import LED

PIN = LED(17)
MAX_TEMP = 51
MIN_TEMP = 45
PATTERN = "^temp=([0-9.]*)'C$"

def getTemp():
    result = subprocess.check_output(["sudo", "vcgencmd", "measure_temp"])
    match = re.search(PATTERN, result)
    return float(match.group(1))


while(True):
    temperature = getTemp()
    if temperature >= MAX_TEMP:
        PIN.on()
    elif temperature <= MIN_TEMP:
        PIN.off()
    #print str(temperature) + " -> " + str(PIN.is_lit)
    time.sleep(30)
