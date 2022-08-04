#!/usr/bin/env bash

source /usr/local/share/dodasts/script/oidc_agent_init.sh

BASE_CACHE_DIR="/usr/local/share/dodasts/sts-wire/cache"

mkdir -p "${BASE_CACHE_DIR}"
mkdir -p /usr/local/share/dodasts/sts-wire/cache
mkdir -p /var/log/sts-wire/
mkdir -p /s3/
mkdir -p /s3/"${USERNAME}"
mkdir -p /s3/scratch
mkdir -p /s3/cygno
mkdir -p /s3/cygno-analysis
mkdir -p /s3/cygno-sim
mkdir -p /s3/cygno-data

# sts-wire https://iam.cloud.infn.it/ "${USERNAME}" https://minio.cloud.infn.it/ "/${USERNAME}" "/s3/${USERNAME}" &>"/var/log/sts-wire/mount_log_${USERNAME}.log" &
# sts-wire https://iam.cloud.infn.it/ scratch https://minio.cloud.infn.it/ /scratch /s3/scratch &>/var/log/sts-wire/mount_log_scratch.log &
# sts-wire https://iam.cloud.infn.it/ cygnus https://minio.cloud.infn.it/ /cygnus /s3/cygnus &>/var/log/sts-wire/mount_log_cygnus.log &

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
sleep 3s && nice -n 19 sts-wire https://iam.cloud.infn.it/ \
    cygno https://minio.cloud.infn.it/ \
    /cygnus /s3/cygno \
    --localCache full --tryRemount --noDummyFileCheck \
    --localCacheDir "${BASE_CACHE_DIR}/cygno" \
    &>/var/log/sts-wire/mount_log_cygno.txt &
sleep 4s && nice -n 19 sts-wire https://iam.cloud.infn.it/ \
    cygno_analysis https://minio.cloud.infn.it/ \
    /cygno-analysis /s3/cygno-analysis \
    --localCache full --tryRemount --noDummyFileCheck \
    --localCacheDir "${BASE_CACHE_DIR}/cygno_analysis" \
    &>/var/log/sts-wire/mount_log_cygnoalanysis.txt &
sleep 5s && nice -n 19 sts-wire https://iam.cloud.infn.it/ \
    cygno_sim https://minio.cloud.infn.it/ \
    /cygno-sim /s3/cygno-sim \
    --localCache full --tryRemount --noDummyFileCheck \
    --localCacheDir "${BASE_CACHE_DIR}/cygno_sim" \
    &>/var/log/sts-wire/mount_log_cygnosim.txt &
sleep 6s && nice -n 19 sts-wire https://iam.cloud.infn.it/ \
    cygno_data https://minio.cloud.infn.it/ \
    /cygno-data /s3/cygno-data \
    --localCache full --tryRemount --noDummyFileCheck \
    --localCacheDir "${BASE_CACHE_DIR}/cygno_data" \
    &>/var/log/sts-wire/mount_log_cygnodata.txt &

# Start crond
crond
LHOST=`hostname -i`
crontab -l | { cat; echo "* * * * * /bin/rsync -a --delete /jupyter-workspace/private/ /jupyter-workspace/cloud-storage/${USERNAME}/private/${LHOST} 2>&1"; } | crontab -
