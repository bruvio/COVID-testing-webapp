from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security_class import authenticate, identity
from resources.user import UserRegister
from resources.cartridge import Cartridge, CartridgeList


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "br1"
api = Api(app)


@app.before_first_request
def create_tables():
    from models.user import UserModel
    from models.cartridge import CartridgeModel

    db.create_all()  # sql alchemy creates the tables that it sees and this works through imports
    admin = UserModel("bruno", "asdf")

    db.session.add(admin)
    db.session.commit()


jwt = JWT(app, authenticate, identity)  # allows authentication of users /auth

api.add_resource(Cartridge, "/cartridge/<string:cartridgeId>")

api.add_resource(CartridgeList, "/cartridges")
api.add_resource(UserRegister, "/register")


@app.route("/")  # we are specifying the endopoint ##'http://www.google.com
def home():
    return "Hello, bruvio!"


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
