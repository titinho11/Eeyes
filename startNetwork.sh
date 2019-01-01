#!bin/sh
#Script start network, node version 8.14

echo "setting up the network..."
cd ~/fabric-dev-servers
export FABRIC_VERSION=hlfv12
./stopFabric.sh
./teardownFabric.sh
./startFabric.sh
rm -fr ~/.composer
./createPeerAdminCard.sh


cd ..
echo "installing the chaincode..."
composer network install -c PeerAdmin@hlfv1 -a eeyesv4@0.0.1.bna
echo "Starting the network..."
composer network start --networkName eeyesv4 --networkVersion 0.0.1 -A admin -S adminpw -c PeerAdmin@hlfv1
composer card import -f admin@eeyesv4.card
echo "Testing if the network is up..."
composer network ping -c admin@eeyesv4

echo "Launching API..."
cd Documents/eeyes
#composer-rest-server
##admin@eeyes
#never use namespaces
#n
#n
#n (pour test oui)
#rien
#y
#n
#lancer ca en arriere plan ou dans un autre terminal car blockant
composer-rest-server -c admin@eeyesv4 -n never -w true >> api.log &
#composer-rest-server -c admin@eeyes -n never -w true
#http://localhost:3000
