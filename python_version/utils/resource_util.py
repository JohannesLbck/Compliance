import xml.etree.ElementTree as ET
from hashmap import HashTable


## executed_by_annotated, returns the resource a path is executed by if the resource does not exist it returns None ( = false), multiple resources need to be separated by ,
def executed_by_annotated(path, root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    call = root.find(path, namespace)
    #Option for annotation to be under Documentation Input
    #item = call.find('.//ns0:documentation/ns0:input/ns0:Resource', namespace) 
    # Option for annotation to be under Annotations/Generic/ label Resource
    item = call.find('.//ns0:annotations/ns0:_generic/ns0:Resource', namespace)
    #print(ET.tostring(item, encoding="utf8").decode("utf8"))
    print(item)
    if item is not None:
        return item.text
    else:
        return None 
    

## executed_by_data
def executed_by_data():
    pass
