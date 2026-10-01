from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId
from pymongo import ReturnDocument


class TransferService:
    """Transfer money atomically between two accounts owned by the same user."""
    def __init__(self, mongo_client, database):
        self.client = mongo_client
        self.accounts = database["accounts"]
        self.transactions = database["transactions"]

    def transfer(self, from_account_id, to_account_id, amount):
        if not isinstance(amount, (int, float)) or not amount > 0 or not amount < float("inf"):
            raise ValueError("Transfer amount must be a positive finite number")
        if round(amount, 2) != amount:
            raise ValueError("Transfer amount can have at most two decimal places")
        if from_account_id == to_account_id:
            raise ValueError("Choose two different accounts")
        try:
            from_oid, to_oid = ObjectId(from_account_id), ObjectId(to_account_id)
        except Exception as exc:
            raise ValueError("Invalid account ID") from exc

        transfer_id = str(uuid4())
        created_at = datetime.now(timezone.utc)
        # MongoDB multi-document transactions require a replica set or sharded cluster.
        with self.client.start_session() as session:
            with session.start_transaction():
                source = self.accounts.find_one({"_id": from_oid}, session=session)
                destination = self.accounts.find_one({"_id": to_oid}, session=session)
                if source is None or destination is None:
                    raise ValueError("Source or destination account was not found")
                if source.get("user_id") != destination.get("user_id"):
                    raise ValueError("Transfers are only allowed between your own accounts")
                debited = self.accounts.find_one_and_update(
                    {"_id": from_oid, "balance": {"$gte": float(amount)}},
                    {"$inc": {"balance": -float(amount)}},
                    return_document=ReturnDocument.AFTER,
                    session=session,
                )
                if debited is None:
                    raise ValueError("Insufficient balance")
                credited = self.accounts.find_one_and_update(
                    {"_id": to_oid},
                    {"$inc": {"balance": float(amount)}},
                    return_document=ReturnDocument.AFTER,
                    session=session,
                )
                if credited is None:
                    raise ValueError("Destination account was not found")
                self.transactions.insert_many([
                    {"account_id": from_account_id, "txn_type": "TRANSFER_OUT", "amount": float(amount),
                     "created_at": created_at, "transfer_id": transfer_id, "related_account_id": to_account_id},
                    {"account_id": to_account_id, "txn_type": "TRANSFER_IN", "amount": float(amount),
                     "created_at": created_at, "transfer_id": transfer_id, "related_account_id": from_account_id},
                ], session=session)
        return {
            "transferId": transfer_id,
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": float(amount),
            "fromBalance": debited["balance"],
            "toBalance": credited["balance"],
            "createdAt": created_at.isoformat(),
        }
