#!/bin/bash
source prepare-scripts/prepare.sh

cd $HOME/src/julius-cy
./setup.sh
./compile.sh
cd -

