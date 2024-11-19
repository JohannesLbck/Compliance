import xml.etree.ElementTree as ET

tree = ET.parse("Test2.xml")
root = tree.getroot()
print(tree)
print(root.tag)
print(root.attrib)

for child in root:
    print(child.tag, child.attrib)
