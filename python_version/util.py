import xml.etree.ElementTree as ET
from hashmap import HashTable

hash_t = HashTable(20)
hash_t.load_disk("TrackedUIDsHashmap.json")
notification = hash_t.get("8ff5ea21-3ee8-4f34-a0ca-36b6097d95c7")


namespace = {"ns0": "http://cpee.org/ns/description/1.0"}

tree = ET.fromstring(notification["content"]["description"])
print(ET.tostring(tree, encoding='utf8').decode('utf8'))

#root = tree.getroot()

print(tree.tag)
print(tree.attrib)

for child in tree:
    print(child.tag, child.attrib)
    for children in child:
        print(children.tag, children.attrib)
        

print("test")
print(tree.findall(".", namespace))
print(tree.findall("ns0:call", namespace))


## find xpath by label
def exists_by_label(root, namespace, mlabel):
    for call in root.findall(".//ns0:call", namespace):
        label = call.find("ns0:parameters/ns0:label", namespace)
        if label is not None and label.text == mlabel:
            call_id = call.attrib.get('id')
            return f".//ns0:call[@id='{call_id}']" if call_id else None
    return None

a = exists_by_label(tree, namespace, "A")
print("A: " + a)
b = exists_by_label(tree, namespace, "B")
print("B: " + b)
f = exists_by_label(tree, namespace, "F")
print("F: " + f)
e = exists_by_label(tree, namespace, "E")
print("E: " + e)
d = exists_by_label(tree, namespace, "D")

def get_ancestors(root, xpath, namespace):
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
def compare_xpaths(root, xpath1, xpath2, namespace):
    typesplit = xpath1.split("[")[0]
    ancestors1 = get_ancestors(root, xpath1, namespace)
    ancestors2 = get_ancestors(root, xpath2, namespace)
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

print("compare a, e")
print(compare_xpaths(tree, a, e, namespace))
print("compare f, e")
print(compare_xpaths(tree, f, e, namespace))
print("compare a, f")
print(compare_xpaths(tree, a, f, namespace))
print("compare e, d")
print(compare_xpaths(tree, e, d, namespace))

def get_ancestors(root, xpath, namespace):
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

print(get_ancestors(tree, d, namespace))
