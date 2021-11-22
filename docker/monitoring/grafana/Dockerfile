# Image name: dodasts/monitoring-grafana
FROM  grafana/grafana:8.2.1

USER root

# Install INFN-CLOUD CAs
RUN wget "https://crt.sh/?d=2475254782" --progress=bar -O /usr/local/share/ca-certificates/ca.crt && \
    update-ca-certificates