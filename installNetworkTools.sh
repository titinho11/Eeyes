#!bin/sh
#Script start network, node version 8.14

echo "setting up the network tools..."
cp eeyesv4@0.0.1.bna ~/eeyesv4@0.0.1.bna
cp admin@eeyesv4.card ~/admin@eeyesv4.card
cd ~/fabric-dev-servers
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

#lancer ca en arriere plan ou dans un autre terminal car blockant
composer-rest-server -c admin@eeyesv4 -n never -w true >> api_log.log &
#composer-rest-server -c admin@eeyes -n never -w true
#http://localhost:3000
