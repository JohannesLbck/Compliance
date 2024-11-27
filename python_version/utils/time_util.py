import xml.etree.ElementTree as ET
from hashmap import HashTable
from datetime import datetime
from dateutil.parser import parse


## time exists returns a list of all timeouts with their timeout fields
def timeouts_exists(root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    results = []
    # Iterate through all <call> elements
    for call in root.findall(".//ns0:call[@endpoint='timeout']", namespace):
        call_id = call.attrib.get('id', 'unknown') 
        xpath = f".//ns0:call[@id='{call_id}']"
        timeout_element = call.find(".//ns0:arguments/ns0:timeout", namespace)

        if timeout_element is not None:
            if timeout_element.text is not None:
                timeout_value = timeout_element.text.strip()
                results.append((xpath, timeout_value))
            else:
                results.append((xpath, None))
    return results


def parse_timestamp(txt):
    if txt.isdigit():
        timestamp = int(txt)
        return datetime.utcfromtimestamp(timestamp).isoformat()
    if txt.startswith("data"):
        return input_string[4:].strip()
    try:
        return parse(txt).isoformat()
    except ValueError:
        print("The timestamp sent could not be parsed")
        return None

## sync exists: returns a list of all syncs with their timestamp fields
## if timestamp field = string: label of a dataobject
## if timestamp is a datatime: it is the passed timestamp
def sync_exists(root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    results = []
    # Iterate through all <call> elements
    for call in root.findall(".//ns0:call[@endpoint='sync']", namespace):
        call_id = call.attrib.get('id', 'unknown')
        xpath = f".//ns0:call[@id='{call_id}']"
        timeout_element = call.find(".//ns0:arguments/ns0:timestamp", namespace)

        if timeout_element is not None:
            if timeout_element.text is not None:
                timeout_value = timeout_element.text.strip()
                return_value = parse_timestamp(timeout_value)
                results.append((xpath, return_value))
            else:
                results.append((xpath, None))
    return results

