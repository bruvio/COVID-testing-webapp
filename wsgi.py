"""Application entry point."""
# from application import create_app

# # app = create_app()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', debug=True)


# from src.app import app as application

# if __name__ == '__main__':
#     application.run()


from src.server import server

from src.app1 import app as app1
from src.app2 import app as app2

if __name__ == "__main__":
    server.run()
