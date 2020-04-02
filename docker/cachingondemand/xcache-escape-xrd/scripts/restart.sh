#! /bin/bash

kill `cat /var/run/xrootd/http/xrootd.pid`

sudo -E -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrootd.log -c /etc/xrootd/xrootd-escape.cfg -n escape &


