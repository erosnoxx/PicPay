from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Numeric


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    socialname = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    types = db.relationship('Type', secondary='user_types', backref='users')
    transactions_as_payer = db.relationship('Transaction', foreign_keys='Transaction.id_payer', backref='payer_transactions')
    transactions_as_payee = db.relationship('Transaction', foreign_keys='Transaction.id_payee', backref='payee_transactions')
    balances = db.relationship('Balance', backref='owner_balance')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.socialname}>'


class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    utype = db.Column(db.String(10), unique=True)

    user_types = db.relationship('UserType', backref='types')


class UserType(db.Model):
    __tablename__ = 'user_types'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))

    user = db.relationship('User', backref='user_type')
    type = db.relationship('Type', backref='user_type')


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(Numeric(precision=10, scale=2), default=0)
    id_payer = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_payee = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    payer = db.relationship('User', foreign_keys=[id_payer], backref=db.backref('payer_transactions', lazy='dynamic'))
    payee = db.relationship('User', foreign_keys=[id_payee], backref=db.backref('payee_transactions', lazy='dynamic'))

    def __repr__(self):
        return f'<Transaction {self.amount}>'


class Balance(db.Model):
    __tablename__ = 'balances'

    id = db.Column(db.Integer, primary_key=True)
    id_owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(Numeric(precision=10, scale=2), default=0)

    owner = db.relationship('User', backref=db.backref('balance', lazy='dynamic'))
