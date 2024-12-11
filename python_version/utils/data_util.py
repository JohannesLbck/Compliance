import xml.etree.ElementTree as ET
from hashmap import HashTable

## Data 
# Data_List: Returns a list of all data elements that are accessed during the process tree
# Structure of return is [(label, {"type": "", "xpath": "xpath", "code": "code"}, (,)...]
# Types are: Send, Receive, Rescue, Write, Conditional Read, for full documentation see BPM24 Implementation
# This will either be a recursive function or a depth first search 
def data_objects(root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    tags_to_match = ["call", "manipulate", "loop", "alternative"]

    # Find and iterate over all matching elements
    for tag in tags_to_match:
        for elem in root.findall(tag, namespace):
            # Extract details
            name = elem.find('name').text
            value = elem.find('value').text
            print(f"Tag: {elem.tag}, Name: {name}, Value: {value}")
    return True
