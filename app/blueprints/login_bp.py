from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask import current_app
from flask_login import login_user, logout_user
from app.forms import LoginForm, UserForm, VerificationForm
from app.models import User, UserType, Type, Balance
from app.extensions import db, lm
from app.mail import send_email
from app.generators import generate_otp
from werkzeug.security import generate_password_hash, check_password_hash


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


login = Blueprint('login', __name__)


@login.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        existing_cpf = User.query.filter(User.cpf == form.cpf.data).first()
        existing_email = User.query.filter(User.email == form.email.data).first()
        if not existing_cpf:
            if not existing_email:
                hashed_password = generate_password_hash(form.password.data)

                session['new_user'] = {
                    'fullname': form.fullname.data,
                    'socialname': form.socialname.data,
                    'cpf': form.cpf.data,
                    'email': form.email.data,
                    'password': hashed_password
                }

                session['type'] = form.type.data.lower()
                session['otp'] = str(generate_otp())
                otp = session.get('otp')
                subject = 'PicPay - Verificação de Email'
                body = f'Olá {form.socialname.data}, seu código de verificação é {otp}'

                send_email(subject=subject, body=body, to=form.email.data)

                return redirect(url_for('login.otp'))
            else:
                flash('Email já cadastrado')
        else:
            flash('CPF já cadastrado')
    return render_template('login/register.html', form=form)


@login.route('/register/verification', methods=['GET', 'POST'])
def otp():
    form = VerificationForm()
    otp = session.get('otp')
    if form.validate_on_submit():
        if otp == form.otp.data:
            new_user = User(**session['new_user'])
            db.session.add(new_user)
            db.session.commit()

            types = Type.query.filter_by(utype=session.get('type').lower()).first()
            user_type = UserType(user_id=new_user.id, type_id=types.id)
            db.session.add(user_type)
            db.session.commit()

            user_balance = Balance(id_owner=new_user.id, amount=0)
            db.session.add(user_balance)
            db.session.commit()

            session.pop('otp', None)
            session.pop('new_user', None)
            session.pop('type', None)

            return redirect(url_for('login.login_'))
        else:
            flash('Código inválido')
    return render_template('login/verification.html', form=form, email=session['new_user']['email'])


@login.route('/login', methods=['GET', 'POST'])
def login_():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.cpf == form.cpf.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Senha inválida')
        else:
            flash('CPF não cadastrado')
    return render_template('login/login.html', form=form)
