from flask import Blueprint, jsonify

from services.transaction_service import TransactionService
from repos.transaction_repository import TransactionRepository

transaction_controller = Blueprint("transaction_controller", __name__)
transaction_repository = TransactionRepository()
transaction_service = TransactionService(transaction_repository)

@transaction_controller.route(
    "/accounts/<int:account_id>/transactions", methods=["GET"])
def get_transactions(account_id):
    transactions = transaction_service.get_transactions(account_id)
    return jsonify([transaction.to_dict() for transaction in transactions]), 200