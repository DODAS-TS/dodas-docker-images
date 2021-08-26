#!/bin/bash

# Configure oidc-agent for user token management
echo "eval \`oidc-keychain\`" >>~/.bashrc
eval $(OIDC_CONFIG_DIR=$HOME/.config/oidc-agent oidc-keychain)
oidc-gen infncloud --issuer $IAM_SERVER \
    --client-id $IAM_CLIENT_ID \
    --client-secret $IAM_CLIENT_SECRET \
    --rt $REFRESH_TOKEN \
    --confirm-yes \
    --scope "openid profile email" \
    --redirect-uri http://localhost:8843 \
    --pw-cmd "echo \"DUMMY PWD\""

oidc-token infncloud >~/.token

kill $(ps faux | grep "sts-wire ${USERNAME}" | awk '{ print $2 }')
kill $(ps faux | grep ".${USERNAME}" | awk '{ print $2 }')
kill $(ps faux | grep "sts-wire scratch" | awk '{ print $2 }')
kill $(ps faux | grep ".scratch" | awk '{ print $2 }')

mkdir -p /s3/
mkdir -p /s3/${USERNAME}
mkdir -p /s3/scratch

cd /.init/

./sts-wire https://iam.cloud.infn.it/ ${USERNAME} https://minio.cloud.infn.it/ /${USERNAME} ../s3/${USERNAME} >.mount_log_${USERNAME}.txt &
./sts-wire https://iam.cloud.infn.it/ scratch https://minio.cloud.infn.it/ /scratch ../s3/scratch >.mount_log_scratch.txt &

source ~/htc.rc
