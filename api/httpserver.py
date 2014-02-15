from http.server import BaseHTTPRequestHandler,HTTPServer
import urllib
import json

from node import Node
from ring import ConsistentRing
import api.httpclient as client

# The node containing container (our node container only) and the ring metadata
node = None


class NodeServerHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

        # Simple Protocol
        #----------------
        #
        # Requests
        # ---------
        #
        # /add-node: adds a node to the ring (local, each node has to add on its own)
        # /rm-node: removes a node from the ring (local, each node has to add on its own)
        # /stats: gets the stats of this node
        # /get: gets the data from the cache, if not in this node, this node
        #    requests to the appropiate one
        # /add: gets the data from the cache, if not in this node, this node
        #    requests to the appropiate one
        #
        # Responses
        # ---------
        #
        # 201: OK
        # 500: Error
        # 200: Hit
        # 204: Miss
        #
        #
        # Payload
        # -------
        #
        # All the requests will be POST. 
        # The /get will have 1 parameter named "key" that will be the key to get
        # The /add will have 2 parameters named "key" that will be the key to
        #   store and "data", this will be the data to store
        # The /add-node will have 1 parameter named "node-key" that will be the
        #   node key (this key will be: "hostname:port" format)
        # The /rm-node will have 1 parameter named "node-key" that will be the
        #   node key (this key will be: "hostname:port" format)
        # 

        if self.path == "/get":
            cached_data = self._get_data(post_data["key"][0])
            if not cached_data: # this is a miss               
                print("Missed!")
                self._respond(None, 204)
            else:
                print("Hit!")
                self._respond(bytes(cached_data, 'UTF-8'), 200)

        elif self.path == "/add":
            self._add_data(post_data["key"][0], post_data["data"][0])
            self._respond(None, 201)
        elif self.path == "/rm-node":
            self._rm_node(post_data["node-key"][0])
            self._respond(None, 201)
        elif self.path == "/add-node":
            self._add_node(post_data["node-key"][0])
            self._respond(None, 201)
        else:
            self._respond(None, 400)

        return

    def do_GET(self):
        if self.path == "/stats":
            # for now return all the cached data in the node
            stats = json.dumps(node.get_all_data())
            self._respond(bytes(stats, 'UTF-8'), 201)
        else:
            self._respond(None, 400)

        return

    def _respond(self, response, status=200):

        self.send_response(status)
        if response:
            self.send_header("Content-type", "text/json")
            self.send_header("Content-length", len(response))
            self.end_headers()
            self.wfile.write(response)  
        else:
            self.end_headers()

    # Helper functions
    def _get_data(self, key):
        # Check in wich node is the key
        node_key = node.where(key)

        # Is us?
        if node_key == node.key:
            return node.get_data(key)
        else: # If not, ask to the proper node (We know the key)
            print("asking to: {0}".format(node_key))

            return client.get(node_key, key)


    def _add_data(self, key, data):
        global node
        # Check in wich node is the key
        node_key = node.where(key)

        # Is us?
        if node_key == node.key:
            return node.set_data(key, data)
        else: # If not, ask to the proper node (We know the key)
            return client.add(node_key, key, data)

    def _add_node(self, key):
        node.add_node_to_ring(key)


    def _rm_node(self, key):
        node.rm_node_from_ring(key)


class NodeServer(object):
    
    def __init__(self, host, port):
        self._host = host
        self._port = port

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

            server = HTTPServer((self._host, self._port), NodeServerHandler)
            print ("Node listening {0}:{1}".format(self._host, self._port))
            
            #Wait forever for incoming http requests
            server.serve_forever()

        except KeyboardInterrupt:
            print("^C received, shutting down the node")
            #TODO: Notify
            server.socket.close()

