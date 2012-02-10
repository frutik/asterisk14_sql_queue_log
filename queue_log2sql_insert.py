#!/usr/bin/python

import pyinotify
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
    log_file = sys.argv[1]
except:
    print "Usage: %s logfile_path" % sys.argv[0]
    sys.exit(-1)

wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        print event
 
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(log_file, mask, rec=True)

notifier.loop()

