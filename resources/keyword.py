from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from models.keyword import KeywordModel


def admin_required(fn):
    """Decorator that enforces admin-only access."""
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'message': 'Admin access required.'}, 403
        return fn(*args, **kwargs)
    return wrapper


class Keyword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('keyword',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @admin_required
    def delete(self):
        data = Keyword.parser.parse_args()
        keyword = KeywordModel.find_by_keyword(data['keyword'])
        if not keyword:
            return {'message': 'Keyword not found.'}, 404
        keyword.delete_from_db()
        return {'message': 'Keyword deleted successfully.'}, 200

    @admin_required
    def post(self):
        data = Keyword.parser.parse_args()
        keyword = data['keyword']

        if KeywordModel.find_by_keyword(data['keyword']):
            return {'message': "Keyword already exist!"}, 400

        keyword = KeywordModel(**data)

        try:
            keyword.save_to_db()
        except IOError:
            return {"message": "An error occurred creating the keyword"}, 500

        return {'message':'Keyword created successfully'}, 201


class KeywordList(Resource):
    @admin_required
    def get(self):
        return {'keywords': list(map(lambda x: x.json(), KeywordModel.query.all()))}

