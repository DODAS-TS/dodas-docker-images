#!/usr/bin/env bash

BASE_CACHE_DIR="/usr/local/share/dodasts/sts-wire/cache"

mkdir -p "${BASE_CACHE_DIR}"
mkdir -p /usr/local/share/dodasts/sts-wire/cache
mkdir -p /var/log/sts-wire/
mkdir -p /s3/
mkdir -p /s3/"${USERNAME}"
mkdir -p /s3/scratch

sleep 1s && nice -n 19 sts-wire https://iam.cloud.infn.it/ \
    "${USERNAME}" https://minio.cloud.infn.it/ \
    "/${USERNAME}" "/s3/${USERNAME}" \
    --localCache full --tryRemount --noDummyFileCheck \
    --localCacheDir "${BASE_CACHE_DIR}/${USERNAME}" \
    &>"/var/log/sts-wire/mount_log_${USERNAME}.txt" &
sleep 2s && nice -n 19 sts-wire https://iam.cloud.infn.it/ \
    scratch https://minio.cloud.infn.it/ \
    /scratch /s3/scratch \
    --localCache full --tryRemount --noDummyFileCheck \
    --localCacheDir "${BASE_CACHE_DIR}/scratch" \
    &>/var/log/sts-wire/mount_log_scratch.txt &
