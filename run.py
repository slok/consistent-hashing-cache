import sys

from server import NodeServer
import client


if __name__ == "__main__":
    node = NodeServer(sys.argv[1], int(sys.argv[2]))
    node.run()

