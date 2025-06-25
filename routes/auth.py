from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User
from utils.encryption import generate_token, verify_token
from utils.email_service import send_verification_email
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__)

# Signup (Client Only)
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data["email"]
    password = generate_password_hash(data["password"])
    
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    new_user = User(email=email, password=password, role="client")
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(email)
    send_verification_email(email, token)
    return jsonify({"msg": "Signup successful. Check your email for verification."})

# Email Verification
@auth_bp.route("/verify/<token>", methods=["GET"])
def verify_email(token):
    email = verify_token(token)
    if not email:
        return jsonify({"msg": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        user.is_verified = True
        db.session.commit()
        return jsonify({"msg": "Email verified successfully!"})
    return jsonify({"msg": "User not found"}), 404

# Login (Both Roles)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401

    if user.role == "client" and not user.is_verified:
        return jsonify({"msg": "Please verify your email"}), 403

    payload = {
        "id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
    return jsonify({"token": token})
