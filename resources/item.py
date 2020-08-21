from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field can not be left blank"
    )
    parser.add_argument('store_id',
    type = int,
    required = True,
    help = "Every item needs a store id"
    )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "an item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        print(item.name, item.price)
        item.save_to_db()
        return item.json(), 201
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if(item):
            item.delete_from_db()
        return {'meesage': 'Item deleted'}
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, **data)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

class ItemsList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
