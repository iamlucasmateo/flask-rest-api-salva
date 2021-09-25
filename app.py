from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from db import db
from security import authenticate, identity
from resources.item import Item, Items
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'my_password'
api = Api(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)
jwt = JWT(app, authenticate, identity) # /auth

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
