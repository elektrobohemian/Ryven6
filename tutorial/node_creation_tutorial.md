# How to Create a Node and a Custom Node GUI Widget


A Ryven nodes package is simply a typical Python package which contains at least a `nodes.py` file, and calls the Ryven node API to expose node definitions.

Navigate to `~/.ryven/nodes/` and create a sub-directory of the following structure (or copy the shipped files from the `tutorial/`directory or see the deployment section below)

```
~/.ryven/nodes
└── tutorial_nodes
    ├── __init__.py
    ├── nodes.py
    └── gui.py
```

`__init__.py` is left empty in most cases.

`nodes.py` will contain all your (logical) node definitions, i.e., two nodes in the following example: `CustomNode` and `PrintNode`.

```python
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
        print(f"{self.title}'s output: {self.input(0).payload}")

# you have to make sure to export your nodes at the end of the file, otherwise they won't be available in the node editor
export_nodes([CustomNode, PrintNode])

@on_gui_load
def load_gui():
    # import gui sources here only
    from . import gui
```
In `gui.py` you can create a custom widget for your nodes. Please note, that the GUI widget is independent from the actual node. 
In other words: you can also run the nodes without the GUI.

```python
from qtpy.QtWidgets import  QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel

from ryven.gui_env import *

from . import nodes

class CustomWidget(NodeInputWidget, QWidget):
    def __init__(self, params):
        """Layouts the custom widget. Please note that all widgets will be disabled if the input port is connected."""

        NodeInputWidget.__init__(self, params)
        QWidget.__init__(self)

        self.edit = QTextEdit()
        self.edit.setPlaceholderText("result = ...")
        self.edit.setMinimumSize(300, 150)
        self.edit.textChanged.connect(self.value_changed_text)

        self.debug_button = QPushButton("Debug")
        self.debug_button.clicked.connect(self.on_play_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)

        layout.addWidget(self.debug_button)
        self.setLayout(layout)

    def value_changed_text(self):
        code = self.edit.toPlainText()
        local_vars = {"data": Data, "result": None}
        exec(code, {}, local_vars)
        print(f"local var: result (CustomWidget): {local_vars["result"]}")
        if local_vars["result"] is not None:
            # updates the node input this widget is attached to
            self.update_node_input(Data(local_vars["result"]))

    def on_play_button_clicked(self):
        print("Play button clicked!")
        self.update_node_input(Data("Button pressed."))

    def get_val(self):
        return self.edit.toPlainText()

    # states are used to save and load the node's state when saving/loading a project
    def get_state(self) -> dict:
        return {"value": self.edit.toPlainText()}

    def set_state(self, state: dict):
        self.edit.setPlainText(str(state["value"]))
        self.edit.setPlainText(str(state["value"]))

@node_gui(nodes.CustomNode)
class CustomNodeGUI(NodeGUI):
    color = "#fcba03"

    # register the input widget class
    input_widget_classes = {"custom_widget": CustomWidget}

    # attach the custom widget to the first node input
    # display it _below_ the input pin
    init_input_widgets = {0: {"name": "custom_widget", "pos": "below"}}

class PrintWidget(NodeInputWidget, QWidget):
    def __init__(self, params):
        """Layouts the custom widget. Please note that all widgets will be disabled if the input port is connected."""

        NodeInputWidget.__init__(self, params)
        QWidget.__init__(self)

        self.label_inp = QLabel()
        self.label_inp.setMinimumSize(300, 20)


        layout = QVBoxLayout()
        layout.addWidget(self.label_inp)

        self.setLayout(layout)

    def val_update_event(self, val: Data):
        """ This method is called every time the input port is connected or updated."""
        self.label_inp.setText(str(val.payload))

    def get_val(self):
        return self.label_inp.text()

    # states are used to save and load the node's state when saving/loading a project
    def get_state(self) -> dict:
        return {"value": self.label_inp.text()}

    def set_state(self, state: dict):
        self.label_inp.setText(str(state["value"]))

@node_gui(nodes.PrintNode)
class PrintNodeGUI(NodeGUI):
    color = "#fcba03"

    # register the input widget class
    input_widget_classes = {"print_widget": PrintWidget}

    # attach the custom widget to the first node input
    # display it _below_ the input pin
    init_input_widgets = {0: {"name": "print_widget", "pos": "below"}}
```

## Deployment
To facilitate the deployment process during development, you might want to use [`copy_nodes.py`](../deployment_utils/copy_nodes.py) from the `deployment_utils/` directory.
This script will copy all Python scripts (the ones described above) from `tutorial/` to `~/.ryven/nodes/tutorial_nodes/` and should be run before launching `Ryven.py` in order to use your modifications directly.

## Additional Examples

More example are available [here](../ryven-editor/ryven/example_nodes/).