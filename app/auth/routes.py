from flask import jsonify, request, Blueprint, session
from app.extensions import db
from app.models import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/Register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    Name = data.get("Name")
    Email = data.get("Email")
    Password = data.get("Password")

    if not Name or not Email or not Password:
        return jsonify({"message": "All fields are required"}), 400
    if User.query.filter_by(Email=Email).first():
        return jsonify({"message": "Email already registered"}), 409
    if "@" not in Email or "." not in Email:
        return jsonify({"message": "Invalid email format"}), 400
    if len(Password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400
    user = User(Name=Name, Email=Email)
    user.set_password(Password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/Login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    Email = data.get("Email")
    Password = data.get("Password")

    if not Email or not Password:
        return jsonify({"Message": "Email and Password is Required"}), 400

    user = User.query.filter_by(Email=Email).first()
    if not user:
        return jsonify({"message": "Invalid Email or Password"}), 401

    if not check_password_hash(user.password_hash,Password):
        return jsonify({"message": "Invalid Email or Password"}), 401
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": new_access_token}), 200