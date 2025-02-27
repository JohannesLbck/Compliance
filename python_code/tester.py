import xml.etree.ElementTree as ET
from hashmap import HashTable
from util import * 
from annotated_verification import * 

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
    #print("data_objects")
    #output = data_objects
    #print(output)
    #print("Activity data checks")
    #a_dict= activity_data_checks(tree, exists_by_label(tree, "F"))
    #arguments = a_dict["arguments"]
    #for occurance in arguments:
    #    print(occurance)
    #    print(occurance == "fen_param")
    #print(output)
    #print("data_value_alternative")
    #output = data_value_alternative(tree, "not data.x >3")
    print("data_value_alternative_directly_follows_test")
    print(data_value_alternative_directly_follows(tree, "not data.x > 3",  "D"))

def time_tests(tree):
    print("Timeouts:")
    print(timeouts_exists(tree))
    print("Syncs:")
    print(sync_exists(tree))
    pass

def general_util_tests(tree):
    #pathslist = find_subprocess(tree)
    combine_sub_trees(tree )

def control_flow_tests(tree):
    event_based_gateway(tree, exists_by_label(tree, "Hello"), exists_by_label(tree, "Bello"))

def run_tests(tree):
    print("Generic Tests:")
    generic_tests(tree)
    #print("Control Flow Tests:")
    #control_flow_tests(tree)
    #time_tests(tree)
    #print("Data Tests")
    #data_tests(tree)
    #print("Resource Tests:")
    #resource_tests(tree)
    #print("General Util Tests:")
    #general_util_tests(tree)

