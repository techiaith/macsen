import polib
from techiaith_api import cyfieithu_testun

po = polib.pofile('Macsen_cy.po')

try:

	for entry in po.untranslated_entries():
		print entry.msgid
		entry.msgstr = cyfieithu_testun(entry.msgid, "Meddalwedd", "en", "cy")
finally:
	po.save('Macsen_cy.po')
