#!/usr/bin/python

import tailer
import fcntl
import os, sys
import time

lockfile = os.path.normpath('/tmp/' + os.path.basename(__file__).replace('.py', '') + '.lock')
exclusive_lock = open(lockfile, 'w')

try:
    fcntl.lockf(exclusive_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print "Another instance is already running, quitting."
    time.sleep(1)
    sys.exit(-1)

try:
    log_file = open(sys.argv[1])
except:
    print "Usage: %s logfile_path" % sys.argv[0]
    sys.exit(-1)

SEPARATOR="|"

for line in tailer.follow(log_file):
    t = line.split(SEPARATOR)
    print "insert into queue_log (time, callid, queuename, agent, event, data) values ('%s', '%s', '%s', '%s', '%s', '%s');" % (t[0],t[1],t[2],t[3],t[4],SEPARATOR.join(t[5:]))
    