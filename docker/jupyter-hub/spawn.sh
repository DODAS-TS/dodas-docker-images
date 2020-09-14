#!/bin/bash
if ![ -z $S3_ENABLED ]; then
    mkdir -p s3/${USERNAME} && cd .init/ && ./sts-wire ${USERNAME} ${S3_HOST} /${USERNAME} ../s3/${USERNAME} > .mount_log_${USERNAME}.txt &
else
    echo "S3 disable."
fi