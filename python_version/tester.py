import xml.etree.ElementTree as ET
from hashmap import HashTable
from util import timeouts_exists, exists_by_label, get_ancestors, compare_xpaths

def run_tests(tree):

    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}

    print(ET.tostring(tree, encoding='utf8').decode('utf8'))


    print(tree.tag)
    print(tree.attrib)

    for child in tree:
        print(child.tag, child.attrib)
        for children in child:
            print(children.tag, children.attrib)


    print(tree.findall(".", namespace))
    print(tree.findall("ns0:call", namespace))

