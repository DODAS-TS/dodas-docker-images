#!/bin/bash

ZOOKEEPER_SCHEDD_PUB_KEY=$(dodas_cache --wait-for true zookeeper SCHEDD_PUB_KEY || echo "None")
LOCAL_PUB_KEY=$(< /opt/dodas/keys/id_rsa.pub)

if [ "$LOCAL_PUB_KEY" == "$ZOOKEEPER_SCHEDD_PUB_KEY" ];
then
    exit 0 ;
else
    exit 1 ;
fi