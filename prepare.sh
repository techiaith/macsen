#!/bin/bash
sudo apt-get update

sudo easy_install --upgrade pip
sudo pip install --upgrade setuptools
sudo pip install -r jasper/client/requirements.txt

sudo apt-get install festival festival-dev
sudo mkdir -p /usr/share/festival/voices/welsh
wget --progress=dot:mega -O -https://github.com/PorthTechnolegauIaith/llais_festival/archive/v1.0.tar.gz | tar -zxf - -C /usr/share/festival/voices/welsh

sudo apt-get install build-essential zlib1g-dev flex libasound2-dev libesd0-dev libsndfile1-dev

wget http://sourceforge.jp/projects/julius/downloads/60273/julius-4.3.1.tar.gz | tar -zxf - -C ~/
cd ~/julius
./configure --enable-words-int
make
sudo make install
