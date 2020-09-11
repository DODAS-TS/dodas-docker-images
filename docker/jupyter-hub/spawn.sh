#!/bin/bash
mkdir -p s3/${USERNAME} && cd .init/ && ./sts-wire ${USERNAME} https://131.154.97.112:9000/ /${USERNAME} ../s3/${USERNAME} > .mount_log_${USERNAME}.txt &
mkdir -p s3/raw-arpa && cd .init/ && ./sts-wire raw-arpa https://131.154.97.112:9000/ /raw-arpa ../s3/raw-arpa > .mount_log_raw-arpa.txt &
mkdir -p s3/raw-covid && cd .init/ && ./sts-wire raw-covid https://131.154.97.112:9000/ /raw-covid ../s3/raw-covid > .mount_log_raw-covid.txt &
mkdir -p s3/raw-meteo && cd .init/ && ./sts-wire raw-meteo https://131.154.97.112:9000/ /raw-meteo ../s3/raw-meteo > .mount_log_raw-meteo.txt &
mkdir -p s3/scratch && cd .init/ && ./sts-wire scratch https://131.154.97.112:9000/ /scratch ../s3/scratch > .mount_log.txt &
