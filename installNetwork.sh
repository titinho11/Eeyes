#!/bin/sh
mkdir ~/fabric-dev-servers
cd ~/fabric-dev-servers
curl -O https://raw.githubusercontent.com/hyperledger/composer-tools/master/packages/fabric-dev-servers/fabric-dev-servers.tar.gz
tar -xvf fabric-dev-servers.tar.gz
export FABRIC_VERSION=hlfv12
./downloadFabric.sh
sudo ./stopFabric.sh
./teardownFabric.sh
./startFabric.sh
rm -fr ~/.composer
