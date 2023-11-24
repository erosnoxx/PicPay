from app.blueprints.main_bp import main
from app.blueprints.login_bp import login


def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(login)
