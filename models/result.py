from db import db


class ResultModel(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(80))
    number = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    result = db.relationship('UserModel')

    def __init__(self, keyword, number):
        self.keyword = keyword
        self.number = number

    def json(self):
        return {'keyword': self.keyword,'number': self.number}

    @classmethod
    def find_results(cls, keyword, number):
        return cls.query.filter_by(keyword=keyword, number=number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
