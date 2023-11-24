from flask import Blueprint, render_template
from flask_login import login_required
from app.extensions import lm


main = Blueprint('main', __name__)
lm.login_view = 'login.login_'


@main.route('/')
@login_required
def index():
    return render_template('main/index.html')