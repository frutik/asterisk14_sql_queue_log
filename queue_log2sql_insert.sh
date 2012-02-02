#!/bin/bash

LOG=${1}

inotifywait -mq -e modify ${LOG} | while read file; do tail -1 ${LOG} | awk -vd="'" -F '|' \
    '{printf("insert into queue_log (time, callid, queuename, agent, event, data) values (%s%s%s, %s%s%s, %s%s%s, %s%s%s, %s%s%s", d,$1,d,d,$2,d,d,$3,d,d,$4,d,d,$5,d)} END {printf(", %s", d)} END { for (i = 6; i <= NF; i++) printf("%s%s", FS,$i)} END {print d} END {print ");"}'; done
