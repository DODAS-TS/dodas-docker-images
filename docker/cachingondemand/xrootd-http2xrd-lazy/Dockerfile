FROM dodasts/dodas-x509 as GETCERTS

FROM opensciencegrid/software-base:fresh

RUN groupadd -o -g 10940 xrootd
RUN useradd -o -u 10940 -g 10940 -s /bin/sh xrootd

RUN yum install -y openssl sudo davix xrootd-server xrootd-scitokens xrootd-multiuser

COPY --from=0 /usr/local/bin/dodas-x509 /usr/local/bin/dodas-x509

RUN chmod +x /usr/local/bin/dodas-x509

RUN mkdir -p /data && chown -R xrootd: /data
