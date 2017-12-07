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

sudo mkdir -p /usr/share/festival/voices/welsh
cd /usr/share/festival/voices/welsh
wget --progress=dot:mega -O - https://github.com/PorthTechnolegauIaith/llais_festival/archive/v1.1.0.tar.gz | sudo tar -zxf -
sudo mv llais_festival-1.1.0/* .
sudo rmdir llais_festival-1.1.0
cd -

mkdir -p $HOME/src/
cd $HOME/src/
if [ ! -d "julius-cy" ]; then 
	#wget --progress=dot:mega -O - https://github.com/techiaith/julius-cy/archive/v1.0.tar.gz | tar -zxf -
	git clone --branch v2.2 https://github.com/techiaith/julius-cy.git
fi 
cd -

cd $HOME/src/julius-cy
./setup.sh
./compile.sh
cd -

PYTHONPATH=${PYTHONPATH}:${HOME}/src/macsen/client
export PYTHONPATH

