from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.cartridge import CartridgeModel
from flask_restful import inputs


class Cartridge(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "cartridgeId", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("testStatus", type=str, required=True)
    parser.add_argument("departmentName", type=str, required=True)
    parser.add_argument("boxName", type=str, required=True)
    parser.add_argument("pattern", type=str, required=True)
    parser.add_argument("hospitalName", type=str, required=True)
    parser.add_argument("operatorName", type=str, required=True)
    parser.add_argument("organisationId", type=str, required=True)
    parser.add_argument("participantId", type=str, required=True)
    parser.add_argument("trustName", type=str, required=True)

    parser.add_argument(
        "submissionDateTime", type=str, help="ISO8601 UTC Timestamp (ms precision)"
    )
    parser.add_argument(
        "testStartDateTime", type=str, help="ISO8601 UTC Timestamp (ms precision)"
    )
    parser.add_argument(
        "lastUpdatedDateTime", type=str, help="ISO8601 UTC Timestamp (ms precision)"
    )

    @jwt_required()
    def get(self, cartridgeId):
        cartridge = CartridgeModel.find_by_id(cartridgeId)
        if cartridge:
            return cartridge.json()
        return {"message": "cartridge not found"}, 404

    @jwt_required()
    def post(self, cartridgeId):
        if CartridgeModel.find_by_id(cartridgeId):
            return {
                "message": "An cartridge with id '{}' already exists.".format(
                    cartridgeId
                )
            }, 400

        data = Cartridge.parser.parse_args()

        cartridge = CartridgeModel(**data)

        try:
            cartridge.save_to_db()
        except:
            return {"message": "An error occurred inserting the cartridge."}, 500

        return cartridge.json(), 201

    @jwt_required()
    def delete(self, cartridgeId):
        cartridge = CartridgeModel.find_by_id(cartridgeId)
        if cartridge:
            cartridge.delete_from_db()
            return {"message": "cartridge deleted."}
        return {"message": "cartridge not found."}, 404

    @jwt_required()
    def put(self, cartridgeId):
        data = Cartridge.parser.parse_args()

        cartridge = CartridgeModel.find_by_id(cartridgeId)

        if cartridge:
            cartridge.testStatus = data["testStatus"]
        else:
            cartridge = CartridgeModel(**data)

        cartridge.save_to_db()

        return cartridge.json()


class CartridgeList(Resource):
    @jwt_required()
    def get(self):
        return {"cartridges": list(map(lambda x: x.json(), CartridgeModel.query.all()))}
