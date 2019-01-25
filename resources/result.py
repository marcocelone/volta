from flask_restful import Resource, reqparse
from models.result import ResultModel
from models.keyword import KeywordModel
from flask_jwt import jwt_required


class Results(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('keyword',
                        type=str,
                        required=True,
                        help="A 3 character string is needed"
                        ),
    parser.add_argument('number',
                        type=int,
                        required=True,
                        help="A 3 digit number is needed"
                        )

    @jwt_required()
    def post(self):
        data = Results.parser.parse_args()
        keyword = data['keyword']
        number = data['number']

        if len(str(number)) !=3:
            return  {'message': "Please enter a 3 digit number"}, 400

        elif KeywordModel.find_by_keyword(data['keyword']) is None:
            return {'message': "You are Not a winner try again!!!!"}, 201

        elif number % 11 == 0 and ResultModel.find_results(keyword, number) is None:
                keyword = ResultModel(**data)
                try:
                    keyword.save_to_db()
                    return {'message': "You are a winner"}, 201
                except IOError:
                    return {"message": "An error occurred saving the results"}, 500

        else:
            return {'message': "We already have a winner!!"}, 201

        return {'message': "You are Not a winner try again later!!"}, 201

class ResultList(Resource):
    def get(self):
        return {'results': list(map(lambda x: x.json(), ResultModel.query.all()))}