#!/bin/bash
sudo apt-get update
sudo apt-get install python-dev festival festival-dev gettext

sudo easy_install --upgrade pip
sudo pip install --upgrade setuptools
sudo pip install -r client/requirements.txt
sudo pip install python-dateutil feedparser
sudo pip install polib
sudo pip install ws4py
sudo pip install unidecode
sudo pip install wikipedia

sudo mkdir -p /usr/share/festival/voices/welsh
cd /usr/share/festival/voices/welsh
wget --progress=dot:mega -O - https://github.com/PorthTechnolegauIaith/llais_festival/archive/v1.1.0.tar.gz | sudo tar -zxf -
sudo mv llais_festival-1.1.0/* .
sudo rmdir llais_festival-1.1.0
cd -

mkdir -p $HOME/src/
cd $HOME/src/
if [ ! -d "julius-cy" ]; then 
	git clone --branch v2.4 https://github.com/techiaith/julius-cy.git
fi 
cd -

cd $HOME/src/julius-cy
./setup.sh
./compile.sh
cd -

cd $HOME/src/
if [ ! -d "marytts" ]; then
	git clone https://github.com/techiaith/marytts.git
fi
cd -

cd $HOME/src/marytts
source scripts/setup.sh
source scripts/update-marytts-server-cy.sh
source scripts/voice-download.sh wispr
cd -


PYTHONPATH=${PYTHONPATH}:${HOME}/src/macsen/client
export PYTHONPATH

