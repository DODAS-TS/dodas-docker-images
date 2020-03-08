#!/bin/bash

echo "Executing pre"
mkdir -p /var/log/dodas
dodasexe_pre.sh > /var/log/dodas/dodasexe_pre.stdout 2> /var/log/dodas/dodasexe_pre.stderr

if [ $? -eq 0 ]; then
    echo "Pre-Start went ok.. launchin not dodas executable..."
    dodasexe.sh > /var/log/dodas/dodasexe.stdout 2> /var/log/dodas/dodasexe.stderr
else 
    echo "Pre-Start failed... stopping here"
    exit 9
fi