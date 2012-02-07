#!/bin/bash

/home/andriy/queue_log2sql_insert.sh /var/log/asterisk/queue_log 2>/dev/null | psql -U postgres asterisk
 