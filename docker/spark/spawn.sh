#!/bin/bash
if ! [ -z $S3_ENABLED ]; then
    if ! [ -z $S3_BUCKET ]; then
      mkdir -p s3/${S3_BUCKET} && cd .init/ && ./sts-wire myminio ${S3_ENDPOINT} /${S3_BUCKET} ../s3/${S3_BUCKET} > .mount_log_${S3_BUCKET}.txt &
    fi
else
    echo "S3 disable."
fi
