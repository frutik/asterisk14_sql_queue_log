Asterisk 1.4.x and lower does not currently support dumping queue_log data straight to a SQL table. (See details http://www.voip-info.org/wiki/view/Asterisk+queue_log+on+MySQL)

If we plan to use the real-time monitoring features, we must upload data to MySQL as events happen.

To use the script use command like in the following example (use proper sql client and credentials):


    ./queue_log2sql_insert.sh /var/log/asterisk/queue_log 2>/null | psql -U postgres asterisk

Postgresql and MySQL are supported both... I hope 

Create database table as described on voip-info.org before first run.