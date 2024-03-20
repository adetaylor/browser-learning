#!/bin/sh

sudo apt-get -y update
curl -o code.deb -L http://go.microsoft.com/fwlink/?LinkID=760868
sudo dpkg -i code.deb
sudo apt -y --fix-broken install
sudo apt-get -y install python3.11-venv python3.11-tk pip openssl tcpdump libnss3 libnspr4
