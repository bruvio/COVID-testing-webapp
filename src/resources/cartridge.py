from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.cartridge import CartridgeModel
from flask_restful import inputs


class Cartridge(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "cartridgeId", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument("testStatus", type=int, required=True)
    parser.add_argument("departmentName", type=int, required=True)
    parser.add_argument("pattern", type=int, required=True)
    parser.add_argument("hospitalName", type=int, required=True)
    parser.add_argument("operatorName", type=int, required=True)
    parser.add_argument("participantId", type=int, required=True)
    parser.add_argument("trustName", type=int, required=True)

    parser.add_argument("submissionDateTime", type=inputs.datetime_from_iso8601)
    parser.add_argument("testStartDateTime", type=inputs.datetime_from_iso8601)
    parser.add_argument("lastUpdatedDateTime", type=inputs.datetime_from_iso8601)

    @jwt_required()
    def get(self, cartridgeId):
        cartridge = CartridgeModel.find_by_name(cartridgeId)
        if cartridge:
            return cartridge.json()
        return {"message": "cartridge not found"}, 404

    def post(self, cartridgeId):
        if CartridgeModel.find_by_name(cartridgeId):
            return {
                "message": "An cartridge with name '{}' already exists.".format(
                    cartridgeId
                )
            }, 400

        data = Item.parser.parse_args()

        cartridge = CartridgeModel(cartridgeId, **data)

        try:
            cartridge.save_to_db()
        except:
            return {"message": "An error occurred inserting the cartridge."}, 500

        return cartridge.json(), 201

    def delete(self, cartridgeId):
        cartridge = CartridgeModel.find_by_name(cartridgeId)
        if cartridge:
            cartridge.delete_from_db()
            return {"message": "cartridge deleted."}
        return {"message": "cartridge not found."}, 404

    def put(self, cartridgeId):
        data = Cartridge.parser.parse_args()

        cartridge = CartridgeModel.find_by_name(cartridgeId)

        if cartridge:
            cartridge.testStatus = data["testStatus"]
        else:
            cartridge = CartridgeModel(cartridgeId, **data)

        cartridge.save_to_db()

        return cartridge.json()


class CartridgeList(Resource):
    def get(self):
        return {"cartridges": list(map(lambda x: x.json(), CartridgeModel.query.all()))}
