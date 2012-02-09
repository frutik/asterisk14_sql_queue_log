#!/bin/bash

#LOCKFILE='/var/lock/queue_log.lock'

#if [ ! -e $LOCKFILE ]; then
#   trap "rm -f $LOCKFILE; exit" INT TERM EXIT
#   touch $LOCKFILE

   /opt/asterisk14_sql_queue_log/queue_log2sql_insert.sh /var/log/asterisk/queue_log 2>/dev/null | psql -U postgres asterisk

#   rm $LOCKFILE
#   trap - INT TERM EXIT
#else
#   echo "already running"
#fi

