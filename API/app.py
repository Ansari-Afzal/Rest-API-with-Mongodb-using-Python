from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client.bookdb
books = db.books

# Create a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book_id = books.insert_one({
        'name': data['name'],
        'img': data['img'],
        'summary': data['summary']
    }).inserted_id
    new_book = books.find_one({'_id': book_id})
    return jsonify({
        '_id': str(new_book['_id']),
        'name': new_book['name'],
        'img': new_book['img'],
        'summary': new_book['summary']
    }), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    all_books = books.find()
    result = []
    for book in all_books:
        result.append({
            '_id': str(book['_id']),
            'name': book['name'],
            'img': book['img'],
            'summary': book['summary']
        })
    return jsonify(result), 200

# Get a book by id
@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = books.find_one({'_id': ObjectId(id)})
    if book:
        return jsonify({
            '_id': str(book['_id']),
            'name': book['name'],
            'img': book['img'],
            'summary': book['summary']
        }), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

# Update a book by id
@app.route('/books/<id>', methods=['PATCH'])
def update_book(id):
    data = request.get_json()
    updated_book = books.find_one_and_update(
        {'_id': ObjectId(id)},
        {'$set': data},
        return_document=True
    )
    if updated_book:
        return jsonify({
            '_id': str(updated_book['_id']),
            'name': updated_book['name'],
            'img': updated_book['img'],
            'summary': updated_book['summary']
        }), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

# Delete a book by id
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    result = books.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Book deleted'}), 200
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
