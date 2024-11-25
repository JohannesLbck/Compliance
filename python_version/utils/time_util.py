import xml.etree.ElementTree as ET
from hashmap import HashTable



## time exists returns a list of all timeouts with their timeout values
def timeouts_exists(root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    results = []
    # Iterate through all <call> elements
    for call in root.findall(".//ns0:call[@endpoint='timeout']", namespace):
        call_id = call.attrib.get('id', 'unknown') 
        xpath = f".//ns0:call[@id='{call_id}']"
        timeout_element = call.find(".//ns0:arguments/ns0:timeout", namespace)

        if timeout_element is not None and timeout_element.text is not None:
            timeout_value = timeout_element.text.strip()
            results.append((xpath, timeout_value))
    return results
 
