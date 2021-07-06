#!/usr/bin/env bash

if [[ -z $REPO_LIST ]]; then

    echo "Env variable REPO_LIST must be specified in the form REPO_LIST=\"cms.cern.ch oasis.cern.ch\""

else
    for repo in $REPO_LIST; do
        if ! [[ -d /cvmfs/$repo ]]; then
            mkdir /cvmfs/$repo
        fi
	if mountpoint -q /cvmfs/$repo ; then
	    umount /cvmfs/$repo
	fi
	
    mount -t cvmfs $repo /cvmfs/$repo
    done

    while true
    do
        for repo in $REPO_LIST; do
            echo "Checking $repo"
            ls /cvmfs/$repo && mountpoint -q /cvmfs/$repo
            if [ $? -ne 0 ]; then 
                echo "ls /cvmfs/$repo --> failed"; 
                umount /cvmfs/$repo || exit 1
                mount -t cvmfs $repo /cvmfs/$repo || exit 1
            fi
            echo "$repo OK"
        done
        sleep 60
    done
fi
