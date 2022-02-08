#!/usr/bin/env bash
# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

USERDIR="/jupyter-workspace/cloud-storage/$USERNAME"

# Source user environment
if [ -d "$USERDIR" ] && [ -f "$USERDIR/.bashrc" ]; then
    . "$USERDIR/.bashrc"
fi

# Configure oidc-agent for user token management
# Ref: https://indigo-dc.gitbook.io/oidc-agent/user/oidc-keychain
export OIDC_CONFIG_DIR=$HOME/.oidc-agent
eval $(oidc-keychain)
