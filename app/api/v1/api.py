from app.models import User, Type, UserType, Balance, Transaction
from flask import jsonify, request
from app.extensions import db
from werkzeug.security import generate_password_hash
from app.services.mail import simulate_email_notification
from app.services.transfer import transfer


def init_app(app):
    @app.route('/api/v1/users/<id>', methods=['GET'])
    def get_user(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {
                "message": "Usuário não encontrado",
                "statuscode": "404"
            }, 404

        balance = Balance.query.filter_by(id_owner=user.id).first()
        usertype = UserType.query.filter_by(user_id=user.id).first()
        types = Type.query.filter_by(id=usertype.type_id).first()
        data = {
            'id': user.id,
            'fullname': user.fullname,
            'socialname': user.socialname,
            'cpf': user.cpf,
            'email': user.email,
            'balance': balance.amount if balance else 0,
            'type': types.level
        }

        return jsonify(data), 200

    @app.route('/api/v1/users', methods=['POST'])
    def post_users():
        data = request.json
        if not data:
            return {
                "message": "Dados inválidos",
                "statuscode": "400"
            }, 400
        
        existing_cpf = User.query.filter_by(cpf=data['cpf']).first()
        existing_email = User.query.filter_by(email=data['email']).first()

        if not existing_cpf:
            if not existing_email:
                password = generate_password_hash(data['password'])

                user = User(fullname=data['fullname'], socialname=data['socialname'],
                            cpf=data['cpf'], email=data['email'], password=password)
                db.session.add(user)
                db.session.commit()

                balance = Balance(id_owner=user.id, amount=data['amount'])
                types = Type.query.filter_by(level=data['type']).first()
                user_type = UserType(user_id=user.id, type_id=types.id)
                db.session.add(balance)
                db.session.commit
                db.session.add(user_type)
                db.session.commit()

                data = {
                    'id': user.id,
                    'fullname': user.fullname,
                    'socialname': user.socialname,
                    'cpf': user.cpf,
                    'email': user.email,
                    'balance': balance.amount if balance else 0,
                    'type': types.level
                }

                return jsonify(data), 201
            else:
                return {
                    "message": "Email ja cadastrado",
                    "statuscode": 500
                }, 500
        else:
            return {
                    "message": "CPF ja cadastrado",
                    "statuscode": "500"
                }, 500

    @app.route('/api/v1/transactions/<id>', methods=['GET'])
    def get_transactions(id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {
                "message": "Usuário não encontrado",
                "statuscode": "404"
            }, 404

        payer = Transaction.query.filter_by(id_payer=user.id).all()
        payee = Transaction.query.filter_by(id_payee=user.id).all()

        all_trans = {
            'payer': [transaction.to_dict() for transaction in payer if payer is not None],
            'payee': [transaction.to_dict() for transaction in payee if payee is not None]
        }

        return jsonify(all_trans), 200

    @app.route('/api/v1/transactions', methods=['POST'])
    def post_transactions():
        data = request.json
        if not data:
            return {
                "message": "Dados inválidos",
                "statuscode": "400"
            }, 400

        user_type = UserType.query.filter_by(user_id=data['id_payer']).first()
        types = Type.query.filter_by(id=user_type.type_id).first()
        balance = Balance.query.filter_by(id_owner=data['id_payer']).first()

        if types.level != 'logista':
            if balance.amount > 0 and balance.amount >= data['amount']:
                if transfer():
                    transaction = Transaction(id_payer=data['id_payer'], id_payee=data['id_payee'], amount=data['amount'])
                    db.session.add(transaction)
                    db.session.commit()

                    balance_payer = Balance.query.filter_by(id_owner=data['id_payer']).first()
                    balance_payee = Balance.query.filter_by(id_owner=data['id_payee']).first()

                    balance_payer.amount -= data['amount']
                    db.session.commit()
                    balance_payee.amount += data['amount']
                    db.session.commit()

                    data = transaction.to_dict()

                    user = User.query.filter_by(id='id_payer').first()
                    
                    return simulate_email_notification(user.id)
                else:
                    return {
                        "message": "Serviço indisponiível",
                        "statuscode": "400"
                    }, 400
            else:
                return {
                    "message": "Saldo insuficiente",
                    "statuscode": "500"
                }, 500
        else:
            return {
                "message": "Usuário 'logista' não pode realizar transferências",
                "statuscode": "500"
            }, 500

    @app.route('/api/v1/balance', methods=['POST'])
    def post_balance():
        data = request.json
        if not data:
            return {
                "message": "Dados inválidos",
                "statuscode": "400"
            }, 400

        user = User.query.filter_by(id=data['id_owner']).first()

        if user:
            balance = Balance.query.filter_by(id_owner=user.id).first()
            balance.amount += data['amount']
            db.session.commit()

            data = balance.to_dict()

            return jsonify(data), 201
        else:
            return {
                "message": "Usuário não encontrado",
                "statuscode": "404"
            }, 404
        