#!/bin/bash

ZOOKEEPER_CONDOR_HOST=$(dodas_cache --wait-for true zookeeper CONDOR_HOST || echo "None")
CONDOR_HOST=$(condor_config_val CONDOR_HOST | sed -e 's/^[ \t\n]*//')

if [ "$CONDOR_HOST" == "$ZOOKEEPER_CONDOR_HOST" ];
then
    exit 0 ;
else
    exit 1 ;
fi