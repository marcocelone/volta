from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.result import ResultModel
from models.keyword import KeywordModel


class Results(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('keyword', type=str, required=True, help="Keyword is required.")
    parser.add_argument('number', type=int, required=True, help="A number is required.")

    @jwt_required()
    def post(self):
        data = Results.parser.parse_args()
        keyword = data['keyword']
        number = data['number']
        user_id = int(get_jwt_identity())

        if len(str(abs(number))) != 3:
            return {'message': 'Please enter a 3-digit number.'}, 400

        if KeywordModel.find_by_keyword(keyword) is None:
            return {'message': 'Invalid keyword. You are not a winner.'}, 400

        if number % 11 != 0:
            return {'message': 'Not a winner. Try again!'}, 200

        existing = ResultModel.find_results(keyword, number)
        if existing:
            return {'message': 'We already have a winner for this keyword and number!'}, 409

        result = ResultModel(keyword=keyword, number=number, user_id=user_id)
        try:
            result.save_to_db()
        except Exception:
            return {'message': 'An error occurred saving the result.'}, 500

        return {'message': 'Congratulations, you are a winner!'}, 201


class ResultList(Resource):
    @jwt_required()
    def get(self):
        return {'results': [r.json() for r in ResultModel.query.all()]}, 200