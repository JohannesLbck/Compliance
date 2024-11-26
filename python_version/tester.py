import xml.etree.ElementTree as ET
from hashmap import HashTable
from util import directly_follows_must, directly_follows_can, timeouts_exists, exists_by_label, get_ancestors, compare_xpaths, executed_by_annotated

def run_tests(tree):

    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}

    print(ET.tostring(tree, encoding='utf8').decode('utf8'))


    print(tree.tag)
    print(tree.attrib)

    for child in tree:
        print(child.tag, child.attrib)
        #for children in child:
        #    print(children.tag, children.attrib)


    print(tree.findall(".", namespace))
    print(tree.findall("ns0:call", namespace))

    print(executed_by_annotated(exists_by_label(tree, "F"), tree,))
    print("f and d")
    print(directly_follows_must(tree, exists_by_label(tree, "F"), exists_by_label(tree, "D")))
    print("f and g")
    print(directly_follows_must(tree, exists_by_label(tree, "F"), exists_by_label(tree, "G")))
    print("f and Hello")
    print(directly_follows_must(tree, exists_by_label(tree, "F"), exists_by_label(tree, "Hello")))
    print("test and wait")
    print(directly_follows_must(tree, exists_by_label(tree, "test"), exists_by_label(tree, "wait")))

