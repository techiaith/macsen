#!/bin/bash
if [ ! -f Macsen.po ]; then
	echo "" > Macsen.po
fi

find . -path ./client/modules -prune -o -iname "*.py" -print | xargs xgettext -j --from-code=UTF-8 --default-domain=Macsen
sed --in-place Macsen.po --expression=s/CHARSET/UTF-8/
