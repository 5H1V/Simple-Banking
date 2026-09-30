from flask import Blueprint, request, jsonify

from models.user import User
from services.user_service import UserService
from repos.repositories import user_repository


user_controller = Blueprint("user_controller", __name__)

user_service = UserService(user_repository)


# GET /api/users
@user_controller.route("/users", methods=["GET"])
def get_all_users():
    users = user_service.get_all_users()

    return jsonify([
        user.to_dict()
        for user in users
    ]), 200


# GET /api/users/<id>
@user_controller.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(user.to_dict()), 200


# POST /api/users
@user_controller.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "name" not in data:
        return jsonify({
            "error": "Name is required"
        }), 400

    if "email" not in data:
        return jsonify({
            "error": "Email is required"
        }), 400

    user = User(
        user_id=None,
        name=data["name"],
        email=data["email"]
    )

    created_user, error = user_service.create_user(user)

    if error:
        return jsonify({
            "error": error
        }), 400

    return jsonify(created_user.to_dict()), 201


# PUT /api/users/<id>
@user_controller.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "name" not in data:
        return jsonify({
            "error": "Name is required"
        }), 400

    if "email" not in data:
        return jsonify({
            "error": "Email is required"
        }), 400

    user, error = user_service.update_user(
        user_id,
        data["name"],
        data["email"]
    )

    if error:
        status_code = 404 if error == "User not found" else 400

        return jsonify({
            "error": error
        }), status_code

    return jsonify(user.to_dict()), 200


# DELETE /api/users/<id>
@user_controller.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    deleted = user_service.delete_user(user_id)

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200