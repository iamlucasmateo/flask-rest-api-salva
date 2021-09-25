from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return { "message": "Connection with database refused"}, 500
        if item:
            return item.json()
        return {"message": "Item does not exist"}
        
    def post(self, name):
        if ItemModel.find_by_name(name):
            return { "message": f"An item with name {name} already exists" }, 400
        data = Item.get_parsed_req()
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item"}, 500

        return item.json(), 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return { 'message': 'Item deleted' }
    
    def put(self, name):
        data = Item.get_parsed_req()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data["price"], data["store_id"]) # **data
        else:
            item.price, item.store_id = data["price"], data["store_id"]
        
        item.save_to_db()

        return item.json()
    
    @classmethod
    def get_parsed_req(cls, name=False, price=True):
        parser = reqparse.RequestParser()
        if name:
            parser.add_argument('name',
                type=str,
                required=True,
                help="This field cannot be left blank!"
            )
        if price:
            parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank!"
            )
        parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item needs a store id"
        )
        data = parser.parse_args()
        return data


# class ItemsModel(Resource):
#     def get(self):
#         conn = sqlite3.connect('data.db')
#         cursor = conn.cursor()
#         query = "SELECT * FROM items"
#         result = cursor.execute(query)
#         items = []
#         for row in result:
#             items.append({"name": row[1], "price": row[2]})
#         return {'items': items}, 200

class Items(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()] }