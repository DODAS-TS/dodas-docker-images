# XCache usage

## Prereq

mkdir rucio/etc/ca
wget https://gist.githubusercontent.com/dciangot/daf80b3c763f3e652e362e5c31587dea/raw/18917c8f6b5b2a4bc43363eaf4aec28cd3f726cb/DODAS.pem -O rucio/etc/ca
wget https://gist.githubusercontent.com/dciangot/daf80b3c763f3e652e362e5c31587dea/raw/18917c8f6b5b2a4bc43363eaf4aec28cd3f726cb/DODAS.pem -O rucio/etc/ca/DODAS.pem
ln -s $PWD/rucio/etc/ca/DODAS.pem $PWD/rucio/etc/ca/eec62e9c.0
export XrdSecGSICADIR=$PWD/rucio/etc/ca
