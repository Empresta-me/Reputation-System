
from node import Node

class ReputationSystem:

    def __init__(self, observer_node, nodes=None):
        self.observer_node = observer_node
        self.nodes = nodes if nodes is not None else {}
        self.weights = {}
        self.topology = None

    def add_node(self, id : str) -> Node:
        """Creates a new node with a unique identifier."""

        # Enforces that ids are uniques
        if id in self.nodes.keys():
            raise Exception('Id is not unique. Node not created.')
        else:
            # Creates the new node
            node = Node(id)
            self.nodes[id] = node
            return node
        
    def delete_node(self, id : str) -> None:
        """Deletes a node with a given identifier."""
        self.nodes.pop(id)