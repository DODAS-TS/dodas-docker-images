#!/bin/bash  
echo "xrdcp -np $1 $2 $3" >> /tmp/copy.log  
xrdcp -np $1 $2 
