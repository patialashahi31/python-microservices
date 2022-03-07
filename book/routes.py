from flask import Blueprint, request, jsonify
from models import Book, db

book_blueprint = Blueprint("book_api_routes", __name__, url_prefix="/api/book")


@book_blueprint.route('/all', methods=["GET"])
def get_all_books():
    all_books = Book.query.all()
    result  = [book.serialize() for book in all_books]
    response = {
        'message' : 'Returning all books',
        'result' : result
    }
    return jsonify(response)


@book_blueprint.route("/create", methods=["POST"])
def create_books():
    try:
        book = Book()
        form = request.form
        book.name = form["name"]
        book.slug = form["slug"]
        book.image = form["image"]
        book.price = form["price"]

        db.session.add(book)
        db.session.commit()
        response = {
            "message" : "Book created", "result" : book.serialize()
        }
    except Exception as e:
        print(str(e))
        response = {
           "message" :  "Book creation failed"
        }
    return jsonify(response)


@book_blueprint.route("/<slug>", methods=["GET"])
def book_details(slug):
    book = Book.query.filter_by(slug=slug).first()
    if book:
        return jsonify({
            "result": book.serialize()
        }), 200
    return jsonify({
        "result": False
    }), 401
