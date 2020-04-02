#! /bin/bash

if [ ! -f /etc/grid-security/hostcert.pem ]; then
    if [ -f /etc/grid-security/certificates/DODAS.pem ]; then

        echo "Using predefined CA"
        /usr/local/bin/dodas-x509 --hostname $XRD_HOST --generate-cert --ca-path /etc/grid-security/certificates --cert-path /etc/grid-security --ca-name DODAS
        for i in `openssl x509 -in /etc/grid-security/certificates/DODAS.pem -subject_hash`; do
            ln -s /etc/grid-security/certificates/DODAS.pem /etc/grid-security/certificates/$i.0
            chown -R xrootd: /etc/grid-security/hostcert.pem /etc/grid-security/hostcert.key
            break
        done

    fi
fi

if [ ! -f /etc/grid-security/hostcert.pem ]; then
    /usr/local/bin/dodas-x509 --hostname $XRD_HOST --ca-path /etc/grid-security/certificates --cert-path /etc/grid-security --ca-name DODAS
    chown -R xrootd: /etc/grid-security/hostcert.pem /etc/grid-security/hostcert.key
    for i in `openssl x509 -in /etc/grid-security/certificates/DODAS.pem -subject_hash`; do
        ln -s /etc/grid-security/certificates/DODAS.pem /etc/grid-security/certificates/$i.0
        chown -R xrootd: /etc/grid-security/hostcert.pem /etc/grid-security/hostcert.key
        break
    done
fi

sudo -E -u xrootd /usr/bin/xrootd -l /var/log/xrootd/xrootd.log -c /etc/xrootd/xrootd-http.cfg -n http &

sleep infinity
