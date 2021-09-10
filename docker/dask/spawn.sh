#!/bin/bash

# Configure oidc-agent for user token management
echo "eval \`oidc-keychain\`" >>~/.bashrc
eval $(OIDC_CONFIG_DIR=$HOME/.config/oidc-agent oidc-keychain)
oidc-gen dodas --issuer $IAM_SERVER \
    --client-id $IAM_CLIENT_ID \
    --client-secret $IAM_CLIENT_SECRET \
    --rt $REFRESH_TOKEN \
    --confirm-yes \
    --scope "openid profile email" \
    --redirect-uri http://localhost:8843 \
    --pw-cmd "echo \"DUMMY PWD\""

oidc-token dodas >~/.token

source ~/htc.rc
