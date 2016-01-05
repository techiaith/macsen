#!/bin/bash
if [ ! -f Macsen.pot ]; then
	echo "" > Macsen.pot
fi

echo "Create POT file"
find . -path ./client/modules -prune -o -iname "*.py" -print | xargs xgettext -j --from-code=UTF-8 --output=Macsen.pot
sed --in-place Macsen.pot --expression=s/CHARSET/UTF-8/

echo "Create/Update English PO file"
if [ -f Macsen_en.po ]; then
	msgmerge --update Macsen_en.po Macsen.pot  
else
	msginit -i Macsen.pot -o Macsen_en.po
fi

echo "Create/Update Welsh PO file"
if [ -f Macsen_cy.po ]; then
	msgmerge --update Macsen_cy.po Macsen.pot 
else
	msginit -i Macsen.pot -o Macsen_cy.po
fi

echo "Machine Translate PO files"
python l10n/mt_translate.py

echo "Create/Update MO files"
msgfmt Macsen_en.po -o res/Macsen_en.mo
msgfmt Macsen_cy.po -o res/Macsen_cy.mo 




