#!bin/sh
#Script start network, node version 8.14

echo "setting up the network..."
cd ~/fabric-dev-servers
export FABRIC_VERSION=hlfv12
./stopFabric.sh
./teardownFabric.sh
./startFabric.sh


cd ..
echo "installing the chaincode..."
composer network install -c PeerAdmin@hlfv1 -a eeyes@0.0.1.bna
echo "Starting the network..."
composer network start --networkName eeyes --networkVersion 0.0.1 -A admin -S adminpw -c PeerAdmin@hlfv1
echo "Testing if the network is up..."
composer network ping -c admin@eeyes

echo "Launching API..."
cd Documents/eeyes
composer-rest-server
admin@eeyes
never use namespaces
n
n
n (pour test oui)
rien
y
n
composer-rest-server -c admin@eeyes -n never -w true
http://localhost:3000
