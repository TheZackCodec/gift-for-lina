#!/bin/bash

brew install git python dialog;
git clone https://github.com/dvigne/gift-for-lina.git /tmp/gift-for-lina;
cd /tmp/gift-for-lina;
pip3 install virtualenv;
virtualenv --system-site-packages env && source ./env/bin/activate;
pip3 install -r ./requirements.txt
dialog --yesno "Is your volume up?" 10 50 && dialog --yesno "Is your terminal maximized, not fullscreened?" 10 50 && python3 ./gfl.py;
deactivate;
rm -R -v -f /tmp/gift-for-lina;
