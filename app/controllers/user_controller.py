from flask import request, jsonify, current_app
from http import HTTPStatus
from secrets import token_urlsafe

from sqlalchemy.exc import IntegrityError

from app.configs.auth import auth
from app.exc.invalids_keys import InvalidsKeys, InvalidsValues
from app.models.user_model import User
from app.services.user_services import check_keys, check_values


@auth.login_required
def get_user():
    bearer_token = request.headers.get('Authorization').split(' ')[1]

    user: User = User.query.filter_by(api_key=bearer_token).first()

    return jsonify(user), HTTPStatus.OK


@auth.login_required
def updated_user():
    session = current_app.db.session

    try:
        data = request.get_json()
        check_values(data)

        bearer_token = request.headers.get('Authorization').split(' ')[1]
        user: User = User.query.filter_by(api_key=bearer_token).first()

        for key, value in data.items():
            setattr(user, key, value)

        session.add(user)
        session.commit()

        return jsonify(user), HTTPStatus.OK

    except InvalidsValues as error:
        return jsonify(error.message), HTTPStatus.BAD_REQUEST


@auth.login_required
def delete_user():
    session = current_app.db.session

    bearer_token = request.headers.get('Authorization').split(' ')[1]
    user: User = User.query.filter_by(api_key=bearer_token).first()

    session.delete(user)
    session.commit()

    return jsonify({"msg": f'User {user.name} has been deleted'}), HTTPStatus.OK



def login_user():
    data = request.get_json()

    user: User = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {"error": "user not found"}, HTTPStatus.NOT_FOUND
    
    if not user.check_password(data["password"]):
        return {"error": "email and passowrd missmatch!"}, HTTPStatus.UNAUTHORIZED

    token = user.api_key

    return jsonify({"token": token}), HTTPStatus.OK


def create_user():
    session = current_app.db.session
    try:
        data = request.get_json()
        check_keys(data)
        check_values(data)
        data["api_key"] = token_urlsafe(16)

        new_user = User(**data)

        session.add(new_user)
        session.commit()

        return jsonify(new_user), HTTPStatus.CREATED
    
    except InvalidsKeys as error:
        return jsonify(error.message), HTTPStatus.BAD_REQUEST
    
    except InvalidsValues as error:
        return jsonify(error.message), HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return jsonify({"error": "email already exists!"})
