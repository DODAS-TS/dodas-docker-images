#!/bin/bash

# Configure oidc-agent for user token management
echo "eval \`oidc-keychain\`" >> ~/.bashrc
eval `oidc-keychain`
oidc-gen dodas --issuer $IAM_SERVER \
 --client-id $IAM_CLIENT_ID \
 --client-secret $IAM_CLIENT_SECRET \
 --rt $REFRESH_TOKEN \
 --confirm-yes \
 --scope "openid profile email" \
 --redirect-uri http://localhost:8843 \
 --pw-cmd "echo \"DUMMY PWD\""


if [ ${S3_BUCKETS%% *} ] && [ $S3_ENDPOINT ]; then
	mkdir -p s3
	for S3_BUCKET in ${S3_BUCKETS};
	do
	    .init/sts-wire $IAM_SERVER ${S3_BUCKET} ${S3_ENDPOINT} /${S3_BUCKET} s3/${S3_BUCKET} > .mount_log_${S3_BUCKET}.txt &
	    sleep 10
	done
else
	echo "S3 mounting default folders."
	kill `ps faux | grep "sts-wire ${USERNAME}" | awk '{ print $2 }'`
	kill `ps faux | grep ".${USERNAME}" | awk '{ print $2 }'`
	kill `ps faux | grep "sts-wire scratch" | awk '{ print $2 }'`
	kill `ps faux | grep ".scratch" | awk '{ print $2 }'`

	mkdir -p /s3/
	mkdir -p /s3/${USERNAME}
	mkdir -p /s3/scratch

	cd /.init/

	.init/sts-wire https://iam.cloud.infn.it/  ${USERNAME} https://minio.cloud.infn.it/ /${USERNAME} s3/${USERNAME} > .mount_log_${USERNAME}.txt &
	.init/sts-wire https://iam.cloud.infn.it/ scratch https://minio.cloud.infn.it/  /scratch s3/scratch > .mount_log_scratch.txt &
fi
