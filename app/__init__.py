from flask import Flask
from dynaconf import FlaskDynaconf
import logging


def create_app():
    app = Flask(__name__)
    FlaskDynaconf(app, extensions_list=True)
    app.logger.setLevel(logging.INFO)

    return app
