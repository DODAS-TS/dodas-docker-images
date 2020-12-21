#!/bin/bash
if [ ${S3_BUCKETS%% *} ] && [ $S3_ENDPOINT ]; then
    mkdir -p s3
    for S3_BUCKET in ${S3_BUCKETS};
    do
            .init/sts-wire ${S3_BUCKET} ${S3_ENDPOINT} /${S3_BUCKET} s3/${S3_BUCKET} > .mount_log_${S3_BUCKET}.txt &
    done
else
    echo "S3 disabled."
fi
