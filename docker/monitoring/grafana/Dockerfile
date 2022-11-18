# Image name: dodasts/monitoring-grafana
FROM  grafana/grafana:9.2.4

USER root

# Install INFN-CLOUD CAs
RUN wget "https://crt.sh/?d=2475254782" -q -O /usr/local/share/ca-certificates/ca.crt && \
    update-ca-certificates
