#!/bin/bash
    ### Configure condor
    str1=$(grep "GLIDEIN_Site =" /etc/condor/config.d/99_DODAS_local)
    sed -i -e "s/$str1/GLIDEIN_Site = \"$CMS_LOCAL_SITE\"/g" /etc/condor/config.d/99_DODAS_local
    str2=$(grep "GLIDEIN_CMSSite =" /etc/condor/config.d/99_DODAS_local)
    sed -i -e "s/$str2/GLIDEIN_CMSSite = \"$CMS_LOCAL_SITE\"/g" /etc/condor/config.d/99_DODAS_local
    str3=$(grep "GLIDEIN_Gatekeeper =" /etc/condor/config.d/99_DODAS_local)
    sed -i -e "s/$str3/GLIDEIN_Gatekeeper = \"$GATKEEPER\"/g" /etc/condor/config.d/99_DODAS_local

    if ! [[ -z "${MARATHON_APP_RESOURCE_CPUS}" ]]; then
      NUM_CPUS="${MARATHON_APP_RESOURCE_CPUS}"
    elif ! [[ -z "${DETECTED_CORES}" ]]; then
      NUM_CPUS="${DETECTED_CORES}"
    else
      NUM_CPUS="1"
    fi

    str4=$(grep "NUM_CPUS" /etc/condor/config.d/03_DODAS_Partitionable_Slots)
    sed -i -e "s/$str4/NUM_CPUS = ${NUM_CPUS%.*}/g" /etc/condor/config.d/03_DODAS_Partitionable_Slots


    COLLECTOR_PORT=`shuf -i 9621-9720 -n 1`
    sed -i -e "s/COLLECTOR_PORT/${COLLECTOR_PORT}/g" /etc/condor/config.d/99_DODAS_tweaks

    CCB_PORT=`shuf -i 9621-9720 -n 1`
    sed -i -e "s/CCB_PORT/${CCB_PORT}/g" /etc/condor/config.d/99_DODAS_tweaks

    export PATH=$PATH:/usr/libexec/condor