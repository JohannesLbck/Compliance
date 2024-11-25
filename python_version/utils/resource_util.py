import xml.etree.ElementTree as ET
from hashmap import HashTable


## executed_by_annotated, returns the resource a path is executed by, does not check for existence
def executed_by_annotated(path, root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    call = root.find(path, namespace)
    item = call.find('.//ns0:documentation/ns0:input/ns0:item[@label="Resource"]', namespace)
    #print(ET.tostring(item, encoding="utf8").decode("utf8"))
    return item.text
    

## executed_by_data
def executed_by_data():
    pass
