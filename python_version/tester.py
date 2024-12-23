import xml.etree.ElementTree as ET
from hashmap import HashTable
from util import data_objects, sync_exists, directly_follows_must, directly_follows_can, timeouts_exists, exists_by_label, get_ancestors, compare_xpaths, executed_by_annotated


namespace = {"ns0": "http://cpee.org/ns/description/1.0"}

def generic_tests(tree):

    print(ET.tostring(tree, encoding='utf8').decode('utf8'))


    print(tree.tag)
    print(tree.attrib)

    for child in tree:
        print(child.tag, child.attrib)
        #for children in child:
        #    print(children.tag, children.attrib)


    print(tree.findall(".", namespace))
    print(tree.findall("ns0:call", namespace))

def resource_tests(tree):
    print(executed_by_annotated(exists_by_label(tree, "F"), tree,))

def directly_follows_must_tests(tree):
    print(directly_follows_must(tree, exists_by_label(tree, "F"), exists_by_label(tree, "D")))
    print("f and g")
    print(directly_follows_must(tree, exists_by_label(tree, "F"), exists_by_label(tree, "G")))
    print("f and Hello")
    print(directly_follows_must(tree, exists_by_label(tree, "F"), exists_by_label(tree, "Hello")))
    print("test and wait")
    print(directly_follows_must(tree, exists_by_label(tree, "test"), exists_by_label(tree, "wait")))

def directly_follows_can_tests(tree):
    print("can tests")
    print(executed_by_annotated(exists_by_label(tree, "F"), tree,))
    print("f and d")
    print(directly_follows_can(tree, exists_by_label(tree, "F"), exists_by_label(tree, "D")))
    print("f and g")
    print(directly_follows_can(tree, exists_by_label(tree, "F"), exists_by_label(tree, "G")))
    print("f and Hello")
    print(directly_follows_can(tree, exists_by_label(tree, "F"), exists_by_label(tree, "Hello")))
    print("test and wait")
    print(directly_follows_can(tree, exists_by_label(tree, "test"), exists_by_label(tree, "wait")))
    print("Hello and Bello")
    print(directly_follows_can(tree, exists_by_label(tree, "Hello"), exists_by_label(tree, "Bello")))
    print("E and wait")
    print(directly_follows_can(tree, exists_by_label(tree, "E"), exists_by_label(tree, "wait")))
    print("D and wait")
    print(directly_follows_can(tree, exists_by_label(tree, "D"), exists_by_label(tree, "wait")))

def data_tests(tree):
    print("data_objects")
    output = data_objects
    print(output)

def time_tests(tree):
    print("Timeouts:")
    print(timeouts_exists(tree))
    print("Syncs:")
    print(sync_exists(tree))
    pass

def run_tests(tree):
    print("Generic Tests:")
    generic_tests(tree)
    #time_tests(tree)
    #data_tests(tree)
    print("Resource Tests:")
    resource_tests(tree)

