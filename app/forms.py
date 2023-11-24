from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class UserForm(FlaskForm):
    fullname = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=255)])
    socialname = StringField('Nome Social', validators=[DataRequired(), Length(min=3, max=255)])
    cpf = StringField('CPF/CNPJ', validators=[DataRequired(), Length(min=11, max=14)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=255)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=255)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    type = SelectField('Tipo', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        type_choices = ['Usuário', 'Logista']
        self.type.choices = [(choice, choice) for choice in type_choices]


class LoginForm(FlaskForm):
    cpf = StringField('CPF/CNPJ', validators=[DataRequired(), Length(min=11, max=11)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=255)])
    submit = SubmitField('Entrar')


class VerificationForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired(), Length(min=7, max=7)])
    submit = SubmitField('Verificar')


class BalanceForm(FlaskForm):
    amount = IntegerField('Valor a Adicionar', validators=[DataRequired()])
    submit = SubmitField('Adicionar')


class TransferForm(FlaskForm):
    cpf = StringField('CPF/CNPJ Destinatário', validators=[DataRequired(), Length(min=11, max=14)])
    amount = IntegerField('Valor', validators=[DataRequired()])
    submit = SubmitField('Transferir')