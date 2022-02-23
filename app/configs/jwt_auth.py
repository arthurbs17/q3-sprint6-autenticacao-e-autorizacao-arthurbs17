from flask import Flask
from flask_jwt_extended import JWTManager
from environs import Env

def init_app(app:Flask):
    env = Env()
    env.read_env()

    app.config["JWT_SECRET_KEY"] = env("SECRET_KEY")
    JWTManager(app)