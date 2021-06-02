"""Application entry point."""


from src.server import server

from src.app1 import app as app1
from src.app2 import app as app2

if __name__ == "__main__":
    server.run()
