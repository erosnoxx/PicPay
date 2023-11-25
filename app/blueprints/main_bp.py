from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import lm, db
from app.models import User, UserType, Balance, Transaction, Type
from app.forms import BalanceForm, TransferForm
from app.services.mail import simulate_email_notification
from app.services.transfer import transfer

main = Blueprint('main', __name__)
lm.login_view = 'login.login_'


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    formB = BalanceForm()
    formT = TransferForm()
    balance = Balance.query.filter_by(id_owner=current_user.id).first()
    user_type = UserType.query.filter_by(user_id=current_user.id).first()
    types = Type.query.filter_by(id=user_type.type_id).first()

    if formB.validate_on_submit() and request.form.get('form') == 'formB':
        amount = formB.amount.data
        if isinstance(amount, int) and amount > 0:
            balance.amount += amount
            db.session.commit()
            flash('Saldo atualizado com sucesso!')
            return redirect(url_for('main.index'))
        else:
            flash('Valor inválido')

    if formT.validate_on_submit() and request.form.get('form') == 'formT':
        receiver = User.query.filter_by(cpf=formT.cpf.data).first()
        if receiver:
            amount = formT.amount.data
            if balance.amount > 0 and balance.amount >= amount:
                if isinstance(amount, int) and amount > 0:
                    if transfer():
                        balance.amount -= amount
                        db.session.commit()

                        receiver_balance = Balance.query.filter_by(id_owner=receiver.id).first()
                        receiver_balance.amount += amount
                        db.session.commit()

                        transaction = Transaction(id_payer=current_user.id, id_payee=receiver.id, amount=amount)
                        db.session.add(transaction)
                        db.session.commit()

                        flash('Transferência realizada com sucesso!')
                        simulate_email_notification(receiver.email)
                        return redirect(url_for('main.index'))
                    else:
                        flash('Transferência negada')
                else:
                    flash('Valor inválido')
            else:
                flash('Saldo Insuficiente')
        else:
            flash('CPF/CNPJ não encontrado')
    return render_template('main/index.html', formB=formB, formT=formT, balance=balance.amount, user=current_user, types=types)