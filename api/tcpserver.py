import socket
import socketserver
import threading


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
    "cmd": "addnode",
    "args": 1,
    "response_ok": 4,
    "response_err": -4,
}
STATS = {
    "cmd": "addnode",
    "args": 1,
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
        data = str(self.request.recv(1024), 'utf-8').split()

        command = data[0]

        if command == ADD_NODE["cmd"]:
            if len(data)-1 < ADD_NODE["args"]:
                response = "-99 Wrong parameters"
            else:
                response = command

        elif command == RM_NODE["cmd"]:
            if len(data)-1 < RM_NODE["args"]:
                response = "-99 Wrong parameters"
            else:
                response = command

        elif command == ADD["cmd"]:
            if len(data)-1 < ADD["args"]:
                response = "-99 Wrong parameters"
            else:
                response = command

        elif command == GET["cmd"]:
            if len(data)-1 < GET["args"]:
                response = "-99 Wrong parameters"
            else:
                response = command

        elif command == STATS["cmd"]:
            if len(data)-1 < STATS["args"]:
                response = "-99 Wrong parameters"
            else:
                response = command

        else:
            response = "-99 Wrong command"


        self.request.sendall(bytes(response, 'utf-8'))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



if __name__ == "__main__":

    HOST = "127.0.0.1"
    PORT = 8080

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    while True:
        pass

    server.shutdown()