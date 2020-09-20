#! /usr/bin/python

from flask import Flask
from flask import request
import subprocess
import datetime

http_server = Flask(__name__)

@http_server.route('/<int:count>', methods=['GET'])
def scan(count):
    scan = subprocess.Popen('/home/pi/scan.sh ' + str(count) + ' 2>&1', stdout=subprocess.PIPE, shell=True)
    out, err = scan.communicate()
    if scan.returncode == 0:
        return "scanned " + str(count) + " pages"
    else:
        with open('/tmp/scan.log', 'a') as log:
            log.write(str(datetime.datetime.now()) + '\n')
            log.write(out + '\n')
        return "error trying to scan, error code: " + str(scan.returncode) + "\n" + out, 500

if __name__ == '__main__':
    http_server.run(host='0.0.0.0', port=8080)
