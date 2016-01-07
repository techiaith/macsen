#!/bin/bash
sudo apt-get update

sudo easy_install --upgrade pip
sudo pip install --upgrade setuptools
sudo pip install -r client/requirements.txt

sudo apt-get install festival festival-dev
sudo mkdir -p /usr/share/festival/voices/welsh
cd /usr/share/festival/voices/welsh
wget --progress=dot:mega -O - https://github.com/PorthTechnolegauIaith/llais_festival/archive/v1.1.0.tar.gz | sudo tar -zxf -
sudo mv llais_festival-1.1.0/* .
sudo rmdir llais_festival-1.1.0
cd -

mkdir -p $HOME/src/

cd $HOME/src
sudo apt-get install -y cvs build-essential zlib1g-dev flex libasound2-dev libesd0-dev libsndfile1-dev
cvs -z3 -d:pserver:anonymous@cvs.sourceforge.jp:/cvsroot/julius co julius4
#export CFLAGS="-O2 -mcpu=arm1176jzf-s -mfpu=vfp -mfloat-abi=hard -pipe -fomit-frame-pointer"
cd -

cd $HOME/src/julius4
./configure --enable-words-int
make
sudo make install
cd -

sudo mkdir -p /usr/share/julius/acoustic/cy
cd /usr/share/julius/acoustic/cy
wget --progress=dot:mega -O - http://techiaith.cymru/htk/paldaruo-2016-01-07.tar.gz | sudo tar -zxf -
cd -

sudo mkdir -p /usr/share/julius/lexicon/cy
cd /usr/share/julius/lexicon/cy
sudo wget --progress=dot:mega -O lexicon.tgz - http://techiaith.cymru/htk/lexicon-2016-01-07.tar.gz 
cd -

