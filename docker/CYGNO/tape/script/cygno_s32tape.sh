#!/bin/bash
fileIndex="./index_backet.txt"
fileSaved="./index_saved.txt"
fileNotSaved="./index_not_saved.txt"
inbaket="cygnus"
outtag="RED"
inurl="https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a"
outurl="davs://xfer-archive.cr.cnaf.infn.it:8443/cygno"
# wget https://s3.cloud.infn.it/v1/AUTH_2ebf769785574195bde2ff418deac08a/$inbaket/ -O $fileIndex
# $PWD/s32list.py $fileIndex -b $inbaket 
echo "Index file dimesion"
wc $fileIndex
source ./oicd-setup.sh
SECONDS_START=$SECONDS
echo "Starting at $SECONDS_START"
echo "" > $fileSaved
echo "" > $fileNotSaved
cat $fileIndex | while read line
do
   if (( $[$SECONDS-$SECONDS_START] > 1800 )); then
        SECONDS_START=$SECONDS
        source ./oicd-setup.sh
        echo "TOKEN refresh done..."
   fi
   echo -e "Coping file $line\n"       
   echo "Starting"
   file=`echo $line | rev | cut -d'/' -f1 | rev`
   ishidden=`echo $file | cut -d'.' -f1`
   if [[ $ishidden != "" ]] ; then
       encoded_file=$(python2 -c "import urllib; print urllib.pathname2url('''$line''')")
       wget $inurl/$inbaket/$encoded_file -O $file
       # if [ $? -ne 0 ]; then
       #     exit 1
       #     fi
       if [[ $outtag == "" ]] ; then
           gfal-copy $file $outurl/$line
           # if [ $? -ne 0 ]; then
           #     exit 1
           #     fi 
       else
           gfal-copy $file $outurl/$outtag/$line
       #     if [ $? -ne 0 ]; then
       #         exit 1
       #         fi
       fi
       rm -f $file
       echo $line >> $fileSaved
   else
       echo $line >> $fileNotSaved
   fi
   echo "Done"
done
UTIME=`date +%s`
cp  $fileIndex ./arch/$UTIME_$fileIndex
cp  $fileSaved ./arch/$UTIME_$fileSaved
cp  $fileNotSaved ./arch/$UTIME_fileNotSaved 
echo "ALL DONE!"
exit 0 
