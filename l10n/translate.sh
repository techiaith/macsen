#!/bin/bash
if [ ! -f Macsen.pot ]; then
	echo "" > Macsen.pot
fi

find . -path ./client/modules -prune -o -iname "*.py" -print | xargs xgettext -j --from-code=UTF-8 --output=Macsen.pot
sed --in-place Macsen.pot --expression=s/CHARSET/UTF-8/

if [ -f Macsen_en.po ]; then
	msgmerge Macsen_en.po Macsen.pot
else
	msginit -i Macsen.pot -o Macsen_en.po
fi


if [ -f Macsen_cy.po ]; then
	msgmerge Macsen_cy.po Macsen.pot
else
	msginit -i Macsen.pot -o Macsen_cy.po
fi

python l10n/mt_translate.py

msgfmt Macsen_en.po -o res/Macsen_en.mo
msgfmt Macsen_cy.po -o res/Macsen_cy.mo 




