#    Copyright (C) <2025>  <author>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import xml.etree.ElementTree as ET


## executed_by_annotated, returns the resource a path is executed by if the resource does not exist it returns None ( = false), multiple resources need to be separated by ,
def executed_by_annotated(ele, root):
    namespace = {"ns0": "http://cpee.org/ns/description/1.0"}
    call = ele 
    #Option for annotation to be under Documentation Input
    #item = call.find('.//ns0:documentation/ns0:input/ns0:Resource', namespace) 
    # Option for annotation to be under Annotations/Generic/ label Resource
    item = call.find('.//ns0:annotations/ns0:_generic/ns0:Resource', namespace)
    if item is not None:
        return item.text.split(",")
    else:
        return None 
    

## executed_by_data
def executed_by_data():
    pass
