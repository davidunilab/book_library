from models.books import Books as BooksModel
from models.books import AllBooks as AllBooksModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify


class Item(Resource):

    keys = ("name", "author", "genre", "publishDate", "quantity")

    i_prs = reqparse.RequestParser()

    i_prs.add_argument("name",
                       type=str,
                       required=True,
                       help="parameter should be String"
                       )
    i_prs.add_argument("author",
                       type=str,
                       required=True,
                       help="parameter should be String"
                       )
    i_prs.add_argument("genre",
                       type=str,
                       required=True,
                       help="parameter should be String"
                       )
    i_prs.add_argument("publishdate",
                       type=str,
                       required=True,
                       help="parameter should be String"
                       )
    i_prs.add_argument("quantity",
                       type=int,
                       required=True,
                       help="parameter should be String"
                       )

    def get(self, item_id=None):
        ret = BooksModel.find_by_id(item_id)
        if ret is not None:
            return jsonify(ret.json())
        return {"message": f"Item with ID {item_id} was not found"}, 200

    @jwt_required()
    def post(self, item_id):
        ret = BooksModel.find_by_id(item_id)

        if ret is not None:
            return {"message": f"ID {item_id} უკვე არსებობს სიაში"}, 400

        book = Item.i_prs.parse_args()
        bm = BooksModel(**book)
        bm.save()
        return {"message": f"book {item_id} is added successfully"}, 200

    @jwt_required()
    def delete(self, item_id):
        book = BooksModel.find_by_id(item_id)
        if book is not None:
            book.delete()
            return {"message": "book is deleted successfully"}, 200
        return {"message": "We have not this book"}, 400

    @jwt_required()
    def put(self, item_id):
        book = Item.i_prs.parse_args()
        book_from_db = BooksModel.find_by_id(item_id)
        print(book_from_db)
        if book_from_db is not None:
            # update
            book_from_db.name = book.name
            book_from_db.author = book.author
            book_from_db.genre = book.genre
            book_from_db.publishdate = book.publishdate
            book_from_db.quantity = book.quantity
            book_from_db.save()
            return {"message": f"book {item_id} is updated successfully"}, 200
        # insert
        book = Item.i_prs.parse_args()
        bm = BooksModel(**book)
        bm.save()
        return {"message": f"book {item_id} is added successfully"}, 200




class ItemList(Resource):

    def get(self):
        return {'items': list(map(lambda x: x.json(), AllBooksModel.get()))}


    @jwt_required()
    def delete(self):
        AllBooksModel.delete()
        return {"message": "list was deleted successfully"}, 200
