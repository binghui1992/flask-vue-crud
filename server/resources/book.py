import uuid

from flask import jsonify, request
from flask_restful import Resource

from db import db
from models.book import Book


# sanity check route
class PingPong(Resource):
    def get(self):
        return jsonify("pong!")


class Books(Resource):
    def get(self):
        books = [book.as_dict() for book in db.session.query(Book).all()]
        response_object = {"status": "success", "books": books}

        return jsonify(response_object)

    def post(self):
        post_data = request.get_json()
        book = Book(
            title=post_data.get("title"),
            author=post_data.get("author"),
            read=post_data.get("read"),
        )
        db.session.add(book)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": "Book added!",
            "book_id": book.book_id,
        }

        return jsonify(response_object)

    def put(self, book_id):
        response_object = self._verify_uuid(book_id)
        if response_object:
            return response_object

        book = db.session.query(Book).filter_by(book_id=book_id).first()
        if book:
            post_data = request.get_json()
            book.title = post_data.get("title")
            book.author = post_data.get("author")
            book.read = post_data.get("read")
            db.session.commit()
            response_object = {"status": "success", "message": "Book updated!"}
        else:
            response_object = {
                "status": "error",
                "message": f"Book ID({book_id}) not found!",
            }

        return jsonify(response_object)

    def delete(self, book_id):
        response_object = self._verify_uuid(book_id)
        if response_object:
            return jsonify(response_object)

        book = db.session.query(Book).filter_by(book_id=book_id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            response_object = {"status": "success", "message": "Book removed!"}
        else:
            response_object = {
                "status": "error",
                "message": f"Book ID({book_id}) not found!",
            }

        return jsonify(response_object)

    def _verify_uuid(self, book_id):
        # Verify if a valid uuid string
        try:
            uuid.UUID(book_id)
        except ValueError:
            response_object = {
                "status": "error",
                "message": f'Invalid book ID format: "{book_id}"!',
            }
            return response_object
