#!bin/sh
#Script stop network, node version 8.14

echo "Turning off the network..."
cd ~/fabric-dev-servers
./stopFabric.sh
./teardownFabric.sh
rm -fr ~/.composer

echo "Eeyes Network is shutted down."