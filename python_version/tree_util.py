import bigtree

## Find by attribute value: Finds a node from a tree by its attribute value, returns the attribute if found, returns None if not found
def find_by_attribute(tree, attribute, value):
    for child in list(tree.descendants):
        if not control_pattern.match(child.node_name):
            if child.get_attr(attribute) == value:
                return child
    return None


