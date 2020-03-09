#! /bin/bash

if [ ! -f /etc/grid-security/hostcert.pem ]; then
    /usr/local/bin/dodas-x509 --hostname $XRD_HOST --ca-path /etc/grid-security/certificates --cert-path /etc/grid-security --ca-name DODAS
    chown -R xrootd: /etc/grid-security/hostcert.pem /etc/grid-security/hostcert.key
fi

sudo -u xrootd /usr/bin/xrootd -k 3 -l /var/log/xrootd/xrootd.log -c /etc/xrootd/xrootd-http.cfg -n http &

sleep infinity