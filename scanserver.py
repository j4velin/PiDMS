#! /usr/bin/python

from flask import Flask
from flask import request
import os

http_server = Flask(__name__)

@http_server.route('/<int:count>', methods=['GET'])
def scan(count):
    os.system('/home/pi/scan.sh ' + str(count) + ' 2>&1 | tee /tmp/scan.log')
    return "scanning " + str(count) + " pages..."

if __name__ == '__main__':
    http_server.run(host='0.0.0.0', port=8080)
