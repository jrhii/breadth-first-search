# A Node for a network with no specific organization, other than each node can be linked to any number of nodes
class NetworkNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.links = []

    def __eq__(self, key):
        return self.key == key

# A Node for a generic tree that can only be traverse towards the root
class OneWayTreeNode:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent