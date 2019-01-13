#!/bin/sh
chmod u+x prereqs-ubuntu.sh
./prereqs-ubuntu.sh
rm -rf ~/.nvm
rm -rf ~/.npm
rm -rf ~/.bower
apt update
apt install python3-minimal
apt install python3-pip
apt-get install poppler-utils
pip3 install fpdf
pip3 install pdf2image