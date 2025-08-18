#! /usr/bin/python

from flask import Flask
from flask import request
import subprocess
import datetime

http_server = Flask(__name__)

scan = None

@http_server.route('/next', methods=['GET'])
def next():
    if scan is not None:
        scan.stdin.write(b'\n')
        scan.stdin.flush()
    return "Ok"


@http_server.route('/<int:count>', methods=['GET'])
def doScan(count):
    global scan
    scan = subprocess.Popen('/root/scan.sh ' + str(count), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if count > 1:
        return scan.stdout.readline()
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
