import xml.etree.ElementTree as ET
from hashmap import HashTable
from util import exists_by_label, get_ancestors, compare_xpaths

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

a = exists_by_label(tree, namespace, "A")
print("A: " + a)
b = exists_by_label(tree, namespace, "B")
print("B: " + b)
f = exists_by_label(tree, namespace, "F")
print("F: " + f)
e = exists_by_label(tree, namespace, "E")
print("E: " + e)
d = exists_by_label(tree, namespace, "D")
print("D: " + d)
i = exists_by_label(tree, namespace, "I")
print("i: " + i)
j = exists_by_label(tree, namespace, "J")
print("J: " + j)

print("compare a, e")
print(compare_xpaths(tree, a, e, namespace))
print("compare f, e")
print(compare_xpaths(tree, f, e, namespace))
print("compare a, f")
print(compare_xpaths(tree, a, f, namespace))
print("compare e, d")
print(compare_xpaths(tree, e, d, namespace))

print("i and j")
print(compare_xpaths(tree, i, j, namespace))

print(get_ancestors(tree, d, namespace))

