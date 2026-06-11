from qtpy.QtWidgets import  QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog


from ryven.gui_env import *
from ryvencore import Node

from . import nodes
from . import pdf_processors as pdf_processors

## pdf processors
class PDFWidget(NodeInputWidget, QWidget):
    def __init__(self, params):
        """Layouts the custom widget. Please note that all widgets will be disabled if the input port is connected."""

        NodeInputWidget.__init__(self, params)
        QWidget.__init__(self)

        self.label_inp = QLabel()
        self.label_inp.setMinimumSize(300, 40)
        self.label_inp.setWordWrap(True)


        layout = QVBoxLayout()
        layout.addWidget(self.label_inp)

        self.setLayout(layout)

    def val_update_event(self, val: Data):
        """ This method is called every time the input port is connected or updated."""
        if val is not None and type(val.payload) is dict:
            if "type" in val.payload:
                if val.payload["type"] == "path":
                    self.label_inp.setText(str(val.payload["value"]))
                else:
                    self.label_inp.setText("⚠️ Type not excepted!")
            else:
                self.label_inp.setText("⚠️ Type not excepted!")
        else:
            self.label_inp.setText("⚠️ Type not excepted!")

    def get_val(self):
        return self.label_inp.text()

    # states are used to save and load the node's state when saving/loading a project
    def get_state(self) -> dict:
        return {"value": self.label_inp.text()}

    def set_state(self, state: dict):
        self.label_inp.setText(str(state["value"]))

@node_gui(pdf_processors.PDFNode)
class PDFNodeGUI(NodeGUI):
    color = "#ff0003"

    # register the input widget class
    input_widget_classes = {"pdf_widget": PDFWidget}

    # attach the custom widget to the first node input
    # display it _below_ the input pin
    init_input_widgets = {0: {"name": "pdf_widget", "pos": "below"}}