import pytz
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
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Sao_Paulo')).replace(tzinfo=None))

    types = db.relationship('Type', secondary='user_types', backref='users')
    balance = db.relationship('Balance', backref='users')
    payer = db.relationship('Transaction', foreign_keys='Transaction.id_payer',
                            backref='payer_user', lazy='dynamic')
    payee = db.relationship('Transaction', foreign_keys='Transaction.id_payee',
                            backref='payee_user', lazy='dynamic')

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
    level = db.Column(db.String(10), nullable=False)


class UserType(db.Model):
    __tablename__ = 'user_types'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(Numeric(precision=10, scale=2), default=0)
    id_payer = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_payee = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.now(pytz.timezone('America/Sao_Paulo')).replace(tzinfo=None))

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'id_payer': self.id_payer,
            'id_payee': self.id_payee,
            'date': self.date
        }

    def __repr__(self):
        return f'<Transaction {self.amount}>'


class Balance(db.Model):
    __tablename__ = 'balances'

    id = db.Column(db.Integer, primary_key=True)
    id_owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(Numeric(precision=10, scale=2), default=0)

    def to_dict(self):
        return {
            "id_owner": self.id_owner,
            "amount": self.amount
        }
