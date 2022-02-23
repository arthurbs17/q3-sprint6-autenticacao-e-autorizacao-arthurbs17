from flask import Blueprint

from app.routes.user_route import bp_user


bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

bp_api.register_blueprint(bp_user)