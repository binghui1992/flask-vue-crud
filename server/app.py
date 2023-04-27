import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS


BOOKS = [
    {
        'book_id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

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
        book_id = uuid.uuid4().hex
        BOOKS.append({
            'book_id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
        })
        response_object = {'status': 'success', 'message': 'Book added!',
                           'bookId': book_id}
    elif request.method == 'GET':
        response_object = {'status': 'success', 'books': BOOKS}

    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'error'}
    if request.method == 'PUT':
        post_data = request.get_json()
        incoming_book = {
            'book_id': book_id,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
        }

        for i, book in enumerate(BOOKS):
            if book['book_id'] == book_id:
                BOOKS[i].update(incoming_book)
                response_object = {'status': 'success',
                                   'message': 'Book updated!'}
                break
        else:
            response_object = {'status': 'error',
                               'message': f'Book ID({book_id}) not found!'}
    elif request.method == 'DELETE':
        for i, book in enumerate(BOOKS):
            if book['book_id'] == book_id:
                BOOKS.pop(i)
                response_object = {'status': 'success',
                                   'message': 'Book removed!'}
                break
        else:
            response_object = {'status': 'error',
                               'message': f'Book ID({book_id}) not found!'}

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
