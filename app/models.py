from app import db


class Book(db.Model):
    def __init__(self, book=None):
        self.book = book
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(300))

    def __repr__(self):
        return '<id {}>'.format(self.id)
