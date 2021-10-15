#!/bin/bash

USERS=`cat /home/uwdir/condormapfile | grep SCITOKENS | grep -wv "users.htcondor.org" | awk '{print $3}'`

for u in $USERS; do
    useradd -m $u
done

/usr/bin/python /usr/bin/supervisord -c /etc/supervisord.conf