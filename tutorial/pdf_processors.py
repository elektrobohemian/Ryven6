from ryven.node_env import *

class PDFNode(Node):
    """Prints the input directly to the widget and the console."""
    title = "PDF Node"
    init_inputs = [NodeInputType()]

    def update_event(self, inp=-1):
        if self.input(0) is not None:
            if "type" in self.input(0).payload:
                if self.input(0).payload["type"]=="path":
                    print(f"{self.title}: Typed input: {self.input(0).payload["type"]}")
            else:
                pass

        else:
            print(f"{self.title}: Expected 'path' type.")

# prepare publication
node_types = [
    PDFNode,
]

export_nodes(
    node_types=node_types,
    sub_pkg_name='pdf_processors',
)