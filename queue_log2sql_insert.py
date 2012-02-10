#!/usr/bin/python

import tailer
import fcntl
import os, sys
import time
from sqlobject import *

SEPARATOR = "|"
DSN = 'postgres://postgres@/asterisk'

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


class QueueLog(SQLObject):
    time = StringCol()
    callid = StringCol()
    queuename = StringCol()
    agent = StringCol()
    event = StringCol()
    data = StringCol()

connection = connectionForURI(DSN)
sqlhub.processConnection = connection

for line in tailer.follow(log_file):
    t = line.split(SEPARATOR)

    print t
    
    QueueLog(
	time = t[0], 
	callid = t[1],
	queuename = t[2],
	agent = t[3],
	event = t[4],
	data = SEPARATOR.join(t[5:])
    )


    