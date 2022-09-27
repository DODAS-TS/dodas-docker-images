#!/bin/bash
fileIndex="./index.xml"
wget https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygno-data/ -O $fileIndex
echo "Index file dimesion"
wc $fileIndex
source ./oicd-setup.sh
SECONDS_START=$SECONDS
echo "Starting at $SECONDS_START"
# fileIndex="./index2.xml"
cat $fileIndex | while read line
do
   if (( $[$SECONDS-$SECONDS_START] > 1800 )); then
        SECONDS_START=$SECONDS
        source ./oicd-setup.sh
        echo "TOKEN refresh done..."
   fi
   echo -e "Coping file $line\n"
   tag=`echo $line | cut -d "/" -f 1`
   file=`echo $line | cut -d "/" -f 2`
   echo "Starting"
   wget https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/cygno-data/$tag/$file
   gfal-copy -f --log-file ./tape_copy.log $file davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/$tag/$file
   rm -f $file
   echo "Done"
done
UTIME=`date +%s`
gfal-copy -f --log-file ./tape_copy.log $fileIndex davs://xfer-archive.cr.cnaf.infn.it:8443/cygno/index_$UTIME.xml
echo "ALL DONE!"
