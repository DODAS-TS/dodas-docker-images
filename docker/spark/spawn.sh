#!/bin/bash
if [ $S3_BUCKET ] && [ $S3_ENDPOINT ]; then
    mkdir -p s3/${S3_BUCKET} && cd .init/ && ./sts-wire myminio ${S3_ENDPOINT} /${S3_BUCKET} ../s3/${S3_BUCKET} > .mount_log_${S3_BUCKET}.txt &
else
    echo "S3 disabled."
fi
