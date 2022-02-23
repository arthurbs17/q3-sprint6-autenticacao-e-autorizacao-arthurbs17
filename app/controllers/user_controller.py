from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError

from app.exc.invalids_keys import InvalidsKeys, InvalidsValues
from app.models.user_model import User
from app.services.user_services import check_keys, check_values


@jwt_required()
def get_user():

    user = get_jwt_identity()

    return jsonify(user), HTTPStatus.OK


@jwt_required()
def updated_user():
    session = current_app.db.session

    try:
        data = request.get_json()
        check_values(data)

        decoded_user = get_jwt_identity()
        user: User = User.query.filter_by(email=decoded_user["email"]).first()

        for key, value in data.items():
            setattr(user, key, value)

        session.add(user)
        session.commit()

        return jsonify(user), HTTPStatus.OK

    except InvalidsValues as error:
        return jsonify(error.message), HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_user():
    session = current_app.db.session

    decoded_user = get_jwt_identity()
    user: User = User.query.filter_by(email=decoded_user["email"]).first()

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

    token = create_access_token(user)

    return jsonify({"access_token": token}), HTTPStatus.OK


def create_user():
    session = current_app.db.session
    try:
        data = request.get_json()
        check_keys(data)
        check_values(data)

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
