from flask_restful import Resource, reqparse
from models.keyword import KeywordModel


class Keyword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('keyword',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def delete(self):
        data = Keyword.parser.parse_args()
        keyword = KeywordModel.find_by_keyword(data['keyword'])
        if keyword:
            keyword.delete_from_db()
        return {'message': 'Deleted keyword'}

    def post(self):
        data = Keyword.parser.parse_args()
        keyword = data['keyword']
        if len(keyword) !=3:
            return  {'message': "Please enter a 3 word string"}, 400

        if KeywordModel.find_by_keyword(data['keyword']):
            return {'message': "Keyword already exist!"}, 400

        keyword = KeywordModel(**data)

        try:
            keyword.save_to_db()
        except IOError:
            return {"message": "An error occurred creating the keyword"}, 500

        return {'message':'Keyword created successfully'}, 201


class KeywordList(Resource):
    def get(self):
        return {'keywords': list(map(lambda x: x.json(), KeywordModel.query.all()))}

