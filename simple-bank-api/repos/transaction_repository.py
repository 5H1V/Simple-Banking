from datetime import datetime, timezone
from bson import ObjectId
from database import db
from models.transaction import Transaction


class TransactionRepository:
    def __init__(self):
        self.collection = db["transactions"]

    @staticmethod
    def _to_model(transaction):
        created_at = transaction.get("created_at")
        if created_at is None:
            try:
                created_at = transaction["_id"].generation_time
            except Exception:
                created_at = datetime.now(timezone.utc)
        return Transaction(
            txn_id=str(transaction["_id"]),
            account_id=transaction["account_id"],
            txn_type=transaction["txn_type"],
            amount=transaction["amount"],
            created_at=created_at,
            transfer_id=transaction.get("transfer_id"),
            related_account_id=transaction.get("related_account_id"),
        )

    def find_by_account_id(self, account_id):
        return [self._to_model(item) for item in self.collection.find({"account_id": account_id}).sort("_id", 1)]

    def find_all(self):
        return [self._to_model(item) for item in self.collection.find().sort("_id", -1)]

    def save(self, transaction):
        if transaction.txn_id is None:
            document = {
                "account_id": transaction.account_id,
                "txn_type": transaction.txn_type,
                "amount": transaction.amount,
                "created_at": transaction.created_at or datetime.now(timezone.utc),
            }
            if transaction.transfer_id:
                document["transfer_id"] = transaction.transfer_id
            if transaction.related_account_id:
                document["related_account_id"] = transaction.related_account_id
            result = self.collection.insert_one(document)
            transaction.txn_id = str(result.inserted_id)
        else:
            self.collection.update_one({"_id": ObjectId(transaction.txn_id)}, {"$set": {
                "account_id": transaction.account_id,
                "txn_type": transaction.txn_type,
                "amount": transaction.amount,
                "created_at": transaction.created_at,
                "transfer_id": transaction.transfer_id,
                "related_account_id": transaction.related_account_id,
            }})
        return transaction
