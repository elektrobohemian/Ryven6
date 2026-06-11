from qtpy.QtWidgets import  QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog


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

        self.btn_run = QPushButton("Run")
        self.btn_run.clicked.connect(self.on_play_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)

        layout.addWidget(self.btn_run)
        self.setLayout(layout)

    def value_changed_text(self):
        #code = self.edit.toPlainText()
        #local_vars = {"data": Data, "result": None}
        #exec(code, {}, local_vars)
        #print(f"local var: result (CustomWidget): {local_vars["result"]}")
        #if local_vars["result"] is not None:
            # updates the node input this widget is attached to
            #self.update_node_input(Data(local_vars["result"]))
        pass

    def on_play_button_clicked(self):
        print("Play button clicked!")
        #self.update_node_input(Data("Button pressed."))
        code = self.edit.toPlainText()
        local_vars = {"data": Data, "result": None}
        exec(code, {}, local_vars)
        print(f"local var: result (CustomWidget): {local_vars["result"]}")
        if local_vars["result"] is not None:
            # updates the node input this widget is attached to
            self.update_node_input(Data(local_vars["result"]))

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
        self.label_inp.setMinimumSize(300, 40)
        self.label_inp.setWordWrap(True)


        layout = QVBoxLayout()
        layout.addWidget(self.label_inp)

        self.setLayout(layout)

    def val_update_event(self, val: Data):
        """ This method is called every time the input port is connected or updated."""
        if val is not None:
            self.label_inp.setText(str(val.payload))
        else:
            self.label_inp.setText("⚠️ Nothing to display")

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

class PickyPrintWidget(NodeInputWidget, QWidget):
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

@node_gui(nodes.PickyPrintNode)
class PickyPrintNodeGUI(NodeGUI):
    color = "#fcba03"

    # register the input widget class
    input_widget_classes = {"pprint_widget": PickyPrintWidget}

    # attach the custom widget to the first node input
    # display it _below_ the input pin
    init_input_widgets = {0: {"name": "pprint_widget", "pos": "below"}}

class PathSelector_MainWidget(NodeMainWidget, QWidget):
    state_dict=dict()

    def __init__(self, params):
        NodeMainWidget.__init__(self, params)
        #QPushButton.__init__(self)

        QWidget.__init__(self)

        self.label_path = QLabel()
        self.label_path.setMinimumSize(300, 20)

        self.btn_run = QPushButton("Choose...")

        layout = QVBoxLayout()
        layout.addWidget(self.label_path)
        layout.addWidget(self.btn_run)

        self.btn_run.clicked.connect(self.btn_clicked)

        self.setLayout(layout)

    def btn_clicked(self):
        print(f"Path Selector: {self.state_dict}")
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", ""
        )

        if directory:
            directory_text=directory
            if len(directory) > 40:
                directory_text = "..."+directory[-40:]
            self.label_path.setText(directory_text)
            self.state_dict={"type":"path","value": directory}
            self.node.set_output_val(0, Data(self.state_dict))
            #self.node.set_output_val(0,Data(directory))
        self.update_node()
        pass

    def get_val(self):
        return self.label_path.text()

    # states are used to save and load the node's state when saving/loading a project
    def get_state(self) -> dict:
        return {"value": self.label_path.text(),"state_dict":self.state_dict}

    def set_state(self, state: dict):
        self.label_path.setText(str(state["value"]))
        self.state_dict=state["state_dict"]

@node_gui(nodes.PathSelector_Node)
class PathSelectorNodeGui(NodeGUI):
    main_widget_class = PathSelector_MainWidget
    main_widget_pos = 'between ports'
    color = '#99dd55'

