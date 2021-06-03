from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from src.db import db
from src.security_class import authenticate, identity
from src.resources.user import UserRegister
from src.resources.cartridge import Cartridge, CartridgeList


# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {"bruno": "asdf"}

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
server.secret_key = "br1"
api = Api(server)


@server.before_first_request
def create_tables():
    from src.models.user import UserModel

    db.create_all()  # sql alchemy creates the tables that it sees and this works through imports
    # admin = UserModel("bruno", "asdf")

    # db.session.add(admin)
    db.session.commit()


jwt = JWT(server, authenticate, identity)  # allows authentication of users /auth

api.add_resource(Cartridge, "/cartridge/<string:cartridgeId>")

api.add_resource(CartridgeList, "/cartridges")
api.add_resource(UserRegister, "/register")


db.init_app(server)


@server.route("/")  # we are specifying the endopoint ##'http://www.google.com
def home():
    return "Hello, bruvio!"


# if __name__ == "__main__":
#     app.run_server(port=5000, debug=True)
