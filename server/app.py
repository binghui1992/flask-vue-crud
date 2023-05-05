import uuid
import yaml
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UUID
import sqlalchemy


config_file = os.path.join(os.path.dirname(__file__), 'database/config.yaml')
with open(config_file, "r") as f:
    DB_CONFIG = yaml.load(f, Loader=yaml.FullLoader)


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{DB_CONFIG["username"]}:{DB_CONFIG["password"]}@'
    f'{DB_CONFIG["hostname"]}:{DB_CONFIG["port"]}/{DB_CONFIG["dbName"]}')


db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "book"
    book_id = db.Column(UUID(as_uuid=True), primary_key=True,
                        server_default=sqlalchemy.text("uuid_generate_v4()"))
    title = db.Column(db.String(128))
    author = db.Column(db.String(128))
    read = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


with app.app_context():
    db.create_all()

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'error'}
    if request.method == 'POST':
        post_data = request.get_json()
        book = Book(title=post_data.get('title'),
                    author=post_data.get('author'),
                    read=post_data.get('read'))
        db.session.add(book)
        db.session.commit()
        response_object = {'status': 'success', 'message': 'Book added!',
                           'book_id': book.book_id}
    elif request.method == 'GET':
        books = [book.as_dict() for book in db.session.query(Book).all()]
        response_object = {'status': 'success', 'books': books}

    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'error'}

    # Verify if a valid uuid string
    try:
        uuid.UUID(book_id)
    except ValueError:
        response_object = {'status': 'error',
                           'message': f'Invalid book ID format: "{book_id}"!'}
        return response_object

    book = db.session.query(Book).filter_by(book_id=book_id).first()
    if book:
        if request.method == 'PUT':
            post_data = request.get_json()
            book.title = post_data.get('title')
            book.author = post_data.get('author')
            book.read = post_data.get('read')
            db.session.commit()
            response_object = {'status': 'success',
                               'message': 'Book updated!'}
        elif request.method == 'DELETE':
            db.session.delete(book)
            db.session.commit()
            response_object = {'status': 'success',
                               'message': 'Book removed!'}
    else:
        response_object = {'status': 'error',
                           'message': f'Book ID({book_id}) not found!'}

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
