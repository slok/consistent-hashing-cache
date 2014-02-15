import sys

from api.httpserver import NodeServer


if __name__ == "__main__":
    node = NodeServer(sys.argv[1], int(sys.argv[2]))
    node.run()

