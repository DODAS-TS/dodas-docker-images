#!/usr/bin/env bash

mkdir -p /var/log/sts-wire/
mkdir -p /s3/
mkdir -p /s3/"${USERNAME}"
mkdir -p /s3/scratch
mkdir -p /s3/cygnus

sts-wire https://iam.cloud.infn.it/ "${USERNAME}" https://minio.cloud.infn.it/ "/${USERNAME}" "/s3/${USERNAME}" &>"/var/log/sts-wire/mount_log_${USERNAME}.log" &
sts-wire https://iam.cloud.infn.it/ scratch https://minio.cloud.infn.it/ /scratch /s3/scratch &>/var/log/sts-wire/mount_log_scratch.log &
sts-wire https://iam.cloud.infn.it/ cygnus https://minio.cloud.infn.it/ /cygnus /s3/cygnus &>/var/log/sts-wire/mount_log_cygnus.log &
