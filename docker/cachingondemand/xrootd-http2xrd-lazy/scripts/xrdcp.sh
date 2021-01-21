#!/bin/bash  
echo "xrdcp -np $1 $2 $3" >> /var/log/xrootd/http/copy.log  
xrdcp -np $1 $2 
