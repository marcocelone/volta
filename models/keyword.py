from db import db


class KeywordModel(db.Model):

    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(3))

    def __init__(self, keyword):
        self.keyword = keyword

    def json(self):
        return {'keyword': self.keyword}

    @classmethod
    def find_by_keyword(cls, keyword):
        return cls.query.filter_by(keyword=keyword).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
