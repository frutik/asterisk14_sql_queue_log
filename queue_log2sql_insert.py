#!/usr/bin/python

import tailer
import fcntl
import os, sys
import time
from sqlobject import *

SEPARATOR = "|"
LOCK_DIR = "/tmp/"

try:
    log_file = open(sys.argv[1])
    dsn = sys.argv[2]
except:
    print "Usage: %s logfile_path 'dsn'" % sys.argv[0]
    sys.exit(-1)

lockfile = os.path.normpath(LOCK_DIR + os.path.basename(__file__).replace('.py', '') + '.lock')
exclusive_lock = open(lockfile, 'w')

try:
    fcntl.lockf(exclusive_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print "Another instance is already running, quitting."
    time.sleep(1)
    sys.exit(-1)

class QueueLog(SQLObject):
    time = StringCol()
    callid = StringCol()
    queuename = StringCol()
    agent = StringCol()
    event = StringCol()
    data = StringCol()

connection = connectionForURI(dsn)
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


    