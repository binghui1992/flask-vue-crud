from flask_restful import Api
from flask import Blueprint

from resources.book import PingPong, Books
from resources.auth import Login, Logout


bp = Blueprint("/", __name__)
api = Api(bp)

api.add_resource(PingPong, "/ping")
api.add_resource(Books, "/books", "/books/<book_id>")

api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
