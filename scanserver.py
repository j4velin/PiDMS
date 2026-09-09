#! /usr/bin/python

from flask import Flask
import datetime
import subprocess
import threading
import time

http_server = Flask(__name__)

SCAN_SCRIPT = '/root/scan.sh'
LOGFILE = '/tmp/scan.log'

# How long a new job waits for the previous one to get out of the way before giving up on it.
SETTLE_SECONDS = 30

# The most recently started scan job, or None. A multi-page job runs `scanimage --batch-prompt`,
# which waits for a newline on its stdin before every sheet; /next is what writes that newline.
scan = None

# /<count> assigns the global that /next writes to, and the two run on different request threads.
lock = threading.Lock()


def log(message):
    with open(LOGFILE, 'a') as logfile:
        logfile.write('%s: %s\n' % (datetime.datetime.now(), message))


@http_server.route('/next', methods=['GET'])
def nextPage():
    with lock:
        if scan is None:
            return 'no scan job has been started', 409
        if scan.poll() is not None:
            return 'the scan job has already ended, exit code %d' % scan.returncode, 409
        try:
            scan.stdin.write(b'\n')
            scan.stdin.flush()
        except (IOError, OSError, ValueError) as e:
            # The job ended, or was given up on, between the poll above and the write.
            return 'could not reach the scan job: %s' % e, 500
    return 'Ok'


def reclaim(job):
    """Gets a still-running job out of the way, and reports whether that worked.

    Its sheets land on fixed filenames in one directory, so two jobs at once would eat each
    other's pages - but by the time the last /next is answered the job still has to scan that
    sheet and convert them all, which is a long time to refuse the next scan for. So wait for it.

    Closing its stdin is the way out of a batch prompt that scanimage documents as Ctrl + D, so a
    job abandoned halfway through its sheets ends here too, rather than holding the scanner until
    someone restarts this server. One that is merely converting ignores it and takes its moment.
    """
    try:
        job.stdin.close()
    except (IOError, OSError, ValueError):
        pass
    deadline = time.time() + SETTLE_SECONDS
    while job.poll() is None and time.time() < deadline:
        time.sleep(0.2)
    return job.poll() is not None


@http_server.route('/<int:count>', methods=['GET'])
def doScan(count):
    global scan
    if count < 1:
        return 'page count must be at least 1', 400

    with lock:
        if scan is not None and scan.poll() is None and not reclaim(scan):
            return 'the previous scan job is still running', 409

        if count > 1:
            # A multi-page job is fed sheet by sheet by /next, so this must not wait for it: those
            # requests would be queued behind a response that only arrives once they have all been
            # served. Its output goes to the log rather than to a pipe, because nothing drains a
            # pipe while the job runs and `scanimage --batch-prompt` writes a prompt per sheet, so
            # a pipe would eventually fill up and wedge the scan.
            with open(LOGFILE, 'a') as logfile:
                scan = subprocess.Popen([SCAN_SCRIPT, str(count)], stdin=subprocess.PIPE,
                                        stdout=logfile, stderr=logfile)
            log('scanning %d pages' % count)
            return 'scanning %d pages, send /next for each sheet' % count

        scan = subprocess.Popen([SCAN_SCRIPT, str(count)], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        job = scan

    # A single page needs no /next, so it can be waited for and reported on. Outside the lock,
    # because it takes as long as the scan does.
    out = job.communicate()[0].decode('utf-8', 'replace')
    if job.returncode == 0:
        return 'scanned %d pages' % count
    log('exit code %d\n%s' % (job.returncode, out))
    return 'error trying to scan, error code: %d\n%s' % (job.returncode, out), 500


if __name__ == '__main__':
    http_server.run(host='0.0.0.0', port=8080)
