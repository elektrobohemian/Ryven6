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
            if "type" in self.input(0).payload:
                print(f"{self.title}: Typed input: {self.input(0).payload["type"]}")
            else:
                print(f"{self.title}'s output: {self.input(0).payload}")
                print(f"\tID: {self.input(0).identifier}")
                print(f"\tGlobal ID: {self.input(0).global_id}")
                print(f"\tVersion: {self.input(0).version}")
                print(f"\tGlobal ID: {self.input(0).payload.keys()}")

        else:
            print(f"{self.title}: Nothing to print")

class PickyPrintNode(Node):
    """Prints the input directly to the widget and the console if it is of a certain type."""
    title = "Picky Print Node"
    init_inputs = [NodeInputType()]

    def update_event(self, inp=-1):
        if self.input(0) is not None:
            print("PICKY NODE")
            if "type" in self.input(0).payload:
                print(f"{self.title}: Typed input: {self.input(0).payload["type"]}")
                if self.input(0).payload["type"]=="path":
                    print(f"{self.title}'s detected a 'path' data type: {self.input(0).payload}")
                    print(f"\tID: {self.input(0).identifier}")
        else:
            print(f"{self.title}: Nothing to print")

class PathSelector_Node(Node):
    title = 'Path Selector'
    init_inputs = []
    init_outputs = [
        NodeOutputType()
    ]

    def update_event(self, inp=-1):
        self.additional_data=self.outputs(0)
        self.exec_output(0)

# you have to make sure to export your nodes at the end of the file, otherwise they won't be available in the node editor
export_nodes([CustomNode, PrintNode, PickyPrintNode, PathSelector_Node])
# export_nodes([CustomNode, PrintNode, PythonExecNode])


@on_gui_load
def load_gui():
# import gui sources here only
    from . import gui
