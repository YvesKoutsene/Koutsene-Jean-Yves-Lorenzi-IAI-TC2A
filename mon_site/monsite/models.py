from . import db

class Account(db.Model):
    __tablename__= 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(150),nullable=False)
    password = db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(150),nullable=False)

