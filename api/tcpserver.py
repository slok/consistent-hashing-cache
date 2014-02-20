import socket
import socketserver
import threading
import json

from node import Node
from ring import ConsistentRing
import api.tcpclient as client


# The node containing container (our node container only) and the ring metadata
node = None

# Globals for commands
ADD_NODE = {
    "cmd": "addnode",
    "args": 1,
    "response_ok": 1,
    "response_err": -1,
}
RM_NODE = {
    "cmd": "rmnode",
    "args": 1,
    "response_ok": 2,
    "response_err": -2,
}
ADD = {
    "cmd": "add",
    "args": 2,
    "response_ok": 3,
    "response_err": -3,
}
GET = {
    "cmd": "get",
    "args": 1,
    "response_ok": 4,
    "response_err": -4,
}
STATS = {
    "cmd": "stats",
    "args": 0,
    "response_ok": 5,
    "response_err": -5,
}
ERROR = {
    "cmd": None,
    "args": 0,
    "response_ok": 0,
    "response_err": -99,
}

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # Protocol
        # --------   
        # 
        # addnode {key}
        # rmnode {key}
        # add {key} {value}
        # get {key}
        # stats
        #
        # Returned data
        # -------------
        #
        # Added node: 1 {message}
        # Error added node: -1 {message}
        # Removed node: 2 {message}
        # Error removed node: -2 {message}
        # Added key: 3 {message}
        # Error added key: -3 {message}
        # get key: 4 {key} {value}
        # Missed key: -4 {message}
        # stats: 5 {stats}
        # Error stats: -5 {stats}
        # CMD Error : -99 {message}


        # Get data and split
        data = str(self.request.recv(1024), 'utf-8').split(None, 2)

        command = data[0]

        if command == ADD_NODE["cmd"]:
            if len(data)-1 < ADD_NODE["args"]:
                response = "-99 Wrong parameters"
            else:
                # TODO: Check key
                self._add_node(data[1])
                response = "{0} {1}".format(ADD_NODE["response_ok"], "Added node")

        elif command == RM_NODE["cmd"]:
            if len(data)-1 < RM_NODE["args"]:
                response = "-99 Wrong parameters"
            else:
                # TODO: Check key
                self._rm_node(data[1])
                response = "{0} {1}".format(RM_NODE["response_ok"], "removed node")

        elif command == ADD["cmd"]:
            if len(data)-1 < ADD["args"]:
                response = "-99 Wrong parameters"
            else:
                # TODO: Check key
                try:
                    self._add_data(data[1], data[2])
                    response = "{0} {1}".format(ADD["response_ok"], "Added data")
                except ConnectionRefusedError:
                    response = "{0} {1}".format(ADD["response_err"], "Connection error")

        elif command == GET["cmd"]:
            if len(data)-1 < GET["args"]:
                response = "-99 Wrong parameters"
            else:
                # TODO: Check key
                try:
                    res_data = self._get_data(data[1])
                    if not res_data:
                        response = "{0} {1}".format(GET["response_err"], "Missed data")
                    else:
                        response = "{0} {1}".format(GET["response_ok"], res_data)
                except ConnectionRefusedError:
                    response = "{0} {1}".format(GET["response_err"], "Connection error")

        elif command == STATS["cmd"]:
            if len(data)-1 < STATS["args"]:
                response = "-99 Wrong parameters"
            else:
                response = json.dumps(node.stats())
        else:
            response = "-99 Wrong command"


        self.request.sendall(bytes(response, 'utf-8'))


    # Helper functions
    def _get_data(self, key):
        # Check in wich node is the key
        node_key = node.where(key)

        # Is us?
        if node_key == node.key:
            return node.get_data(key)
        else: # If not, ask to the proper node (We know the key)
            print("asking to: {0}".format(node_key))
            host, port = node_key.split(":")

            # TODO: Check correct return
            return client.get(host, int(port), key)[1]


    def _add_data(self, key, data):
        global node
        # Check in wich node is the key
        node_key = node.where(key)

        # Is us?
        if node_key == node.key:
            print("Inserting in this node")
            return node.set_data(key, data)
        else: # If not, ask to the proper node (We know the key)
            # TODO: Check node is up before inserting
            print("Inserting in node {0}".format(node_key))
            host, port = node_key.split(":")
            return client.add(host, int(port), key, data)

    def _add_node(self, key):
        node.add_node_to_ring(key)


    def _rm_node(self, key):
        node.rm_node_from_ring(key)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



class NodeServer(object):

    def __init__(self, host="127.0.0.1", port=8000):

        self._host = host
        self._port = port
        self._server = None

    def _set_environment(self):
        """
            Starts the node, ring and stuff
        """
        # Global vriables will enable accesing from threads
        global node

        # Create a new ring, with default values
        ring = ConsistentRing()

        node = Node("{0}:{1}".format(self._host, self._port), ring)

    def run(self):
        try:
            self._set_environment()

            print ("Node listening {0}:{1}".format(self._host, self._port))
            self._server = ThreadedTCPServer((self._host, self._port), ThreadedTCPRequestHandler)
            server_thread = threading.Thread(target=self._server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            print("Server loop running in thread:", server_thread.name)
            self._server.serve_forever()

        except KeyboardInterrupt:
            print("^C received, shutting down the node")
            #TODO: Notify

            self._server.shutdown()
