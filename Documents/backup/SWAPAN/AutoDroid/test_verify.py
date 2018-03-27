import xml.etree.ElementTree as ET

tree = ET.parse('view.xml')

all = tree.findall(".//*[@text='House Hunters']")

for a in all:
	print a