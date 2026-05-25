from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import UserRegister, UserLogin
from resources.keyword import Keyword, KeywordList
from resources.result import Results, ResultList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret-change-me'  # Change in production!

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Keyword, '/keyword')
api.add_resource(KeywordList, '/keywords')
api.add_resource(Results, '/results')
api.add_resource(ResultList, '/results/all')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
