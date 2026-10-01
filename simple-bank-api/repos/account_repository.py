from bson import ObjectId
from database import db
from models.account import Account

class AccountRepository:
    def __init__(self):
        self.collection = db["accounts"]

    def find_all(self):
        accounts = self.collection.find()

        return [
            Account(
                account_id=str(account["_id"]),
                user_id=account["user_id"],
                balance=account["balance"],
                account_type=account["account_type"]
            )
            for account in accounts
        ]

    def find_by_id(self, account_id):
        try:
            object_id = ObjectId(account_id)
        except Exception:
            return None

        account = self.collection.find_one({
            "_id": object_id
        })

        if account is None:
            return None

        return Account(
            account_id=str(account["_id"]),
            user_id=account["user_id"],
            balance=account["balance"],
            account_type=account["account_type"]
        )

    def save(self, account):
        if account.account_id is None:
            result = self.collection.insert_one({
                "user_id": account.user_id,
                "balance": account.balance,
                "account_type": account.account_type
            })
            account.account_id = str(result.inserted_id)
        else:
            self.collection.update_one(
                {
                    "_id": ObjectId(account.account_id)
                },
                {
                    "$set": {
                        "user_id": account.user_id,
                        "balance": account.balance,
                        "account_type": account.account_type
                    }
                }
            )
        return account

    def delete_by_id(self, account_id):
        try:
            object_id = ObjectId(account_id)
        except Exception:
            return False

        result = self.collection.delete_one({
            "_id": object_id
        })

        return result.deleted_count > 0