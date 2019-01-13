#!bin/sh
#Script nettoie et start network

cd ~/fabric-dev-servers
export FABRIC_VERSION=hlfv12
./stopFabric.sh
./teardownFabric.sh
./startFabric.sh
rm -fr ~/.composer