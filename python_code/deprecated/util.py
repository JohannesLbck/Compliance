from bigtree import dict_to_tree
import re

def to_tree(text):
    # Regular expressions
    root_pattern = re.compile(r'control flow do') 
    call_pattern = re.compile(r'call\s*:\s*(\w+).*?parameters:\s*{([^}]+)}', re.DOTALL)
    ex_pattern = re.compile(r'choose :exclusive do') 
    alt_pattern = re.compile(r'alternative test\("([^"]*)"\) do', re.DOTALL)
    default_pattern = re.compile(r'otherwise  do')
    para_pattern = re.compile(r"parallel\s(:wait\s*=>\s*-?\d+,\s*:cancel\s*=>\s*:\w+\s*do)")
    para_branch_pattern = re.compile(r'parallel_branch do')
    stop_pattern = re.compile(r'stop') 
    script_pattern = re.compile(r'manipulate') #this needs some more work, since the actual scrip is in the next line between too ends, solve later 
    loop_pattern = re.compile('loop')## read out pretest, give id to thingy
    termi_pattern = re.compile(r'terminate')
    control_pattern = re.compile(r'c\d+\d*\d*')
    
    # Stack to track the nested hierarchy of the tree 
    id_stack= [""]
    result_dict = {}
    
    previous_Node = None
    previous_split = [""] 
    # Split text by lines to process each line individually
    for ids, line in enumerate(text.splitlines()):
        line = line.strip()

        if root_pattern.search(line):
            result_dict["root"] = {"typ" : "root"}
            id_stack.append("root")
        elif call_pattern.search(line):
            id_stack.append(call_pattern.search(line).group(1))
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "call", "value": call_pattern.search(line).group(2)}
        elif ex_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "exclusive"}
            previous_split.append(key)  
        elif alt_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "exclusive_path", "value": alt_pattern.search(line).group(1)}
        elif default_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "default_path", "value": "defaul"}
        elif para_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "parallel"}
            previous_split.append(key) 
        elif para_branch_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "parallel_branch"}
        elif stop_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "stop"}
        elif script_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            id_stack.append(key+str(ids))
            id_stack.append(key+str(ids))
            result_dict[full_key] = { "typ": "script"}
        elif loop_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "loop"}
            previous_split.append(key)
        elif termi_pattern.search(line):
            key = "c"+str(ids)
            id_stack.append(key)
            full_key = "/".join(id_stack)
            result_dict[full_key] = { "typ": "terminate"}
        elif line == "end":
            #while id_stack[-1] != previous_split[-1]:
            while not control_pattern.match(id_stack[-1]):
                id_stack.pop()
            id_stack.pop()

    print(result_dict) 
    return dict_to_tree(result_dict) 
