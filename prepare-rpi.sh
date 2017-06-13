#!/bin/bash
source prepare-scripts/prepare.sh

sudo apt-get install -y python-pyaudio mpg123
sudo pip install python-dateutil feedparser BeautifulSoup4
sudo modprobe snd_bcm2835
sudo amixer cset numid=3 1

cd $HOME/src/julius-cy
./setup.sh
./compile.sh
cd -

