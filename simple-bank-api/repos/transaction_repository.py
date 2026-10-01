from bson import ObjectId
from database import db
from models.transaction import Transaction

class TransactionRepository:
    def __init__(self):
        self.collection = db["transactions"]

    def find_by_account_id(self, account_id):
        transactions = self.collection.find({
            "account_id": account_id
        }).sort("_id", 1)

        return [
            Transaction(
                txn_id=str(transaction["_id"]),
                account_id=transaction["account_id"],
                txn_type=transaction["txn_type"],
                amount=transaction["amount"]
            )
            for transaction in transactions
        ]

    def find_all(self):
        transactions = self.collection.find().sort("_id", -1)
        return [
            Transaction(
                txn_id=str(transaction["_id"]),
                account_id=transaction["account_id"],
                txn_type=transaction["txn_type"],
                amount=transaction["amount"]
            )
            for transaction in transactions
        ]

    def save(self, transaction):
        if transaction.txn_id is None:
            result = self.collection.insert_one({
                "account_id": transaction.account_id,
                "txn_type": transaction.txn_type,
                "amount": transaction.amount
            })
            transaction.txn_id = str(result.inserted_id)
        else:
            self.collection.update_one(
                {
                    "_id": ObjectId(transaction.txn_id)
                },
                {
                    "$set": {
                        "account_id": transaction.account_id,
                        "txn_type": transaction.txn_type,
                        "amount": transaction.amount
                    }
                }
            )
        return transaction