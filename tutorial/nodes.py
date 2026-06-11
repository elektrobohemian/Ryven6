from ryven.node_env import *
from random import random

# each class is a node type, and each instance of the class is a node in the graph

class CustomNode(Node):
    """A custom node with one node input and one node output."""

    title = "Custom Node"
    tags = ["some tag", "tutorial"]
    init_inputs = [NodeInputType()]
    init_outputs = [NodeOutputType()]

    def update_event(self, inp=-1):
        # writes the current data payload to the first output
        self.set_output_val(0, Data(self.input(0).payload))
        self.set_state(Data())


class PrintNode(Node):
    """Prints the input directly to the widget and the console."""
    title = "Simple Print Node"
    init_inputs = [NodeInputType()]

    def update_event(self, inp=-1):
        if self.input(0) is not None:
            print(f"{self.title}'s output: {self.input(0).payload}")
        else:
            print(f"{self.title}: Nothing to print")


class PathSelector_Node(Node):
    title = 'Path Selector'
    init_inputs = []
    init_outputs = [
        NodeOutputType()
    ]

    def update_event(self, inp=-1):
        self.exec_output(0)

# you have to make sure to export your nodes at the end of the file, otherwise they won't be available in the node editor
export_nodes([CustomNode, PrintNode, PathSelector_Node])
# export_nodes([CustomNode, PrintNode, PythonExecNode])


@on_gui_load
def load_gui():
# import gui sources here only
    from . import gui
