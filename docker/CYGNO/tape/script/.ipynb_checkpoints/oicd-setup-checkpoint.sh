#!/bin/bash

eval `oidc-agent-service use`
oidc-gen --issuer https://iam-t1-computing.cloud.cnaf.infn.it/ --pw-cmd="echo pwd" --scope "openid profile email address phone offline_access eduperson_scoped_affiliation eduperson_entitlement"  t1-tape
export TAPE_TOKEN=$(oidc-token t1-tape)
export BEARER_TOKEN=$TAPE_TOKEN
echo "$TAPE_TOKEN"
