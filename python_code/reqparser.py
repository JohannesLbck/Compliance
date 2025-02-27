#    Copyright (C) <2025>  <Johannes Löbbecke>
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

## Methods for parsing the Requirements from whatever language we choose
import json
import re

## when using the "language" I used, only this tiny bit of replacement is needed, but this could be replaced with an extensive dictionary to enable a mapping between any language and the code 
method_dict = {
    "prohibition": "not ",
    "root": "Start Activity",
    "end": "End Activity",
}


#parses the requirements into requirements that can be passed to the AST
def parse_requirements(req):
    req = re.sub(r'=>', ':', req)
    req = json.loads(req)
    eval_req = []
    for tag, content in req.items():
        eval_req.append(parse_req(content))
    return eval_req

# This really only replaces function(a, b) with function(tree, a, b) to highlight the potential to support other languages and make the used language a little cleaner by not requiring the tree call, which would not be necessary in a object oriented implementation as well
#def parse_req(content):
#    pattern = r'\w+\([^\)]+\)|\S+'
#    patterns = re.findall(pattern, content)
#    result = []
#    print(patterns)
#    for word in patterns:
#        print(f'word: {word}')
#        if "(" in word and ")" in word:
#            function_name, args = word.split("(", 1)
#            print(f'function_name: {function_name}')
#            print(f'args: {args}')
#            args = args.rstrip(")")
#
#            # Replace the function name if it's in the replacements dictionary
#            new_function_name = method_dict.get(function_name, function_name)
#
#            # Recursively process the arguments
#            new_args = parse_req(args)
#
#            modified_args = f"tree, {new_args}"
#
#            # Reconstruct the function call with updated name and arguments
#            result.append(f"{new_function_name}({modified_args})")
#        else:
#            result.append(word)
#        print(f'result: {result}')
#    return " ".join(result)


## The other messy regparser had some errors, replaced with this much simpler reqparser, hopefully its fine
def parse_req(string):
    result = []
    for word in string.split("("):
        word = f'(tree, {word}'
        result.append(word)
    result = " ".join(result)
    return result[7:]

