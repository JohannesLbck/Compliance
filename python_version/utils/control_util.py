import xml.etree.ElementTree as ET
from hashmap import HashTable


## find xpath by label
def exists_by_label(root, mlabel):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    for call in root.findall(".//ns0:call", namespace):
        label = call.find("ns0:parameters/ns0:label", namespace)
        if label is not None and label.text == mlabel:
            call_id = call.attrib.get('id')
            return f".//ns0:call[@id='{call_id}']" if call_id else None
    return None

## Returns the ancestors of two xpaths, currently only used to enable the compare_xpaths method
def get_ancestors(root, xpath):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    target = root.find(xpath,namespace)
    ancestors = []
    current = target
    while current is not None:
        for parent in root.iter():
            if current in parent:
                ancestors.append(parent)
                current = parent
                break
        else:
            break
    return ancestors

## This method is idenpendent of the annotation style, this code is absolutly disgusting, I search through the entire tree
## 3 times which should really only take one search, but whatever, I dont like xpath, this method assumes that the xpath
## exists in the tree
def compare_xpaths(root, xpath1, xpath2):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    typesplit = xpath1.split("[")[0]
    ancestors1 = get_ancestors(root, xpath1 )
    ancestors2 = get_ancestors(root, xpath2 )
    ## if they share a choose or a parrallel node, adress the special case, otherwise break out and do the normal comparison
    shared_ancestors = set(ancestors1) & set(ancestors2)
    shared_branch = False
    for ancestor in shared_ancestors:
        if ancestor.tag.endswith("otherwise") or ancestor.tag.endswith("alternative") or ancestor.tag.endswith("parallel_branch"):
            shared_branch = True
        if ancestor.tag.endswith("choose") and not shared_branch:
            return 0 
        elif ancestor.tag.endswith("parallel") and not shared_branch:
            return -1

    for element in root.findall(typesplit, namespace):
        if element == root.find(xpath1, namespace):
            return 1 
        elif element == root.find(xpath2, namespace):
            return 2 

## directly follows
def directly_follows(root, xpath1, xpath2):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}

