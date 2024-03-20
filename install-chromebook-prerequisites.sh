#!/bin/sh

curl -o code.deb -L http://go.microsoft.com/fwlink/?LinkID=760868
sudo dpkg -i code.deb
sudo apt-get update
sudo apt --fix-broken install
sudo apt-get install python3.11-venv python3.11-tk pip openssl tcpdump libnss3 libnspr4
