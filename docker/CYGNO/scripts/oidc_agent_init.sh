#!/usr/bin/env bash

export OIDC_CONFIG_DIR=$HOME/.oidc-agent

eval $(oidc-keychain)

oidc-gen dodas --issuer "$IAM_SERVER" \
    --client-id "$IAM_CLIENT_ID" \
    --client-secret "$IAM_CLIENT_SECRET" \
    --rt "$REFRESH_TOKEN" \
    --confirm-yes \
    --scope "openid profile email" \
    --redirect-uri http://localhost:8843 \
    --pw-cmd "echo \"DUMMY PWD\""

oidc-gen condor --issuer "$IAM_SERVER" \
    --client-id "$WLCG_IAM_CLIENT_ID" \
    --client-secret "$WLCG_IAM_CLIENT_SECRET" \
    --rt "$WLCG_REFRESH_TOKEN" \
    --confirm-yes \
    --scope "openid profile email wlcg wlcg.groups" \
    --redirect-uri http://localhost:8843 \
    --pw-cmd "echo \"DUMMY PWD\""

while true; do
    oidc-token condor --time 1200 >/tmp/token
    sleep 600
done &
