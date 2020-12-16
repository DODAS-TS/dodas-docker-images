#!/bin/bash
if [ ${S3_BUCKETS%% *} ] && [ $S3_ENDPOINT ]; then
    for S3_BUCKET in ${S3_BUCKETS}; do mkdir -p s3 && cd .init && ./sts-wire ${S3_BUCKET} ${S3_ENDPOINT} /${S3_BUCKET} ../s3/${S3_BUCKET} > .mount_log_${S3_BUCKET}.txt & && cd ..; done
else
    echo "S3 disabled."
fi
