
from flask import Blueprint, jsonify, request, make_response
from flask_login import login_user, logout_user, current_user
from models import db, User
from werkzeug.security import generate_password_hash , check_password_hash

user_blueprint = Blueprint("user_api_routes", __name__, url_prefix="/api/user")

@user_blueprint.route('/all', methods=["GET"])
def get_all_users():
    all_user = User.query.all()
    result  = [user.serialize() for user in all_user]
    response = {
        'message' : 'Returning all users',
        'result' : result
    }
    return jsonify(response)


@user_blueprint.route('/create', methods=["POST"])
def create_user():
    try:
        user = User()
        form = request.form
        user.username = form["username"]
        user.password = generate_password_hash(form["password"], method="sha256")
        user.is_admin = True
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message" : "User created",
            "result" : user.serialize()
        })
    except Exception as e:
        print(str(e))
        return jsonify({
            "message" : "Error in user creation",
            
        })


@user_blueprint.route('/login', methods=["POST"])
def login():
    form = request.form
    username = form["username"]
    password = form["password"]
    user = User.query.filter_by(username=username).first()
    if not user:
        return make_response(jsonify({
            "message" : "username does not exist"
        }),401)

    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        login_user(user)
        response = {
            "message":"logged in",
            "api_key": user.api_key
        }
        return make_response(jsonify(response),200)
    return make_response(jsonify({
        "message": "Access denied"
    }), 401)


@user_blueprint.route('/logout', methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({
            "message" : "logout"
        })
    return jsonify({
        "message": "No user logged in"
    }), 401


@user_blueprint.route('/<username>/exists', methods=["GET"])
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "result" : True
        }),200
    return jsonify({
        "result": False
    }),401

@user_blueprint.route('/', methods=["GET"])
def current_user_info():
    if current_user.is_authenticated:
        return jsonify({
            "result":current_user.serialize()
        }),200
    return jsonify({
        "message" : "user not logged in"
    }),401

