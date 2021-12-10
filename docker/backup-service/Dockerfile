# Image name: dodasts/backup-service
FROM ubuntu:20.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y rsnapshot rsync \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY rsnapshot.conf /etc/
COPY rsnapshot /etc/cron.d/

RUN chmod 644 /etc/cron.d/rsnapshot \
    && crontab /etc/cron.d/rsnapshot \
    && /bin/bash -c "mkdir -p /source"
# Smoke test
RUN rsnapshot configtest

CMD ["cron", "-f"]
