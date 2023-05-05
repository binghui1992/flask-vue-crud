import uuid

from flask import jsonify, request, Blueprint

from db import db
from models.book import Book


# Create a blueprint object
bp = Blueprint("/", __name__)


# sanity check route
@bp.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


@bp.route("/books", methods=["GET", "POST"])
def all_books():
    response_object = {"status": "error"}
    if request.method == "POST":
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
    elif request.method == "GET":
        books = [book.as_dict() for book in db.session.query(Book).all()]
        response_object = {"status": "success", "books": books}

    return jsonify(response_object)


@bp.route("/books/<book_id>", methods=["PUT", "DELETE"])
def single_book(book_id):
    response_object = {"status": "error"}

    # Verify if a valid uuid string
    try:
        uuid.UUID(book_id)
    except ValueError:
        response_object = {
            "status": "error",
            "message": f'Invalid book ID format: "{book_id}"!',
        }
        return response_object

    book = db.session.query(Book).filter_by(book_id=book_id).first()
    if book:
        if request.method == "PUT":
            post_data = request.get_json()
            book.title = post_data.get("title")
            book.author = post_data.get("author")
            book.read = post_data.get("read")
            db.session.commit()
            response_object = {"status": "success", "message": "Book updated!"}
        elif request.method == "DELETE":
            db.session.delete(book)
            db.session.commit()
            response_object = {"status": "success", "message": "Book removed!"}
    else:
        response_object = {
            "status": "error",
            "message": f"Book ID({book_id}) not found!",
        }

    return jsonify(response_object)
