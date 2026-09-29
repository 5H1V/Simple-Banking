from flask import Blueprint, jsonify, request

from repos.repositories import (
    user_repository,
    account_repository,
    transaction_repository
)

from services.account_service import AccountService
from services.transaction_service import TransactionService

account_controller = Blueprint("account_controller", __name__)

transaction_service = TransactionService(transaction_repository)

account_service = AccountService(
    account_repository,
    user_repository,
    transaction_service
)

# POST /api/accounts
@account_controller.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "userId" not in data:
        return jsonify({"error": "userId is required"}), 400

    if "accountType" not in data:
        return jsonify({"error": "accountType is required"}), 400

    account, error = account_service.create_account(data["userId"],
                                                    data["accountType"])
    if error:
        return jsonify({"error": error}), 404

    return jsonify(account.to_dict()), 201

# GET /api/accounts/<id>
@account_controller.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    account = account_service.get_account(account_id)
    if account is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(account.to_dict()), 200

# POST /api/accounts/<id>/deposit
@account_controller.route("/accounts/<int:account_id>/deposit", methods=["POST"])
def deposit(account_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "amount" not in data:
        return jsonify({"error": "amount is required"}), 400

    account, error = account_service.deposit(account_id, data["amount"])
    if error:
        status_code = 404
        if error == "Deposit amount must be positive":
            status_code = 400
        
        return jsonify({"error": error}), status_code
    return jsonify(account.to_dict()), 200

# POST /api/accounts/<id>/withdraw
@account_controller.route("/accounts/<int:account_id>/withdraw", methods=["POST"])
def withdraw(account_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "amount" not in data:
        return jsonify({"error": "amount is required"}), 400

    account, error = account_service.withdraw(account_id, data["amount"])
    if error:
        return jsonify({"error": error}), 400 if error != "Account not found" else 404

    return jsonify(account.to_dict()), 200

# GET /api/accounts/<id>/transactions
@account_controller.route("/accounts/<int:account_id>/transactions", methods=["GET"])
def get_transactions(account_id):
    transactions, error = (account_service.get_transactions(account_id))
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify([transaction.to_dict() for transaction in transactions]), 200