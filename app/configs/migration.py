from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models.user_model import User

    Migrate(app, app.db, compare_type=True)