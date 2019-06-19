#!/bin/bash

apt update; apt install -y git python3 python3-pip dialog libgstreamer1.0-0;
git clone https://github.com/dvigne/gift-for-lina.git /tmp/gift-for-lina;
cd /tmp/gift-for-lina;
pip3 install virtualenv;
virtualenv --system-site-packages  -p python3 env && source ./env/bin/activate;
pip3 install -r ./requirements_linux.txt
dialog --yesno "Is your volume up?" 10 50 && dialog --yesno "Is your terminal maximized, not fullscreened?" 10 50 && python3 ./gfl.py;
deactivate;
rm -R -v -f /tmp/gift-for-lina;
