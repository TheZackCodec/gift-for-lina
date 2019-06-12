#!/bin/bash

brew install git python dialog;
git clone https://github.com/dvigne/gift-for-lina.git /tmp;
cd /tmp/gift-for-lina;
pip install virtualenv;
virtualenv --system-site-packages env && source ./env/bin/activate;
pip install -r ./requirements.txt
dialog --yesno "Is your volume up?" 10 50 && dialog --yesno "Is your terminal maximized, not fullscreened?" 10 50 && python gfl.py;
deactivate;
rm -R -v -f /tmp/gift-for-lina;
