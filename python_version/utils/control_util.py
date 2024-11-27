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

## Helper: Returns the ancestors of two xpaths 
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

## Helper: get shared ancestors and ancestors
def get_shared_ancestors(root, xpath1, xpath2):
    ancestors1 = get_ancestors(root, xpath1)
    ancestors2 = get_ancestors(root, xpath2)
    shared_ancestors = set(ancestors1) & set(ancestors2)
    return ancestors1, ancestors2, shared_ancestors


## This method is idenpendent of the annotation style, this code is absolutly disgusting, I search through the entire tree
## 3 times which should really only take one search, but whatever, I dont like xpath, this method assumes that the xpath
## exists in the tree
def compare_xpaths(root, xpath1, xpath2):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    typesplit = xpath1.split("[")[0]
    ancestors1, ancestors2, shared_ancestors = get_shared_ancestors(root, xpath1, xpath2)
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

def directly_follows_must(root, xpath1, xpath2):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    elements = [elem for elem in root.iter() if elem.tag.endswith('call')]
    ele1 = root.find(xpath1, namespace)
    ele2 = root.find(xpath2, namespace)
    ancestors1, ancestors2, shared_ancestors = get_shared_ancestors(root, xpath1, xpath2)
    shared_branch = False
    potentially_follows = True
    shared_exclusive = False
    for ancestor in shared_ancestors:
        if ancestor.tag.endswith("otherwise") or ancestor.tag.endswith("alternative"):
            shared_branch = True
        if ancestor.tag.endswith("choose"):
            shared_exclusive = True
            if not shared_branch:
                return False 
    for ancestor in ancestors1:
        if ancestor.tag.endswith("parallel_branch"):
            return False
        if ancestor.tag.endswith("choose"):
            if not shared_exclusive:
                return False
    for ancestor in ancestors2:
        if ancestor.tag.endswith("parallel_branch"):
            return False
        if ancestor.tag.endswith("choose"):
            if not shared_exclusive:
                return False
    for i in range(len(elements) - 1):
        if elements[i] is ele1 and elements[i + 1] is ele2:
            return True 
    return False

def directly_follows_can(root, xpath1, xpath2):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    ancestors1, ancestors2, shared_ancestors = get_shared_ancestors(root, xpath1, xpath2)
    shared_parallel = False
    shared_branch = False
    shared_exclusive = False
    for ancestor in shared_ancestors:
        if ancestor.tag.endswith("choose"):
            shared_exclusive = True
        if ancestor.tag.endswith("parallel_branch"):
            shared_parallel = True
        if ancestor.tag.endswith("parallel"):
            if not shared_parallel:
                return True
        if ancestor.tag.endswith("otherwise") or ancestor.tag.endswith("alternative"):
            shared_branch = True 
        if ancestor.tag.endswith("choose") and not shared_branch:
           return False ## if on different branches in exclusive, they can never follow each other
    ele1 = root.find(xpath1, namespace)
    ele2 = root.find(xpath2, namespace)
    elements = [elem for elem in root.iter() if elem.tag.endswith('call')]
    for i in range(len(elements) - 1):
        if elements[i] is ele1 and elements[i + 1] is ele2:
            return True
    last_in_branch = False
    for ancestor in ancestors1:
        if ancestor.tag.endswith("parallel") or ancestor.tag.endswith("choose"):
            elementsall = [elem for elem in root.iter() if elem.tag.endswith("call") or elem.tag.endswith("parallel") or elem.tag.endswith("choose") or elem.tag.endswith("parallel_branch") or elem.tag.endswith("alternative") or elem.tag.endswith("otherwise")]
            for i in range(len(elementsall)-1):
                if elementsall[i] is ele1:
                    if not elementsall[i + 1].tag.endswith("call"):
                        last_in_branch = True
                if elementsall[i] is ele2:
                    return last_in_branch and not shared_exclusive
    return False


