from node import Node
from constants import PORT_NODE
from tracking_decorator.track_changes import track_changes

@track_changes('is_port')
class PortNode(Node):
    def __init__(self, id, pos, is_port):

        super().__init__(id, pos)
        self.item_type = PORT_NODE
        self.is_port = is_port

        self.start_values = self.start_values | {'is_port'}