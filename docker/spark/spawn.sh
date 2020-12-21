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
# Configure oidc-agent for user token management
echo "eval \`oidc-keychain\`" >> ~/.bashrc
eval `oidc-keychain`
oidc-gen dodas --issuer $IAM_SERVER \
 --client-id $IAM_CLIENT_ID \
 --client-secret $IAM_CLIENT_SECRET \
 --rt $REFRESH_TOKEN \
 --confirm-yes \
 --scope "openid profile email" \
 --redirect-uri http://dummy:8843 \
 --pw-cmd "echo \"DUMMY PWD\""
