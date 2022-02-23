from flask import Flask
from environs import Env

def init_app(app: Flask):
    env = Env()
    env.read_env()

    app.config["SQLALCHEMY_DATABASE_URI"] = env("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False